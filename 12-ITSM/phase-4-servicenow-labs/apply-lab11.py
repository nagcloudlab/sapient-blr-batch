#!/usr/bin/env python3
"""Lab 11: Service Catalog & Request Management - Apply to ServiceNow"""

import urllib.request
import json
import ssl
import base64

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

def find_or_create(table, query_field, query_value, data):
    encoded = urllib.parse.quote(f"{query_field}={query_value}", safe='=^')
    results = api("GET", f"{table}?sysparm_query={encoded}&sysparm_fields=sys_id,{query_field}&sysparm_limit=1")
    if results:
        return results[0]["sys_id"], False
    result = api("POST", table, data)
    return result["sys_id"], True

import urllib.parse

# ============================================================
# Step 1: Get Service Catalog sys_id
# ============================================================
print("=== Lab 11: Service Catalog & Request Management ===\n")

catalog_id = find_one("sc_catalog", "title=Service Catalog")
print(f"Service Catalog: {catalog_id}")

# ============================================================
# Step 2: Create parent category "UPI Platform Services"
# ============================================================
parent_id, created = find_or_create("sc_category", "title", "UPI Platform Services", {
    "title": "UPI Platform Services",
    "sc_catalog": catalog_id,
    "description": "Self-service catalog for NPCI UPI Payment Platform. Request access, onboarding, infrastructure, and compliance services.",
    "active": "true"
})
print(f"{'Created' if created else 'Found'} parent category: UPI Platform Services ({parent_id})")

# ============================================================
# Step 3: Create sub-categories
# ============================================================
sub_cats = [
    ("Access & Onboarding", "Request access to systems, APIs, and onboard new team members or merchants."),
    ("Merchant Services", "Merchant onboarding, configuration, and lifecycle management services."),
    ("Report an Issue", "Report payment issues, settlement discrepancies, and system problems."),
    ("Infrastructure Requests", "Request new environments, infrastructure changes, and resource provisioning."),
    ("Compliance & Security", "Request compliance audit reports, security reviews, and regulatory documentation."),
]

cat_ids = {}
for title, desc in sub_cats:
    sid, created = find_or_create("sc_category", "title", title, {
        "title": title,
        "sc_catalog": catalog_id,
        "parent": parent_id,
        "description": desc,
        "active": "true"
    })
    cat_ids[title] = sid
    print(f"  {'Created' if created else 'Found'} sub-category: {title}")

# ============================================================
# Helper: add variable to a catalog item
# ============================================================
def add_variable(cat_item_id, var_type, order, question, name, mandatory=True, tooltip=""):
    # Check if variable already exists
    q = urllib.parse.quote(f"cat_item={cat_item_id}^name={name}", safe='=^')
    existing = api("GET", f"item_option_new?sysparm_query={q}&sysparm_fields=sys_id&sysparm_limit=1")
    if existing:
        return existing[0]["sys_id"]

    data = {
        "cat_item": cat_item_id,
        "type": str(var_type),
        "order": str(order),
        "question_text": question,
        "name": name,
        "mandatory": str(mandatory).lower()
    }
    if tooltip:
        data["tooltip"] = tooltip
    result = api("POST", "item_option_new", data)
    return result["sys_id"]

def add_choice(variable_id, text, value, order):
    q = urllib.parse.quote(f"question={variable_id}^value={value}", safe='=^')
    existing = api("GET", f"question_choice?sysparm_query={q}&sysparm_fields=sys_id&sysparm_limit=1")
    if existing:
        return
    api("POST", "question_choice", {
        "question": variable_id,
        "text": text,
        "value": value,
        "order": str(order)
    })

# ============================================================
# Step 4: Create Catalog Items
# ============================================================

