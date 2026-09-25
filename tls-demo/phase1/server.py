#!/usr/bin/env python3
"""Phase 1: intentionally plaintext TCP server for a classroom demo."""

import argparse
import socketserver


class PlaintextHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.request.settimeout(30)
        print(f"\nClient connected: {self.client_address}", flush=True)
        try:
            for expected in ("USERNAME", "PASSWORD", "MESSAGE"):
                line = self.rfile.readline(4097)
                if len(line) > 4096 or not line.endswith(b"\n"):
                    self.wfile.write(b"ERROR: missing or oversized line\n")
                    return
                text = line.decode("utf-8").rstrip("\r\n")
                if not text.startswith(expected + ": "):
                    self.wfile.write(b"ERROR: expected USERNAME, PASSWORD, MESSAGE lines\n")
                    return
                print(f"Received > {text}", flush=True)
            response = (
                "SERVER: Message received. This is a demo; no login was performed.\n"
                "SERVER: Your username, password, and message traveled in plaintext.\n"
            )
            self.wfile.write(response.encode("utf-8"))
            print(response, end="", flush=True)
        except (OSError, UnicodeError) as exc:
            print(f"Connection ended: {exc}", flush=True)


class PlaintextServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    try:
        with PlaintextServer((args.host, args.port), PlaintextHandler) as server:
            print(f"PLAINTEXT server listening on {args.host}:{args.port}", flush=True)
            print("Use fake data only. Press Ctrl+C to stop.", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as exc:
        parser.exit(1, f"Server error: {exc}\n")


if __name__ == "__main__":
    main()
