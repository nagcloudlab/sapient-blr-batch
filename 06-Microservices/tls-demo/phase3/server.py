#!/usr/bin/env python3
"""Phase 3: require a verified client certificate before accepting demo data."""

import argparse
from pathlib import Path
import socketserver
import ssl

CERTS = Path(__file__).resolve().parent / "certs"
READY = b"READY: client certificate verified\n"


class MTLSHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.request.settimeout(15)
        certificate = self.request.getpeercert()
        subject = dict(item for group in certificate["subject"] for item in group)
        print(f"\nVerified client certificate: {subject}", flush=True)
        print(f"Client SAN: {certificate.get('subjectAltName', ())}", flush=True)
        print(f"TLS: {self.request.version()} / {self.request.cipher()[0]}", flush=True)
        try:
            # A TLS 1.3 client may finish its local handshake before learning
            # that the server rejected its certificate. Gate data on this reply.
            self.wfile.write(READY)
            for expected in ("USERNAME", "PASSWORD", "MESSAGE"):
                line = self.rfile.readline(4097)
                if len(line) > 4096 or not line.endswith(b"\n"):
                    self.wfile.write(b"ERROR: missing or oversized line\n")
                    return
                value = line.decode("utf-8").rstrip("\r\n")
                if not value.startswith(expected + ": "):
                    self.wfile.write(b"ERROR: expected USERNAME, PASSWORD, MESSAGE lines\n")
                    return
                print(f"Received > {value}", flush=True)
            self.wfile.write(
                b"OK: Message received over mutual TLS.\n"
                b"INFO: Certificate authenticated; demo username/password were not checked.\n"
                b"END\n"
            )
        except (OSError, UnicodeError) as exc:
            print(f"Connection ended: {exc}", flush=True)


class MTLSServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def process_request_thread(self, request, client_address):
        request.settimeout(10)
        try:
            secured = self.context.wrap_socket(request, server_side=True)
        except OSError as exc:
            print(f"Client handshake rejected: {exc}", flush=True)
            request.close()
            return
        super().process_request_thread(secured, client_address)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=6443)
    args = parser.parse_args()
    try:
        context = ssl.create_default_context(
            purpose=ssl.Purpose.CLIENT_AUTH, cafile=str(CERTS / "ca.crt")
        )
        context.minimum_version = ssl.TLSVersion.TLSv1_3
        context.keylog_filename = None
        context.load_cert_chain(CERTS / "server.crt", CERTS / "server.key")
        context.verify_mode = ssl.CERT_REQUIRED
        with MTLSServer((args.host, args.port), MTLSHandler) as server:
            server.context = context
            print(f"mTLS server listening on {args.host}:{args.port}", flush=True)
            print("A trusted client certificate is required. Press Ctrl+C to stop.", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except FileNotFoundError:
        parser.exit(1, "Certificate files missing. Follow the manual steps in phase3/lab.md.\n")
    except OSError as exc:
        parser.exit(1, f"Server error: {exc}\n")


if __name__ == "__main__":
    main()
