# Phase 2 — TLS, certificates, and the secure connection

## Learning goals

- Build a classroom certificate authority (CA) and server certificate manually.
- Explain what a private key, public key, certificate, and CSR do.
- Follow a full TLS 1.3 handshake from TCP connection to encrypted application data.
- Compare what the endpoints know with what a packet observer can see.
- Demonstrate rejection of an untrusted issuer or incorrect server name.
- Use fake classroom credentials throughout; this server acknowledges messages without performing a user login.
- Follow the sections in order; commands assume the `phase2/` directory unless stated otherwise.
- Keep [client.py](client.py) and [server.py](server.py) open alongside this guide.

## 1. Understand the setup

```text
ONE MAC

Terminal 2                                        Terminal 1
client.py                                         server.py
127.0.0.1:<temporary port>                         127.0.0.1:5443
      |                                                |
      +------------- TCP connection over lo0 ----------+
                             |
                         Wireshark

Application:   username / password / message / reply
TLS 1.3:       authentication + encryption + integrity
TCP:           reliable, ordered byte transport
IP/loopback:   local delivery
```

- Port `5443` is our choice; the port number itself provides no security.
- TLS is used directly over TCP; this is not HTTP or HTTPS.
- Both programs can print plaintext because they are endpoints of the encrypted connection.
- Wireshark observes the bytes transported between those endpoints.
- The default client connects to IP `127.0.0.1` but verifies certificate identity `localhost`.
- The destination IP answers “where do I connect?”; the expected name answers “which server must prove its identity?”

## 2. Check tools and prepare a fresh certificate directory

- Check the command-line OpenSSL and Python's TLS library separately; they can use different OpenSSL versions.

```sh
cd /Users/nag/tls-demo/phase2
openssl version
python3 -c 'import ssl; print(ssl.OPENSSL_VERSION); print("TLS 1.3 supported:", ssl.HAS_TLSv1_3)'
```

