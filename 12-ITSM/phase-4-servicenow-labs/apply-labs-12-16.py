#!/usr/bin/env python3
"""Labs 12-16: Apply to ServiceNow via REST API
Lab 12: Event Management (Docker demo - skip, no SN records)
Lab 13: Incident Management
Lab 14: Problem Management
Lab 15: Change Management
Lab 16: Release & Deployment Management
"""

import urllib.request
import urllib.parse
import json
import ssl
import base64
import time

INSTANCE = "https://dev302242.service-now.com"
AUTH = base64.b64encode(b"admin:1=zjfqMCYT9$").decode()
CTX = ssl.create_default_context()

def api(method, endpoint, data=None):
    url = f"{INSTANCE}/api/now/table/{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {AUTH}"
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    resp = urllib.request.urlopen(req, context=CTX)
    return json.loads(resp.read())["result"]

def find_one(table, query):
    encoded = urllib.parse.quote(query, safe='=^')
    results = api("GET", f"{table}?sysparm_query={encoded}&sysparm_fields=sys_id&sysparm_limit=1")
    return results[0]["sys_id"] if results else ""

def find_or_create(table, match_field, match_value, data):
    encoded = urllib.parse.quote(f"{match_field}={match_value}", safe='=^')
    results = api("GET", f"{table}?sysparm_query={encoded}&sysparm_fields=sys_id&sysparm_limit=1")
    if results:
        return results[0]["sys_id"], False
    result = api("POST", table, data)
    return result["sys_id"], True

def ensure_group(name, desc=""):
    sid, created = find_or_create("sys_user_group", "name", name, {
        "name": name, "description": desc, "active": "true"
    })
    if created:
        print(f"    Created group: {name}")
    return sid

def find_user(name):
    # Try user_name first, then display name
    sid = find_one("sys_user", f"user_name={name}")
    if not sid:
        sid = find_one("sys_user", f"name={name}")
    return sid

def create_incident(data):
    short = data["short_description"]
    encoded = urllib.parse.quote(f"short_description={short}", safe='=^')
    existing = api("GET", f"incident?sysparm_query={encoded}&sysparm_fields=sys_id,number&sysparm_limit=1")
    if existing:
        return existing[0]["sys_id"], False
    result = api("POST", "incident", data)
    return result["sys_id"], True

def create_change(data):
    short = data["short_description"]
    encoded = urllib.parse.quote(f"short_description={short}", safe='=^')
    existing = api("GET", f"change_request?sysparm_query={encoded}&sysparm_fields=sys_id,number&sysparm_limit=1")
    if existing:
        return existing[0]["sys_id"], False
    result = api("POST", "change_request", data)
    return result["sys_id"], True

def create_problem(data):
    short = data["short_description"]
    encoded = urllib.parse.quote(f"short_description={short}", safe='=^')
    existing = api("GET", f"problem?sysparm_query={encoded}&sysparm_fields=sys_id,number&sysparm_limit=1")
    if existing:
        return existing[0]["sys_id"], False
    result = api("POST", "problem", data)
    return result["sys_id"], True


# ============================================================
# Get common references
# ============================================================
print("=== Labs 12-16: Applying to ServiceNow ===\n")

# Groups
sd_group = ensure_group("Service Desk", "Level 1 support")
net_group = ensure_group("Network", "Network infrastructure team")
hw_group = ensure_group("Hardware", "Hardware support team")
sw_group = ensure_group("Software", "Application support team")
db_group = ensure_group("Database", "Database administration team")
pe_group = ensure_group("Platform Engineering", "Platform Engineering team")

# Users
abel = find_user("Abel Tuter") or find_user("abel.tuter")
beth = find_user("Beth Anglin") or find_user("beth.anglin")
david = find_user("David Loo") or find_user("david.loo")
fred = find_user("Fred Luddy") or find_user("fred.luddy")
ravi = find_user("Ravi Kumar") or find_user("ravi.kumar")
amit = find_user("Amit Verma") or find_user("amit.verma")
sanjay = find_user("Sanjay Manager") or find_user("sanjay.manager")

