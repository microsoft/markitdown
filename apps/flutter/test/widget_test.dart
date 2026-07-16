import 'package:flutter_test/flutter_test.dart';

import 'package:markitdown/main.dart';

void main() {
  testWidgets('App launches with the empty-state prompt', (tester) async {
    await tester.pumpWidget(const MarkItDownApp());
    await tester.pump();

    expect(find.text('Turn any file into Markdown'), findsOneWidget);
  });
}
