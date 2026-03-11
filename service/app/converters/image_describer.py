"""LLM-powered image description with parallel processing and retry."""
import asyncio
import base64
import logging
from pathlib import Path
from typing import NamedTuple

from openai import AsyncOpenAI, APIError, RateLimitError, APIConnectionError

from ..config import get_settings
from .pdf_extractor import ImageRef

logger = logging.getLogger(__name__)


class DescriptionResult(NamedTuple):
    """Result of describing a single image."""
    ref: ImageRef
    description: str | None
    error: str | None


async def describe_images(
    markdown_content: str,
    image_refs: list[ImageRef],
    images_dir: Path,
) -> str:
    """
    Add LLM-generated descriptions to images in the markdown.

    Processes images in parallel with configurable concurrency and retry logic.

    For each image, inserts:
    - Context before the image
    - Image description from LLM
    - Context after the image
    """
    settings = get_settings()

    if not settings.openai_api_token:
        logger.warning("No OpenAI API token configured, skipping image descriptions")
        return markdown_content

    if not image_refs:
        return markdown_content

    client_kwargs = {"api_key": settings.openai_api_token}
    if settings.openai_base_url:
        client_kwargs["base_url"] = settings.openai_base_url
    client = AsyncOpenAI(**client_kwargs)

    # Semaphore to limit concurrent API calls
    semaphore = asyncio.Semaphore(settings.max_concurrent_descriptions)

    logger.info(
        f"Describing {len(image_refs)} images "
        f"(max {settings.max_concurrent_descriptions} concurrent)"
    )

    # Process all images in parallel
    tasks = [
        _describe_single_image(client, ref, images_dir, semaphore)
        for ref in image_refs
    ]
    results: list[DescriptionResult] = await asyncio.gather(*tasks)

    # Apply results to markdown
    success_count = 0
    error_count = 0

    for result in results:
        old_pattern = f"![{result.ref.image_id}](images/{result.ref.filename})"

        if result.description:
            description_block = _build_description_block(result.ref, result.description)
            success_count += 1
        else:
            description_block = _build_description_block(
                result.ref,
                f"description unavailable ({result.error or 'unknown error'})"
            )
            error_count += 1

        markdown_content = markdown_content.replace(old_pattern, description_block)

    logger.info(f"Image descriptions complete: {success_count} success, {error_count} failed")

    return markdown_content


async def _describe_single_image(
    client: AsyncOpenAI,
    ref: ImageRef,
    images_dir: Path,
    semaphore: asyncio.Semaphore,
) -> DescriptionResult:
    """Describe a single image with retry logic."""
    settings = get_settings()

    async with semaphore:
        last_error: str | None = None

        for attempt in range(settings.description_max_retries):
            try:
                description = await _get_image_description(client, ref, images_dir)
                return DescriptionResult(ref=ref, description=description, error=None)

            except RateLimitError as e:
                last_error = f"rate limit: {e}"
                # Longer wait for rate limits
                wait_time = settings.description_retry_delay * (2 ** attempt) * 2
                logger.warning(
                    f"Rate limit for {ref.image_id}, "
                    f"retry {attempt + 1}/{settings.description_max_retries} "
                    f"in {wait_time:.1f}s"
                )
                await asyncio.sleep(wait_time)

            except APIConnectionError as e:
                last_error = f"connection error: {e}"
                wait_time = settings.description_retry_delay * (2 ** attempt)
                logger.warning(
                    f"Connection error for {ref.image_id}, "
                    f"retry {attempt + 1}/{settings.description_max_retries} "
                    f"in {wait_time:.1f}s"
                )
                await asyncio.sleep(wait_time)

            except APIError as e:
                last_error = f"API error: {e}"
                # Don't retry 4xx errors (except rate limits)
                if e.status_code and 400 <= e.status_code < 500:
                    logger.error(f"Non-retryable API error for {ref.image_id}: {e}")
                    break
                wait_time = settings.description_retry_delay * (2 ** attempt)
                logger.warning(
                    f"API error for {ref.image_id}, "
                    f"retry {attempt + 1}/{settings.description_max_retries} "
                    f"in {wait_time:.1f}s"
                )
                await asyncio.sleep(wait_time)

            except FileNotFoundError as e:
                # Don't retry missing files
                last_error = str(e)
                logger.error(f"Image file not found: {ref.image_id}")
                break

            except Exception as e:
                last_error = str(e)[:100]
                wait_time = settings.description_retry_delay * (2 ** attempt)
                logger.warning(
                    f"Unexpected error for {ref.image_id}: {e}, "
                    f"retry {attempt + 1}/{settings.description_max_retries}"
                )
                await asyncio.sleep(wait_time)

        logger.error(f"Failed to describe {ref.image_id} after all retries: {last_error}")
        return DescriptionResult(ref=ref, description=None, error=last_error)


async def _get_image_description(
    client: AsyncOpenAI,
    ref: ImageRef,
    images_dir: Path,
) -> str:
    """Get description for a single image using OpenAI Vision."""
    settings = get_settings()
    image_path = images_dir / ref.filename

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Read and encode image
    image_data = image_path.read_bytes()
    image_b64 = base64.b64encode(image_data).decode("utf-8")

    # Determine media type
    ext = image_path.suffix.lower()
    media_type = "image/png" if ext == ".png" else "image/jpeg"

    # Build prompt with context
    context_prompt = ""
    if ref.context_before:
        context_prompt += f"Text before the image: {ref.context_before}\n\n"
    if ref.context_after:
        context_prompt += f"Text after the image: {ref.context_after}\n\n"

    system_prompt = """You are an expert at describing images in documents.
Your task is to provide a clear, concise description of the image that helps
someone understand what the image shows and how it relates to the surrounding text.

Keep descriptions factual and focused. If the image contains text, include the
key textual content. If it's a diagram, chart, or figure, describe what it shows.
For photos, describe the subject matter."""

    user_prompt = f"""Please describe this image from a document.

{context_prompt}Provide a clear, concise description of what the image shows."""

    response = await client.chat.completions.create(
        model=settings.openai_vision_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{image_b64}",
                            "detail": "auto",
                        },
                    },
                ],
            },
        ],
        max_tokens=500,
    )

    description = response.choices[0].message.content
    return description.strip() if description else "No description available"


def _build_description_block(ref: ImageRef, description: str) -> str:
    """Build the description block according to PDR specification."""
    # Format from PDR:
    # <context before image p3-i3>
    # Image p3-i3: the image describes .....
    # <context after image p3-i3>

    lines = []

    # Context before (may be empty)
    if ref.context_before:
        lines.append(ref.context_before)
        lines.append("")

    # Image reference and description
    lines.append(f"![{ref.image_id}](images/{ref.filename})")
    lines.append(f"Image {ref.image_id}: {description}")
    lines.append("")

    # Context after (may be empty)
    if ref.context_after:
        lines.append(ref.context_after)

    return "\n".join(lines)
