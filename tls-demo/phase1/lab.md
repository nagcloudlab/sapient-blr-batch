# Phase 1 — See plaintext on the network

- **Goal:** observe a TCP conversation and read its contents in Wireshark.
- This demo deliberately has **no TLS**.
- Use the included fake credentials.
- The server acknowledges data but does not authenticate users.

```text
Python client  ── username, password, message ──>  Python server
              <── plaintext acknowledgment ───
                         ↑
                 Wireshark on lo0
```

- Both programs run on one computer by default.
- Loopback traffic stays on that computer.
- Traffic passes through its networking stack and can be captured locally.

## Requirements

- Python 3 (no third-party packages).
- [Wireshark](https://www.wireshark.org/download.html), including its **ChmodBPF** capture-permissions package on macOS.

## Install Wireshark on macOS

- Open **Apple menu → About This Mac** to check your chip: Apple M-series uses the Apple Silicon / Arm installer; Intel uses the Intel installer.
- Visit the [official download page](https://www.wireshark.org/download.html) and download the stable macOS disk image for your chip.
- Open the downloaded `.dmg` and drag **Wireshark** into **Applications**.
- In the same disk image, open **Install ChmodBPF.pkg** and complete the installer, entering your Mac administrator credentials when prompted. This component enables packet capture.
- Open **Applications → Wireshark**. If you missed ChmodBPF, access its installer through **Wireshark → About Wireshark → Folders → macOS Extras** (double-click that entry).
- For this lab, double-click **Loopback: lo0** to start capturing. Run the client only after capture starts, as described below.

- Installation reference: [Wireshark's official macOS guide](https://www.wireshark.org/docs/wsug_html_chunked/ChBuildInstallOSXInstall.html).

## Live demo — use this order

### 1. Start the server in Terminal 1

```sh
cd /Users/nag/tls-demo/phase1
python3 server.py
```

- The server listens on `127.0.0.1:5000` and stays running for repeat demonstrations.

### 2. Start Wireshark before running the client

- Select **Loopback: lo0** on macOS. On Linux use `lo`; on Windows use the Npcap loopback capture interface.
- Optionally set the **capture filter** to `tcp port 5000`.
- Start the capture by double-clicking the interface.
- In the **display filter** bar, enter `tcp.port == 5000` and press Enter.

- Capture and display filters use different syntax.
- Select loopback for this same-computer demo; Wi-Fi will not show the conversation.
- Reference: [Wireshark loopback guide](https://wiki.wireshark.org/CaptureSetup/Loopback).

### 3. Run the client in Terminal 2

```sh
cd /Users/nag/tls-demo/phase1
python3 client.py
```

- The client sends:

```text
USERNAME: student
PASSWORD: demo-password-123
MESSAGE: Hello server! This message is NOT encrypted.
```

- The server prints the received data and sends back:

```text
SERVER: Message received. This is a demo; no login was performed.
SERVER: Your username, password, and message traveled in plaintext.
```

### 4. Reveal the conversation in Wireshark

- Stop capturing with the red square.
- Right-click a packet for TCP port 5000 and choose **Follow → TCP Stream**.
- Select **Entire conversation** and **ASCII** (or UTF-8) if needed.
- Point out the readable password, message, and server reply. The directions appear in different colors.
- Close the stream window and restore `tcp.port == 5000` to inspect the packets.
- Optionally save the capture as `phase1-plaintext.pcapng` using **File → Save As**.

- Follow TCP Stream reassembles the byte stream; one application message does not necessarily equal one packet. See the [Wireshark guide](https://www.wireshark.org/docs/wsug_html_chunked/ChapterAdvanced.html).

## Classroom prompts

- Before revealing the stream, ask: “The password arrived correctly. Does that mean it arrived securely?”

- Find the TCP handshake: SYN, SYN/ACK, ACK. It establishes the TCP connection; it does not encrypt it.
- Read the fake password from the capture. An observer with access to these packets can read the application data without any decryption key.
- Read the reply too. Both directions are exposed.
- Ask: “What would change if this were a real password or a private message?”
- Explain that this capture demonstrates loss of confidentiality. Plain TCP also provides no cryptographic protection against an active attacker changing application data, but this exercise does not demonstrate modification.

- **Phase 2 preview:** wrap the same conversation in TLS.
- Demonstrate encryption, integrity protection, and server authentication through certificate validation.
- TLS still exposes metadata such as IP addresses, timing, and traffic sizes.
- Phase 1 implements only plaintext.

## Repeat with another message

- Start a new capture, then run:

```sh
python3 client.py --username alice --password fake-secret-456 --message "The classroom code is BLUEBIRD."
```

- Stop the server with **Ctrl+C** when finished.

## Optional: use two computers

- On the server computer, bind to its LAN interface:

```sh
python3 server.py --host 0.0.0.0
```

- On the client computer, replace the example address with the server's LAN IP:

```sh
python3 client.py --host 192.168.1.20
```

- Capture on the active Ethernet/Wi-Fi interface of either endpoint.
- Both computers need connectivity.
- The server firewall must allow TCP port 5000.
- Capturing on a third computer does not automatically reveal traffic between the endpoints.

## Troubleshooting

- **Connection refused:** start the server first; use the same host and port in both commands.
- **Address already in use:** run the server and client with `--port 5050`, and change the Wireshark filters to match.
- **No packets:** start capture before the client, choose `lo0` for the local demo, and check the filter.
- **Only ACKs or no readable text:** follow the entire TCP stream, and rerun the client during capture if the original data was missed.
- **Capture permission denied on macOS:** install Wireshark's bundled ChmodBPF package and reopen Wireshark.