# --- Item 1: Request Merchant Onboarding ---
print("\n--- Catalog Items ---")
item1_id, created = find_or_create("sc_cat_item", "name", "Request Merchant Onboarding", {
    "name": "Request Merchant Onboarding",
    "sc_catalogs": catalog_id,
    "category": cat_ids["Merchant Services"],
    "short_description": "Request onboarding of a new merchant to the UPI payment platform",
    "description": "Use this form to request onboarding of a new merchant to the NPCI UPI Payment Platform. This process includes document verification, technical configuration, and sandbox testing. Expected completion: 5 business days.",
    "delivery_time": "5 00:00:00",
    "active": "true"
})
print(f"{'Created' if created else 'Found'} Item 1: Request Merchant Onboarding")

# Variables for Item 1
v = add_variable(item1_id, 6, 100, "Merchant Name", "merchant_name", True, "Registered business name")
v = add_variable(item1_id, 5, 200, "Business Type", "business_type", True)
add_choice(v, "Retail", "retail", 100)
add_choice(v, "E-commerce", "ecommerce", 200)
add_choice(v, "Government", "government", 300)
add_choice(v, "Education", "education", 400)

add_variable(item1_id, 6, 300, "Merchant ID", "merchant_id", True, "Unique NPCI merchant identifier")

v = add_variable(item1_id, 5, 400, "Integration Type", "integration_type", True)
add_choice(v, "SDK", "sdk", 100)
add_choice(v, "API", "api", 200)
add_choice(v, "Plugin", "plugin", 300)

add_variable(item1_id, 14, 500, "Expected TPS (Transactions Per Second)", "expected_tps", True, "Peak transactions per second")
add_variable(item1_id, 10, 600, "Planned Go-live Date", "golive_date", True)

# --- Item 2: Request API Access ---
item2_id, created = find_or_create("sc_cat_item", "name", "Request API Access", {
    "name": "Request API Access",
    "sc_catalogs": catalog_id,
    "category": cat_ids["Access & Onboarding"],
    "short_description": "Request access credentials for UPI platform APIs",
    "description": "Request API access for UPI platform services. Sandbox and UAT access is auto-approved. Production access requires Technical Lead approval.",
    "delivery_time": "2 00:00:00",
    "active": "true"
})
print(f"{'Created' if created else 'Found'} Item 2: Request API Access")

v = add_variable(item2_id, 5, 100, "API Name", "api_name", True)
add_choice(v, "Transaction API", "transaction", 100)
add_choice(v, "Settlement API", "settlement", 200)
add_choice(v, "Dispute API", "dispute", 300)
add_choice(v, "Reporting API", "reporting", 400)

v = add_variable(item2_id, 5, 200, "Target Environment", "target_environment", True)
add_choice(v, "Sandbox", "sandbox", 100)
add_choice(v, "UAT", "uat", 200)
add_choice(v, "Production", "production", 300)

add_variable(item2_id, 2, 300, "Purpose / Use Case", "purpose", True, "Describe how you intend to use this API")
add_variable(item2_id, 8, 400, "Requestor Team", "requestor_team", True)

# --- Item 3: Request New UPI Service Environment ---
item3_id, created = find_or_create("sc_cat_item", "name", "Request New UPI Service Environment", {
    "name": "Request New UPI Service Environment",
    "sc_catalogs": catalog_id,
    "category": cat_ids["Infrastructure Requests"],
    "short_description": "Request provisioning of a new UPI service environment",
    "description": "Request a new environment for UPI services. Includes compute, storage, and network provisioning. Requires management and admin approval.",
    "delivery_time": "10 00:00:00",
    "active": "true"
})
print(f"{'Created' if created else 'Found'} Item 3: Request New UPI Service Environment")

v = add_variable(item3_id, 5, 100, "Environment Type", "env_type", True)
add_choice(v, "Development", "dev", 100)
add_choice(v, "QA / Testing", "qa", 200)
add_choice(v, "Staging / Pre-Production", "staging", 300)
add_choice(v, "Disaster Recovery", "dr", 400)

