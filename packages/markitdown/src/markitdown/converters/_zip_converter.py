import os
import zipfile
import shutil
from typing import Any, Union

from ._base import DocumentConverter, DocumentConverterResult


class ZipConverter(DocumentConverter):
    """Converts ZIP files to markdown by extracting and converting all contained files.

    The converter extracts the ZIP contents to a temporary directory, processes each file
    using appropriate converters based on file extensions, and then combines the results
    into a single markdown document. The temporary directory is cleaned up after processing.

    Example output format:
    ```markdown
    Content from the zip file `example.zip`:

    ## File: docs/readme.txt

    This is the content of readme.txt
    Multiple lines are preserved

    ## File: images/example.jpg

    ImageSize: 1920x1080
    DateTimeOriginal: 2024-02-15 14:30:00
    Description: A beautiful landscape photo

    ## File: data/report.xlsx

    ## Sheet1
    | Column1 | Column2 | Column3 |
    |---------|---------|---------|
    | data1   | data2   | data3   |
    | data4   | data5   | data6   |
    ```

    Key features:
    - Maintains original file structure in headings
    - Processes nested files recursively
    - Uses appropriate converters for each file type
    - Preserves formatting of converted content
    - Cleans up temporary files after processing
    """

    def __init__(
        self, priority: float = DocumentConverter.PRIORITY_SPECIFIC_FILE_FORMAT
    ):
        super().__init__(priority=priority)

    def convert(
        self, local_path: str, **kwargs: Any
    ) -> Union[None, DocumentConverterResult]:
        # Bail if not a ZIP
        extension = kwargs.get("file_extension", "")
        if extension.lower() != ".zip":
            return None

        # Get parent converters list if available
        parent_converters = kwargs.get("_parent_converters", [])
        if not parent_converters:
            return DocumentConverterResult(
                title=None,
                text_content=f"[ERROR] No converters available to process zip contents from: {local_path}",
            )

        extracted_zip_folder_name = (
            f"extracted_{os.path.basename(local_path).replace('.zip', '_zip')}"
        )
        extraction_dir = os.path.normpath(
            os.path.join(os.path.dirname(local_path), extracted_zip_folder_name)
        )
        md_content = f"Content from the zip file `{os.path.basename(local_path)}`:\n\n"

        try:
            # Extract the zip file safely
            with zipfile.ZipFile(local_path, "r") as zipObj:
                # Safeguard against path traversal
                for member in zipObj.namelist():
                    member_path = os.path.normpath(os.path.join(extraction_dir, member))
                    if (
                        not os.path.commonprefix([extraction_dir, member_path])
                        == extraction_dir
                    ):
                        raise ValueError(
                            f"Path traversal detected in zip file: {member}"
                        )

                # Extract all files safely
                zipObj.extractall(path=extraction_dir)

            # Process each extracted file
            for root, dirs, files in os.walk(extraction_dir):
                for name in files:
                    file_path = os.path.join(root, name)
                    relative_path = os.path.relpath(file_path, extraction_dir)

                    # Get file extension
                    _, file_extension = os.path.splitext(name)

                    # Update kwargs for the file
                    file_kwargs = kwargs.copy()
                    file_kwargs["file_extension"] = file_extension
                    file_kwargs["_parent_converters"] = parent_converters

                    # Try converting the file using available converters
                    for converter in parent_converters:
                        # Skip the zip converter to avoid infinite recursion
                        if isinstance(converter, ZipConverter):
                            continue

                        result = converter.convert(file_path, **file_kwargs)
                        if result is not None:
                            md_content += f"\n## File: {relative_path}\n\n"
                            md_content += result.text_content + "\n\n"
                            break

            # Clean up extracted files if specified
            if kwargs.get("cleanup_extracted", True):
                shutil.rmtree(extraction_dir)

            return DocumentConverterResult(title=None, text_content=md_content.strip())

        except zipfile.BadZipFile:
            return DocumentConverterResult(
                title=None,
                text_content=f"[ERROR] Invalid or corrupted zip file: {local_path}",
            )
        except ValueError as ve:
            return DocumentConverterResult(
                title=None,
                text_content=f"[ERROR] Security error in zip file {local_path}: {str(ve)}",
            )
        except Exception as e:
            return DocumentConverterResult(
                title=None,
                text_content=f"[ERROR] Failed to process zip file {local_path}: {str(e)}",
            )
