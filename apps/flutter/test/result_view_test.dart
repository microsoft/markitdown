import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:markitdown/src/core/conversion_result.dart';
import 'package:markitdown/src/core/input_document.dart';
import 'package:markitdown/src/ui/conversion_job.dart';
import 'package:markitdown/src/ui/widgets/result_view.dart';

ConversionJob _doneJob() {
  final job = ConversionJob(
    document: InputDocument(
      fileName: 'report.pdf',
      bytes: Uint8List.fromList(utf8.encode('x')),
    ),
  );
  job.status = JobStatus.done;
  job.result = ConversionResult(
    markdown: '# Title\n\nSome **content** here.',
    converterName: 'PDF',
    warnings: const ['A sample warning to render the banner.'],
  );
  return job;
}

Future<void> _pumpAt(WidgetTester tester, Size size) async {
  tester.view.physicalSize = size;
  tester.view.devicePixelRatio = 1.0;
  addTearDown(tester.view.resetPhysicalSize);
  addTearDown(tester.view.resetDevicePixelRatio);
  await tester.pumpWidget(
    MaterialApp(home: Scaffold(body: ResultView(job: _doneJob()))),
  );
  await tester.pump();
}

void main() {
  testWidgets('ResultView lays out on a narrow phone with no overflow',
      (tester) async {
    await _pumpAt(tester, const Size(360, 720));
    expect(tester.takeException(), isNull);
    expect(find.text('Preview'), findsOneWidget);
    expect(find.text('Markdown'), findsOneWidget);
  });

  testWidgets('ResultView lays out on a wide window with no overflow',
      (tester) async {
    await _pumpAt(tester, const Size(1200, 800));
    expect(tester.takeException(), isNull);
    expect(find.text('Save .md'), findsOneWidget);
  });
}