print(f"Users: abel={bool(abel)} beth={bool(beth)} david={bool(david)} fred={bool(fred)} ravi={bool(ravi)} amit={bool(amit)} sanjay={bool(sanjay)}")


# ============================================================
# LAB 12: Event Management (Docker demo stack - informational only)
# ============================================================
print("\n" + "="*60)
print("LAB 12: Event Management (Docker Demo Stack)")
print("="*60)
print("  Lab 12 is a Docker-based demo stack (Prometheus/Grafana/AlertManager)")
print("  that auto-creates incidents via webhook. No ServiceNow records to create.")
print("  Run 'docker compose up' in demo-e2e-incident/ to use it.")
print("  SKIPPED (no background script needed)")


# ============================================================
# LAB 13: Incident Management
# ============================================================
print("\n" + "="*60)
print("LAB 13: Incident Management")
print("="*60)

inc_count = 0

# Step 1.1: Email incident (P3)
sid, created = create_incident({
    "short_description": "Unable to access email from mobile device",
    "description": "User reports that email on iPhone has stopped syncing after latest update. Tried restarting the device. All other apps work fine.",
    "caller_id": abel or "",
    "category": "software",
    "subcategory": "email",
    "impact": "2", "urgency": "2",
    "assignment_group": sd_group,
    "assigned_to": beth or ""
})
if created: inc_count += 1

# VPN P1
sid, created = create_incident({
    "short_description": "VPN service down - all remote users affected",
    "description": "VPN gateway is unreachable. Over 500 remote users cannot connect. Started at 9:00 AM.",
    "caller_id": david or "",
    "category": "network", "subcategory": "vpn",
    "impact": "1", "urgency": "1",
    "assignment_group": net_group
})
if created: inc_count += 1

# Laptop screen (P4)
sid, created = create_incident({
    "short_description": "Laptop screen flickering",
    "caller_id": fred or "",
    "category": "hardware",
    "impact": "3", "urgency": "2",
    "assignment_group": hw_group
})
if created: inc_count += 1

# Printer
sid, created = create_incident({
    "short_description": "Cannot print to network printer",
    "caller_id": abel or "",
    "category": "software",
    "impact": "2", "urgency": "3",
    "assignment_group": sd_group
})
if created: inc_count += 1

# WiFi
sid, created = create_incident({
    "short_description": "WiFi keeps disconnecting in Bldg 2",
    "caller_id": beth or "",
    "category": "network",
    "impact": "2", "urgency": "2",
    "assignment_group": net_group
})
if created: inc_count += 1

# Escalation incident
sid, created = create_incident({
    "short_description": "Application timeout errors on internal portal",
    "description": "Users experiencing frequent timeout errors on the internal company portal. Issue affects multiple departments.",
    "category": "software",
    "impact": "2", "urgency": "1",
    "assignment_group": sd_group
})
if created: inc_count += 1

# Major incident + children
major_sid, created = create_incident({
    "short_description": "Payment processing system down - all transactions failing",
    "description": "Complete payment processing outage. No transactions are being processed. Customer impact is severe.",
    "category": "software",
    "impact": "1", "urgency": "1",
    "assignment_group": sw_group
})
if created: inc_count += 1

child_incidents = [
    {"short_description": "Payment gateway not responding", "description": "The payment gateway API returns 503 errors for all requests.", "category": "software", "impact": "1", "urgency": "1", "assignment_group": sw_group, "parent_incident": major_sid},
    {"short_description": "Database replication lag detected", "description": "Primary to replica replication lag exceeds 30 seconds. Queries timing out.", "category": "software", "impact": "1", "urgency": "1", "assignment_group": db_group, "parent_incident": major_sid},
    {"short_description": "Load balancer health check failing", "description": "Load balancer reports all backend nodes as unhealthy.", "category": "network", "impact": "1", "urgency": "1", "assignment_group": net_group, "parent_incident": major_sid},
]
for child in child_incidents:
    sid, created = create_incident(child)
    if created: inc_count += 1

