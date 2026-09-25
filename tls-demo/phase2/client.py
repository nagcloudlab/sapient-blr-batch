#!/usr/bin/env python3
"""Send example data over verified TLS 1.3 to the Phase 2 server."""

import argparse
import socket
import ssl
from pathlib import Path

CERTS = Path(__file__).resolve().parent / "certs"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=6443)
    parser.add_argument("--username", default="student")
    parser.add_argument("--password", default="demo-password-123")
    parser.add_argument("--message", default="Hello server! This message is encrypted in transit.")
    parser.add_argument("--server-name", default="localhost", help="Expected certificate identity")
    parser.add_argument("--system-trust", action="store_true", help="Use system CAs instead of the lab CA; expected to fail")
    args = parser.parse_args()
    lines = []
    for name in ("username", "password", "message"):
        value = getattr(args, name)
        line = f"{name.upper()}: {value}\n"
        if "\r" in value or "\n" in value or len(line.encode("utf-8")) > 4096:
            parser.error(f"{name} must be a single line of at most 4096 bytes including its label")
        lines.append(line)
    payload = "".join(lines)
    print(f"Connecting to {args.host}:{args.port} using verified TLS 1.3...")
    try:
        context = ssl.create_default_context(cafile=None if args.system_trust else str(CERTS / "ca.crt"))
        context.minimum_version = ssl.TLSVersion.TLSv1_3
        # Keep this observation exercise encrypted even if SSLKEYLOGFILE is set.
        context.keylog_filename = None
        with socket.create_connection((args.host, args.port), timeout=10) as raw_socket, context.wrap_socket(raw_socket, server_hostname=args.server_name) as connection:
            print(f"Verified server: {args.server_name}; {connection.version()} / {connection.cipher()[0]}")
            print(f"\nSending fake classroom data:\n{payload}", end="", flush=True)
            connection.sendall(payload.encode("utf-8"))
            with connection.makefile("r", encoding="utf-8") as response:
                print("\nServer response:")
                for line in response:
                    print(line, end="")
    except ssl.SSLCertVerificationError as exc:
        parser.exit(1, f"Certificate verification failed: {exc.verify_message}. No application data sent.\n")
    except OSError as exc:
        parser.exit(1, f"Connection error: {exc}. Check that server.py is running at this host and port.\n")


if __name__ == "__main__":
    main()
