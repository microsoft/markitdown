// Dev-only CLI to run the converters on real files for validation.
// Usage: dart run tool/convert_file.dart <path-to-file>
import 'dart:io';

import 'package:markitdown/src/core/input_document.dart';
import 'package:markitdown/src/core/markitdown.dart';
import 'package:path/path.dart' as p;

Future<void> main(List<String> args) async {
  if (args.isEmpty) {
    stderr.writeln('Usage: dart run tool/convert_file.dart <file>');
    exit(64);
  }
  final path = args.first;
  final bytes = await File(path).readAsBytes();
  final md = MarkItDown();
  final result = await md.convert(
    InputDocument(fileName: p.basename(path), bytes: bytes),
  );
  stdout.write(result.markdown);
  if (result.warnings.isNotEmpty) {
    stderr.writeln('\n--- warnings ---');
    for (final w in result.warnings) {
      stderr.writeln('• $w');
    }
  }
}
