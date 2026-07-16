import 'dart:convert';
import 'dart:typed_data';

import 'package:archive/archive.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:markitdown/src/core/conversion_result.dart';
import 'package:markitdown/src/core/input_document.dart';
import 'package:markitdown/src/core/markitdown.dart';

InputDocument doc(String name, String content) => InputDocument(
      fileName: name,
      bytes: Uint8List.fromList(utf8.encode(content)),
    );

Uint8List zipOf(Map<String, String> entries) {
  final archive = Archive();
  entries.forEach((name, content) {
    archive.addFile(ArchiveFile.string(name, content));
  });
  return ZipEncoder().encodeBytes(archive);
}

void main() {
  final md = MarkItDown();

  test('CSV becomes a Markdown table', () async {
    final r = await md.convert(doc('data.csv', 'Name,Age\nAlice,30\nBob,25'));
    expect(r.markdown, contains('| Name | Age |'));
    expect(r.markdown, contains('| --- | --- |'));
    expect(r.markdown, contains('| Alice | 30 |'));
  });

  test('JSON becomes a nested outline', () async {
    final r = await md.convert(
        doc('x.json', '{"name":"Ada","langs":["dart","python"]}'));
    expect(r.markdown, contains('**name:** Ada'));
    expect(r.markdown, contains('dart'));
  });

  test('HTML converts headings and links', () async {
    final r = await md.convert(doc('p.html',
        '<html><body><h1>Hi</h1><p>See <a href="https://x.com">link</a></p></body></html>'));
    expect(r.markdown, contains('# Hi'));
    expect(r.markdown, contains('[link](https://x.com)'));
  });

  test('XML becomes an outline', () async {
    final r = await md.convert(
        doc('n.xml', '<root><item id="1">Hello</item></root>'));
    expect(r.markdown, contains('item'));
    expect(r.markdown, contains('Hello'));
  });

  test('Plain code files are fenced', () async {
    final r = await md.convert(doc('a.py', 'print("hi")'));
    expect(r.markdown, contains('```python'));
    expect(r.markdown, contains('print("hi")'));
  });

  test('DOCX extracts headings, bold and tables', () async {
    const document = '''<?xml version="1.0"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>
  <w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>My Title</w:t></w:r></w:p>
  <w:p><w:r><w:t xml:space="preserve">Hello </w:t></w:r><w:r><w:rPr><w:b/></w:rPr><w:t>world</w:t></w:r></w:p>
  <w:tbl>
    <w:tr><w:tc><w:p><w:r><w:t>A</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>B</w:t></w:r></w:p></w:tc></w:tr>
    <w:tr><w:tc><w:p><w:r><w:t>1</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>2</w:t></w:r></w:p></w:tc></w:tr>
  </w:tbl>
</w:body>
</w:document>''';
    final bytes = zipOf({'word/document.xml': document});
    final r = await md.convert(InputDocument(fileName: 'f.docx', bytes: bytes));
    expect(r.markdown, contains('# My Title'));
    expect(r.markdown, contains('Hello **world**'));
    expect(r.markdown, contains('| A | B |'));
    expect(r.markdown, contains('| 1 | 2 |'));
  });

  test('XLSX extracts a table with shared strings', () async {
    final bytes = zipOf({
      'xl/workbook.xml':
          '<workbook xmlns:r="r"><sheets><sheet name="Data" r:id="rId1"/></sheets></workbook>',
      'xl/_rels/workbook.xml.rels':
          '<Relationships><Relationship Id="rId1" Target="worksheets/sheet1.xml"/></Relationships>',
      'xl/sharedStrings.xml':
          '<sst><si><t>Name</t></si><si><t>Age</t></si><si><t>Alice</t></si></sst>',
      'xl/worksheets/sheet1.xml': '<worksheet><sheetData>'
          '<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1" t="s"><v>1</v></c></row>'
          '<row r="2"><c r="A2" t="s"><v>2</v></c><c r="B2"><v>30</v></c></row>'
          '</sheetData></worksheet>',
    });
    final r = await md.convert(InputDocument(fileName: 'f.xlsx', bytes: bytes));
    expect(r.markdown, contains('| Name | Age |'));
    expect(r.markdown, contains('| Alice | 30 |'));
  });

  test('PPTX extracts slide titles and bullets', () async {
    const slide = '<p:sld xmlns:p="p" xmlns:a="a"><p:cSld><p:spTree>'
        '<p:sp><p:nvSpPr><p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr>'
        '<p:txBody><a:p><a:r><a:t>My Slide</a:t></a:r></a:p></p:txBody></p:sp>'
        '<p:sp><p:txBody><a:p><a:r><a:t>Point one</a:t></a:r></a:p></p:txBody></p:sp>'
        '</p:spTree></p:cSld></p:sld>';
    final bytes = zipOf({'ppt/slides/slide1.xml': slide});
    final r = await md.convert(InputDocument(fileName: 'f.pptx', bytes: bytes));
    expect(r.markdown, contains('## Slide 1'));
    expect(r.markdown, contains('### My Slide'));
    expect(r.markdown, contains('- Point one'));
  });

  test('PDF extracts text from an uncompressed content stream', () async {
    const pdf = '%PDF-1.4\n'
        '1 0 obj<< /Length 40 >>\n'
        'stream\n'
        'BT /F1 12 Tf (Hello PDF World) Tj ET\n'
        'endstream\n'
        'endobj\n';
    final r = await md.convert(InputDocument(
      fileName: 'f.pdf',
      bytes: Uint8List.fromList(latin1.encode(pdf)),
    ));
    expect(r.markdown, contains('Hello PDF World'));
  });

  test('Unsupported binary throws a friendly error', () async {
    final bytes = Uint8List.fromList([0, 1, 2, 3, 0, 255, 12]);
    expect(
      () => md.convert(InputDocument(fileName: 'x.bin', bytes: bytes)),
      throwsA(isA<UnsupportedFormatException>()),
    );
  });
}