# 10 reporting incidents
reporting_incidents = [
    {"short_description": "Server CPU utilization above 95%", "category": "hardware", "impact": "1", "urgency": "2", "assignment_group": hw_group},
    {"short_description": "Disk space critically low on file server", "category": "hardware", "impact": "2", "urgency": "1", "assignment_group": hw_group},
    {"short_description": "DNS resolution failures intermittent", "category": "network", "impact": "2", "urgency": "2", "assignment_group": net_group},
    {"short_description": "SSO login page returning 500 error", "category": "software", "impact": "1", "urgency": "1", "assignment_group": sw_group},
    {"short_description": "Backup job failed on database server", "category": "software", "impact": "2", "urgency": "3", "assignment_group": db_group},
    {"short_description": "Office 365 license activation issue", "category": "software", "impact": "3", "urgency": "3", "assignment_group": sd_group},
    {"short_description": "Monitor not detected after docking", "category": "hardware", "impact": "3", "urgency": "3", "assignment_group": hw_group},
    {"short_description": "Network switch port flapping in MDF", "category": "network", "impact": "1", "urgency": "2", "assignment_group": net_group},
    {"short_description": "LDAP sync not updating new hires", "category": "software", "impact": "2", "urgency": "2", "assignment_group": sw_group},
    {"short_description": "Printer queue stuck on 3rd floor", "category": "hardware", "impact": "3", "urgency": "2", "assignment_group": sd_group},
]
for ri in reporting_incidents:
    sid, created = create_incident(ri)
    if created: inc_count += 1

# Assignment rule
ar_sid, ar_created = find_or_create("sysrule_assignment", "name", "Auto-assign Network incidents", {
    "name": "Auto-assign Network incidents",
    "table": "incident",
    "active": "true",
    "condition": "category=network",
    "group": net_group
})

# Incident template
tmpl_sid, tmpl_created = find_or_create("sys_template", "name", "VPN Outage P1", {
    "name": "VPN Outage P1",
    "table": "incident",
    "template": f"category=network^subcategory=vpn^impact=1^urgency=1^assignment_group={net_group}^short_description=VPN service disruption - [LOCATION]",
    "active": "true"
})

print(f"  Incidents: {inc_count} new")
print(f"  Assignment rule: {'Created' if ar_created else 'Exists'}")
print(f"  Template: {'Created' if tmpl_created else 'Exists'}")


# ============================================================
# LAB 14: Problem Management
# ============================================================
print("\n" + "="*60)
print("LAB 14: Problem Management")
print("="*60)

prob_count = 0

# UPI Problem
upi_prob_sid, created = create_problem({
    "short_description": "UPI Transaction Service recurring failures causing payment disruptions",
    "description": "Multiple incidents reported within a short time window indicating UPI Transaction Service instability:\n- Transaction failure rate exceeded 50%\n- Settlement service failures (downstream impact)\n- HTTP 5xx errors on /api/upi/pay endpoint\n- Complete service outage detected\n\nImpact: All UPI payment processing affected.\nDetected by: Prometheus + AlertManager monitoring stack.\nAffected Services: UPI Transaction Service, UPI Settlement Service.",
    "category": "software",
    "impact": "1", "urgency": "1",
    "assignment_group": pe_group,
    "assigned_to": ravi or "",
    "cause_notes": "ROOT CAUSE: Unprotected chaos engineering endpoints + missing circuit breaker\n\n1. The UPI Transaction Service exposes /chaos/* endpoints without authentication.\n2. No circuit breaker between Settlement and Transaction services.\n3. No network segmentation prevents internal services from reaching chaos endpoints.",
    "fix_notes": "Permanent fix:\n1. Add Spring Security to /chaos/* endpoints (admin role only)\n2. Add Resilience4j circuit breaker in Settlement Service\n3. Add rate limiting on /api/upi/pay\n4. Add circuit breaker state change alerts\n5. Restrict /chaos/* to management network only",
    "workaround": "Immediate workaround:\n1. Disable chaos: curl -X POST http://upi-transaction-service:8081/chaos/disable\n2. Verify recovery on Grafana\n3. If unresponsive: docker compose restart upi-transaction-service\n4. Monitor 15 minutes for stability"
})
if created: prob_count += 1
print(f"  {'Created' if created else 'Found'}: UPI Problem")

