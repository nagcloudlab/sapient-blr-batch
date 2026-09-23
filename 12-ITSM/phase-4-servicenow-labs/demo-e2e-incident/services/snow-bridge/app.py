"""
ServiceNow Incident Bridge
Receives Prometheus AlertManager webhooks and creates incidents in ServiceNow.
Maps UPI-specific alert labels to ServiceNow incident fields.
"""
import os
import json
import logging
import requests
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# --- ServiceNow Configuration ---
SNOW_INSTANCE = os.environ.get('SNOW_INSTANCE', 'https://devXXXXXX.service-now.com').rstrip('/')
SNOW_USER = os.environ.get('SNOW_USER', 'admin')
SNOW_PASSWORD = os.environ.get('SNOW_PASSWORD', 'password')
SNOW_ENABLED = os.environ.get('SNOW_ENABLED', 'true').lower() == 'true'

# --- Alert to Incident Mapping ---
SEVERITY_MAP = {
    'critical': {'impact': '1', 'urgency': '1'},  # P1 Critical
    'warning':  {'impact': '2', 'urgency': '2'},   # P3 Moderate
    'info':     {'impact': '3', 'urgency': '3'},   # P5 Planning
}

CATEGORY_MAP = {
    'upi-transaction-service': 'software',
    'upi-settlement-service':  'software',
    'default':                 'network',
}

# Map service names to CMDB CI names (must match CIs created in Lab 07)
CI_NAME_MAP = {
    'upi-transaction-service': 'UPI Transaction Service',
    'upi-settlement-service':  'UPI Settlement Service',
    'prometheus':              'Prometheus Monitoring',
    'grafana':                 'Grafana Dashboard',
    'snow-bridge':             'Snow Bridge Integration',
}

# Cache CI sys_ids after first lookup
ci_cache = {}

# Track created incidents to avoid duplicates
active_alerts = {}


def lookup_ci_sys_id(ci_name):
    """Look up a CMDB CI sys_id by name. Results are cached."""
    if ci_name in ci_cache:
        return ci_cache[ci_name]
    if not SNOW_ENABLED:
        return None
    try:
        url = (f"{SNOW_INSTANCE}/api/now/table/cmdb_ci"
               f"?sysparm_query=name={ci_name}&sysparm_limit=1&sysparm_fields=sys_id,name")
        resp = requests.get(url, auth=(SNOW_USER, SNOW_PASSWORD),
                           headers={'Accept': 'application/json'}, timeout=15)
        resp.raise_for_status()
        results = resp.json().get('result', [])
        if results:
            sys_id = results[0]['sys_id']
            ci_cache[ci_name] = sys_id
            logger.info(f"CI lookup: '{ci_name}' -> {sys_id}")
            return sys_id
    except requests.exceptions.RequestException as e:
        logger.warning(f"CI lookup failed for '{ci_name}': {e}")
    return None


def create_snow_incident(alert):
    """Create a ServiceNow incident from an AlertManager alert."""
    labels = alert.get('labels', {})
    annotations = alert.get('annotations', {})
    status = alert.get('status', 'firing')

    alert_name = labels.get('alertname', 'Unknown Alert')
    severity = labels.get('severity', 'warning')
    service = labels.get('application', labels.get('job', 'unknown'))
    instance = labels.get('instance', 'unknown')

    # Build incident description
    summary = annotations.get('summary', alert_name)
    description = annotations.get('description', '')
    runbook = annotations.get('runbook', '')

    short_desc = f"[AUTO] {summary}"
    full_desc = (
        f"Alert: {alert_name}\n"
        f"Service: {service}\n"
        f"Instance: {instance}\n"
        f"Severity: {severity}\n"
        f"Status: {status}\n"
        f"Time: {alert.get('startsAt', 'unknown')}\n"
        f"\n--- Description ---\n{description}"
    )
    if runbook:
        full_desc += f"\n\n--- Runbook ---\n{runbook}"

    # Map severity to impact/urgency
    priority = SEVERITY_MAP.get(severity, SEVERITY_MAP['warning'])
    category = CATEGORY_MAP.get(service, CATEGORY_MAP['default'])

    incident_data = {
        'short_description': short_desc[:160],
        'description': full_desc,
        'impact': priority['impact'],
        'urgency': priority['urgency'],
        'category': category,
        'assignment_group': 'Platform Engineering',
        'caller_id': 'admin',
    }

    # Attach CMDB CI if we can find it
    ci_name = CI_NAME_MAP.get(service)
    if ci_name:
        ci_sys_id = lookup_ci_sys_id(ci_name)
        if ci_sys_id:
            incident_data['cmdb_ci'] = ci_sys_id
            logger.info(f"Attaching CI '{ci_name}' to incident")

    # Dedup: check if we already have an open incident for this alert
    alert_key = f"{alert_name}_{service}_{instance}"
    if alert_key in active_alerts:
        logger.info(f"Duplicate alert, incident already exists: {alert_key} -> {active_alerts[alert_key]}")
        return active_alerts[alert_key]

    if not SNOW_ENABLED:
        logger.info(f"[DRY RUN] Would create incident: {short_desc}")
        logger.info(f"[DRY RUN] Data: {json.dumps(incident_data, indent=2)}")
        fake_number = f"INC-DRY-{len(active_alerts) + 1:04d}"
        active_alerts[alert_key] = fake_number
        return fake_number

    # POST to ServiceNow Table API
    url = f"{SNOW_INSTANCE}/api/now/table/incident"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    try:
        resp = requests.post(
            url,
            auth=(SNOW_USER, SNOW_PASSWORD),
            headers=headers,
            json=incident_data,
            timeout=30
        )
        resp.raise_for_status()
        result = resp.json().get('result', {})
        inc_number = result.get('number', 'UNKNOWN')
        inc_sys_id = result.get('sys_id', '')
        logger.info(f"Incident created in ServiceNow: {inc_number} (sys_id: {inc_sys_id})")
        active_alerts[alert_key] = inc_number
        return inc_number
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to create ServiceNow incident: {e}")
        return None