- Expect `TLS 1.3 supported: True`.
- The commands below use OpenSSL; if your Mac's `openssl` reports LibreSSL or rejects an option, select an installed OpenSSL executable before continuing.
- Wireshark requires ChmodBPF for capture; see [Phase 1 setup](../phase1/lab.md#install-wireshark-on-macos).
- Stop any running Phase 2 server before replacing its certificates.
- Earlier setup already generated certificates; preserve that directory so you can create your own from scratch.
- Run this block once; it moves the old directory into a uniquely named backup without deleting it.

```sh
if [ -d certs ]; then
    cert_backup=$(mktemp -d ./certs-backup.XXXXXX)
    mv certs "$cert_backup/"
fi
umask 077
mkdir certs
```

- `umask 077` restricts newly created files to your user.
- The following manual steps replace the need to run `generate-certs.sh`.
- Keep generated `.key` files and backup directories private.

## 3. Identify the keys before generating them

```text
LONGER-LIVED FILES                         PER-CONNECTION SECRETS

ca.key                                    Ephemeral key-exchange private keys
  | signs server certificate                | generated in memory by TLS
  v                                         v
server.crt + server.key                    Shared key-exchange secret
  | authenticate server                     | key derivation
  |                                         v
  +---- bind identity to handshake ------> Handshake and application keys
                                            | encrypt/authenticate records
                                            v
                                          Protected username/message/reply
```

- **CA private key:** signs certificates; it does not encrypt this conversation.
- **Server private key:** proves possession of the certificate's matching key during the handshake.
- **Certificate:** public identity information, public key, validity dates, extensions, and issuer signature.
- **CSR:** certificate signing request containing a public key and requested identity, signed by the applicant's private key.
- **Ephemeral key-exchange material:** fresh material negotiated for this connection, distinct from the RSA certificate key.
- **Symmetric traffic keys:** derived in memory to protect records, with separate keys for each direction.
- The `.key` files created here are RSA signing keys; TLS 1.3 does not send a session key encrypted with the server's RSA public key.

## 4. Create the classroom CA manually

### 4.1 Generate the CA private key

```sh
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out certs/ca.key
openssl pkey -in certs/ca.key -check -noout
```

- Expect a successful key check.
- The 2048-bit RSA key includes private material and enough information to derive its public key.
- This lab uses an unencrypted key file for simple startup; filesystem permissions protect access to the file.
- Do not display private key contents to explain a public certificate.

### 4.2 Describe the CA certificate

```sh
cat > certs/ca.cnf <<'EOF'
[req]
prompt = no
distinguished_name = dn
x509_extensions = ca_extensions

[dn]
CN = TLS Classroom Lab CA

[ca_extensions]
basicConstraints = critical,CA:true
keyUsage = critical,keyCertSign,cRLSign
subjectKeyIdentifier = hash
EOF
```

- `CN`: human-readable name of this classroom CA.
- `CA:true`: marks this certificate as a CA certificate.
- `keyCertSign`: permits its key to sign certificates.
- `cRLSign`: permits signing certificate revocation lists; this lab does not create one.
- `critical`: a validator must understand and enforce that extension or reject the certificate.
- `subjectKeyIdentifier`: identifies the certificate's public key.

### 4.3 Create the self-signed root certificate

```sh
openssl req -new -x509 -key certs/ca.key -sha256 -days 30 \
    -config certs/ca.cnf -out certs/ca.crt
openssl x509 -in certs/ca.crt -noout -subject -issuer -dates
```

- `-x509`: create a certificate rather than a CSR.
- `-key`: use the existing key rather than generating another one.
- `-sha256`: use SHA-256 in the certificate signature process.
- `-days 30`: set a short lab validity period.
- Expect the CA's subject and issuer to match: it signs its own root certificate.
- A self-signature does not make a CA trustworthy; the client must explicitly choose to trust it.
- `ca.crt` is public and can be distributed to clients through a trusted channel.
- `ca.key` stays with whoever issues certificates; the running server and client do not need it.
- Command reference: [OpenSSL req](https://docs.openssl.org/3.6/man1/openssl-req/).

## 5. Create the server identity manually

### 5.1 Generate a different private key for the server

```sh
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out certs/server.key
openssl pkey -in certs/server.key -check -noout
```

- Never reuse the CA key as the server key.
- The server will load `server.key` at startup and use it for handshake signatures.

### 5.2 Write the server certificate configuration

```sh
cat > certs/server.cnf <<'EOF'
[req]
prompt = no
distinguished_name = dn
req_extensions = requested_extensions

[dn]
CN = localhost

[requested_extensions]
subjectAltName = DNS:localhost,IP:127.0.0.1

[server_extensions]
basicConstraints = critical,CA:false
keyUsage = critical,digitalSignature
extendedKeyUsage = serverAuth
subjectAltName = DNS:localhost,IP:127.0.0.1
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
EOF
```

- **SAN / Subject Alternative Name:** names and IP addresses the certificate identifies.
- `DNS:localhost`: matches the client's default expected server name.
- `IP:127.0.0.1`: also permits validation against this IP literal.
- `CN=localhost` is a descriptive subject field; use SAN for identity matching.
- `CA:false`: this is an endpoint certificate, not a certificate issuer.
- `digitalSignature`: permits signatures, including this lab's TLS server authentication.
- `serverAuth`: permits use for TLS server authentication.
- `authorityKeyIdentifier`: links the certificate to its issuer's key.

### 5.3 Create and inspect the CSR

```sh
openssl req -new -key certs/server.key -config certs/server.cnf -out certs/server.csr
openssl req -in certs/server.csr -noout -verify -text
```

- Find the subject, public key information, and requested SAN entries.
- The CSR contains the public key, not the private key.
- Its signature establishes that the request was signed with the matching private key.
- A valid CSR signature does not establish that the applicant is entitled to a requested name.
- In this classroom, you are the CA operator and approve `localhost` yourself.
- Public CAs use separate validation procedures before issuing certificates.

### 5.4 Sign the server certificate using the CA

```sh
openssl x509 -req -in certs/server.csr \
    -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial \
    -out certs/server.crt -days 30 -sha256 \
    -extfile certs/server.cnf -extensions server_extensions
```

- `-CA` supplies the issuer certificate; `-CAkey` supplies the signing key.
- `-CAcreateserial` creates a serial-number file when needed.
- `-extfile` and `-extensions` explicitly select the certificate extensions approved by our CA.
- The CA signs the certificate's identity, public key, validity, and other signed fields.
- The resulting `server.crt` is public; a signature authenticates its contents but does not make them secret.
- Command reference: [OpenSSL x509](https://docs.openssl.org/3.6/man1/openssl-x509/).

### 5.5 Inspect the issued certificate

```sh
openssl x509 -in certs/server.crt -noout -subject -issuer -dates -serial
openssl x509 -in certs/server.crt -noout -text
```

- Locate `Subject: ... localhost` and `Issuer: ... TLS Classroom Lab CA`.
- Locate SAN entries, `CA:FALSE`, digital-signature usage, and server-authentication purpose.
- Locate the public key and certificate signature algorithm.
- Distinguish the CA's signature on this certificate from the server's later signature on the handshake.

### 5.6 Verify the chain, purpose, and identity before starting the server

```sh
openssl verify -CAfile certs/ca.crt -purpose sslserver \
    -verify_hostname localhost certs/server.crt
openssl verify -CAfile certs/ca.crt -purpose sslserver \
    -verify_ip 127.0.0.1 certs/server.crt
```

- Expect `certs/server.crt: OK` from both commands.
- Confirm that the certificate's public key matches the server private key by comparing these two fingerprints:

```sh
openssl pkey -in certs/server.key -pubout -outform DER | openssl dgst -sha256
openssl x509 -in certs/server.crt -pubkey -noout | openssl pkey -pubin -outform DER | openssl dgst -sha256
```

- Expect identical SHA-256 values; these commands output fingerprints of public keys.
- Offline verification does not prove a live server possesses its private key; the TLS handshake will do that.
- Verification reference: [OpenSSL verify](https://docs.openssl.org/3.6/man1/openssl-verify/).

## 6. Trace the trust chain and file ownership

```text
YOU, AS THE CA OPERATOR
ca.key ---- signs ----> server.crt
                          |
                          | contains server public key + localhost SAN
                          v
SERVER                              CLIENT
server.crt                          ca.crt (explicit trust anchor)
server.key                          expected name: localhost
    |                                   |
    +--- presents certificate ---------->
    +--- proves private-key possession -> validates identity and proof

Not sent over the connection:
  ca.key, server.key, ephemeral private keys, derived traffic keys
```

- The client trusts this CA because `client.py` loads `certs/ca.crt` explicitly.
- The server loads `certs/server.crt` and `certs/server.key`.
- The CSR, CA private key, serial file, and configuration files are issuance artifacts; they are not needed during ordinary connections.
- Our CA signs the server directly; there are no intermediate CAs in this lab.
- Real deployments often send a leaf certificate plus intermediate certificates; the root is already trusted by the client.
- Sending a root certificate during a handshake does not make the client trust it.
- No macOS Keychain changes are needed for this lab.

## 7. Run the first secure exchange

### 7.1 Start the server in Terminal 1

```sh
cd /Users/nag/tls-demo/phase2
python3 server.py
```

- Expect `TLS 1.3 server listening on 127.0.0.1:5443`.
- At startup the server loads its certificate and key; it has not yet negotiated any connection keys.

### 7.2 Start Wireshark before the client

- Select **Loopback: lo0**.
- Optionally set the capture filter to `tcp port 5443`.
- Start capture, then set the display filter to `tcp.port == 5443`.
- Capture filters select what gets recorded; display filters select what is shown afterward.

### 7.3 Run the client in Terminal 2

```sh
cd /Users/nag/tls-demo/phase2
python3 client.py
```

- Expect `Verified server: localhost; TLSv1.3` followed by a cipher name.
- The exact cipher and key-exchange group depend on the installed TLS libraries.
- Expect these application values in the endpoint terminals:

```text
USERNAME: student
PASSWORD: demo-password-123
MESSAGE: Hello server! This message is encrypted in transit.
```

- Expect the server to acknowledge receipt and confirm TLS transport.
- Leave the server running for the remaining exercises.

## 8. Follow the full TLS 1.3 handshake

- The diagram shows a fresh certificate-authenticated connection without client certificates, resumption, or early data.
- Arrows represent logical messages, not necessarily individual packets.

```text
CLIENT                                                   SERVER
  |                                                         |
  |---------------- TCP SYN ------------------------------->|
  |<--------------- TCP SYN + ACK --------------------------|
  |---------------- TCP ACK ------------------------------->|
  |                                                         |
  |---------------- ClientHello --------------------------->| clear
  |<--------------- ServerHello ----------------------------| clear
  |                                                         |
  |   both derive handshake traffic keys from key exchange   |
  |                                                         |
  |<--------------- EncryptedExtensions ---------------------| encrypted
  |<--------------- Certificate -----------------------------| encrypted
  |<--------------- CertificateVerify -----------------------| encrypted
  |<--------------- Finished --------------------------------| encrypted
  |                                                         |
  | validate certificate, expected name, signature, Finished |
  |                                                         |
  |---------------- Finished ------------------------------->| encrypted
  |                                                         |
  |---------------- username/password/message -------------->| application keys
  |<--------------- acknowledgment --------------------------| application keys
```

### 8.1 TCP connects first

- TCP establishes an ordered byte stream through SYN, SYN/ACK, and ACK.
- No server certificate has been checked at this point.
- TCP itself does not keep the application data confidential.
- In the code, `socket.create_connection(...)` performs this stage.

### 8.2 ClientHello proposes the cryptographic settings

- The client supplies supported TLS versions, cipher suites, signature algorithms, and key-exchange groups.
- Its `key_share` extension carries public key-exchange material; the corresponding private material stays local.
- The default DNS server name `localhost` is supplied through SNI for server selection.
- SNI is not certificate validation: requesting a name and proving a name are different operations.
- This lab does not configure Encrypted ClientHello, so its ClientHello metadata is visible.

### 8.3 ServerHello selects settings

- The server selects a mutually supported version, cipher suite, and key share.
- For example, `TLS_AES_256_GCM_SHA384` specifies AES-256-GCM record protection and SHA-384 for the TLS key schedule.
- In TLS 1.3 the cipher suite does not also select the certificate signature algorithm or key-exchange group.
- Read the actual selected group in the capture; do not assume it is always X25519.
- A server that needs a different offered group can send HelloRetryRequest; the client then sends another ClientHello.

### 8.4 Key exchange produces a shared secret

- For an elliptic-curve Diffie-Hellman exchange, each side combines its private value with the other side's public value.
- Both calculations produce the same secret; a passive observer cannot feasibly recover it from the public values alone.
- The following is conceptual ECDHE notation, not code and not a description of every possible negotiated group.

```text
Client private a                         Server private b
Client public A = a*G                    Server public B = b*G

               A ---------------------->
                 <---------------------- B

Client calculates a*B                    Server calculates b*A
                  \                      /
                   same shared secret Z
```

- The certificate key is separate from `a` and `b`; it authenticates the exchange.
- Key exchange without authentication would allow an active intermediary to establish separate secrets with each peer.
- Ephemeral exchange provides forward secrecy against later compromise of the server signing key, assuming ephemeral secrets have been discarded and the algorithms remain secure.

### 8.5 Derive handshake keys

- TLS uses HKDF and transcript hashes to turn key-exchange inputs into purpose-specific secrets.
- The transcript is the ordered handshake messages; hashing it binds key derivation and authentication to this conversation.
- Separate client and server handshake traffic secrets yield separate keys and IVs.
- Encryption starts before the client has completed server authentication; the application waits for validation before sending the password.

```text
Key-exchange secret + TLS key schedule + transcript hashes
                         |
                         v
       client/server HANDSHAKE traffic secrets
                         |
                         v
        handshake keys + IVs (one per direction)

Later transcript stage + key schedule
                         |
                         v
       client/server APPLICATION traffic secrets
                         |
                         v
        application keys + IVs (one per direction)
```

### 8.6 EncryptedExtensions and Certificate

- EncryptedExtensions carries negotiated parameters that do not belong in ServerHello.
- Certificate carries the server certificate and any needed intermediate certificates.
- In TLS 1.3 these messages are encrypted using handshake keys.
- The client checks a trusted certification path, certificate validity, server purpose, and expected identity.
- This demo does not configure online revocation checking; avoid presenting it as a complete public-Web PKI implementation.

### 8.7 CertificateVerify proves possession of the server key

- The server signs handshake-related data using `server.key`.
- The client verifies that signature with the public key in `server.crt`.
- Copying the public certificate alone does not let an attacker produce this proof.
- The CA's certificate signature establishes an identity-to-key binding; CertificateVerify binds possession of that key to this handshake.

### 8.8 Finished confirms handshake integrity

- Each peer sends a Finished message based on a derived secret and the handshake transcript.
- The recipient verifies it before accepting the corresponding handshake as valid.
- Unexpected alterations to the handshake cause verification to fail.
- The client in this lab sends application data only after its `wrap_socket(...)` handshake succeeds.
- The server completes its handshake before entering the application handler.
- Protocol reference: [TLS 1.3 handshake, authentication, and key schedule](https://www.rfc-editor.org/rfc/rfc8446).

## 9. Follow one application message under the hood

```text
CLIENT APPLICATION
  "PASSWORD: demo-password-123\n"
                  |
           UTF-8 encoding
                  |
          TLS record protection
     application key + nonce + plaintext
                  |
                  v
     record header | ciphertext | authentication tag
                  |
            TCP byte stream
                  |
             Wireshark sees
          protected record bytes
                  |
                  v
SERVER TLS
  verify tag + decrypt with matching receive key
                  |
             plaintext bytes
                  |
SERVER APPLICATION
  readline() -> decode UTF-8 -> print password
```

- TLS records use authenticated encryption, such as AES-GCM or ChaCha20-Poly1305.
- A per-record nonce is derived using an IV and sequence number; nonce reuse with the same key must be avoided.
- The authentication tag detects unauthorized modification of protected data.
- A failed tag check causes TLS to reject the record; it does not deliver attacker-modified plaintext to the application.
- TLS record sequencing also prevents a copied record from simply being accepted again later in the same connection.
- The reply uses the server-to-client application key, not the client-to-server key.
- A single `sendall()` may span records or TCP packets; one packet is not one application message.
- TLS protects transit, not endpoint logs or memory; the demo deliberately prints the fake password.
- The server never checks whether the fake password is valid: TLS authentication and user login are separate layers.

## 10. Map the protocol to the Python code

- In `server.py`, `SSLContext(PROTOCOL_TLS_SERVER)` creates server-side TLS settings.
- `minimum_version = TLSVersion.TLSv1_3` requires TLS 1.3 or later rather than allowing older versions.
- `load_cert_chain(...)` loads the server certificate and matching private key.
- `wrap_socket(..., server_side=True)` performs the handshake on an accepted TCP socket.
- Only after success does the server call the application handler.
- In `client.py`, `create_default_context(cafile=...)` enables certificate validation and trusts the lab CA.
- `server_hostname=args.server_name` supplies the expected certificate identity and, for DNS names, SNI.
- Client `wrap_socket(...)` negotiates TLS and validates the server before returning.
- `sendall()` on the TLS socket encrypts the supplied bytes; reading its file wrapper yields decrypted bytes.
- `version()` and `cipher()` report negotiated results; they do not select them.
- The Python `ssl` module delegates cryptographic operations and the handshake state machine to its TLS library.
- The code explicitly disables session-key logging for the baseline Wireshark exercise.
- API reference: [Python ssl](https://docs.python.org/3/library/ssl.html).

## 11. Inspect the baseline capture in Wireshark

### 11.1 Read the visible handshake

- Stop capture and retain the display filter `tcp.port == 5443`.
- If only TCP is decoded, choose **Analyze → Decode As**, select TCP port 5443, and choose **TLS**.
- Find TCP SYN, SYN/ACK, and ACK before ClientHello.
- Filter ClientHello with `tcp.port == 5443 && tls.handshake.type == 1`.
- Expand supported versions, cipher suites, supported groups, signature algorithms, SNI, and key share.
- Filter ServerHello with `tcp.port == 5443 && tls.handshake.type == 2`.
- Inspect its selected cipher, key share, and `supported_versions` extension.
- Use the negotiated version extension to identify TLS 1.3; legacy version fields can show TLS 1.2 for compatibility.
- A dummy ChangeCipherSpec can appear for compatibility; it is not the key exchange.

### 11.2 Observe what encryption hides

- Restore `tcp.port == 5443`, then right-click a packet → **Follow → TCP Stream**.
- Select the entire conversation and ASCII or UTF-8 display.
- Look for `demo-password-123`; it should not appear as plaintext.
- Compare with the Phase 1 stream, where the same fake password was readable.
- Do not expect to inspect the TLS 1.3 server certificate in the baseline capture: it is encrypted after ServerHello.
- Packets labeled Application Data can contain encrypted handshake messages, application messages, or alerts.
- Addresses, ports, sizes, timing, and the unencrypted Hello metadata remain visible.
- A `localhost` string in ClientHello is not a leaked application password.
- Save as `phase2-tls.pcapng` if desired.
- Inspection reference: [Wireshark TLS guide](https://wiki.wireshark.org/TLS).

## 12. Observe decrypted handshake messages at an endpoint

- Keep the Python server running.
- Use OpenSSL as an alternate TLS client to print handshake state and message details locally.
- This works because the endpoint has the secrets; it does not break encryption.

```sh
openssl s_client -connect 127.0.0.1:5443 \
    -servername localhost -CAfile certs/ca.crt \
    -verify_hostname localhost -verify_return_error \
    -tls1_3 -state -msg
```

- Find ClientHello, ServerHello, EncryptedExtensions, Certificate, CertificateVerify, and Finished in the diagnostic output.
- OpenSSL can display received handshake contents after decrypting them locally.
- `-servername` requests a server name; `-verify_hostname` separately checks the certificate identity.
- `-verify_return_error` makes certificate verification failures stop the connection.
- Once connected, paste these three lines promptly; the server's application read timeout is 30 seconds.

```text
USERNAME: student
PASSWORD: demo-password-123
MESSAGE: Hello from the OpenSSL endpoint.
```

- Read the server acknowledgment; use Ctrl+C if the diagnostic client remains open.
- Some OpenSSL versions report `unexpected eof while reading` when this demo server closes its socket without a full TLS `close_notify` exchange.
- That shutdown limitation is separate from successful handshake validation and receipt of the acknowledged message; do not interpret bare EOF as authenticated message completion in a production protocol.
- Diagnostic reference: [OpenSSL s_client](https://docs.openssl.org/3.6/man1/openssl-s_client/).

## 13. Demonstrate authentication failures

### 13.1 Correct server, wrong expected name

```sh
python3 client.py --server-name wrong.example
```

- Expect a hostname mismatch and `No application data sent`.
- The TCP destination stays `127.0.0.1`; only the expected identity changes.
- The CA is trusted, but the certificate does not cover `wrong.example`.

### 13.2 Correct name, untrusted issuer

```sh
python3 client.py --system-trust
```

- Expect verification failure because the lab CA was not installed in system trust.
- TCP and part of the TLS handshake can occur; the username/password payload is not sent.
- The server should log the rejected handshake and continue accepting clients.

### 13.3 Restore the working case

```sh
python3 client.py
```

- Expect successful verification and the server response.
- Ask students to explain why both trusted issuance and name matching are necessary.
- Do not disable verification to fix these deliberately failing exercises.

## 14. Check student understanding

- **Who signs `server.crt`?** The lab CA using `ca.key`.
- **Who signs CertificateVerify?** The server using `server.key`.
- **Where does the client get trust?** From its explicitly configured `ca.crt`.
- **Is the CA contacted for each connection?** No; local trust and signature checks suffice for this lab.
- **Is the password encrypted with RSA?** No; derived symmetric application keys encrypt TLS records.
- **Are shared traffic keys sent over the wire?** No; the peers derive them.
- **Does encryption begin only after checking the certificate?** No; handshake encryption starts after ServerHello, before authentication completes.
- **Does the server authenticate the student?** No; this lab performs server authentication, not client-certificate authentication or password checking.
- **Can someone with only the public certificate impersonate the server?** Not without the matching private-key proof or another validation failure.
- **Can the server's RSA key alone decrypt an old ECDHE TLS 1.3 capture?** No; ephemeral exchange provides forward secrecy under its assumptions.
- **What remains visible?** Addresses, ports, timing, sizes, and some handshake metadata.

## 15. Troubleshooting and cleanup

- **Certificate files missing:** complete manual sections 4 and 5; filenames must match those loaded by the code.
- **Key/certificate mismatch:** compare public-key fingerprints and sign a CSR made from the intended server key.
- **Expired or not-yet-valid certificate:** inspect dates and the Mac's clock; regenerate if needed.
- **Unexpected trust failure:** confirm the running server and client use certificates from the same newly created CA; restart the server after replacing files.
- **Connection refused:** start `server.py` first and check port 5443.
- **Port occupied:** use `--port 5444` on both Python commands and update capture/display filters and diagnostic commands.
- **No packets:** start capture on `lo0` before the client.
- **Cannot see Certificate in Wireshark:** expected for TLS 1.3 without traffic secrets; use the endpoint diagnostics in section 12.
- **Private key does not decrypt TLS 1.3 capture:** expected for ephemeral exchange; private certificate keys are not session traffic secrets.
- **Repeated client runs:** each invocation creates a new process and context; this lab does not demonstrate session resumption or 0-RTT.
- **Completion:** stop the server with Ctrl+C and stop Wireshark capture.
- Keep certificate artifacts for repeating the lab; exclude private keys, backups, and captures from version control.
