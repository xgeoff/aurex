#!/usr/bin/env python3

import argparse
import http.server
import socketserver
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve a directory with no-cache headers.")
    parser.add_argument(
        "--dir",
        default="docs",
        help="Directory to serve relative to the repo root. Default: docs",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind. Default: 8000",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    directory = (REPO_ROOT / args.dir).resolve()

    if not directory.is_dir():
      raise SystemExit(f"Directory not found: {directory}")

    class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *handler_args, **handler_kwargs):
            super().__init__(*handler_args, directory=str(directory), **handler_kwargs)

        def end_headers(self) -> None:
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            super().end_headers()

    with socketserver.TCPServer(("", args.port), NoCacheHandler) as httpd:
        print(f"Serving {directory} at http://localhost:{args.port} with no-cache headers")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