def resolve_snow_incident(alert):
    """Add a work note when an alert resolves."""
    labels = alert.get('labels', {})
    alert_name = labels.get('alertname', 'Unknown')
    service = labels.get('application', labels.get('job', 'unknown'))
    instance = labels.get('instance', 'unknown')

    alert_key = f"{alert_name}_{service}_{instance}"
    inc_number = active_alerts.pop(alert_key, None)

    if not inc_number:
        logger.info(f"No active incident found for resolved alert: {alert_key}")
        return

    logger.info(f"Alert resolved: {alert_key} -> incident {inc_number}")

    if not SNOW_ENABLED or inc_number.startswith('INC-DRY'):
        logger.info(f"[DRY RUN] Would add resolution note to {inc_number}")
        return

    # Find and auto-resolve the incident
    try:
        url = f"{SNOW_INSTANCE}/api/now/table/incident?sysparm_query=number={inc_number}&sysparm_limit=1"
        resp = requests.get(url, auth=(SNOW_USER, SNOW_PASSWORD),
                          headers={'Accept': 'application/json'}, timeout=30)
        resp.raise_for_status()
        results = resp.json().get('result', [])
        if results:
            sys_id = results[0]['sys_id']
            update_url = f"{SNOW_INSTANCE}/api/now/table/incident/{sys_id}"
            requests.patch(
                update_url,
                auth=(SNOW_USER, SNOW_PASSWORD),
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                json={
                    'state': '6',  # Resolved
                    'close_code': 'Solved (Permanently)',
                    'close_notes': f"Auto-resolved: alert cleared at {alert.get('endsAt', 'unknown')}.",
                    'work_notes': f"[AUTO] Alert resolved at {alert.get('endsAt', 'unknown')}. "
                                  f"Monitoring confirms service has recovered. "
                                  f"Incident auto-resolved by Snow Bridge."
                },
                timeout=30
            )
            logger.info(f"Auto-resolved incident {inc_number}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to resolve incident {inc_number}: {e}")


@app.route('/webhook', methods=['POST'])
def alertmanager_webhook():
    """Receive AlertManager webhook payload."""
    logger.info("Received webhook from AlertManager")
    data = request.get_json(silent=True)
    logger.debug(f"Webhook payload: {data}")
    if not data:
        return jsonify({'error': 'No JSON payload'}), 400

    alerts = data.get('alerts', [])
    logger.info(f"Received {len(alerts)} alert(s) from AlertManager")

    results = []
    for alert in alerts:
        status = alert.get('status', 'firing')
        if status == 'firing':
            inc = create_snow_incident(alert)
            results.append({'alert': alert.get('labels', {}).get('alertname'), 'incident': inc, 'action': 'created'})
        elif status == 'resolved':
            resolve_snow_incident(alert)
            results.append({'alert': alert.get('labels', {}).get('alertname'), 'action': 'resolved'})

    return jsonify({'status': 'processed', 'results': results}), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'UP',
        'service': 'snow-bridge',
        'snow_enabled': SNOW_ENABLED,
        'snow_instance': SNOW_INSTANCE,
        'active_alerts': len(active_alerts)
    })


@app.route('/active-alerts', methods=['GET'])
def get_active_alerts():
    """Show current active alert → incident mapping."""
    return jsonify(active_alerts)


@app.route('/test-incident', methods=['POST'])
def test_incident():
    """Manually create a test incident (for demo/verification)."""
    data = request.get_json(silent=True) or {}
    test_alert = {
        'status': 'firing',
        'labels': {
            'alertname': data.get('alertname', 'TestAlert'),
            'severity': data.get('severity', 'critical'),
            'application': data.get('service', 'upi-transaction-service'),
            'instance': 'manual-test',
        },
        'annotations': {
            'summary': data.get('summary', 'Manual test incident from snow-bridge'),
            'description': data.get('description', 'This is a test incident created manually.'),
        },
        'startsAt': datetime.utcnow().isoformat() + 'Z',
    }
    inc = create_snow_incident(test_alert)
    return jsonify({'incident': inc, 'alert': test_alert['labels']})


if __name__ == '__main__':
    logger.info(f"ServiceNow Bridge starting...")
    logger.info(f"  Instance: {SNOW_INSTANCE}")
    logger.info(f"  Enabled:  {SNOW_ENABLED}")
    app.run(host='0.0.0.0', port=5005)
