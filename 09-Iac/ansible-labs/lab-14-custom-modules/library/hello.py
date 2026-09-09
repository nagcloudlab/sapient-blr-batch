#!/usr/bin/python3
# ============================================
# Custom Module: hello
# ============================================
# The simplest custom module — returns a greeting
#
# Usage in playbook:
#   - hello:
#       name: "World"
#
# Usage ad-hoc:
#   ansible all -m hello -a "name=World"

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # Define the arguments this module accepts
    module_args = dict(
        name=dict(type='str', required=False, default='Ansible'),
    )

    # Create the module
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,    # supports --check (dry run)
    )

    # Check mode — don't do anything, just report
    if module.check_mode:
        module.exit_json(changed=False, message="Would say hello")

    # Your logic here
    name = module.params['name']
    greeting = f"Hello, {name}!"

    # Return result (changed=False because we didn't modify anything)
    module.exit_json(
        changed=False,
        message=greeting,
        name=name,
    )


def main():
    run_module()


if __name__ == '__main__':
    main()
