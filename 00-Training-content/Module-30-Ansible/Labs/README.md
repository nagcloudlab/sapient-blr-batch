# Module 30: Ansible -- Lab Setup

## Prerequisites

- Ansible 2.14 or higher (`ansible --version` to confirm)
  - Windows: install via WSL2 -- `pip install ansible` inside Ubuntu
  - macOS/Linux: `pip install ansible` or `brew install ansible`
- Optional: `ansible-lint` for playbook quality checks (`pip install ansible-lint`)

## Running the Starter Code

```bash
cd Labs/starter-code
ansible-playbook -i inventory.ini playbook.yml --check
```

The `--check` flag performs a dry run -- no changes are made to the host. Expect errors from the
bugs in the playbook. Fix each issue and re-run `--check` to verify.

## Verifying Your Fixes

```bash
# Dry run with diff output showing what would change
ansible-playbook -i inventory.ini playbook.yml --check --diff

# Lint check (no warnings expected after fixes)
ansible-lint playbook.yml

# Run for real (local connection -- safe for this lab)
ansible-playbook -i inventory.ini playbook.yml --connection=local
```

Confirm the Nginx config file was deployed and the service is running:
```bash
curl http://localhost
systemctl status nginx
```

## Expected Behavior

- Playbook runs through all tasks without errors in `--check` mode.
- Nginx is installed and the FoodExpress virtual host config is deployed.
- Handler restarts Nginx when the config file changes (idempotent -- no restart on second run).
- Variables in Jinja2 templates are correctly interpolated (no `{{ variable_name }}` literals).
- Inventory correctly defines host groups and connection settings.

## Troubleshooting

**SSH connection refused:** Add `ansible_connection=local` to `inventory.ini` for local testing so
Ansible does not try to SSH to localhost.

**`become` permission denied:** Tasks that need root (installing packages, restarting services)
must have `become: true`. Add it to the task or the entire play block.
