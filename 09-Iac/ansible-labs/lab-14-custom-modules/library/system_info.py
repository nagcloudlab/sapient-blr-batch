#!/usr/bin/python3
# ============================================
# Custom Module: system_info
# ============================================
# Collects custom system metrics beyond standard Ansible facts
#
# Usage in playbook:
#   - system_info:
#       top_n: 5
#       check_services:
#         - nginx
#         - springboot
#
# Returns:
#   - disk_usage: disk usage per mount
#   - top_processes: top N processes by CPU
#   - services: status of specified services
#   - load_average: system load

import os

from ansible.module_utils.basic import AnsibleModule


def get_disk_usage(module):
    """Get disk usage for all mounted filesystems."""
    rc, stdout, stderr = module.run_command("df -h --output=target,pcent,size,used,avail -x tmpfs -x devtmpfs")
    if rc != 0:
        return []

    disks = []
    lines = stdout.strip().split('\n')[1:]  # skip header
    for line in lines:
        parts = line.split()
        if len(parts) >= 5:
            disks.append({
                'mount': parts[0],
                'percent_used': parts[1],
                'total': parts[2],
                'used': parts[3],
                'available': parts[4],
            })
    return disks


def get_top_processes(module, top_n):
    """Get top N processes by CPU usage."""
    rc, stdout, stderr = module.run_command(f"ps aux --sort=-%cpu | head -n {top_n + 1}")
    if rc != 0:
        return []

    processes = []
    lines = stdout.strip().split('\n')[1:]  # skip header
    for line in lines:
        parts = line.split(None, 10)
        if len(parts) >= 11:
            processes.append({
                'user': parts[0],
                'pid': parts[1],
                'cpu_percent': parts[2],
                'mem_percent': parts[3],
                'command': parts[10][:80],  # truncate long commands
            })
    return processes


def get_service_status(module, services):
    """Check status of specified services."""
    results = {}
    for svc in services:
        rc, stdout, stderr = module.run_command(f"systemctl is-active {svc}")
        results[svc] = {
            'status': stdout.strip(),
            'running': stdout.strip() == 'active',
        }
    return results


def get_load_average():
    """Get system load average."""
    load = os.getloadavg()
    return {
        '1min': round(load[0], 2),
        '5min': round(load[1], 2),
        '15min': round(load[2], 2),
    }


def run_module():
    module_args = dict(
        top_n=dict(type='int', required=False, default=5),
        check_services=dict(type='list', elements='str', required=False, default=[]),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=False, msg="Would collect system info")

    top_n = module.params['top_n']
    services = module.params['check_services']

    result = {
        'disk_usage': get_disk_usage(module),
        'top_processes': get_top_processes(module, top_n),
        'load_average': get_load_average(),
    }

    if services:
        result['services'] = get_service_status(module, services)

    module.exit_json(
        changed=False,
        system_info=result,
        msg=f"Collected system info: {len(result['disk_usage'])} disks, {len(result['top_processes'])} processes",
    )


def main():
    run_module()


if __name__ == '__main__':
    main()