add_variable(item3_id, 2, 200, "Business Justification", "justification", True, "Explain why this environment is needed")
add_variable(item3_id, 6, 300, "Project Code", "project_code", True, "e.g., UPI-2024-PROJ-001")

# --- Item 4: Request Compliance Audit Report ---
item4_id, created = find_or_create("sc_cat_item", "name", "Request Compliance Audit Report", {
    "name": "Request Compliance Audit Report",
    "sc_catalogs": catalog_id,
    "category": cat_ids["Compliance & Security"],
    "short_description": "Request generation of a compliance audit report",
    "description": "Request a compliance audit report for regulatory submissions. Reports are generated from the NPCI compliance database and delivered within 3 business days.",
    "delivery_time": "3 00:00:00",
    "active": "true"
})
print(f"{'Created' if created else 'Found'} Item 4: Request Compliance Audit Report")

v = add_variable(item4_id, 5, 100, "Audit Framework", "audit_type", True)
add_choice(v, "PCI-DSS", "pci_dss", 100)
add_choice(v, "SOC 2 Type II", "soc2", 200)
add_choice(v, "RBI IT Framework", "rbi_it", 300)
add_choice(v, "ISO 27001", "iso27001", 400)

add_variable(item4_id, 10, 200, "Audit Period Start Date", "audit_from_date", True)
add_variable(item4_id, 10, 300, "Audit Period End Date", "audit_to_date", True)
add_variable(item4_id, 2, 400, "Audit Scope Description", "audit_scope", True, "Describe systems, processes, and data in scope")

# --- Item 5: Request Team Member Access ---
item5_id, created = find_or_create("sc_cat_item", "name", "Request Team Member Access", {
    "name": "Request Team Member Access",
    "sc_catalogs": catalog_id,
    "category": cat_ids["Access & Onboarding"],
    "short_description": "Request system access or role assignment for a team member",
    "description": "Request access to ServiceNow and UPI platform systems for a team member. Access requests require manager approval and are provisioned within 1 business day.",
    "delivery_time": "1 00:00:00",
    "active": "true"
})
print(f"{'Created' if created else 'Found'} Item 5: Request Team Member Access")

add_variable(item5_id, 8, 100, "User Requiring Access", "target_user", True)

v = add_variable(item5_id, 5, 200, "Role Requested", "role_requested", True)
add_choice(v, "ITIL User", "itil", 100)
add_choice(v, "Admin", "admin", 200)
add_choice(v, "Approver", "approver_user", 300)

v = add_variable(item5_id, 5, 300, "Access Duration", "access_duration", True)
add_choice(v, "Permanent", "permanent", 100)
add_choice(v, "30 Days", "30_days", 200)
add_choice(v, "90 Days", "90_days", 300)

add_variable(item5_id, 8, 400, "Approving Manager", "approving_manager", True, "Select the manager who will approve this access request")

# ============================================================
# Step 5: Create Record Producer - Report UPI Payment Issue
# ============================================================
print("\n--- Record Producer ---")
rp_id, created = find_or_create("sc_cat_item_producer", "name", "Report UPI Payment Issue", {
    "name": "Report UPI Payment Issue",
    "sc_catalogs": catalog_id,
    "category": cat_ids["Report an Issue"],
    "table_name": "incident",
    "short_description": "Report a UPI payment transaction issue for investigation",
    "description": "Use this form to report a failed, stuck, or incorrect UPI payment transaction. This will create an incident for the Platform Engineering team to investigate.",
    "active": "true",
    "script": (
        "current.category = 'software';\n"
        "current.contact_type = 'self-service';\n"
        "current.impact = 2;\n"
        "current.urgency = 2;\n"
        "current.assignment_group.setDisplayValue('Platform Engineering');\n"
        "current.short_description = 'UPI Payment Issue - Transaction: ' + producer.transaction_id;\n"
        "var desc = 'UPI Payment Issue Report\\n';\n"
        "desc += '========================\\n';\n"
        "desc += 'Transaction ID: ' + producer.transaction_id + '\\n';\n"
        "desc += 'Amount (INR): ' + producer.transaction_amount + '\\n';\n"
        "desc += 'Error Code: ' + producer.error_code + '\\n';\n"
        "desc += 'Timestamp: ' + producer.txn_timestamp + '\\n';\n"
        "desc += 'Remitter Bank: ' + producer.bank_name + '\\n';\n"
        "current.description = desc;\n"
    )
})
print(f"{'Created' if created else 'Found'} Record Producer: Report UPI Payment Issue")

