#!/bin/sh
# Create an isolated classroom CA and a localhost server certificate.
set -eu
cd "$(dirname "$0")"
command -v openssl >/dev/null 2>&1 || { echo 'OpenSSL is required.' >&2; exit 1; }
if [ -e certs ]; then
    echo 'certs already exists; reuse it, or move it aside before generating new certificates.' >&2
    exit 1
fi
umask 077
mkdir certs
cat > certs/ca.cnf <<'EOF'
[req]
distinguished_name = dn
x509_extensions = ca
prompt = no
[dn]
CN = TLS Classroom Lab CA
[ca]
basicConstraints = critical,CA:true
keyUsage = critical,keyCertSign,cRLSign
subjectKeyIdentifier = hash
EOF
cat > certs/server.cnf <<'EOF'
[req]
distinguished_name = dn
prompt = no
[dn]
CN = localhost
[server]
basicConstraints = critical,CA:false
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = DNS:localhost,IP:127.0.0.1
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
EOF
openssl req -x509 -newkey rsa:2048 -nodes -sha256 -days 30 \
    -config certs/ca.cnf -keyout certs/ca.key -out certs/ca.crt
openssl req -new -newkey rsa:2048 -nodes -sha256 \
    -config certs/server.cnf -keyout certs/server.key -out certs/server.csr
openssl x509 -req -in certs/server.csr -CA certs/ca.crt -CAkey certs/ca.key \
    -CAcreateserial -days 30 -sha256 -extfile certs/server.cnf -extensions server \
    -out certs/server.crt
openssl verify -CAfile certs/ca.crt certs/server.crt
echo 'Certificates ready for 30 days. Trust is local to this demo; no macOS trust settings were changed.'
