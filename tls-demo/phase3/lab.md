# Phase 3 — Mutual TLS: both peers prove their identity

## 1. Learning goals and differences from Phase 2

- **Phase 1:** TCP transports readable application data.
- **Phase 2:** TLS encrypts traffic and the client authenticates the server.
- **Phase 3:** mTLS also requires the client to authenticate with a certificate and proof of private-key possession.
- Create all certificates manually; no generation script is needed.
- Use a new, independent Phase 3 CA so this exercise does not depend on Phase 2 certificates.
- Observe successful authentication and deliberate failures before the demo payload is sent.
- Continue using fake credentials; the server does not implement password login.

```text
PHASE 2: server authentication

Client  <--- server certificate + proof ---  Server
        checks server identity

PHASE 3: mutual authentication

Client  <--- server certificate + proof ---  Server
        checks server identity
Client  ---- client certificate + proof -->  Server
                                      checks client identity

          <==== encrypted application data ====>
```

- mTLS uses the same TLS record encryption mechanisms as Phase 2; it adds client authentication.
- A certificate identifies a key holder according to the issuing CA's identity policy.
- Authentication asks “which identity proved possession of its key?”
- Authorization asks “what may that identity do?”
- This server accepts any valid client-authentication certificate from its configured CA; it has no per-user authorization policy.
- A client certificate does not automatically mean a human user typed a password or consented to an action.

## 2. Prepare the environment

- Use Python with TLS 1.3 support, the OpenSSL command-line tool, and Wireshark with ChmodBPF.
- Review [Phase 2](../phase2/lab.md) for certificate basics and key derivation.
- Use port `6443` and capture the Mac's **Loopback: lo0** interface.
- Run commands from `phase3/` unless a step says otherwise.

```sh
cd /Users/nag/tls-demo/phase3
openssl version
python3 -c 'import ssl; print(ssl.OPENSSL_VERSION); print("TLS 1.3 supported:", ssl.HAS_TLSv1_3)'
```

- Expect TLS 1.3 support to be `True`.
- These commands target OpenSSL; if the executable reports LibreSSL and rejects an option, select an installed OpenSSL executable.
- Stop any running Phase 3 server before replacing its certificate files.
- Run this preparation block once; on a repeat attempt it preserves existing certificates in a unique backup directory.

```sh
if [ -d certs ]; then
    cert_backup=$(mktemp -d ./certs-backup.XXXXXX)
    mv certs "$cert_backup/"
fi
umask 077
mkdir certs
```

- `umask 077` restricts newly created files to your user.
- Private key files are unencrypted for classroom convenience; keep them and their backups private.
- No macOS Keychain or system trust changes are required.

## 3. Plan the certificates and trust relationships

```text
                       Phase 3 Lab CA
                     ca.crt + ca.key
                       /          \
                 signs              signs
                   /                  \
          server.crt                  client.crt
          server.key                  client.key
          SAN: localhost              SAN URI: urn:tls-demo:student
          EKU: serverAuth             EKU: clientAuth

CLIENT TRUSTS ca.crt                  SERVER TRUSTS ca.crt
  verifies server.crt                  verifies client.crt
  checks localhost                     checks client-auth purpose
  checks server's key proof            checks client's key proof
```

- The CA private key signs certificates and is not needed by either running endpoint.
- The server and client each have their own private key.
- Neither sends its private key across the connection.
- Both receive a trusted copy of the CA public certificate before connecting.
- One CA serves both roles in this lab; production systems can use different trust stores for servers and clients.
- The server certificate names `localhost` and `127.0.0.1`.
- The client certificate uses the identity URI `urn:tls-demo:student`; it does not need to match the client's IP address.
- The server logs that URI but does not enforce a URI allowlist.
- Certificate names are assertions approved by a trusted issuer; merely copying the same name into an untrusted certificate does not confer trust.

## 4. Create the certificate configuration manually

- Write one OpenSSL configuration with separate CA, server, and client extension sections.

