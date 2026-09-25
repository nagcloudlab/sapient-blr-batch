#!/usr/bin/env python3
"""Phase 3: verify the server and present a client certificate over TLS 1.3."""

import argparse
from pathlib import Path
import socket
import ssl

CERTS = Path(__file__).resolve().parent / "certs"


def read_line(stream):
    line = stream.readline(4097)
    if len(line) > 4096 or not line.endswith(b"\n"):
        raise OSError("Missing or oversized server response")
    return line.decode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=6443)
    parser.add_argument("--server-name", default="localhost")
    parser.add_argument("--ca", type=Path, default=CERTS / "ca.crt")
    parser.add_argument("--cert", type=Path, default=CERTS / "client.crt")
    parser.add_argument("--key", type=Path, default=CERTS / "client.key")
    parser.add_argument("--no-client-cert", action="store_true", help="Negative test: omit client certificate")
    parser.add_argument("--username", default="student")
    parser.add_argument("--password", default="demo-password-123")
    parser.add_argument("--message", default="Hello server! Both peers use certificates.")
    args = parser.parse_args()
    lines = []
    for name in ("username", "password", "message"):
        value = getattr(args, name)
        line = f"{name.upper()}: {value}\n"
        if "\r" in value or "\n" in value or len(line.encode("utf-8")) > 4096:
            parser.error(f"{name} must be one line of at most 4096 bytes including its label")
        lines.append(line)
    payload = "".join(lines)
    payload_attempted = False
    try:
        context = ssl.create_default_context(cafile=str(args.ca))
        context.minimum_version = ssl.TLSVersion.TLSv1_3
        context.keylog_filename = None
        if not args.no_client_cert:
            context.load_cert_chain(args.cert, args.key)
        print(f"Connecting to {args.host}:{args.port} using mTLS...", flush=True)
        with socket.create_connection((args.host, args.port), timeout=10) as raw:
            with context.wrap_socket(raw, server_hostname=args.server_name) as connection:
                print(f"Verified server: {args.server_name}; {connection.version()} / {connection.cipher()[0]}", flush=True)
                with connection.makefile("rb") as response:
                    if read_line(response) != "READY: client certificate verified\n":
                        raise OSError("Server did not acknowledge client certificate verification")
                    print("Server accepted the client certificate.", flush=True)
                    print(f"\nSending fake classroom data:\n{payload}", end="", flush=True)
                    payload_attempted = True
                    connection.sendall(payload.encode("utf-8"))
                    if read_line(response) != "OK: Message received over mutual TLS.\n":
                        raise OSError("Server did not acknowledge the message")
                    info = read_line(response)
                    if read_line(response) != "END\n":
                        raise OSError("Incomplete server response")
                    print("OK: Message received over mutual TLS.")
                    print(info, end="")
    except (OSError, UnicodeError) as exc:
        status = "Message delivery was not confirmed." if payload_attempted else "No application payload sent."
        parser.exit(1, f"Connection failed: {exc}\n{status}\n")


if __name__ == "__main__":
    main()
