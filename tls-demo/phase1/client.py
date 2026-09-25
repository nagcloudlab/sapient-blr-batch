#!/usr/bin/env python3
"""Send visible, unencrypted example data to the Phase 1 server."""

import argparse
import socket


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--username", default="student")
    parser.add_argument("--password", default="demo-password-123")
    parser.add_argument("--message", default="Hello server! This message is NOT encrypted.")
    args = parser.parse_args()
    lines = []
    for name in ("username", "password", "message"):
        value = getattr(args, name)
        line = f"{name.upper()}: {value}\n"
        if "\r" in value or "\n" in value or len(line.encode("utf-8")) > 4096:
            parser.error(f"{name} must be a single line of at most 4096 bytes including its label")
        lines.append(line)
    payload = "".join(lines)
    print(f"Connecting to {args.host}:{args.port} using TCP without TLS...")
    try:
        with socket.create_connection((args.host, args.port), timeout=10) as connection:
            print(f"\nSending fake classroom data:\n{payload}", end="", flush=True)
            connection.sendall(payload.encode("utf-8"))
            with connection.makefile("r", encoding="utf-8") as response:
                print("\nServer response:")
                for line in response:
                    print(line, end="")
    except OSError as exc:
        parser.exit(1, f"Connection error: {exc}. Check that server.py is running at this host and port.\n")


if __name__ == "__main__":
    main()