```sh
cat > certs/pki.cnf <<'EOF'
[req]
prompt = no
distinguished_name = dn

[dn]
CN = Phase 3 Lab CA

[ca_extensions]
basicConstraints = critical,CA:true
keyUsage = critical,keyCertSign,cRLSign
subjectKeyIdentifier = hash

[server_extensions]
basicConstraints = critical,CA:false
keyUsage = critical,digitalSignature
extendedKeyUsage = serverAuth
subjectAltName = DNS:localhost,IP:127.0.0.1
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer

[client_extensions]
basicConstraints = critical,CA:false
keyUsage = critical,digitalSignature
extendedKeyUsage = clientAuth
subjectAltName = URI:urn:tls-demo:student
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
EOF
```

- `CA:true` permits the CA role; `CA:false` marks endpoint certificates.
- `keyCertSign` permits certificate signing; `digitalSignature` permits endpoint handshake signatures.
- **EKU / Extended Key Usage:** `serverAuth` and `clientAuth` identify the permitted TLS roles.
- The server certificate is deliberately server-only; it should fail the later client-authentication test.
- The client SAN URI represents an application identity rather than a DNS destination.
- `subjectKeyIdentifier` identifies a key; `authorityKeyIdentifier` links a leaf to its issuer.
- Extensions marked `critical` must be understood and enforced by validators.
- This lab explicitly applies approved extensions when signing; it does not blindly copy CSR requests.

## 5. Create the CA manually

```sh
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out certs/ca.key
openssl req -new -x509 -key certs/ca.key -sha256 -days 30 \
    -config certs/pki.cnf -extensions ca_extensions -out certs/ca.crt
openssl x509 -in certs/ca.crt -noout -subject -issuer -dates
```

- Expect matching subject and issuer: `Phase 3 Lab CA`.
- `ca.crt` is a self-signed root certificate; explicitly configured trust makes it an anchor.
- `ca.key` must remain with the issuer; clients and servers only need `ca.crt` at runtime.
- Certificates in this exercise expire after 30 days.

## 6. Create the server certificate manually

```sh
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out certs/server.key
openssl req -new -key certs/server.key -subj '/CN=localhost' \
    -config certs/pki.cnf -out certs/server.csr
openssl req -in certs/server.csr -noout -verify -subject
openssl x509 -req -in certs/server.csr \
    -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial \
    -days 30 -sha256 -extfile certs/pki.cnf -extensions server_extensions \
    -out certs/server.crt
```

- The CSR contains the public key and subject and is signed with the server private key.
- CSR signature verification checks possession of the key, not entitlement to a name.
- You act as CA operator and approve `localhost` through the selected extensions.
- `server.crt` now binds the server's public key to its identity and server-authentication purpose.

## 7. Create the client certificate manually

```sh
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out certs/client.key
openssl req -new -key certs/client.key -subj '/CN=student' \
    -config certs/pki.cnf -out certs/client.csr
openssl req -in certs/client.csr -noout -verify -subject
openssl x509 -req -in certs/client.csr \
    -CA certs/ca.crt -CAkey certs/ca.key -CAserial certs/ca.srl \
    -days 30 -sha256 -extfile certs/pki.cnf -extensions client_extensions \
    -out certs/client.crt
```

- Use the existing CA serial file created during server certificate issuance.
- `client.key` belongs to the client, independently of the server key.
- `client.crt` has client-authentication EKU and the student URI SAN.
- No client password is needed to prove possession of this unencrypted key file.
- Real deployments must provision and protect client private keys; anyone who obtains the key can potentially use its certificate identity until it expires or is otherwise rejected.

## 8. Inspect and verify both certificates

```sh
openssl x509 -in certs/server.crt -noout -text
openssl x509 -in certs/client.crt -noout -text
openssl verify -CAfile certs/ca.crt -purpose sslserver \
    -verify_hostname localhost certs/server.crt
openssl verify -CAfile certs/ca.crt -purpose sslclient certs/client.crt
```

