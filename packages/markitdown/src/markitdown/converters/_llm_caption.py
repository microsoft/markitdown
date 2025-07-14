from typing import BinaryIO, Union
import base64
import mimetypes
from .._stream_info import StreamInfo


def llm_caption(
    file_stream: BinaryIO, stream_info: StreamInfo, *, client, model, prompt=None
) -> Union[None, str]:
    if prompt is None or prompt.strip() == "":
        prompt = "Write a detailed caption for this image."

    # Get the content type
    content_type = stream_info.mimetype
    if not content_type:
        content_type, _ = mimetypes.guess_type("_dummy" + (stream_info.extension or ""))
    if not content_type:
        content_type = "application/octet-stream"

    # Convert to base64
    cur_pos = file_stream.tell()
    try:
        base64_image = base64.b64encode(file_stream.read()).decode("utf-8")
    except Exception as e:
        return None
    finally:
        file_stream.seek(cur_pos)

    # Prepare the data-uri
    data_uri = f"data:{content_type};base64,{base64_image}"

    # Prepare the OpenAI API request
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": data_uri,
                    },
                },
            ],
        }
    ]

    # Call the OpenAI API
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content
