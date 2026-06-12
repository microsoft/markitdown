# SPDX-FileCopyrightText: 2026-present Aryan Kaushik <aryankaushik251@gmail.com>
#
# SPDX-License-Identifier: MIT

import re
import sys
from typing import Any, BinaryIO, Dict, List, Optional

from markitdown import DocumentConverter, DocumentConverterResult, StreamInfo, MissingDependencyException

# Lazy loading of pydicom to raise MissingDependencyException during conversion if not installed.
_dependency_exc_info = None
try:
    import pydicom
except ImportError:
    _dependency_exc_info = sys.exc_info()


class DicomConverter(DocumentConverter):
    """
    Converts DICOM (.dcm) files to structured, token-efficient Markdown.
    Extracts key Study, Series, Acquisition, Equipment, and Image characteristics.
    Omits and redacts Patient PII (Name, ID, Birth Date) by default.
    """

    def __init__(self, redact_pii: bool = True, **kwargs: Any):
        super().__init__()
        self._redact_pii = redact_pii

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        # Check standard extension / MIME type
        if extension in (".dcm", ".dicom") or mimetype == "application/dicom":
            return True

        # Peek at stream to check signature 'DICM' at offset 128
        cur_pos = file_stream.tell()
        try:
            file_stream.seek(128)
            sig = file_stream.read(4)
            if sig == b"DICM":
                return True
        except Exception:
            pass
        finally:
            file_stream.seek(cur_pos)

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        # Check if pydicom is available
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                "markitdown-dicom requires pydicom to be installed. "
                "To resolve, run: pip install pydicom"
            ) from _dependency_exc_info[1].with_traceback(_dependency_exc_info[2])  # type: ignore

        # Resolve redact_pii setting (defaulting to True)
        redact_pii = kwargs.get("redact_pii", self._redact_pii)

        # Parse DICOM from the stream.
        # Use defer_size="1 KB" so we don't load large pixel data arrays into memory.
        # force=True allows parsing datasets without file meta header.
        try:
            ds = pydicom.dcmread(file_stream, defer_size="1 KB", force=True)
            if ds is None or len(ds) == 0:
                raise ValueError("Parsed dataset has no elements.")
        except Exception as e:
            raise ValueError(f"Failed to parse DICOM file: {e}") from e

        # Extracted elements
        lines = ["# DICOM File", ""]

        # Date and Time Formatter helpers
        def _format_date(val: Any) -> Optional[str]:
            if not val:
                return None
            val_str = str(val).strip()
            if len(val_str) == 8 and val_str.isdigit():
                return f"{val_str[0:4]}-{val_str[4:6]}-{val_str[6:8]}"
            return val_str

        def _format_time(val: Any) -> Optional[str]:
            if not val:
                return None
            val_str = str(val).strip()
            if "." in val_str:
                time_part, frac_part = val_str.split(".", 1)
            else:
                time_part, frac_part = val_str, ""

            if len(time_part) >= 6 and time_part.isdigit():
                formatted = f"{time_part[0:2]}:{time_part[2:4]}:{time_part[4:6]}"
                if frac_part:
                    formatted += f".{frac_part}"
                return formatted
            elif len(time_part) >= 4 and time_part.isdigit():
                formatted = f"{time_part[0:2]}:{time_part[2:4]}"
                if frac_part:
                    formatted += f".{frac_part}"
                return formatted
            return val_str

        def _get_val(keyword: str) -> Any:
            val = getattr(ds, keyword, None)
            if val is None:
                return None
            if isinstance(val, (list, tuple)) or type(val).__name__ == "MultiValue":
                return ", ".join(str(x) for x in val)
            return val

        # Define category structures
        # 1. Patient Information
        p_name = _get_val("PatientName")
        p_id = _get_val("PatientID")
        p_dob = _get_val("PatientBirthDate")

        if redact_pii:
            p_name = "[REDACTED]" if p_name is not None else None
            p_id = "[REDACTED]" if p_id is not None else None
            p_dob = "[REDACTED]" if p_dob is not None else None
        else:
            if p_name:
                p_name = str(p_name).replace("^", " ").strip()

        patient_fields = {
            "Patient Name": p_name,
            "Patient ID": p_id,
            "Patient Birth Date": _format_date(p_dob),
            "Patient Sex": _get_val("PatientSex"),
            "Patient Age": _get_val("PatientAge"),
        }

        # 2. Study Information
        study_fields = {
            "Study Instance UID": _get_val("StudyInstanceUID"),
            "Study Date": _format_date(_get_val("StudyDate")),
            "Study Time": _format_time(_get_val("StudyTime")),
            "Study Description": _get_val("StudyDescription"),
            "Accession Number": _get_val("AccessionNumber"),
        }

        # 3. Series Information
        series_fields = {
            "Series Instance UID": _get_val("SeriesInstanceUID"),
            "Series Number": _get_val("SeriesNumber"),
            "Series Description": _get_val("SeriesDescription"),
        }

        # 4. Acquisition Information
        acquisition_fields = {
            "Modality": _get_val("Modality"),
            "Protocol Name": _get_val("ProtocolName"),
            "Exposure": _get_val("Exposure"),
            "Exposure Time": _get_val("ExposureTime"),
            "KVP": _get_val("KVP"),
            "Acquisition Date": _format_date(_get_val("AcquisitionDate")),
            "Acquisition Time": _format_time(_get_val("AcquisitionTime")),
        }

        # 5. Equipment Information
        equipment_fields = {
            "Manufacturer": _get_val("Manufacturer"),
            "Manufacturer Model Name": _get_val("ManufacturerModelName"),
            "Device Serial Number": _get_val("DeviceSerialNumber"),
            "Software Versions": _get_val("SoftwareVersions"),
        }

        # 6. Image Characteristics
        rows = _get_val("Rows")
        cols = _get_val("Columns")
        resolution = f"{rows} × {cols}" if rows and cols else None

        pixel_data_present = "Yes" if (0x7FE0, 0x0010) in ds else "No"

        image_fields = {
            "Resolution": resolution,
            "Samples Per Pixel": _get_val("SamplesPerPixel"),
            "Bits Allocated": _get_val("BitsAllocated"),
            "Bits Stored": _get_val("BitsStored"),
            "High Bit": _get_val("HighBit"),
            "Pixel Representation": _get_val("PixelRepresentation"),
            "Photometric Interpretation": _get_val("PhotometricInterpretation"),
            "Frame Count": _get_val("NumberOfFrames"),
            "Pixel Data Present": pixel_data_present,
        }

        # 7. Other Useful Text Fields
        other_fields = {
            "Image Comments": _get_val("ImageComments"),
            "Institution Name": _get_val("InstitutionName"),
            "Station Name": _get_val("StationName"),
            "Body Part Examined": _get_val("BodyPartExamined"),
        }

        # Helper to render sections
        def _render_section(title: str, fields: Dict[str, Any]) -> List[str]:
            active = {k: v for k, v in fields.items() if v is not None and str(v).strip() != ""}
            if not active:
                return []
            sec_lines = [f"## {title}", ""]
            for k, v in active.items():
                sec_lines.append(f"* **{k}**: {v}")
            sec_lines.append("")
            return sec_lines

        # Predefined sections
        lines.extend(_render_section("Patient Information", patient_fields))
        lines.extend(_render_section("Study Information", study_fields))
        lines.extend(_render_section("Series Information", series_fields))
        lines.extend(_render_section("Acquisition Parameters", acquisition_fields))
        lines.extend(_render_section("Equipment", equipment_fields))
        lines.extend(_render_section("Image Properties", image_fields))
        lines.extend(_render_section("Other Information", other_fields))

        # 8. Private / Custom textual tags when reasonable
        EXCLUDED_KEYWORDS = {
            # Study
            "StudyInstanceUID", "StudyDate", "StudyTime", "StudyDescription", "AccessionNumber",
            # Series
            "SeriesInstanceUID", "SeriesNumber", "SeriesDescription",
            # Acquisition
            "Modality", "ProtocolName", "Exposure", "ExposureTime", "KVP", "AcquisitionDate", "AcquisitionTime",
            # Equipment
            "Manufacturer", "ManufacturerModelName", "DeviceSerialNumber", "SoftwareVersions",
            # Image Characteristics
            "Rows", "Columns", "SamplesPerPixel", "BitsAllocated", "BitsStored", "HighBit", "PixelRepresentation", "PhotometricInterpretation", "NumberOfFrames",
            # Other Useful Text Fields
            "ImageComments", "InstitutionName", "StationName", "BodyPartExamined",
            # Patient info
            "PatientName", "PatientID", "PatientBirthDate", "PatientSex", "PatientAge"
        }
        EXCLUDED_VRS = {"OB", "OW", "OF", "OD", "SQ", "UN"}

        custom_fields: Dict[str, str] = {}
        for elem in ds:
            # Skip file meta or pixel group
            if elem.tag.group in (0x0002, 0x7FE0) or elem.tag.element == 0:
                continue

            # Skip binary, sequence, or unknown VRs
            if elem.VR in EXCLUDED_VRS:
                continue

            keyword = elem.keyword
            if not keyword:
                if elem.tag.is_private:
                    label = f"Private Tag ({elem.tag.group:04X},{elem.tag.element:04X})"
                else:
                    label = f"Tag ({elem.tag.group:04X},{elem.tag.element:04X})"
            else:
                if keyword in EXCLUDED_KEYWORDS:
                    continue
                # Split CamelCase to separate words
                label = re.sub(r'(?<!^)(?=[A-Z])', ' ', keyword)

            val = elem.value
            if val is None or val == "":
                continue

            # Check for PII tags if redaction is enabled
            lower_label = label.lower()
            if redact_pii and ("patient" in lower_label or "name" in lower_label or "birth" in lower_label or "id" in lower_label):
                if "sex" not in lower_label and "age" not in lower_label:
                    continue

            # Format list value or other type
            if isinstance(val, (list, tuple)) or type(val).__name__ == "MultiValue":
                val_str = ", ".join(str(x) for x in val)
            else:
                val_str = str(val)

            if elem.VR == "PN":
                val_str = val_str.replace("^", " ").strip()

            custom_fields[label] = val_str

        # Render custom & private tags if any
        if custom_fields:
            sorted_custom = dict(sorted(custom_fields.items()))
            lines.extend(_render_section("Additional Fields", sorted_custom))

        # Strip extra trailing whitespaces/newlines and return result
        markdown_content = "\n".join(lines).strip() + "\n"
        return DocumentConverterResult(
            title=study_fields.get("Study Description") or "DICOM Document",
            markdown=markdown_content,
        )
