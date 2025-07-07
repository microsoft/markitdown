import base64
import mimetypes
from typing import BinaryIO, Union

from openai import AsyncOpenAI, OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionUserMessageParam
from openai.types.chat.chat_completion_content_part_image_param import (
    ChatCompletionContentPartImageParam,
    ImageURL,
)
from openai.types.chat.chat_completion_content_part_text_param import (
    ChatCompletionContentPartTextParam,
)

from .._stream_info import StreamInfo


# TODO: Add Content Safety test to ensure there is no prompt injection
async def _llm_completion(
    client: Union[AsyncOpenAI, OpenAI],
    messages: list[ChatCompletionMessageParam],
    model: str,
) -> Union[str, None]:
    """
    Perform a completion request using the OpenAI API.

    Either an asynchronous or synchronous client can be used. If an sync client is used, user will be warned.

    Return the raw response content.
    """
    # Use either async or sync client based on the type of client provided
    if isinstance(client, AsyncOpenAI):
        response = await client.chat.completions.create(
            messages=messages,
            model=model,
        )
    else:
        print("Warning: Using synchronous OpenAI is blocking the event loop")
        response = client.chat.completions.create(
            messages=messages,
            model=model,
        )

    return response.choices[0].message.content if response.choices else None


async def llm_image_caption(
    file_stream: BinaryIO,
    stream_info: StreamInfo,
    *,
    client: Union[AsyncOpenAI, OpenAI],
    model: str,
    prompt: str = None,
) -> str | None:
    """
    Generate a caption for an image using the OpenAI API.

    Image is converted to a base64 then sent in the request.
    """
    if prompt is None or prompt.strip() == "":
        prompt = "Write a detailed caption for this image."

    # Get the content type
    content_type = stream_info.mimetype
    if not content_type:
        content_type, _ = mimetypes.guess_type("_dummy" + (stream_info.extension or ""))
    if not content_type:
        content_type = "application/octet-stream"

    # Convert to base64
    # TODO: Stream the request to avoid buffering the base64 image in memory
    cur_pos = file_stream.tell()
    try:
        base64_image = base64.b64encode(file_stream.read()).decode("utf-8")
    except Exception:
        return None
    finally:
        file_stream.seek(cur_pos)

    # Prepare the data-uri
    data_uri = f"data:{content_type};base64,{base64_image}"

    # Prepare the OpenAI API request
    messages = [
        ChatCompletionUserMessageParam(
            role="user",
            content=[
                ChatCompletionContentPartTextParam(
                    type="text",
                    text=prompt,
                ),
                ChatCompletionContentPartImageParam(
                    type="image_url",
                    image_url=ImageURL(
                        detail="auto",
                        url=data_uri,
                    ),
                ),
            ],
        ),
    ]

    return await _llm_completion(
        client=client,
        messages=messages,
        model=model,
    )
