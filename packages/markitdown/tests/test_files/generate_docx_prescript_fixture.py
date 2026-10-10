"""Rebuild the minimal DOCX fixture for left-hand equation scripts."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def generate_fixture() -> None:
    parts = {
        "[Content_Types].xml": """<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>""",
        "_rels/.rels": """<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdDocument" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>""",
        "word/document.xml": """<w:document
  xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
  xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <w:body>
    <w:p><w:r><w:t>Isotope notation</w:t></w:r></w:p>
    <w:p>
      <w:r><w:t xml:space="preserve">Carbon isotope: </w:t></w:r>
      <m:oMath><m:sPre>
        <m:sub><m:r><m:t>6</m:t></m:r></m:sub>
        <m:sup><m:r><m:t>14</m:t></m:r></m:sup>
        <m:e><m:r><m:t>C</m:t></m:r></m:e>
      </m:sPre></m:oMath>
      <w:r><w:t>.</w:t></w:r>
    </w:p>
    <m:oMathPara><m:oMath>
      <m:r><m:t>X+</m:t></m:r>
      <m:sPre><m:sPrePr/>
        <m:sub><m:r><m:t>92</m:t></m:r></m:sub>
        <m:sup><m:r><m:t>235</m:t></m:r></m:sup>
        <m:e><m:r><m:t>U</m:t></m:r></m:e>
      </m:sPre>
    </m:oMath></m:oMathPara>
    <w:p>
      <w:r><w:t xml:space="preserve">Equation after: </w:t></w:r>
      <m:oMath><m:r><m:t>x+1</m:t></m:r></m:oMath>
    </w:p>
  </w:body>
</w:document>""",
    }
    destination = Path(__file__).with_name("docx_math_prescripts.docx")
    with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
        for name, content in parts.items():
            archive.writestr(name, content.encode("utf-8"))


if __name__ == "__main__":
    generate_fixture()