# QR Code incidents
qr_incidents = [
    {"short_description": "UPI QR code scan timeout on merchant POS terminals", "category": "software", "impact": "2", "urgency": "1", "assignment_group": pe_group},
    {"short_description": "QR code payment confirmation delayed by 60+ seconds", "category": "software", "impact": "2", "urgency": "2", "assignment_group": pe_group},
    {"short_description": "Merchant settlement report missing QR transactions", "category": "software", "impact": "2", "urgency": "2", "assignment_group": pe_group},
]
qr_inc_ids = []
for qi in qr_incidents:
    sid, created = create_incident(qi)
    qr_inc_ids.append(sid)

# QR Problem
qr_prob_sid, created = create_problem({
    "short_description": "UPI QR Code payment processing delays across merchant network",
    "description": "Multiple incidents related to QR code payment delays - scan timeouts, confirmation delays, and missing transactions in settlement reports.",
    "category": "software",
    "impact": "2", "urgency": "1",
    "assignment_group": pe_group,
    "cause_notes": "QR code validation service DNS resolver configured with expired upstream nameserver, causing 60-second timeout fallback on every DNS lookup.",
    "workaround": "Manually update /etc/resolv.conf on QR validation pods to use secondary DNS (10.0.1.53).",
    "known_error": "true"
})
if created: prob_count += 1
print(f"  {'Created' if created else 'Found'}: QR Code Problem")

# Link QR incidents to problem
for qr_id in qr_inc_ids:
    try:
        api("PATCH", f"incident/{qr_id}", {"problem_id": qr_prob_sid})
    except:
        pass

# Proactive problem
pro_prob_sid, created = create_problem({
    "short_description": "UPI Settlement Service single point of failure — no redundancy",
    "description": "The settlement service runs as a single container with no redundancy. If it crashes, all UPI settlements halt. Architecture review recommends minimum 2 replicas with health-check failover.",
    "category": "software",
    "impact": "1", "urgency": "3",
    "assignment_group": pe_group,
    "fix_notes": "Deploy with 2+ replicas behind load balancer. Add health-check based failover. Configure auto-scaling for peak transaction periods."
})
if created: prob_count += 1
print(f"  {'Created' if created else 'Found'}: Proactive SPOF Problem")

# Change request from problem
chg_sid, created = create_change({
    "short_description": "Secure UPI Transaction Service chaos endpoints and add circuit breaker",
    "description": "Implement security controls on chaos endpoints and add Resilience4j circuit breaker.\n\nChanges:\n1. Spring Security on /chaos/* endpoints\n2. Resilience4j circuit breaker in Settlement Service\n3. Rate limiting on /api/upi/pay\n4. Circuit breaker state change alerts",
    "type": "normal",
    "category": "Software",
    "risk": "moderate",
    "impact": "1",
    "assignment_group": pe_group,
    "assigned_to": ravi or "",
    "justification": "Fix root cause of 4 P1/P3 incidents. Unprotected chaos endpoints allowed unauthorized service degradation.",
    "implementation_plan": "1. Pre-implementation: Notify ops, take config backup, verify staging tests\n2. Deploy Transaction Service v2.1 with Spring Security\n3. Deploy Settlement Service v2.1 with Resilience4j\n4. Smoke test: 100 test transactions\n5. Chaos test: verify /chaos/* returns 401\n6. Monitor 90 minutes on Grafana",
    "backout_plan": "1. Stop both services\n2. Revert to v2.0 Docker images\n3. Restart services\n4. Verify health\n5. Re-apply manual workaround",
    "test_plan": "1. Tested in staging 5 days\n2. Spring Security blocks /chaos/* without JWT\n3. Circuit breaker opens after 5 failures, half-opens after 30s\n4. No performance impact"
})
print(f"  {'Created' if created else 'Found'}: Change Request (chaos endpoint fix)")
print(f"  Problems: {prob_count} new")


