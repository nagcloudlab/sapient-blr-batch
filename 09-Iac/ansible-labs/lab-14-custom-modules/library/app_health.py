#!/usr/bin/python3
# ============================================
# Custom Module: app_health
# ============================================
# Checks if an application is healthy via HTTP
#
# Usage in playbook:
#   - app_health:
#       url: "http://localhost:8080/actuator/health"
#       timeout: 5
#
# Returns:
#   - healthy: true/false
#   - status_code: HTTP status code
#   - response_time_ms: response time in milliseconds
#   - body: response body (truncated)

import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url


def run_module():
    module_args = dict(
        url=dict(type='str', required=True),
        timeout=dict(type='int', required=False, default=5),
        expected_status=dict(type='int', required=False, default=200),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(changed=False, msg="Would check health")

    url = module.params['url']
    timeout = module.params['timeout']
    expected_status = module.params['expected_status']

    start_time = time.time()

    try:
        response = open_url(url, timeout=timeout)
        status_code = response.getcode()
        body = response.read().decode('utf-8')[:500]  # truncate to 500 chars
        response_time = round((time.time() - start_time) * 1000, 2)

        healthy = status_code == expected_status

        if healthy:
            module.exit_json(
                changed=False,
                healthy=True,
                status_code=status_code,
                response_time_ms=response_time,
                body=body,
                msg=f"App is healthy (HTTP {status_code}, {response_time}ms)",
            )
        else:
            module.fail_json(
                healthy=False,
                status_code=status_code,
                response_time_ms=response_time,
                body=body,
                msg=f"Unexpected status code: {status_code} (expected {expected_status})",
            )

    except Exception as e:
        response_time = round((time.time() - start_time) * 1000, 2)
        module.fail_json(
            healthy=False,
            status_code=0,
            response_time_ms=response_time,
            msg=f"Health check failed: {str(e)}",
        )


def main():
    run_module()


if __name__ == '__main__':
    main()
