// Serves the built Flutter web app on localhost with automatic free-port
// selection: if the preferred port is busy (another app is using it), it
// transparently moves to the next free port instead of failing.
//
// Usage:
//   flutter build web
//   dart run tool/serve_web.dart            # serves build/web
//   dart run tool/serve_web.dart <dir> <port>
import 'dart:io';

import 'package:path/path.dart' as p;

const _preferredPorts = [8080, 8081, 8082, 3000, 5000, 4173];

const _contentTypes = <String, String>{
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.wasm': 'application/wasm',
  '.css': 'text/css; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.ttf': 'font/ttf',
  '.otf': 'font/otf',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.map': 'application/json; charset=utf-8',
  '.bin': 'application/octet-stream',
};

Future<void> main(List<String> args) async {
  final rootPath = args.isNotEmpty
      ? args[0]
      : p.join(Directory.current.path, 'build', 'web');
  final root = Directory(rootPath);
  if (!root.existsSync()) {
    stderr.writeln('❌ Web build not found at: ${root.path}');
    stderr.writeln('   Build it first with:  flutter build web');
    exit(1);
  }

  final requested = args.length > 1 ? int.tryParse(args[1]) : null;
  final server = await _bind(requested);

  final url = 'http://localhost:${server.port}';
  stdout.writeln('');
  stdout.writeln('  ✅ MarkItDown is running at  $url');
  stdout.writeln('  📁 Serving: ${root.path}');
  stdout.writeln('  ⏹  Press Ctrl+C to stop.');
  stdout.writeln('');

  await for (final request in server) {
    unawaited(_handle(request, root));
  }
}

/// Binds to [requested] if given and free, else tries the preferred ports,
/// else asks the OS for any free port. Never crashes on a busy port.
Future<HttpServer> _bind(int? requested) async {
  final candidates = <int>[?requested, ..._preferredPorts];
  for (final port in candidates) {
    try {
      return await HttpServer.bind(InternetAddress.loopbackIPv4, port);
    } on SocketException {
      stdout.writeln('  ⚠ Port $port is in use — trying the next free port…');
    }
  }
  // Port 0 => the operating system hands back any available port.
  return HttpServer.bind(InternetAddress.loopbackIPv4, 0);
}

Future<void> _handle(HttpRequest request, Directory root) async {
  final response = request.response;
  try {
    var relative = Uri.decodeComponent(request.uri.path);
    if (relative == '/' || relative.isEmpty) relative = '/index.html';

    // Resolve and guard against path traversal outside the web root.
    final rootAbs = p.normalize(root.absolute.path);
    var target = p.normalize(p.join(rootAbs, relative.substring(1)));
    if (!p.isWithin(rootAbs, target) && target != rootAbs) {
      target = p.join(rootAbs, 'index.html');
    }

    var file = File(target);
    if (!file.existsSync()) {
      // Single-page-app fallback so deep links still load.
      file = File(p.join(rootAbs, 'index.html'));
    }

    final type = _contentTypes[p.extension(file.path).toLowerCase()] ??
        'application/octet-stream';
    response.headers.set(HttpHeaders.contentTypeHeader, type);
    response.headers.set('Cache-Control', 'no-cache');
    await response.addStream(file.openRead());
  } catch (_) {
    response.statusCode = HttpStatus.internalServerError;
  } finally {
    await response.close();
  }
}

void unawaited(Future<void> future) {}
