#!/usr/bin/env python3
"""Phase 2: TLS-protected TCP server for a classroom demo."""

import argparse
import socketserver
import ssl
from pathlib import Path

CERTS = Path(__file__).resolve().parent / "certs"


class TLSHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.request.settimeout(30)
        print(f"TLS established: {self.request.version()} / {self.request.cipher()[0]}", flush=True)
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
                "SERVER: Your username, password, and message traveled inside TLS.\n"
            )
            self.wfile.write(response.encode("utf-8"))
            print(response, end="", flush=True)
        except (OSError, UnicodeError) as exc:
            print(f"Connection ended: {exc}", flush=True)


class TLSServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def process_request_thread(self, request, client_address):
        # Perform the handshake in the worker so one slow peer cannot block accepts.
        request.settimeout(10)
        try:
            secured = self.context.wrap_socket(request, server_side=True)
        except OSError as exc:
            print(f"TLS handshake rejected: {exc}", flush=True)
            request.close()
            return
        super().process_request_thread(secured, client_address)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5443)
    args = parser.parse_args()
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.minimum_version = ssl.TLSVersion.TLSv1_3
        context.load_cert_chain(CERTS / "server.crt", CERTS / "server.key")
        with TLSServer((args.host, args.port), TLSHandler) as server:
            server.context = context
            print(f"TLS 1.3 server listening on {args.host}:{args.port}", flush=True)
            print("Use fake data only. Press Ctrl+C to stop.", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except FileNotFoundError:
        parser.exit(1, "Certificate files missing. Follow the manual certificate steps in phase2/lab.md.\n")
    except OSError as exc:
        parser.exit(1, f"Server error: {exc}\n")


if __name__ == "__main__":
    main()
