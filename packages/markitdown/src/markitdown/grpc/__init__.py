try:
    import grpc  # noqa: F401
except ImportError as exc:
    raise ImportError(
        "The markitdown gRPC server and client require the optional [grpc] "
        "dependencies. Install them with:\n\n"
        "  pip install 'markitdown[grpc]'\n"
    ) from exc

from .client import MarkItDownClient
from .server import MarkItDownServiceServicer, serve

__all__ = ["MarkItDownClient", "MarkItDownServiceServicer", "serve"]