- Find the issuer, validity dates, SAN, public key, and Extended Key Usage in both certificates.
- Expect `certs/server.crt: OK` and `certs/client.crt: OK`.
- The server certificate needs name matching because the client selected a destination identity.
- Client certificate validation does not automatically perform DNS hostname matching against the connecting client's address.
- Confirm that the client certificate and client private key contain the same public key by comparing these fingerprints:

```sh
openssl pkey -in certs/client.key -pubout -outform DER | openssl dgst -sha256
openssl x509 -in certs/client.crt -pubkey -noout | openssl pkey -pubin -outform DER | openssl dgst -sha256
```

- Expect identical values.
- An offline certificate check does not prove that a live peer possesses the matching private key; the handshake signature provides that proof.
- Command references: [OpenSSL certificate issuance](https://docs.openssl.org/3.6/man1/openssl-x509/) and [certificate verification](https://docs.openssl.org/3.6/man1/openssl-verify/).

## 9. Run a successful mTLS exchange

### 9.1 Start the server in Terminal 1

```sh
cd /Users/nag/tls-demo/phase3
python3 server.py
```

- Expect `mTLS server listening on 127.0.0.1:6443`.
- The server loads its identity and a CA trust store for checking clients.
- Loading a CA alone is not enough: the server also sets `verify_mode = ssl.CERT_REQUIRED` to require a certificate.

### 9.2 Start Wireshark

- Select **Loopback: lo0** and start capture before running the client.
- Optional capture filter: `tcp port 6443`.
- Display filter: `tcp.port == 6443`.

### 9.3 Run the client in Terminal 2

```sh
cd /Users/nag/tls-demo/phase3
python3 client.py
```

- The client verifies the server certificate and expected name `localhost`.
- The client presents `client.crt` and proves possession of `client.key`.
- Expect the client to print `Server accepted the client certificate.` before sending the fake payload.
- Expect the server to print the verified certificate subject and URI SAN.
- Expect `OK: Message received over mutual TLS.` on the client.
- The `USERNAME` and `PASSWORD` fields remain demonstration data; certificate authentication is independent of their contents.

## 10. Follow the TLS 1.3 mTLS handshake

- This is a full initial handshake, not post-handshake authentication or session resumption.
- Each arrow is a logical message; TCP packets may combine or split messages.
- Bracketed messages are encrypted using handshake traffic keys.

```text
CLIENT                                                   SERVER
  |---------------- TCP handshake --------------------------|
  |                                                         |
  |---------------- ClientHello --------------------------->| clear
  |<--------------- ServerHello ----------------------------| clear
  |                                                         |
  |             derive handshake traffic keys               |
  |                                                         |
  |<-------------- [EncryptedExtensions] --------------------|
  |<-------------- [CertificateRequest] ---------------------| NEW
  |<-------------- [Server Certificate] ---------------------|
  |<-------------- [Server CertificateVerify] ---------------|
  |<-------------- [Server Finished] ------------------------|
  |                                                         |
  | verify server chain, name, signature, and Finished       |
  |                                                         |
  |--------------- [Client Certificate] -------------------->| NEW
  |--------------- [Client CertificateVerify] -------------->| NEW
  |--------------- [Client Finished] ----------------------->|
  |                                                         |
  |                 server verifies client chain, purpose,  |
  |                 private-key proof, and Finished          |
  |                                                         |
  |<=============== READY acknowledgment ===================| app keys
  |================ demo username/password/message ========>| app keys
  |<=============== OK / INFO / END ========================| app keys
```

### 10.1 TCP, Hello messages, and key exchange

- TCP establishes byte transport without authenticating an application identity.
- ClientHello and ServerHello negotiate settings and exchange public key-exchange material.
- Ephemeral exchange and the TLS key schedule produce handshake keys without sending those symmetric keys directly.
- RSA certificate keys sign authentication proofs; they do not encrypt each message or transport the TLS 1.3 session key.
- Adding client certificates does not replace the ephemeral exchange with the client RSA key.

### 10.2 CertificateRequest asks the client to authenticate

- The server sends CertificateRequest within its encrypted handshake flight.
- It supplies acceptable signature algorithms and may include certificate-authority hints.
- CA hints are optional; an empty or absent advertised CA list does not mean the server trusts every issuer.
- The actual server trust store and verification settings determine acceptance.
- The request is protected by handshake encryption in TLS 1.3.

### 10.3 The client authenticates the server first

- The server sends its certificate, a CertificateVerify signature, and Finished.
- The client validates the CA path, validity period, server purpose, and expected hostname.
- The client checks that the server's signature authenticates the handshake with the certificate's public key.
- The client checks Finished for transcript integrity and proof of the corresponding handshake secrets.
- A server certificate copied without its private key is insufficient for impersonation.

### 10.4 The client sends its identity and private-key proof

- Client Certificate contains the public client certificate, plus any required intermediate certificates.
- Client CertificateVerify signs handshake-related data with the client's private key.
- Client Finished authenticates the handshake transcript using derived secrets.
- CertificateVerify establishes possession of the identity key; Finished establishes handshake integrity and key confirmation.
- Neither the client private key nor the CA private key is sent.
- A client without a suitable certificate can send an empty Certificate message; this server requires a certificate and rejects that case.

### 10.5 The server validates the client

- The server checks that the certificate chains to its trusted CA, is time-valid, and is suitable for client authentication.
- It verifies the client's CertificateVerify and Finished.
- Only after successful TLS validation does the Python application handler run.
- `getpeercert()` exposes the peer certificate to the handler after validation.
- This demo has no online revocation checks or per-identity authorization rules.
- The same chain-validation concept applies in both directions, but client and server certificates have different purposes and identity-matching policies.

### 10.6 Why this demo adds READY

- TLS 1.3 has no final server handshake message specifically acknowledging receipt of the client's authentication flight.
- A client's local `wrap_socket()` can return before it reads a server alert rejecting its certificate.
- A later read or write can surface that rejection.
- Our server sends `READY: client certificate verified` only after its own handshake succeeds.
- Our client waits for that encrypted application message before sending any username, password, or message payload.
- READY is a feature of this classroom application protocol, not an extra standard TLS handshake message.
- This makes failed-authentication exercises deterministic at the application level.

## 11. Follow the application data and identity boundary

```text
Verified client certificate
  subject: student
  SAN URI: urn:tls-demo:student
              |
              v
Server accepts the certificate holder
              |
              v
Encrypted application payload
  USERNAME: someone-else
  PASSWORD: demo-password-123
  MESSAGE: ...
              |
              v
Server displays these fields as unverified demo content
```

- Try changing the username while keeping the same certificate:

```sh
python3 client.py --username someone-else
```

- The connection still authenticates the certificate holder `student`.
- A typed username is not a new certificate identity.
- An application using mTLS for access control should derive its principal from the verified certificate and apply an explicit policy.
- Trusting a CA means trusting its issuance decisions; this server does not restrict access to just one URI.
- Each direction uses its own derived application traffic keys and authenticated encryption, just as in Phase 2.
- Endpoint logs still reveal the fake payload; transport encryption does not hide it from the receiving application.

## 12. Inspect the mTLS connection in Wireshark

- Stop capture after the successful exchange.
- If necessary, use **Analyze → Decode As → TLS** for TCP port 6443.
- Inspect ClientHello with `tcp.port == 6443 && tls.handshake.type == 1`.
- Inspect ServerHello with `tcp.port == 6443 && tls.handshake.type == 2`.
- Expand ServerHello's `supported_versions` extension to identify TLS 1.3; legacy version fields may show older compatibility values.
- Follow **TCP Stream** and look for `demo-password-123`; it should not appear in plaintext.
- CertificateRequest, both Certificates, both CertificateVerify messages, and both Finished messages are encrypted after ServerHello.
- The baseline capture cannot expose the client certificate merely because this is mTLS.
- Encrypted records labeled Application Data can carry handshake messages, actual application data, or alerts.
- A packet capture without secrets may suggest a larger handshake but cannot reliably prove successful mutual authentication by packet size alone.
- Verify mTLS using endpoint logs, the successful exchange, and the failure exercises below.
- Addresses, timing, sizes, and some Hello metadata remain visible.
- Save the capture as `phase3-mtls.pcapng` if desired.
- Wireshark reference: [TLS inspection and decryption](https://wiki.wireshark.org/TLS).

## 13. Inspect handshake messages from an endpoint

- Keep the Python server running and use OpenSSL as an alternative client.
- Supply both the client certificate and its matching private key.

```sh
openssl s_client -connect 127.0.0.1:6443 \
    -servername localhost -CAfile certs/ca.crt \
    -verify_hostname localhost -verify_return_error \
    -cert certs/client.crt -key certs/client.key \
    -tls1_3 -state -msg
```

- Locate CertificateRequest in the incoming handshake.
- Locate the incoming server Certificate and CertificateVerify and the outgoing client Certificate and CertificateVerify.
- `<<<` and `>>>` in OpenSSL diagnostics mark received and sent messages respectively.
- The endpoint can show decrypted handshake contents because it participates in the connection.
- Wait for the READY line, then paste these lines within the server's 15-second application timeout:

```text
USERNAME: student
PASSWORD: demo-password-123
MESSAGE: Hello from the OpenSSL mTLS client.
```

- Expect `OK`, `INFO`, and `END` responses.
- Use Ctrl+C if the diagnostic client remains open.
- This small server closes its socket without a full TLS shutdown exchange; some OpenSSL versions can report an unexpected EOF afterward.
- The Python client requires an explicit complete acknowledgment ending in `END`; it does not treat bare EOF as success.
- The demo does not export session secrets; opening a certificate private key in Wireshark will not decrypt an ephemeral TLS 1.3 exchange.
- Diagnostic reference: [OpenSSL s_client](https://docs.openssl.org/3.6/man1/openssl-s_client/).

## 14. Negative test: no client certificate

```sh
python3 client.py --no-client-cert
```

- Expect nonzero exit status and `No application payload sent.`
- The server should log a rejected handshake, commonly mentioning that the peer did not return a certificate.
- The client may first print that it verified the server; that does not mean the server accepted the client.
- The client never receives READY, so it never sends the fake payload.
- Exact alert wording depends on the TLS library.

## 15. Negative test: untrusted client issuer

### 15.1 Manually create a second, untrusted CA and client

- Keep the legitimate server and its trust store unchanged.
- Issue another client certificate with the same student name and URI, but under a different CA.

```sh
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out certs/untrusted-ca.key
openssl req -new -x509 -key certs/untrusted-ca.key -sha256 -days 30 \
    -subj '/CN=Untrusted Classroom CA' -config certs/pki.cnf \
    -extensions ca_extensions -out certs/untrusted-ca.crt
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out certs/untrusted-client.key
openssl req -new -key certs/untrusted-client.key -subj '/CN=student' \
    -config certs/pki.cnf -out certs/untrusted-client.csr
openssl x509 -req -in certs/untrusted-client.csr \
    -CA certs/untrusted-ca.crt -CAkey certs/untrusted-ca.key -CAcreateserial \
    -days 30 -sha256 -extfile certs/pki.cnf -extensions client_extensions \
    -out certs/untrusted-client.crt
openssl verify -CAfile certs/untrusted-ca.crt -purpose sslclient certs/untrusted-client.crt
```

- The last command succeeds against the untrusted CA's own certificate.
- That success does not make the original server trust this new CA.

### 15.2 Try the untrusted client identity

```sh
python3 client.py --cert certs/untrusted-client.crt --key certs/untrusted-client.key
```

- Expect rejection and no application payload sent.
- The client still trusts the correct server CA; only its presented identity has changed.
- The server cannot build a trusted path for this client's certificate.
- Some stacks may omit an unsuitable client certificate instead; either way, the server rejects the connection.
- Matching the textual name `student` is insufficient without trusted issuance and private-key proof.

## 16. Negative test: wrong certificate purpose

- First perform an offline purpose check; this command is expected to fail:

```sh
openssl verify -CAfile certs/ca.crt -purpose sslclient certs/server.crt
```

- The server certificate has only `serverAuth`, even though it is signed by the trusted CA.
- Try presenting that server-only certificate as the client:

```sh
python3 client.py --cert certs/server.crt --key certs/server.key
```

- Expect rejection, commonly for unsuitable certificate purpose or a missing acceptable client certificate.
- This reinforces that valid issuer signatures alone are not sufficient for every role.
- The key reuse here is only a deliberate failure experiment; the normal client uses its own key.

## 17. Negative test: incorrect server identity

```sh
python3 client.py --server-name wrong.example
```

- Expect hostname verification failure and no application payload sent.
- Client authentication does not remove the client's responsibility to authenticate the server.
- A valid client certificate cannot fix an invalid server identity.
- Rerun the normal client to confirm the server continues working after rejected handshakes:

```sh
python3 client.py
```

## 18. Map mTLS to the code

- In [server.py](server.py), `create_default_context(Purpose.CLIENT_AUTH, cafile=...)` configures a context for verifying client certificates.
- `load_cert_chain(...)` supplies the server's own certificate and private key.
- `verify_mode = CERT_REQUIRED` makes a client certificate mandatory.
- Server `wrap_socket(..., server_side=True)` performs and validates the initial handshake before the handler runs.
- `getpeercert()` retrieves the verified client certificate; the application logs its subject and SAN.
- The handler sends READY, reads three bounded lines, then replies with explicit `OK`, `INFO`, and `END` lines.
- In [client.py](client.py), `create_default_context(cafile=...)` establishes trust for the server.
- Client `load_cert_chain(...)` supplies its own certificate and matching key for the server's request.
- `server_hostname` selects the expected server identity; it does not identify the client.
- `--no-client-cert` deliberately omits loading client identity material.
- A failed or incomplete exchange exits nonzero; the client waits for READY before sending the payload.
- Both contexts disable key logging and require TLS 1.3 or later.
- API reference: [Python TLS contexts and peer certificates](https://docs.python.org/3/library/ssl.html).

## 19. Classroom questions

- **What did mTLS add?** The server authenticates the client certificate holder as well as the client authenticating the server.
- **Did encryption become twice as strong?** No; the principal change is mutual authentication.
- **What proves possession of the client private key?** The client CertificateVerify signature tied to this handshake.
- **Is the client private key transmitted?** No.
- **Does the server contact the CA each time?** No; this lab validates against its local CA certificate and has no online revocation service.
- **Can a trusted certificate with the wrong EKU be used?** Not for the incompatible role demonstrated here.
- **Does `--username someone-else` change the authenticated identity?** No; that field is unverified application content.
- **Can every CA-issued client do everything?** Only if application policy allows it; this lab deliberately has no per-identity restrictions.
- **Can we see the client certificate in the baseline TLS 1.3 capture?** No; it is inside encrypted handshake records.
- **What must be managed in deployment?** Issuance, key protection, renewal, trust distribution, revocation policy, and authorization.

## 20. Troubleshooting and completion

- **Certificate files missing:** complete sections 4–8 before starting either program.
- **Certificate/key mismatch:** use the matching files and compare their public-key fingerprints.
- **Expired certificate:** inspect dates and your clock; preserve the old directory and repeat manual issuance if needed.
- **Unexpected trust failure:** ensure the server and client use the same intended CA; restart the server after replacing certificates.
- **Missing READY or TLS alert:** inspect the server terminal for the client-authentication rejection reason.
- **Application read timeout:** paste all three lines promptly when using OpenSSL interactively.
- **Connection refused:** start the Phase 3 server and use port 6443.
- **Port occupied:** set `--port 6444` on both Python programs and update Wireshark and OpenSSL commands accordingly.
- **No traffic:** start capture on `lo0` before running the client.
- **Only Application Data visible:** expected for encrypted TLS 1.3 handshake records; use endpoint diagnostics to inspect their contents.
- **Completion:** stop the server with Ctrl+C and stop Wireshark capture.
- Keep private key files and backups excluded from version control; `.gitignore` covers this lab's generated directories.
