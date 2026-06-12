# SPDX-FileCopyrightText: 2026-present Aryan Kaushik <aryankaushik251@gmail.com>
#
# SPDX-License-Identifier: MIT

import io
import pytest
from typing import Dict, Any, Optional

import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid

from markitdown import MarkItDown, StreamInfo
from markitdown_dicom import DicomConverter


def create_mock_dicom(
    patient_name: Optional[str] = "Test^Patient",
    patient_id: Optional[str] = "123456",
    patient_dob: Optional[str] = "19800101",
    modality: str = "CT",
    study_description: str = "Mock Study",
    rows: Optional[int] = 512,
    cols: Optional[int] = 512,
    has_pixel_data: bool = True,
    extra_fields: Optional[Dict[str, Any]] = None,
) -> io.BytesIO:
    """Helper to programmatically generate a valid DICOM file in memory."""
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.2"  # CT Image Storage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    file_meta.ImplementationClassUID = pydicom.uid.PYDICOM_IMPLEMENTATION_UID

    ds = FileDataset("in_memory.dcm", {}, file_meta=file_meta, preamble=b"\0" * 128)

    if patient_name is not None:
        ds.PatientName = patient_name
    if patient_id is not None:
        ds.PatientID = patient_id
    if patient_dob is not None:
        ds.PatientBirthDate = patient_dob

    ds.PatientSex = "M"
    ds.PatientAge = "045Y"
    ds.Modality = modality
    ds.StudyInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
    ds.StudyDate = "20260612"
    ds.StudyTime = "120000.123"
    ds.StudyDescription = study_description
    ds.AccessionNumber = "ACC-12345"
    ds.SeriesNumber = 1
    ds.SeriesDescription = "PA View"
    ds.Manufacturer = "GE Medical Systems"

    if rows is not None:
        ds.Rows = rows
    if cols is not None:
        ds.Columns = cols

    ds.SamplesPerPixel = 1
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 0
    ds.PhotometricInterpretation = "MONOCHROME2"

    if has_pixel_data:
        # Use simple dummy bytes for pixel data
        ds.PixelData = b"\x00" * 100

    if extra_fields:
        for keyword, val in extra_fields.items():
            setattr(ds, keyword, val)

    buffer = io.BytesIO()
    ds.save_as(buffer, enforce_file_format=False)
    buffer.seek(0)
    return buffer


def test_dicom_converter_accepts() -> None:
    """Verifies that the DicomConverter accepts DICOM streams using metadata or signature checks."""
    converter = DicomConverter()

    # Case 1: Acceptance by extension
    assert converter.accepts(
        io.BytesIO(b""),
        StreamInfo(extension=".dcm"),
    )
    assert converter.accepts(
        io.BytesIO(b""),
        StreamInfo(extension=".dicom"),
    )

    # Case 2: Acceptance by MIME type
    assert converter.accepts(
        io.BytesIO(b""),
        StreamInfo(mimetype="application/dicom"),
    )

    # Case 3: Acceptance by peeking at DICM signature at offset 128
    mock_dicom = create_mock_dicom()
    assert converter.accepts(
        mock_dicom,
        StreamInfo(extension=".raw"),  # Wrong extension, but valid stream
    )

    # Case 4: Rejection of non-DICOM content
    assert not converter.accepts(
        io.BytesIO(b"\x00" * 200),
        StreamInfo(extension=".txt"),
    )


def test_dicom_converter_default_redaction() -> None:
    """Tests that by default, patient identifying details are redacted but clinical demographics are kept."""
    converter = DicomConverter()
    stream = create_mock_dicom(
        patient_name="Doe^John",
        patient_id="PID-999",
        patient_dob="19750505",
    )

    result = converter.convert(stream, StreamInfo())

    # PatientName, PatientID, and PatientBirthDate must be redacted
    assert "Doe John" not in result.markdown
    assert "PID-999" not in result.markdown
    assert "1975-05-05" not in result.markdown
    assert "Patient Name**: [REDACTED]" in result.markdown
    assert "Patient ID**: [REDACTED]" in result.markdown
    assert "Patient Birth Date**: [REDACTED]" in result.markdown

    # Patient Sex and Age should remain as clinical metadata
    assert "Patient Sex**: M" in result.markdown
    assert "Patient Age**: 045Y" in result.markdown

    # Verifying other standard sections are rendered properly
    assert "Study Description**: Mock Study" in result.markdown
    assert "Resolution**: 512 × 512" in result.markdown
    assert "Study Date**: 2026-06-12" in result.markdown
    assert "Study Time**: 12:00:00.123" in result.markdown