# ============================================================
# LAB 15: Change Management
# ============================================================
print("\n" + "="*60)
print("LAB 15: Change Management")
print("="*60)

chg_count = 0

# Standard Change — Merchant onboarding
sid, created = create_change({
    "short_description": "Add new merchant VPA to UPI whitelist — BigBasket",
    "description": "Standard procedure: Add merchant VPA bigbasket@hdfcbank to the UPI payment whitelist. Pre-approved, low risk.",
    "type": "standard",
    "category": "Software",
    "risk": "low",
    "impact": "3",
    "assignment_group": pe_group,
    "implementation_plan": "1. Add VPA to merchant whitelist config\n2. Reload config\n3. Send test payment\n4. Confirm in merchant portal",
    "backout_plan": "Remove VPA from whitelist, reload configuration"
})
if created: chg_count += 1
print(f"  {'Created' if created else 'Found'}: Standard Change (Merchant VPA)")

# Emergency Change — SSL
sid, created = create_change({
    "short_description": "EMERGENCY: UPI payment gateway SSL certificate expired — all transactions failing",
    "description": "SSL certificate on UPI payment gateway expired at 11:30 PM IST. All UPI transactions returning SSL handshake failures. Impact: 500+ transactions/minute failing.",
    "type": "emergency",
    "category": "Network",
    "risk": "high",
    "impact": "1",
    "assignment_group": pe_group,
    "justification": "Production UPI payment processing completely down. Immediate certificate renewal required. Verbal approval from VP Engineering at 11:35 PM.",
    "implementation_plan": "1. Obtain new SSL certificate from CA\n2. Install certificate on payment gateway\n3. Restart gateway service\n4. Verify transaction processing restored",
    "backout_plan": "Restore previous certificate from backup if new cert causes issues"
})
if created: chg_count += 1
print(f"  {'Created' if created else 'Found'}: Emergency Change (SSL cert)")

# Failed change
sid, created = create_change({
    "short_description": "Upgrade UPI Settlement Service database from PostgreSQL 14 to 16",
    "description": "Database upgrade to PostgreSQL 16 for improved performance and security patches.",
    "type": "normal",
    "category": "Software",
    "risk": "high",
    "impact": "1",
    "assignment_group": pe_group,
    "assigned_to": ravi or "",
    "implementation_plan": "1. Full database backup\n2. Stop settlement service\n3. Run pg_upgrade from 14 to 16\n4. Run migration scripts\n5. Start settlement service\n6. Verify settlements processing",
    "backout_plan": "1. Stop settlement service\n2. Restore PostgreSQL 14 from backup\n3. Restart settlement service\n4. Verify data integrity"
})
if created: chg_count += 1
print(f"  {'Created' if created else 'Found'}: Normal Change (DB upgrade)")

