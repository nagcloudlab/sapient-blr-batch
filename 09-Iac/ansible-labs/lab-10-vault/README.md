# Lab 10 - Ansible Vault

## Objective
Encrypt sensitive data (passwords, API keys) using Ansible Vault

## Prerequisites
- Lab 02 completed (inventory configured with real IPs)

---

## What is Ansible Vault?
- **Encrypts sensitive data** — passwords, keys, tokens
- Uses **AES-256** encryption
- Encrypted files are safe to commit to Git
- Decrypt at runtime with a password

## What to Encrypt?
- Database passwords
- API keys and tokens
- SSL certificates
- Any secret that shouldn't be in plain text

---

## Step 1: Create an Encrypted Secrets File

### Option A: Copy and encrypt the example file (recommended)

```bash
# Look at the example plaintext secrets
cat plaintext-secrets.yml

# Copy it as our working secrets file
cp plaintext-secrets.yml secrets.yml

# Now encrypt it (pick a password you'll remember!)
ansible-vault encrypt secrets.yml

# Verify it's encrypted
cat secrets.yml
# You should see: $ANSIBLE_VAULT;1.1;AES256 followed by encrypted text
```

### Option B: Create from scratch

```bash
# This opens your editor — type your secrets in YAML format
ansible-vault create secrets.yml

# Add these lines in the editor:
#   db_user: admin
#   db_password: SuperSecret123!
#   api_key: sk-abc-xyz-123-456
#   jwt_secret: myJwtSecretKey2024
# Save and exit
```

## Step 2: View / Edit Encrypted Files

```bash
# View contents (asks for password)
ansible-vault view secrets.yml

# Edit the file
ansible-vault edit secrets.yml

# Encrypt an existing file
ansible-vault encrypt plaintext-secrets.yml

# Decrypt a file (back to plain text)
ansible-vault decrypt secrets.yml

# Change the vault password
ansible-vault rekey secrets.yml
```

## Step 3: Use Secrets in a Playbook

```bash
# Run playbook with vault password prompt
ansible-playbook vault-demo.yml --ask-vault-pass

# Or use a password file (for CI/CD)
echo "myVaultPassword" > .vault_pass
chmod 600 .vault_pass
ansible-playbook vault-demo.yml --vault-password-file .vault_pass
```

## Step 4: Encrypt Single Variables (Inline)

```bash
# Encrypt a single string
ansible-vault encrypt_string 'SuperSecret123!' --name 'db_password'

# Output can be pasted directly into a YAML file:
# db_password: !vault |
#   $ANSIBLE_VAULT;1.1;AES256
#   6531326...
```

## Step 5: Best Practices Demo

```bash
# Run the best practices playbook
ansible-playbook vault-best-practices.yml --ask-vault-pass

# Notice: secrets come from group_vars/all/vault.yml
# Non-secret vars come from group_vars/all/vars.yml
```

---

## Files in this lab
| File | Description |
|------|-------------|
| `vault-demo.yml` | Playbook using vault secrets |
| `vault-best-practices.yml` | Best practices pattern |
| `plaintext-secrets.yml` | Example secrets (encrypt this!) |
| `.vault_pass` | Password file (NEVER commit this!) |
| `.gitignore` | Ignores vault password file |

---

## Best Practices
- **Never commit** `.vault_pass` to Git
- Keep secrets in `group_vars/*/vault.yml`
- Prefix vault variables with `vault_` for clarity
- Reference vault vars in regular vars: `db_password: "{{ vault_db_password }}"`
- Use `--vault-password-file` in CI/CD pipelines
- Add `.vault_pass` to `.gitignore`

---

## Troubleshooting

### "Decryption failed"
- Wrong vault password. There's no way to recover it — you must recreate the file
```bash
rm secrets.yml
cp plaintext-secrets.yml secrets.yml
ansible-vault encrypt secrets.yml    # use a new password
```

### "vars_files: secrets.yml not found"
- You haven't created `secrets.yml` yet. Follow Step 1 above

### "ERROR! input is not vault encrypted data"
- You're running `--ask-vault-pass` but the file is not encrypted
```bash
ansible-vault encrypt secrets.yml
```

## Key Takeaways
- Vault = AES-256 encryption for secrets
- `ansible-vault create/edit/view/encrypt/decrypt`
- `--ask-vault-pass` or `--vault-password-file` to decrypt at runtime
- Encrypted files are safe to commit to Git
- Next: **Conditionals and Loops**
