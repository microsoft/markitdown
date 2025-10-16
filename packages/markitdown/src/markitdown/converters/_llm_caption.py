from typing import BinaryIO, Union, Callable, Any
import base64
import mimetypes
from .._stream_info import StreamInfo


def llm_caption(
    file_stream: BinaryIO, stream_info: StreamInfo, **kwargs: Any
) -> Union[None, str]:
    llm_describber = kwargs.get("llm_describber")
    llm_client = kwargs.get("client")
    llm_model = kwargs.get("model")
    llm_prompt = kwargs.get("prompt")

    if llm_describber is not None:
        return _get_llm_description_from_callback(
            file_stream, stream_info, describber=llm_describber, prompt=llm_prompt
        )
    elif llm_client is not None and llm_model is not None:
        return _get_llm_description_openai(
            file_stream, stream_info, client=llm_client, model=llm_model, prompt=llm_prompt
        )
    return None


def _prepare_data_uri(
    file_stream: BinaryIO, stream_info: StreamInfo
) -> Union[str, None]:
    """Prepares a data URI from a file stream."""
    content_type = stream_info.mimetype
    if not content_type:
        content_type, _ = mimetypes.guess_type("_dummy" + (stream_info.extension or ""))
    if not content_type:
        content_type = "application/octet-stream"

    cur_pos = file_stream.tell()
    try:
        base64_image = base64.b64encode(file_stream.read()).decode("utf-8")
    except Exception:
        return None
    finally:
        file_stream.seek(cur_pos)

    return f"data:{content_type};base64,{base64_image}"


def _get_llm_description_from_callback(
    file_stream: BinaryIO,
    stream_info: StreamInfo,
    *,
    describber: Callable[..., Union[str, None]],
    prompt: Union[str, None],
) -> Union[str, None]:
    """Gets image description from a user-provided callback function."""
    if prompt is None or prompt.strip() == "":
        prompt = "Write a detailed caption for this image."

    data_uri = _prepare_data_uri(file_stream, stream_info)
    if not data_uri:
        return None

    try:
        return describber(data_uri=data_uri, prompt=prompt)
    except Exception:
        return None


def _get_llm_description_openai(
    file_stream: BinaryIO,
    stream_info: StreamInfo,
    *,
    client: Any,
    model: str,
    prompt: Union[str, None],
) -> Union[str, None]:
    """Gets image description using the OpenAI client (legacy method)."""
    if prompt is None or prompt.strip() == "":
        prompt = "Write a detailed caption for this image."

    data_uri = _prepare_data_uri(file_stream, stream_info)
    if not data_uri:
        return None

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": data_uri},
                },
            ],
        }
    ]

    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content