def test_dicom_converter_disabled_redaction() -> None:
    """Tests that when redact_pii is set to False, identifiers are extracted normally."""
    converter = DicomConverter(redact_pii=False)
    stream = create_mock_dicom(
        patient_name="Doe^John",
        patient_id="PID-999",
        patient_dob="19750505",
    )

    result = converter.convert(stream, StreamInfo())

    assert "Patient Name**: Doe John" in result.markdown
    assert "Patient ID**: PID-999" in result.markdown
    assert "Patient Birth Date**: 1975-05-05" in result.markdown


def test_dicom_converter_missing_fields() -> None:
    """Verifies that missing optional tags do not raise exceptions and are simply omitted."""
    converter = DicomConverter()
    # Create DICOM file with no manufacturer, resolution, or description
    stream = create_mock_dicom(
        study_description="",
        rows=None,
        cols=None,
    )

    result = converter.convert(stream, StreamInfo())

    # Ensure no empty field or error occurs
    assert "Resolution" not in result.markdown
    assert "Study Description" not in result.markdown
    assert "Manufacturer**" in result.markdown  # Manufacturer remains since it wasn't set to None
    assert "DICOM File" in result.markdown


def test_dicom_converter_custom_and_private_tags() -> None:
    """Verifies that extra textual/numeric tags and private tags are formatted correctly."""
    converter = DicomConverter(include_private_tags=True)

    # Add custom standard tags (e.g. BodyPartExamined, InstitutionName) and a private tag
    # Private tags use odd group numbers, e.g., 0x0009
    extra_fields = {
        "InstitutionName": "Central Hospital",
        "BodyPartExamined": "CHEST",
        "InstitutionAddress": "123 Clinic Rd",
    }
    stream = create_mock_dicom(extra_fields=extra_fields)

    # Let's add a raw private tag directly to the dataset
    ds = pydicom.dcmread(stream, force=True)
    # Register private creator block
    ds.private_block(0x0009, "Mock Creator", create=True)
    # Add a private element in group 0x0009
    ds[0x0009, 0x1001] = pydicom.dataelem.DataElement(0x00091001, "LO", "Mock Private Value")

    # Save modified dataset to a new stream
    new_stream = io.BytesIO()
    ds.save_as(new_stream)
    new_stream.seek(0)

    result = converter.convert(new_stream, StreamInfo())

    # Verify standard custom fields
    assert "Institution Name**: Central Hospital" in result.markdown
    assert "Body Part Examined**: CHEST" in result.markdown

    # Verify additional standard fields split camelcase
    assert "Institution Address**: 123 Clinic Rd" in result.markdown

    # Verify private tag rendering
    assert "Private Tag (0009,1001)**: Mock Private Value" in result.markdown


def test_dicom_converter_exclude_private_tags_by_default() -> None:
    """Verifies that private tags are excluded by default when include_private_tags is False."""
    converter = DicomConverter()  # default is False

    extra_fields = {
        "InstitutionName": "Central Hospital",
    }
    stream = create_mock_dicom(extra_fields=extra_fields)

    ds = pydicom.dcmread(stream, force=True)
    ds.private_block(0x0009, "Mock Creator", create=True)
    ds[0x0009, 0x1001] = pydicom.dataelem.DataElement(0x00091001, "LO", "Mock Private Value")

    new_stream = io.BytesIO()
    ds.save_as(new_stream)
    new_stream.seek(0)

    result = converter.convert(new_stream, StreamInfo())

    # Standard custom fields should still be present
    assert "Institution Name**: Central Hospital" in result.markdown

    # Private tags should be excluded
    assert "Mock Private Value" not in result.markdown
    assert "Private Tag" not in result.markdown


def test_markitdown_plugin_integration() -> None:
    """Tests that MarkItDown loads and uses the DicomConverter when enable_plugins is True."""
    md = MarkItDown(enable_plugins=True)
    stream = create_mock_dicom(study_description="Integration Test")

    # Convert using the file stream with hint
    result = md.convert(stream, stream_info=StreamInfo(extension=".dcm"))

    assert "Study Description**: Integration Test" in result.markdown
    assert "Patient Name**: [REDACTED]" in result.markdown


def test_corrupted_dicom() -> None:
    """Verifies that a corrupted DICOM stream raises ValueError during conversion."""
    converter = DicomConverter()
    corrupt_stream = io.BytesIO(b"DICM" + b"\xff" * 100)

    with pytest.raises(ValueError, match="Failed to parse DICOM file"):
        converter.convert(corrupt_stream, StreamInfo())