# Variables for Record Producer
add_variable(rp_id, 6, 100, "UPI Transaction ID", "transaction_id", True, "e.g., UPI202409151430ABCD")
add_variable(rp_id, 6, 200, "Transaction Amount (INR)", "transaction_amount", True)

v = add_variable(rp_id, 5, 300, "UPI Error Code", "error_code", True)
add_choice(v, "U30 - Device fingerprint mismatch", "u30", 100)
add_choice(v, "U16 - Risk threshold exceeded", "u16", 200)
add_choice(v, "U28 - Transaction timed out", "u28", 300)
add_choice(v, "U09 - Duplicate request", "u09", 400)
add_choice(v, "U67 - Account frozen", "u67", 500)
add_choice(v, "U78 - PSP not available", "u78", 600)
add_choice(v, "U69 - NPCI system error", "u69", 700)
add_choice(v, "Other", "other", 800)

add_variable(rp_id, 11, 400, "Transaction Timestamp", "txn_timestamp", True)
add_variable(rp_id, 6, 500, "Remitter Bank Name", "bank_name", True)

# ============================================================
# Step 6: Create Variable Set - UPI Common Info
# ============================================================
print("\n--- Variable Sets ---")
vs_id, created = find_or_create("item_option_new_set", "title", "UPI Common Info", {
    "title": "UPI Common Info",
    "internal_name": "upi_common_info",
    "description": "Common fields for UPI service requests: Transaction ID, Service Name, Environment",
    "order": "50",
    "type": "one_to_one"
})
print(f"{'Created' if created else 'Found'} Variable Set: UPI Common Info")

# Variables for Variable Set
add_variable(vs_id, 6, 100, "UPI Transaction ID", "upi_txn_id", False, "Optional: enter if this request relates to a specific transaction")

v = add_variable(vs_id, 5, 200, "Related UPI Service", "related_upi_service", False)
add_choice(v, "UPI Core Switch", "core_switch", 100)
add_choice(v, "Settlement Engine", "settlement", 200)
add_choice(v, "Dispute Manager", "dispute", 300)
add_choice(v, "Merchant Portal", "merchant_portal", 400)
add_choice(v, "Analytics Platform", "analytics", 500)

v = add_variable(vs_id, 5, 300, "Environment", "common_environment", False)
add_choice(v, "Production", "production", 100)
add_choice(v, "Staging", "staging", 200)
add_choice(v, "UAT", "uat", 300)
add_choice(v, "Development", "dev", 400)

print("\n=== Lab 11: Service Catalog Setup - COMPLETE ===")
print(f"""
Summary:
  - 1 Parent Category: UPI Platform Services
  - 5 Sub-Categories: Access & Onboarding, Merchant Services, Report an Issue, Infrastructure Requests, Compliance & Security
  - 5 Catalog Items with variables:
    1. Request Merchant Onboarding (6 variables)
    2. Request API Access (4 variables)
    3. Request New UPI Service Environment (3 variables)
    4. Request Compliance Audit Report (4 variables)
    5. Request Team Member Access (4 variables)
  - 1 Record Producer: Report UPI Payment Issue (5 variables, creates Incident)
  - 1 Variable Set: UPI Common Info (3 variables)

View at: {INSTANCE}/nav_to.do?uri=sc_category.do?sys_id={parent_id}
Browse catalog: {INSTANCE}/catalog_home.do
""")