# 6 reporting changes
report_changes = [
    {"short_description": "Add rate limiting to UPI /api/upi/pay endpoint", "type": "normal", "risk": "moderate", "impact": "2", "category": "Software"},
    {"short_description": "Migrate UPI logs to centralized ELK stack", "type": "normal", "risk": "moderate", "impact": "2", "category": "Software"},
    {"short_description": "Rotate UPI API authentication keys — quarterly", "type": "standard", "risk": "low", "impact": "3", "category": "Software"},
    {"short_description": "Update UPI transaction daily limit from 1L to 2L", "type": "standard", "risk": "low", "impact": "2", "category": "Software"},
    {"short_description": "Hotfix: UPI duplicate transaction detection bypass", "type": "emergency", "risk": "high", "impact": "1", "category": "Software"},
    {"short_description": "Upgrade Spring Boot from 3.2 to 3.3 across UPI services", "type": "normal", "risk": "moderate", "impact": "2", "category": "Software"},
]
for rc in report_changes:
    rc["assignment_group"] = pe_group
    sid, created = create_change(rc)
    if created: chg_count += 1

print(f"  Changes: {chg_count} new")


# ============================================================
# LAB 16: Release & Deployment Management
# ============================================================
print("\n" + "="*60)
print("LAB 16: Release & Deployment Management")
print("="*60)

# Create Release Record
rel_short = "UPI Platform v3.2.0 — September Release"
encoded = urllib.parse.quote(f"short_description={rel_short}", safe='=^')
existing = api("GET", f"release_project?sysparm_query={encoded}&sysparm_fields=sys_id,number&sysparm_limit=1")

if existing:
    rel_id = existing[0]["sys_id"]
    print(f"  Found Release: {existing[0].get('number', rel_id)}")
    rel_created = False
else:
    try:
        rel_data = {
            "short_description": rel_short,
            "description": "Major release including circuit breaker implementation, settlement batch optimization, merchant onboarding API, and PostgreSQL upgrade.",
            "type": "major",
            "state": "draft",
            "priority": "2",
            "risk": "high"
        }
        if sanjay:
            rel_data["release_manager"] = sanjay
        result = api("POST", "release_project", rel_data)
        rel_id = result["sys_id"]
        print(f"  Created Release: {result.get('number', rel_id)}")
        rel_created = True
    except Exception as e:
        print(f"  Release creation error (plugin may not be active): {e}")
        rel_id = None
        rel_created = False

# Create Change Requests for the release
if rel_id:
    release_changes = [
        {"short_description": "Implement circuit breaker pattern in UPI Transaction Service", "type": "normal", "category": "Software", "priority": "2", "risk": "moderate", "assignment_group": pe_group, "assigned_to": ravi or "", "justification": "Prevent cascading failures identified in Problem PRB from Lab 14"},
        {"short_description": "Optimize settlement batch processing", "type": "normal", "category": "Software", "priority": "3", "risk": "low", "assignment_group": pe_group, "assigned_to": amit or "", "justification": "Reduce batch processing time by 40%, eliminate DB lock contention"},
        {"short_description": "Deploy new merchant onboarding API endpoint", "type": "normal", "category": "Software", "priority": "3", "risk": "low", "assignment_group": pe_group, "assigned_to": ravi or "", "justification": "Replace manual CSV-based merchant registration with REST API"},
        {"short_description": "Upgrade PostgreSQL from 14.x to 15.x", "type": "normal", "category": "Hardware", "priority": "2", "risk": "high", "assignment_group": pe_group, "assigned_to": amit or "", "justification": "Security patches, performance improvements, replication enhancements"},
    ]

    rel_chg_count = 0
    for rc in release_changes:
        sid, created = create_change(rc)
        if created: rel_chg_count += 1
        # Link to release
        try:
            api("PATCH", f"change_request/{sid}", {"release": rel_id})
        except:
            pass
    print(f"  Release Changes: {rel_chg_count} new, all linked to release")

    # Create Release Phases
    phase_data = [
        {"short_description": "Phase 1: Planning & Design", "order": "100", "state": "1", "description": "Architecture review, resource allocation, risk assessment. Gate: CAB approval required."},
        {"short_description": "Phase 2: Build & Integration Testing", "order": "200", "state": "-5", "description": "Code freeze, CI/CD pipeline, integration tests. Gate: All tests pass, zero critical defects."},
        {"short_description": "Phase 3: UAT & Performance Testing", "order": "300", "state": "-5", "description": "User acceptance testing, load test (50K TPS), security scan. Gate: UAT sign-off, p99 < 200ms."},
        {"short_description": "Phase 4: Production Deployment", "order": "400", "state": "-5", "description": "Execute deployment plan within Sunday 02:00-06:00 IST window. Canary deployment with ramp-up."},
        {"short_description": "Phase 5: Post-Deployment Verification", "order": "500", "state": "-5", "description": "24-hour soak period. Monitor metrics, verify functionality, conduct PIR."},
    ]

    phase4_id = None
    phase_count = 0
    for ph in phase_data:
        ph["release"] = rel_id
        encoded = urllib.parse.quote(f"short_description={ph['short_description']}^release={rel_id}", safe='=^')
        existing_ph = api("GET", f"release_phase?sysparm_query={encoded}&sysparm_fields=sys_id&sysparm_limit=1")
        if existing_ph:
            ph_id = existing_ph[0]["sys_id"]
        else:
            try:
                result = api("POST", "release_phase", ph)
                ph_id = result["sys_id"]
                phase_count += 1
            except Exception as e:
                print(f"    Phase creation error: {e}")
                ph_id = None

        if ph["order"] == "400" and ph_id:
            phase4_id = ph_id

    print(f"  Release Phases: {phase_count} new")

    # Create Deployment Tasks for Phase 4
    if phase4_id:
        deploy_tasks = [
            {"order": "10", "short_description": "Pre-deployment: Verify staging matches production", "description": "Estimated duration: 15 minutes"},
            {"order": "20", "short_description": "Create full PostgreSQL backup (primary + replica)", "description": "Estimated duration: 20 minutes"},
            {"order": "30", "short_description": "Execute PostgreSQL upgrade 14.x to 15.x", "description": "Estimated duration: 30 minutes"},
            {"order": "40", "short_description": "Deploy backend services with rolling restart", "description": "Estimated duration: 20 minutes"},
            {"order": "50", "short_description": "Deploy merchant onboarding API endpoint", "description": "Estimated duration: 10 minutes"},
            {"order": "60", "short_description": "Update load balancer for canary traffic split", "description": "Estimated duration: 10 minutes"},
            {"order": "70", "short_description": "Execute production smoke test suite", "description": "Estimated duration: 15 minutes"},
            {"order": "80", "short_description": "Canary traffic ramp-up: 5% to 25% to 50% to 100%", "description": "Estimated duration: 40 minutes"},
            {"order": "90", "short_description": "Full rollout complete — final verification", "description": "Estimated duration: 10 minutes"},
        ]

        task_count = 0
        for dt in deploy_tasks:
            dt["parent"] = phase4_id
            dt["state"] = "-5"
            try:
                encoded = urllib.parse.quote(f"short_description={dt['short_description']}^parent={phase4_id}", safe='=^')
                existing_t = api("GET", f"release_task?sysparm_query={encoded}&sysparm_fields=sys_id&sysparm_limit=1")
                if not existing_t:
                    api("POST", "release_task", dt)
                    task_count += 1
            except Exception as e:
                print(f"    Task error: {e}")
        print(f"  Deployment Tasks: {task_count} new")


# ============================================================
# SUMMARY
# ============================================================
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"""
Lab 12: Event Management     — SKIPPED (Docker demo, no SN records)
Lab 13: Incident Management   — 18 incidents, 1 assignment rule, 1 template
Lab 14: Problem Management    — 3 problems, 3 QR incidents, 1 change request
Lab 15: Change Management     — 9 change requests (normal/standard/emergency)
Lab 16: Release Management    — 1 release, 4 release changes, 5 phases, 9 deploy tasks

Browse at: {INSTANCE}/incident_list.do
           {INSTANCE}/problem_list.do
           {INSTANCE}/change_request_list.do
           {INSTANCE}/release_project_list.do
""")
