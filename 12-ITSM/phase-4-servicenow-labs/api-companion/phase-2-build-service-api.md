# Phase 2: Build Service — REST API Companion (Labs 07-11)

**Purpose:** Curl commands that replicate every UI action in Phase 2 labs via the ServiceNow Table API.
**Audience:** Instructors and participants who want to script lab setup or understand the REST API.

---

## Prerequisites & Credentials

```bash
# Set these once per session
export SNOW="https://YOUR-INSTANCE.service-now.com"
export AUTH="admin:YOUR-PASSWORD"

# Common curl flags (reused throughout)
# -s  = silent, -S = show errors, -H = header, -u = basic auth
# All POST/PUT commands return JSON; pipe to jq for readability
```

---

## Helper: Extracting sys_id from API Responses

Every POST returns the created record. Capture the sys_id for chaining:

```bash
# Pattern: capture sys_id into a shell variable
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/TABLE_NAME" \
  -d '{"field":"value"}')

SYS_ID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "Created record: $SYS_ID"
```

---

## Helper: Lookup Users and Groups (needed by all labs)

```bash
# ----------------------------------------------------------------
# Lookup user sys_ids — these are referenced throughout all labs
# UI equivalent: User Administration > Users > search by name
# ----------------------------------------------------------------

# Sanjay Manager
SANJAY=$(curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_user?sysparm_query=name=Sanjay Manager&sysparm_fields=sys_id,name&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(r[0]['sys_id'] if r else 'NOT_FOUND')")
echo "Sanjay Manager: $SANJAY"

# Ravi Kumar
RAVI=$(curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_user?sysparm_query=name=Ravi Kumar&sysparm_fields=sys_id,name&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(r[0]['sys_id'] if r else 'NOT_FOUND')")
echo "Ravi Kumar: $RAVI"

# Amit Verma
AMIT=$(curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_user?sysparm_query=name=Amit Verma&sysparm_fields=sys_id,name&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(r[0]['sys_id'] if r else 'NOT_FOUND')")
echo "Amit Verma: $AMIT"

# Priya Sharma
PRIYA=$(curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_user?sysparm_query=name=Priya Sharma&sysparm_fields=sys_id,name&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(r[0]['sys_id'] if r else 'NOT_FOUND')")
echo "Priya Sharma: $PRIYA"

# Platform Engineering group
PLATFORM_ENG=$(curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_user_group?sysparm_query=name=Platform Engineering&sysparm_fields=sys_id,name&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(r[0]['sys_id'] if r else 'NOT_FOUND')")
echo "Platform Engineering: $PLATFORM_ENG"

# Service Desk group
SERVICE_DESK=$(curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_user_group?sysparm_query=name=Service Desk&sysparm_fields=sys_id,name&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(r[0]['sys_id'] if r else 'NOT_FOUND')")
echo "Service Desk: $SERVICE_DESK"

# NOC group
NOC=$(curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_user_group?sysparm_query=name=NOC&sysparm_fields=sys_id,name&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(r[0]['sys_id'] if r else 'NOT_FOUND')")
echo "NOC: $NOC"
```

---

# Lab 07: CMDB & Configuration Management

## 7.1 Create Configuration Items (12 CIs)

### CI 1: Business Application — UPI Payment Platform

```bash
# Navigate to Configuration > Business Applications > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_business_app" \
  -d '{
    "name": "UPI Payment Platform",
    "operational_status": "1",
    "install_status": "1",
    "short_description": "NPCI Unified Payments Interface — core payment processing platform handling 10B+ transactions/month",
    "managed_by": "'"$RAVI"'",
    "owned_by": "'"$SANJAY"'",
    "support_group": "'"$PLATFORM_ENG"'",
    "environment": "Production",
    "description": "The UPI Payment Platform is NPCI flagship digital payment infrastructure. It consists of a Transaction Service, Settlement Service, PostgreSQL databases, a production load balancer, and a comprehensive monitoring stack."
  }')

UPI_PLATFORM=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI Payment Platform: $UPI_PLATFORM"
```

### CI 2: Application Server — UPI Transaction Service

```bash
# Navigate to Configuration > Servers > Application Servers > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_app_server" \
  -d '{
    "name": "UPI Transaction Service",
    "operational_status": "1",
    "install_status": "1",
    "short_description": "Spring Boot microservice for real-time UPI payment processing (port 8081)",
    "host_name": "upi-txn-01.npci.org.in",
    "ip_address": "10.100.1.11",
    "tcp_port": "8081",
    "running_process": "java -jar upi-transaction-service.jar",
    "running_process_key": "upi-transaction-service",
    "version": "3.2.1",
    "managed_by": "'"$RAVI"'",
    "owned_by": "'"$RAVI"'",
    "support_group": "'"$PLATFORM_ENG"'",
    "assigned_to": "'"$RAVI"'",
    "environment": "Production",
    "description": "The UPI Transaction Service is the primary payment processing engine. Handles approximately 4,000 TPS during peak hours. Port 8081."
  }')

UPI_TXN_SVC=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI Transaction Service: $UPI_TXN_SVC"
```

### CI 3: Application Server — UPI Settlement Service

```bash
# Navigate to Configuration > Servers > Application Servers > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_app_server" \
  -d '{
    "name": "UPI Settlement Service",
    "operational_status": "1",
    "install_status": "1",
    "short_description": "Spring Boot microservice for UPI settlement and reconciliation (port 8082)",
    "host_name": "upi-stl-01.npci.org.in",
    "ip_address": "10.100.1.12",
    "tcp_port": "8082",
    "running_process": "java -jar upi-settlement-service.jar",
    "running_process_key": "upi-settlement-service",
    "version": "3.2.1",
    "managed_by": "'"$AMIT"'",
    "owned_by": "'"$RAVI"'",
    "support_group": "'"$PLATFORM_ENG"'",
    "assigned_to": "'"$AMIT"'",
    "environment": "Production",
    "description": "The UPI Settlement Service handles end-of-day settlement between member banks. Settlement windows: 8AM, 12PM, 4PM, 8PM, 12AM. Port 8082."
  }')

UPI_STL_SVC=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI Settlement Service: $UPI_STL_SVC"
```

### CI 4: Database Instance — UPI PostgreSQL Primary

```bash
# Navigate to Configuration > Databases > Database Instances > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_db_instance" \
  -d '{
    "name": "UPI PostgreSQL Primary",
    "operational_status": "1",
    "install_status": "1",
    "short_description": "Primary PostgreSQL 16 database for UPI transaction and settlement data",
    "host_name": "upi-db-01.npci.org.in",
    "ip_address": "10.100.2.11",
    "tcp_port": "5432",
    "type": "PostgreSQL",
    "version": "16.2",
    "database_name": "upi_production",
    "managed_by": "'"$AMIT"'",
    "owned_by": "'"$RAVI"'",
    "support_group": "'"$PLATFORM_ENG"'",
    "assigned_to": "'"$AMIT"'",
    "environment": "Production",
    "description": "Primary PostgreSQL 16.2 database instance. Contains transaction records, settlement batches, member bank configurations. Synchronous replication to replica. RPO: 0. RTO: 15 minutes."
  }')

PG_PRIMARY=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI PostgreSQL Primary: $PG_PRIMARY"
```

### CI 5: Database Instance — UPI PostgreSQL Replica

```bash
# Navigate to Configuration > Databases > Database Instances > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_db_instance" \
  -d '{
    "name": "UPI PostgreSQL Replica",
    "operational_status": "1",
    "install_status": "1",
    "short_description": "Read replica of UPI PostgreSQL Primary for reporting and failover",
    "host_name": "upi-db-02.npci.org.in",
    "ip_address": "10.100.2.12",
    "tcp_port": "5432",
    "type": "PostgreSQL",
    "version": "16.2",
    "database_name": "upi_production",
    "managed_by": "'"$AMIT"'",
    "owned_by": "'"$RAVI"'",
    "support_group": "'"$PLATFORM_ENG"'",
    "assigned_to": "'"$AMIT"'",
    "environment": "Production",
    "description": "Synchronous streaming replica of UPI PostgreSQL Primary. Used for read-only reporting and as hot standby. Patroni manages failover. Replication lag threshold: < 100ms."
  }')

PG_REPLICA=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI PostgreSQL Replica: $PG_REPLICA"
```

### CI 6: Load Balancer — UPI Production LB

```bash
# Navigate to Configuration > Load Balancers > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_lb" \
  -d '{
    "name": "UPI Production LB",
    "operational_status": "1",
    "install_status": "1",
    "short_description": "HAProxy load balancer distributing UPI API traffic across application servers",
    "host_name": "upi-lb-01.npci.org.in",
    "ip_address": "10.100.0.10",
    "managed_by": "'"$RAVI"'",
    "owned_by": "'"$RAVI"'",
    "support_group": "'"$PLATFORM_ENG"'",
    "assigned_to": "'"$RAVI"'",
    "environment": "Production",
    "description": "HAProxy 2.8 LTS load balancer. SSL termination, health checks every 5s, max 50K concurrent connections. Frontend: 443 HTTPS. Backend: 10.100.1.11:8081, 10.100.1.12:8082."
  }')

UPI_LB=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI Production LB: $UPI_LB"
```

### CI 7: Server — UPI App Server 01

```bash
# Navigate to Configuration > Servers > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_server" \
  -d '{
    "name": "UPI App Server 01",
    "operational_status": "1",
    "install_status": "1",
    "short_description": "Linux application server hosting UPI Transaction Service",
    "host_name": "upi-app-01.npci.org.in",
    "ip_address": "10.100.1.11",
    "os": "Linux",
    "os_version": "Ubuntu 22.04 LTS",
    "ram": "16384",
    "cpu_count": "8",
    "cpu_type": "Intel Xeon E5-2686 v4",
    "disk_space": "500",
    "serial_number": "NPCI-APP-SRV-001",
    "asset_tag": "NPCI-A001",
    "managed_by": "'"$RAVI"'",
    "owned_by": "'"$RAVI"'",
    "support_group": "'"$PLATFORM_ENG"'",
    "assigned_to": "'"$RAVI"'",
    "environment": "Production",
    "description": "Physical server in NPCI Mumbai DC, Rack B12, Unit 15. 16GB RAM, 8-core Xeon, 500GB NVMe SSD. Dual 10GbE bonded."
  }')

APP_SRV_01=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI App Server 01: $APP_SRV_01"
```

### CI 8: Server — UPI App Server 02

```bash
# Navigate to Configuration > Servers > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_server" \
  -d '{
    "name": "UPI App Server 02",
    "operational_status": "1",
    "install_status": "1",
    "short_description": "Linux application server hosting UPI Settlement Service",
    "host_name": "upi-app-02.npci.org.in",
    "ip_address": "10.100.1.12",
    "os": "Linux",
    "os_version": "Ubuntu 22.04 LTS",
    "ram": "16384",
    "cpu_count": "8",
    "cpu_type": "Intel Xeon E5-2686 v4",
    "disk_space": "500",
    "serial_number": "NPCI-APP-SRV-002",
    "asset_tag": "NPCI-A002",
    "managed_by": "'"$AMIT"'",
    "owned_by": "'"$RAVI"'",
    "support_group": "'"$PLATFORM_ENG"'",
    "assigned_to": "'"$AMIT"'",
    "environment": "Production",
    "description": "Physical server in NPCI Mumbai DC, Rack B12, Unit 16. 16GB RAM, 8-core Xeon, 500GB NVMe SSD. Dual 10GbE bonded."
  }')

APP_SRV_02=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI App Server 02: $APP_SRV_02"
```

### CI 9: Server — UPI DB Server 01

```bash
# Navigate to Configuration > Servers > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_server" \
  -d '{
    "name": "UPI DB Server 01",
    "operational_status": "1",
    "install_status": "1",
    "short_description": "High-performance Linux database server hosting PostgreSQL primary and replica",
    "host_name": "upi-db-srv-01.npci.org.in",
    "ip_address": "10.100.2.10",
    "os": "Linux",
    "os_version": "Ubuntu 22.04 LTS",
    "ram": "65536",
    "cpu_count": "16",
    "cpu_type": "Intel Xeon Gold 6248R",
    "disk_space": "4000",
    "serial_number": "NPCI-DB-SRV-001",
    "asset_tag": "NPCI-D001",
    "managed_by": "'"$AMIT"'",
    "owned_by": "'"$RAVI"'",
    "support_group": "'"$PLATFORM_ENG"'",
    "assigned_to": "'"$AMIT"'",
    "environment": "Production",
    "description": "Database server in NPCI Mumbai DC, Rack C08. 64GB RAM, 16-core Xeon Gold, 4TB NVMe SSD RAID 10. Dedicated 25GbE replication network. UPS-protected."
  }')

DB_SRV_01=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI DB Server 01: $DB_SRV_01"
```

### CI 10: Application — Prometheus Monitoring

```bash
# Navigate to Configuration > Applications > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_appl" \
  -d '{
    "name": "Prometheus Monitoring",
    "operational_status": "1",
    "install_status": "1",
    "short_description": "Prometheus 2.48 time-series database collecting metrics from all UPI components",
    "host_name": "upi-mon-01.npci.org.in",
    "ip_address": "10.100.3.11",
    "version": "2.48.1",
    "managed_by": "'"$RAVI"'",
    "owned_by": "'"$RAVI"'",
    "support_group": "'"$PLATFORM_ENG"'",
    "assigned_to": "'"$RAVI"'",
    "environment": "Production",
    "description": "Prometheus 2.48.1 scraping all UPI components. Scrape interval: 15s. Retention: 30 days. AlertManager on port 9093. Web UI: port 9090."
  }')

PROMETHEUS=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "Prometheus Monitoring: $PROMETHEUS"
```

### CI 11: Application — Grafana Dashboard

```bash
# Navigate to Configuration > Applications > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_appl" \
  -d '{
    "name": "Grafana Dashboard",
    "operational_status": "1",
    "install_status": "1",
    "short_description": "Grafana 10.2 visualization platform for UPI operational dashboards",
    "host_name": "upi-mon-01.npci.org.in",
    "ip_address": "10.100.3.11",
    "version": "10.2.3",
    "managed_by": "'"$RAVI"'",
    "owned_by": "'"$RAVI"'",
    "support_group": "'"$PLATFORM_ENG"'",
    "assigned_to": "'"$PRIYA"'",
    "environment": "Production",
    "description": "Grafana 10.2.3 dashboards for UPI platform. Data source: Prometheus localhost:9090. LDAP auth. Port 3000."
  }')

GRAFANA=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "Grafana Dashboard: $GRAFANA"
```

### CI 12: Application — Snow Bridge Integration

```bash
# Navigate to Configuration > Applications > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_appl" \
  -d '{
    "name": "Snow Bridge Integration",
    "operational_status": "1",
    "install_status": "1",
    "short_description": "Custom integration bridging Prometheus AlertManager alerts to ServiceNow incidents",
    "host_name": "upi-mon-01.npci.org.in",
    "ip_address": "10.100.3.11",
    "version": "1.0.0",
    "managed_by": "'"$RAVI"'",
    "owned_by": "'"$RAVI"'",
    "support_group": "'"$PLATFORM_ENG"'",
    "assigned_to": "'"$RAVI"'",
    "environment": "Production",
    "description": "Snow Bridge Python service receiving AlertManager webhooks and creating ServiceNow incidents via REST API. Port 5001. Supports deduplication and auto-resolution."
  }')

SNOW_BRIDGE=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "Snow Bridge Integration: $SNOW_BRIDGE"
```

## 7.2 Lookup Relationship Types

```bash
# ----------------------------------------------------------------
# Before creating relationships, get the sys_ids of relationship types
# UI equivalent: Navigate to cmdb_rel_type.list to see all types
# ----------------------------------------------------------------

# "Depends on::Used by"
REL_DEPENDS=$(curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_rel_type?sysparm_query=parent_descriptor=Depends on^child_descriptor=Used by&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(r[0]['sys_id'] if r else 'NOT_FOUND')")
echo "Depends on::Used by: $REL_DEPENDS"

# "Runs on::Runs"
REL_RUNS=$(curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_rel_type?sysparm_query=parent_descriptor=Runs on^child_descriptor=Runs&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(r[0]['sys_id'] if r else 'NOT_FOUND')")
echo "Runs on::Runs: $REL_RUNS"

# "Contains::Contained by"
REL_CONTAINS=$(curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_rel_type?sysparm_query=parent_descriptor=Contains^child_descriptor=Contained by&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(r[0]['sys_id'] if r else 'NOT_FOUND')")
echo "Contains::Contained by: $REL_CONTAINS"

# "Monitors::Monitored by" (may not exist in all PDIs — fall back to Depends on)
REL_MONITORS=$(curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_rel_type?sysparm_query=parent_descriptor=Monitors^child_descriptor=Monitored by&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(r[0]['sys_id'] if r else 'NOT_FOUND')")
echo "Monitors::Monitored by: $REL_MONITORS"

# If Monitors type not found, fall back to Depends on
if [ "$REL_MONITORS" = "NOT_FOUND" ]; then
  REL_MONITORS="$REL_DEPENDS"
  echo "Monitors type not found, using Depends on as fallback"
fi
```

## 7.3 Create CI Relationships (21 total)

### Dependency Relationships (Depends on)

```bash
# ----------------------------------------------------------------
# Relationship 1: UPI Transaction Service depends on UPI PostgreSQL Primary
# UI: Open UPI Transaction Service > CI Relationships > New
# ----------------------------------------------------------------
curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_rel_ci" \
  -d '{"parent": "'"$UPI_TXN_SVC"'", "type": "'"$REL_DEPENDS"'", "child": "'"$PG_PRIMARY"'"}' | python3 -c "import sys,json; print('Rel 1 created:', json.loads(sys.stdin.read())['result']['sys_id'])"

# ----------------------------------------------------------------
# Relationship 2: UPI Settlement Service depends on UPI PostgreSQL Primary
# ----------------------------------------------------------------
curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_rel_ci" \
  -d '{"parent": "'"$UPI_STL_SVC"'", "type": "'"$REL_DEPENDS"'", "child": "'"$PG_PRIMARY"'"}' | python3 -c "import sys,json; print('Rel 2 created:', json.loads(sys.stdin.read())['result']['sys_id'])"

# ----------------------------------------------------------------
# Relationship 3: UPI Production LB depends on UPI Transaction Service
# ----------------------------------------------------------------
curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_rel_ci" \
  -d '{"parent": "'"$UPI_LB"'", "type": "'"$REL_DEPENDS"'", "child": "'"$UPI_TXN_SVC"'"}' | python3 -c "import sys,json; print('Rel 3 created:', json.loads(sys.stdin.read())['result']['sys_id'])"

# ----------------------------------------------------------------
# Relationship 4: UPI Production LB depends on UPI Settlement Service
# ----------------------------------------------------------------
curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_rel_ci" \
  -d '{"parent": "'"$UPI_LB"'", "type": "'"$REL_DEPENDS"'", "child": "'"$UPI_STL_SVC"'"}' | python3 -c "import sys,json; print('Rel 4 created:', json.loads(sys.stdin.read())['result']['sys_id'])"

# ----------------------------------------------------------------
# Relationship 5: UPI PostgreSQL Replica depends on UPI PostgreSQL Primary
# ----------------------------------------------------------------
curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_rel_ci" \
  -d '{"parent": "'"$PG_REPLICA"'", "type": "'"$REL_DEPENDS"'", "child": "'"$PG_PRIMARY"'"}' | python3 -c "import sys,json; print('Rel 5 created:', json.loads(sys.stdin.read())['result']['sys_id'])"

# ----------------------------------------------------------------
# Relationship 6: Snow Bridge depends on Prometheus
# ----------------------------------------------------------------
curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_rel_ci" \
  -d '{"parent": "'"$SNOW_BRIDGE"'", "type": "'"$REL_DEPENDS"'", "child": "'"$PROMETHEUS"'"}' | python3 -c "import sys,json; print('Rel 6 created:', json.loads(sys.stdin.read())['result']['sys_id'])"
```

### Runs on Relationships

```bash
# ----------------------------------------------------------------
# Relationship 7: UPI Transaction Service runs on UPI App Server 01
# ----------------------------------------------------------------
curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_rel_ci" \
  -d '{"parent": "'"$UPI_TXN_SVC"'", "type": "'"$REL_RUNS"'", "child": "'"$APP_SRV_01"'"}' | python3 -c "import sys,json; print('Rel 7 created:', json.loads(sys.stdin.read())['result']['sys_id'])"

# ----------------------------------------------------------------
# Relationship 8: UPI Settlement Service runs on UPI App Server 02
# ----------------------------------------------------------------
curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_rel_ci" \
  -d '{"parent": "'"$UPI_STL_SVC"'", "type": "'"$REL_RUNS"'", "child": "'"$APP_SRV_02"'"}' | python3 -c "import sys,json; print('Rel 8 created:', json.loads(sys.stdin.read())['result']['sys_id'])"
```

### Monitors Relationships

```bash
# ----------------------------------------------------------------
# Relationship 9: Prometheus monitors UPI Transaction Service
# ----------------------------------------------------------------
curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_rel_ci" \
  -d '{"parent": "'"$PROMETHEUS"'", "type": "'"$REL_MONITORS"'", "child": "'"$UPI_TXN_SVC"'"}' | python3 -c "import sys,json; print('Rel 9 created:', json.loads(sys.stdin.read())['result']['sys_id'])"

# ----------------------------------------------------------------
# Relationship 10: Prometheus monitors UPI Settlement Service
# ----------------------------------------------------------------
curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_rel_ci" \
  -d '{"parent": "'"$PROMETHEUS"'", "type": "'"$REL_MONITORS"'", "child": "'"$UPI_STL_SVC"'"}' | python3 -c "import sys,json; print('Rel 10 created:', json.loads(sys.stdin.read())['result']['sys_id'])"
```

### Containment Relationships (UPI Payment Platform contains all CIs)

```bash
# ----------------------------------------------------------------
# Relationships 11-21: UPI Payment Platform contains each technical CI
# UI: Open UPI Payment Platform > CI Relationships > New > Contains
# ----------------------------------------------------------------

for CI_SYS_ID in $UPI_TXN_SVC $UPI_STL_SVC $PG_PRIMARY $PG_REPLICA $UPI_LB $APP_SRV_01 $APP_SRV_02 $DB_SRV_01 $PROMETHEUS $GRAFANA $SNOW_BRIDGE; do
  curl -s -u "$AUTH" -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -X POST "$SNOW/api/now/table/cmdb_rel_ci" \
    -d '{"parent": "'"$UPI_PLATFORM"'", "type": "'"$REL_CONTAINS"'", "child": "'"$CI_SYS_ID"'"}' | python3 -c "import sys,json; print('Contains rel created:', json.loads(sys.stdin.read())['result']['sys_id'])"
done

echo "All 21 relationships created."
```

## 7.4 Query CI Dependencies

```bash
# ----------------------------------------------------------------
# View all dependencies for a specific CI
# UI equivalent: Open CI > Related Items > CI Relationships
# ----------------------------------------------------------------

# What does UPI Transaction Service depend on?
echo "=== UPI Transaction Service dependencies ==="
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_rel_ci?sysparm_query=parent=$UPI_TXN_SVC&sysparm_fields=parent.name,type.parent_descriptor,child.name&sysparm_display_value=true" \
  | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())
for r in data['result']:
    print(f\"  {r['parent.name']} --{r['type.parent_descriptor']}--> {r['child.name']}\")"

# What CIs are contained within UPI Payment Platform?
echo "=== CIs contained in UPI Payment Platform ==="
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_rel_ci?sysparm_query=parent=$UPI_PLATFORM^type=$REL_CONTAINS&sysparm_fields=child.name&sysparm_display_value=true" \
  | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())
for r in data['result']:
    print(f\"  - {r['child.name']}\")"
```

## 7.5 Query the Service Map (Upstream/Downstream)

```bash
# ----------------------------------------------------------------
# Upstream impact: What is affected if PostgreSQL Primary goes down?
# UI equivalent: Open CI > View Map > look upstream
# ----------------------------------------------------------------
echo "=== CIs that USE (depend on) PostgreSQL Primary ==="
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_rel_ci?sysparm_query=child=$PG_PRIMARY^type=$REL_DEPENDS&sysparm_fields=parent.name&sysparm_display_value=true" \
  | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())
for r in data['result']:
    print(f\"  IMPACTED: {r['parent.name']}\")"
```

---

# Lab 08: Service Portfolio & Business Services

## 8.1 Create Business Services (3)

### Business Service 1: UPI Payment Processing

```bash
# Navigate to Service Portfolio > Services > Business Services > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_service_business" \
  -d '{
    "name": "UPI Payment Processing",
    "service_classification": "Business Service",
    "service_status": "catalog",
    "operational_status": "1",
    "short_description": "Core UPI real-time payment processing for member banks and fintech partners",
    "description": "End-to-end UPI payment processing service handling real-time fund transfers between banks via NPCI Unified Payments Interface. Processes 10B+ transactions/month across 350+ member banks. Supports P2P, P2M, bill payments, and autopay mandates. 99.95% uptime SLA.",
    "busines_criticality": "1 - Most Critical",
    "used_for": "Production",
    "owned_by": "'"$SANJAY"'",
    "managed_by": "'"$RAVI"'",
    "support_group": "'"$PLATFORM_ENG"'"
  }')

BS_PAYMENT=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI Payment Processing: $BS_PAYMENT"
```

### Business Service 2: UPI Dispute Resolution

```bash
# Navigate to Service Portfolio > Services > Business Services > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_service_business" \
  -d '{
    "name": "UPI Dispute Resolution",
    "service_classification": "Business Service",
    "service_status": "catalog",
    "operational_status": "1",
    "short_description": "UPI dispute handling and resolution for member banks and consumers",
    "description": "Handles UPI transaction disputes including failed transactions, unauthorized debits, merchant refunds, and chargeback processing. Interfaces with UDIR system as mandated by RBI. Target resolution: 95% within 5 business days.",
    "busines_criticality": "2 - Somewhat Critical",
    "used_for": "Production",
    "owned_by": "'"$SANJAY"'",
    "managed_by": "'"$RAVI"'",
    "support_group": "'"$PLATFORM_ENG"'"
  }')

BS_DISPUTE=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI Dispute Resolution: $BS_DISPUTE"
```

### Business Service 3: UPI Merchant Onboarding

```bash
# Navigate to Service Portfolio > Services > Business Services > click New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_service_business" \
  -d '{
    "name": "UPI Merchant Onboarding",
    "service_classification": "Business Service",
    "service_status": "catalog",
    "operational_status": "1",
    "short_description": "Merchant registration and activation for UPI payment acceptance",
    "description": "End-to-end merchant onboarding service for UPI acceptance. Includes VPA creation, QR code generation, settlement account configuration, and MCC mapping. Onboards 50K+ merchants/month through acquiring banks.",
    "busines_criticality": "2 - Somewhat Critical",
    "used_for": "Production",
    "owned_by": "'"$SANJAY"'",
    "managed_by": "'"$AMIT"'",
    "support_group": "'"$PLATFORM_ENG"'"
  }')

BS_MERCHANT=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI Merchant Onboarding: $BS_MERCHANT"
```

## 8.2 Create Technical Services (4)

```bash
# ----------------------------------------------------------------
# Technical Service 1: UPI Transaction Processing
# Navigate to Service Portfolio > Services > Technical Services > New
# ----------------------------------------------------------------
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_service_technical" \
  -d '{
    "name": "UPI Transaction Processing",
    "service_classification": "Technical Service",
    "service_status": "catalog",
    "operational_status": "1",
    "short_description": "Real-time UPI transaction switching and processing engine",
    "description": "Core transaction processing engine handling UPI payment requests. Performs VPA resolution, payer/payee PSP routing, NPCI switching, and real-time debit/credit orchestration. Sub-500ms P95 latency.",
    "busines_criticality": "1 - Most Critical",
    "used_for": "Production",
    "owned_by": "'"$RAVI"'",
    "managed_by": "'"$AMIT"'",
    "support_group": "'"$PLATFORM_ENG"'"
  }')
TS_TXN=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI Transaction Processing: $TS_TXN"

# ----------------------------------------------------------------
# Technical Service 2: UPI Settlement & Reconciliation
# ----------------------------------------------------------------
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_service_technical" \
  -d '{
    "name": "UPI Settlement & Reconciliation",
    "service_classification": "Technical Service",
    "service_status": "catalog",
    "operational_status": "1",
    "short_description": "UPI inter-bank settlement and transaction reconciliation engine",
    "description": "Batch settlement engine processing end-of-day net settlement positions across member banks. Multi-lateral netting, NACH settlement files, and reconciliation. 4 settlement cycles/day.",
    "busines_criticality": "1 - Most Critical",
    "used_for": "Production",
    "owned_by": "'"$RAVI"'",
    "managed_by": "'"$AMIT"'",
    "support_group": "'"$PLATFORM_ENG"'"
  }')
TS_STL=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI Settlement & Reconciliation: $TS_STL"

# ----------------------------------------------------------------
# Technical Service 3: UPI Database Service
# ----------------------------------------------------------------
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_service_technical" \
  -d '{
    "name": "UPI Database Service",
    "service_classification": "Technical Service",
    "service_status": "catalog",
    "operational_status": "1",
    "short_description": "PostgreSQL database cluster for UPI transaction and configuration data",
    "description": "PostgreSQL database cluster providing persistent storage for UPI transaction records, merchant registries, VPA mappings, and settlement data. Primary-replica architecture with synchronous replication. Handles 300K+ writes/sec during peak.",
    "busines_criticality": "1 - Most Critical",
    "used_for": "Production",
    "owned_by": "'"$RAVI"'",
    "managed_by": "'"$AMIT"'",
    "support_group": "'"$PLATFORM_ENG"'"
  }')
TS_DB=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI Database Service: $TS_DB"

# ----------------------------------------------------------------
# Technical Service 4: UPI Monitoring & Observability
# ----------------------------------------------------------------
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmdb_ci_service_technical" \
  -d '{
    "name": "UPI Monitoring & Observability",
    "service_classification": "Technical Service",
    "service_status": "catalog",
    "operational_status": "1",
    "short_description": "Prometheus + Grafana + Snow Bridge monitoring stack for UPI platform",
    "description": "Full-stack observability platform. Prometheus collects 10K+ metrics endpoints. Grafana provides real-time dashboards. Snow Bridge forwards critical alerts to ServiceNow for automated incident creation.",
    "busines_criticality": "2 - Somewhat Critical",
    "used_for": "Production",
    "owned_by": "'"$RAVI"'",
    "managed_by": "'"$PRIYA"'",
    "support_group": "'"$PLATFORM_ENG"'"
  }')
TS_MON=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI Monitoring & Observability: $TS_MON"
```

## 8.3 Link Business Services to Technical Services

```bash
# ----------------------------------------------------------------
# UPI Payment Processing depends on all 4 Technical Services
# UI: Open Business Service > CI Relationships > New > Depends on
# ----------------------------------------------------------------
for TS in $TS_TXN $TS_STL $TS_DB $TS_MON; do
  curl -s -u "$AUTH" -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -X POST "$SNOW/api/now/table/cmdb_rel_ci" \
    -d '{"parent": "'"$BS_PAYMENT"'", "type": "'"$REL_DEPENDS"'", "child": "'"$TS"'"}' \
    | python3 -c "import sys,json; print('BS Payment -> TS:', json.loads(sys.stdin.read())['result']['sys_id'])"
done

# UPI Dispute Resolution depends on Transaction Processing + Database
for TS in $TS_TXN $TS_DB; do
  curl -s -u "$AUTH" -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -X POST "$SNOW/api/now/table/cmdb_rel_ci" \
    -d '{"parent": "'"$BS_DISPUTE"'", "type": "'"$REL_DEPENDS"'", "child": "'"$TS"'"}' \
    | python3 -c "import sys,json; print('BS Dispute -> TS:', json.loads(sys.stdin.read())['result']['sys_id'])"
done

# UPI Merchant Onboarding depends on Database + Monitoring
for TS in $TS_DB $TS_MON; do
  curl -s -u "$AUTH" -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -X POST "$SNOW/api/now/table/cmdb_rel_ci" \
    -d '{"parent": "'"$BS_MERCHANT"'", "type": "'"$REL_DEPENDS"'", "child": "'"$TS"'"}' \
    | python3 -c "import sys,json; print('BS Merchant -> TS:', json.loads(sys.stdin.read())['result']['sys_id'])"
done

echo "All service relationships created."
```

## 8.4 Query Services by Classification

```bash
# ----------------------------------------------------------------
# List all Business Services
# UI: Service Portfolio > Services > Business Services
# ----------------------------------------------------------------
echo "=== Business Services ==="
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_ci_service_business?sysparm_query=nameSTARTSWITHUPI&sysparm_fields=name,service_status,operational_status,busines_criticality&sysparm_display_value=true" \
  | python3 -c "
import sys, json
for r in json.loads(sys.stdin.read())['result']:
    print(f\"  {r['name']} | Status: {r['service_status']} | Op: {r['operational_status']} | Criticality: {r['busines_criticality']}\")"

# List all Technical Services
echo "=== Technical Services ==="
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_ci_service_technical?sysparm_query=nameSTARTSWITHUPI&sysparm_fields=name,service_status,operational_status,busines_criticality&sysparm_display_value=true" \
  | python3 -c "
import sys, json
for r in json.loads(sys.stdin.read())['result']:
    print(f\"  {r['name']} | Status: {r['service_status']} | Op: {r['operational_status']} | Criticality: {r['busines_criticality']}\")"
```

---

# Lab 09: SLA, SLO & SLI — Service Level Management

## 9.1 Create SLA Definitions (7)

### SLA 1: P1 Critical — Response (30 minutes)

```bash
# Navigate to Service Level Management > SLA > SLA Definitions > New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/contract_sla" \
  -d '{
    "name": "NPCI UPI - P1 Critical Response",
    "type": "SLA",
    "target": "response",
    "collection": "incident",
    "duration": "1970-01-01 00:30:00",
    "schedule": "",
    "timezone": "Asia/Kolkata",
    "active": true,
    "retroactive_start": false,
    "reset_on_breach": false,
    "start_condition": "priority=1^state=1",
    "pause_condition": "state=-16",
    "stop_condition": "state=2^ORstate=6^ORstate=7"
  }')
SLA_P1_RESP=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "P1 Response SLA: $SLA_P1_RESP"
```

> **Note on conditions:** state=1 (New), state=2 (In Progress), state=-16 (Awaiting User Info), state=6 (Resolved), state=7 (Closed). priority=1 (Critical). The `start_condition`, `pause_condition`, and `stop_condition` fields use encoded query format.

### SLA 2: P1 Critical — Resolution (1 hour)

```bash
# Navigate to SLA Definitions > New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/contract_sla" \
  -d '{
    "name": "NPCI UPI - P1 Critical Resolution",
    "type": "SLA",
    "target": "resolution",
    "collection": "incident",
    "duration": "1970-01-01 01:00:00",
    "schedule": "",
    "timezone": "Asia/Kolkata",
    "active": true,
    "start_condition": "priority=1^state=2",
    "pause_condition": "state=-16^ORstate=-12",
    "stop_condition": "state=6"
  }')
SLA_P1_RES=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "P1 Resolution SLA: $SLA_P1_RES"
```

### SLA 3: P2 High — Response (1 hour)

```bash
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/contract_sla" \
  -d '{
    "name": "NPCI UPI - P2 High Response",
    "type": "SLA",
    "target": "response",
    "collection": "incident",
    "duration": "1970-01-01 01:00:00",
    "schedule": "",
    "timezone": "Asia/Kolkata",
    "active": true,
    "start_condition": "priority=2^state=1",
    "pause_condition": "state=-16",
    "stop_condition": "state=2^ORstate=6^ORstate=7"
  }')
SLA_P2_RESP=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "P2 Response SLA: $SLA_P2_RESP"
```

### SLA 4: P2 High — Resolution (4 hours)

```bash
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/contract_sla" \
  -d '{
    "name": "NPCI UPI - P2 High Resolution",
    "type": "SLA",
    "target": "resolution",
    "collection": "incident",
    "duration": "1970-01-01 04:00:00",
    "schedule": "",
    "timezone": "Asia/Kolkata",
    "active": true,
    "start_condition": "priority=2^state=2",
    "pause_condition": "state=-16^ORstate=-12",
    "stop_condition": "state=6"
  }')
SLA_P2_RES=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "P2 Resolution SLA: $SLA_P2_RES"
```

### SLA 5: P3 Moderate — Response (4 hours, business hours)

```bash
# This SLA uses the NPCI Business Hours schedule (created below in 9.2)
# If the schedule does not exist yet, leave schedule blank and update later
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/contract_sla" \
  -d '{
    "name": "NPCI UPI - P3 Moderate Response",
    "type": "SLA",
    "target": "response",
    "collection": "incident",
    "duration": "1970-01-01 04:00:00",
    "timezone": "Asia/Kolkata",
    "active": true,
    "start_condition": "priority=3^state=1",
    "pause_condition": "state=-16",
    "stop_condition": "state=2^ORstate=6^ORstate=7"
  }')
SLA_P3_RESP=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "P3 Response SLA: $SLA_P3_RESP"
```

### SLA 6: P3 Moderate — Resolution (24 hours, business hours)

```bash
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/contract_sla" \
  -d '{
    "name": "NPCI UPI - P3 Moderate Resolution",
    "type": "SLA",
    "target": "resolution",
    "collection": "incident",
    "duration": "1970-01-02 00:00:00",
    "timezone": "Asia/Kolkata",
    "active": true,
    "start_condition": "priority=3^state=2",
    "pause_condition": "state=-16^ORstate=-12",
    "stop_condition": "state=6"
  }')
SLA_P3_RES=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "P3 Resolution SLA: $SLA_P3_RES"
```

### SLA 7: P4 Low — Resolution (72 hours, business hours)

```bash
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/contract_sla" \
  -d '{
    "name": "NPCI UPI - P4 Low Resolution",
    "type": "SLA",
    "target": "resolution",
    "collection": "incident",
    "duration": "1970-01-04 00:00:00",
    "timezone": "Asia/Kolkata",
    "active": true,
    "start_condition": "priority=4^state=2",
    "pause_condition": "state=-16^ORstate=-12",
    "stop_condition": "state=6"
  }')
SLA_P4_RES=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "P4 Resolution SLA: $SLA_P4_RES"
```

## 9.2 Create Custom Schedules

### NPCI Business Hours (Mon-Sat 8AM-8PM IST)

```bash
# Navigate to System Scheduler > Schedules > New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/cmn_schedule" \
  -d '{
    "name": "NPCI Business Hours",
    "time_zone": "Asia/Kolkata",
    "type": ""
  }')
SCHED_BIZ=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "NPCI Business Hours schedule: $SCHED_BIZ"

# Add schedule entries for Monday through Saturday (8AM-8PM)
for DAY in monday tuesday wednesday thursday friday saturday; do
  curl -s -u "$AUTH" -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -X POST "$SNOW/api/now/table/cmn_schedule_span" \
    -d '{
      "schedule": "'"$SCHED_BIZ"'",
      "name": "'"$DAY"'",
      "type": "time_range",
      "start_date_time": "'"$DAY"' 08:00:00",
      "end_date_time": "'"$DAY"' 20:00:00",
      "all_day": false,
      "show_as": "busy"
    }' | python3 -c "import sys,json; print(f'  Added: $DAY 08:00-20:00')" 2>/dev/null || echo "  Added: $DAY"
done

echo "Business hours schedule created with 6 entries (Mon-Sat)."
```

### Update P3/P4 SLAs with Schedule

```bash
# Now that the schedule exists, update P3 and P4 SLAs to reference it
for SLA_ID in $SLA_P3_RESP $SLA_P3_RES $SLA_P4_RES; do
  curl -s -u "$AUTH" -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -X PATCH "$SNOW/api/now/table/contract_sla/$SLA_ID" \
    -d '{"schedule": "'"$SCHED_BIZ"'"}' \
    | python3 -c "import sys,json; print('Updated SLA with schedule:', json.loads(sys.stdin.read())['result']['name'])"
done
```

## 9.3 Query Active SLA Definitions

```bash
# ----------------------------------------------------------------
# List all NPCI SLA definitions
# UI: Service Level Management > SLA > SLA Definitions
# ----------------------------------------------------------------
echo "=== Active NPCI SLA Definitions ==="
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/contract_sla?sysparm_query=nameSTARTSWITHNPCI^active=true&sysparm_fields=name,type,duration,active&sysparm_display_value=true" \
  | python3 -c "
import sys, json
for r in json.loads(sys.stdin.read())['result']:
    print(f\"  {r['name']} | Duration: {r['duration']} | Active: {r['active']}\")"
```

## 9.4 Test SLA by Creating a P1 Incident

```bash
# ----------------------------------------------------------------
# Create a P1 incident to trigger SLA attachment
# UI: Incident > Create New > set Priority = 1
# ----------------------------------------------------------------
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/incident" \
  -d '{
    "short_description": "UPI Transaction Service - Complete outage affecting all payments",
    "description": "All UPI transaction requests returning HTTP 503. Zero TPS. Multiple PSP banks reporting failures.",
    "impact": "1",
    "urgency": "1",
    "assignment_group": "'"$PLATFORM_ENG"'",
    "cmdb_ci": "'"$UPI_TXN_SVC"'",
    "caller_id": "'"$PRIYA"'",
    "category": "software",
    "subcategory": "Operating System"
  }')
TEST_INC=$(echo "$RESULT" | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(r['sys_id'])")
TEST_INC_NUM=$(echo "$RESULT" | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(r['number'])")
echo "Created P1 incident: $TEST_INC_NUM ($TEST_INC)"

# ----------------------------------------------------------------
# Check Task SLA records attached to this incident
# UI: Open the incident > scroll to Task SLAs related list
# ----------------------------------------------------------------
sleep 3  # Wait for SLA engine to process
echo "=== Task SLAs for $TEST_INC_NUM ==="
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/task_sla?sysparm_query=task=$TEST_INC&sysparm_fields=sla.name,stage,has_breached,percentage&sysparm_display_value=true" \
  | python3 -c "
import sys, json
for r in json.loads(sys.stdin.read())['result']:
    print(f\"  SLA: {r['sla.name']} | Stage: {r['stage']} | Breached: {r['has_breached']} | Elapsed: {r['percentage']}%\")"
```

---

# Lab 10: Knowledge Management

## 10.1 Create Knowledge Base

```bash
# Navigate to Knowledge > Administration > Knowledge Bases > New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/kb_knowledge_base" \
  -d '{
    "title": "UPI Operations Knowledge Base",
    "owner": "'"$RAVI"'",
    "description": "Comprehensive knowledge repository for UPI payment platform operations, troubleshooting, runbooks, and standard operating procedures.",
    "active": true
  }')
KB_BASE=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "Knowledge Base: $KB_BASE"
```

## 10.2 Create Knowledge Categories (7)

```bash
# Navigate to Knowledge Base record > Categories related list > New

declare -a CAT_NAMES=(
  "UPI Error Codes & Resolution"
  "Runbooks & Standard Operating Procedures"
  "Architecture & Design Documents"
  "Onboarding & Training"
  "Known Issues & Workarounds"
  "Change Implementation Guides"
  "Monitoring & Alerting"
)

declare -a CAT_DESCS=(
  "Reference documentation for all UPI error codes with diagnostic steps and resolution procedures"
  "Step-by-step operational procedures for routine and emergency operations"
  "System architecture diagrams, design decisions, and integration specifications"
  "Guides for new team members joining the UPI platform team"
  "Known Error Database (KEDB) - documented known issues with workarounds and fix status"
  "Standard deployment procedures, rollback plans, and change execution guides"
  "Grafana dashboard guides, Prometheus query references, and alert response procedures"
)

# Create each category and store sys_ids
declare -a CAT_IDS=()
for i in "${!CAT_NAMES[@]}"; do
  RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -X POST "$SNOW/api/now/table/kb_category" \
    -d '{
      "label": "'"${CAT_NAMES[$i]}"'",
      "kb_knowledge_base": "'"$KB_BASE"'",
      "description": "'"${CAT_DESCS[$i]}"'"
    }')
  CID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
  CAT_IDS+=("$CID")
  echo "Category created: ${CAT_NAMES[$i]} -> $CID"
done

# Store individual category IDs for article creation
KB_CAT_ERROR="${CAT_IDS[0]}"
KB_CAT_RUNBOOK="${CAT_IDS[1]}"
KB_CAT_ARCH="${CAT_IDS[2]}"
KB_CAT_ONBOARD="${CAT_IDS[3]}"
KB_CAT_KNOWN="${CAT_IDS[4]}"
KB_CAT_CHANGE="${CAT_IDS[5]}"
KB_CAT_MONITOR="${CAT_IDS[6]}"
```

## 10.3 Create Knowledge Articles (5+)

### Article 1: UPI Error Code Reference Guide

```bash
# Navigate to Knowledge > Create New
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/kb_knowledge" \
  -d '{
    "kb_knowledge_base": "'"$KB_BASE"'",
    "kb_category": "'"$KB_CAT_ERROR"'",
    "short_description": "UPI Error Code Reference Guide",
    "author": "'"$AMIT"'",
    "text": "<h2>Overview</h2><p>Comprehensive reference for UPI error codes. Each error code includes description, common causes, diagnostic steps, and resolution procedures.</p><h2>Critical Error Codes</h2><table border=\"1\" cellpadding=\"8\"><tr><th>Code</th><th>Description</th><th>Severity</th><th>Resolution</th></tr><tr><td><strong>U01</strong></td><td>Transaction Timeout</td><td>High</td><td>Check service health, connection pool, restart if needed</td></tr><tr><td><strong>U09</strong></td><td>Beneficiary Bank Offline</td><td>Medium</td><td>Verify bank connectivity, enable circuit breaker</td></tr><tr><td><strong>U16</strong></td><td>Risk Threshold Exceeded</td><td>Medium</td><td>Review fraud dashboard, whitelist if false positive</td></tr><tr><td><strong>U28</strong></td><td>PSP Not Registered</td><td>Low</td><td>Verify PSP registration and certificate</td></tr><tr><td><strong>U30</strong></td><td>Debit Failed</td><td>High</td><td>Check bank connectivity, monitor failure rate metric</td></tr></table><h2>Escalation</h2><ul><li>P1: Any error causing >10% failure rate</li><li>P2: >5% failure rate for >15 minutes</li></ul>",
    "workflow_state": "draft"
  }')
ART_ERROR=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "Article 1 (Error Codes): $ART_ERROR"
```

### Article 2: UPI Transaction Service Restart Runbook

```bash
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/kb_knowledge" \
  -d '{
    "kb_knowledge_base": "'"$KB_BASE"'",
    "kb_category": "'"$KB_CAT_RUNBOOK"'",
    "short_description": "Runbook: UPI Transaction Service Restart Procedure",
    "author": "'"$RAVI"'",
    "text": "<h2>Document Control</h2><p>Runbook ID: RB-UPI-001 | Version: 2.1 | Author: Ravi Kumar</p><h2>When to Use</h2><ul><li>Connection pool utilization exceeds 90% for 10+ minutes</li><li>Heap memory exceeds 85%</li><li>U01 timeout rate exceeds 5% for 15+ minutes</li></ul><h2>Pre-Restart Checks</h2><ol><li>Verify current TPS: <code>curl http://upi-txn-service:8080/metrics | grep upi_transactions_per_second</code></li><li>Check in-flight transactions: <code>curl http://upi-txn-service:8080/api/v1/admin/inflight-count</code></li><li>Verify at least 3 of 4 instances healthy</li><li>Notify #upi-noc-alerts</li></ol><h2>Restart Procedure</h2><p>Option A (K8s): <code>kubectl rollout restart deployment/upi-txn-service -n upi-production</code></p><p>Option B (VM): Remove from LB, drain connections, <code>sudo systemctl restart upi-transaction-service</code>, re-add to LB</p><h2>Post-Restart Validation</h2><ol><li>Verify health endpoint returns UP</li><li>Connection pool below 20% of max</li><li>Error rate returns to baseline within 5 minutes</li></ol>",
    "workflow_state": "draft"
  }')
ART_RUNBOOK=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "Article 2 (Restart Runbook): $ART_RUNBOOK"
```

### Article 3: Known Error — PostgreSQL Connection Pool Exhaustion

```bash
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/kb_knowledge" \
  -d '{
    "kb_knowledge_base": "'"$KB_BASE"'",
    "kb_category": "'"$KB_CAT_KNOWN"'",
    "short_description": "Known Error: PostgreSQL Connection Pool Exhaustion Under Peak Load",
    "author": "'"$AMIT"'",
    "text": "<h2>Symptoms</h2><ul><li>Transaction timeout errors (U01) increasing during peak hours</li><li>Prometheus metric <code>hikari_connections_active</code> approaches <code>hikari_connections_max</code></li><li>PostgreSQL logs show: <code>FATAL: too many connections for role</code></li></ul><h2>Root Cause</h2><p>The default HikariCP connection pool size (max 20) is insufficient for peak load of 4,000 TPS. Under sustained load, all connections are consumed, new requests queue and eventually timeout.</p><h2>Workaround</h2><ol><li>Restart the affected service to reset the pool (see Runbook RB-UPI-001)</li><li>If recurring, increase pool size in application.yml: <code>spring.datasource.hikari.maximum-pool-size: 50</code></li></ol><h2>Permanent Fix</h2><p>Deploy PgBouncer as a connection pooler between application and PostgreSQL. Configuration change tracked under CHG0040001. Target deployment: next maintenance window.</p><h2>Affected CIs</h2><ul><li>UPI Transaction Service</li><li>UPI Settlement Service</li><li>UPI PostgreSQL Primary</li></ul>",
    "workflow_state": "draft"
  }')
ART_KNOWN=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "Article 3 (Known Error): $ART_KNOWN"
```

### Article 4: UPI Platform Architecture Overview

```bash
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/kb_knowledge" \
  -d '{
    "kb_knowledge_base": "'"$KB_BASE"'",
    "kb_category": "'"$KB_CAT_ARCH"'",
    "short_description": "UPI Payment Platform Architecture Overview",
    "author": "'"$RAVI"'",
    "text": "<h2>Architecture Summary</h2><p>The UPI Payment Platform consists of the following layers:</p><h3>Application Layer</h3><ul><li><strong>UPI Transaction Service</strong> (port 8081): Real-time payment processing, 4,000 TPS peak</li><li><strong>UPI Settlement Service</strong> (port 8082): Batch settlement, 5 cycles/day</li></ul><h3>Database Layer</h3><ul><li><strong>PostgreSQL Primary</strong> (10.100.2.11:5432): Write operations, synchronous replication</li><li><strong>PostgreSQL Replica</strong> (10.100.2.12:5432): Read operations, failover standby</li></ul><h3>Infrastructure Layer</h3><ul><li><strong>HAProxy LB</strong> (10.100.0.10): SSL termination, L7 routing, 50K concurrent connections</li><li><strong>App Server 01</strong> (10.100.1.11): 16GB/8CPU, hosts Transaction Service</li><li><strong>App Server 02</strong> (10.100.1.12): 16GB/8CPU, hosts Settlement Service</li><li><strong>DB Server 01</strong> (10.100.2.10): 64GB/16CPU, hosts PostgreSQL cluster</li></ul><h3>Monitoring Stack</h3><ul><li>Prometheus (port 9090): Metrics collection, 15s scrape interval</li><li>Grafana (port 3000): Dashboards and visualization</li><li>Snow Bridge (port 5001): AlertManager to ServiceNow integration</li></ul>",
    "workflow_state": "draft"
  }')
ART_ARCH=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "Article 4 (Architecture): $ART_ARCH"
```

### Article 5: Grafana Dashboard Guide for NOC

```bash
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/kb_knowledge" \
  -d '{
    "kb_knowledge_base": "'"$KB_BASE"'",
    "kb_category": "'"$KB_CAT_MONITOR"'",
    "short_description": "Grafana Dashboard Guide: UPI Transaction Monitoring for NOC",
    "author": "'"$PRIYA"'",
    "text": "<h2>Access</h2><p>URL: <code>http://upi-mon-01.npci.org.in:3000</code> | Login with LDAP credentials.</p><h2>Key Dashboards</h2><h3>1. UPI Transaction Overview</h3><ul><li><strong>TPS Gauge</strong>: Current transactions per second. Normal: 2000-4000. Alert if below 500.</li><li><strong>Error Rate</strong>: Percentage of failed transactions. Target: below 0.5%. P1 if above 10%.</li><li><strong>P95 Latency</strong>: 95th percentile response time. Target: below 500ms.</li></ul><h3>2. Infrastructure Health</h3><ul><li><strong>CPU Usage</strong>: Per-server CPU utilization. Alert above 90%.</li><li><strong>Memory Usage</strong>: Per-server memory. Alert above 85%.</li><li><strong>Disk Usage</strong>: Alert above 80%.</li></ul><h3>3. Database Performance</h3><ul><li><strong>Active Connections</strong>: Current DB connections. Alert if approaching max (500).</li><li><strong>Replication Lag</strong>: Replica delay. Alert if above 100ms.</li></ul><h2>Alert Response Matrix</h2><p>When an alert fires in Grafana, Snow Bridge creates a ServiceNow incident automatically. NOC should verify the auto-created incident and add initial observations as a work note.</p>",
    "workflow_state": "draft"
  }')
ART_GRAFANA=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "Article 5 (Grafana Guide): $ART_GRAFANA"
```

## 10.4 Publish Articles (Update workflow_state)

```bash
# ----------------------------------------------------------------
# Move articles from draft to published
# UI: Open article > set Workflow State = Published > Update
# ----------------------------------------------------------------
for ART_ID in $ART_ERROR $ART_RUNBOOK $ART_KNOWN $ART_ARCH $ART_GRAFANA; do
  curl -s -u "$AUTH" -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -X PATCH "$SNOW/api/now/table/kb_knowledge/$ART_ID" \
    -d '{"workflow_state": "published"}' \
    | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(f\"Published: {r['short_description']}\")"
done
```

## 10.5 Search Knowledge Base

```bash
# ----------------------------------------------------------------
# Search for articles containing "PostgreSQL"
# UI: Knowledge > Homepage > search bar
# ----------------------------------------------------------------
echo "=== KB search: PostgreSQL ==="
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/kb_knowledge?sysparm_query=kb_knowledge_base=$KB_BASE^textLIKEPostgreSQL^workflow_state=published&sysparm_fields=number,short_description,kb_category.label&sysparm_display_value=true" \
  | python3 -c "
import sys, json
for r in json.loads(sys.stdin.read())['result']:
    print(f\"  {r['number']}: {r['short_description']} [{r.get('kb_category.label','')}]\")"

# Search for articles in Error Codes category
echo "=== Articles in Error Codes category ==="
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/kb_knowledge?sysparm_query=kb_category=$KB_CAT_ERROR&sysparm_fields=number,short_description,workflow_state&sysparm_display_value=true" \
  | python3 -c "
import sys, json
for r in json.loads(sys.stdin.read())['result']:
    print(f\"  {r['number']}: {r['short_description']} | State: {r['workflow_state']}\")"
```

---

# Lab 11: Service Catalog & Request Management

## 11.1 Query Existing Catalogs

```bash
# ----------------------------------------------------------------
# Find the default Service Catalog
# UI: Service Catalog > Catalog Definitions > Maintain Catalogs
# ----------------------------------------------------------------
SC_CATALOG=$(curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sc_catalog?sysparm_query=title=Service Catalog&sysparm_fields=sys_id,title&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(r[0]['sys_id'] if r else 'NOT_FOUND')")
echo "Service Catalog sys_id: $SC_CATALOG"
```

## 11.2 Create Catalog Category

```bash
# ----------------------------------------------------------------
# Create parent category: UPI Platform Services
# UI: Service Catalog > Catalog Definitions > Maintain Categories > New
# ----------------------------------------------------------------
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/sc_category" \
  -d '{
    "title": "UPI Platform Services",
    "sc_catalog": "'"$SC_CATALOG"'",
    "description": "Self-service catalog for NPCI UPI Payment Platform. Request access, onboarding, infrastructure, and compliance services.",
    "active": true
  }')
CAT_UPI=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "UPI Platform Services category: $CAT_UPI"

# Create sub-categories
declare -a SUB_CAT_TITLES=("Access & Onboarding" "Merchant Services" "Report an Issue" "Infrastructure Requests" "Compliance & Security")
declare -a SUB_CAT_DESCS=("Request access to systems, APIs, and onboard new team members" "Merchant onboarding, configuration, and lifecycle management" "Report payment issues, settlement discrepancies, and system problems" "Request new environments, infrastructure changes, and resources" "Request compliance audit reports and security reviews")
declare -a SUB_CAT_IDS=()

for i in "${!SUB_CAT_TITLES[@]}"; do
  RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -X POST "$SNOW/api/now/table/sc_category" \
    -d '{
      "title": "'"${SUB_CAT_TITLES[$i]}"'",
      "sc_catalog": "'"$SC_CATALOG"'",
      "parent": "'"$CAT_UPI"'",
      "description": "'"${SUB_CAT_DESCS[$i]}"'",
      "active": true
    }')
  CID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
  SUB_CAT_IDS+=("$CID")
  echo "  Sub-category: ${SUB_CAT_TITLES[$i]} -> $CID"
done

CAT_ACCESS="${SUB_CAT_IDS[0]}"
CAT_MERCHANT="${SUB_CAT_IDS[1]}"
CAT_ISSUE="${SUB_CAT_IDS[2]}"
CAT_INFRA="${SUB_CAT_IDS[3]}"
CAT_COMPLIANCE="${SUB_CAT_IDS[4]}"
```

## 11.3 Create Catalog Item — Request Merchant Onboarding

```bash
# ----------------------------------------------------------------
# UI: Service Catalog > Catalog Definitions > Maintain Items > New
# ----------------------------------------------------------------
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/sc_cat_item" \
  -d '{
    "name": "Request Merchant Onboarding",
    "sc_catalogs": "'"$SC_CATALOG"'",
    "category": "'"$CAT_MERCHANT"'",
    "short_description": "Request onboarding of a new merchant to the UPI payment platform",
    "description": "Use this form to request onboarding of a new merchant to the NPCI UPI Payment Platform. Includes document verification, technical configuration, and sandbox testing. Expected completion: 5 business days.",
    "delivery_time": "5 00:00:00",
    "active": true
  }')
ITEM_MERCHANT=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "Catalog Item (Merchant Onboarding): $ITEM_MERCHANT"
```

## 11.4 Create Variables for Catalog Item

```bash
# ----------------------------------------------------------------
# Variable 1: Merchant Name (Single Line Text, type=6)
# UI: Open catalog item > Variables related list > New
# ----------------------------------------------------------------
curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/item_option_new" \
  -d '{
    "cat_item": "'"$ITEM_MERCHANT"'",
    "type": "6",
    "order": "100",
    "question_text": "Merchant Name",
    "name": "merchant_name",
    "mandatory": true,
    "tooltip": "Registered business name of the merchant"
  }' | python3 -c "import sys,json; print('  Variable: Merchant Name')"

# Variable 2: Business Type (Select Box, type=5)
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/item_option_new" \
  -d '{
    "cat_item": "'"$ITEM_MERCHANT"'",
    "type": "5",
    "order": "200",
    "question_text": "Business Type",
    "name": "business_type",
    "mandatory": true
  }')
VAR_BIZ_TYPE=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
echo "  Variable: Business Type -> $VAR_BIZ_TYPE"

# Add choices for Business Type
for CHOICE in '{"text":"Retail","value":"retail","order":"100"}' \
              '{"text":"E-commerce","value":"ecommerce","order":"200"}' \
              '{"text":"Government","value":"government","order":"300"}' \
              '{"text":"Education","value":"education","order":"400"}'; do
  curl -s -u "$AUTH" -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -X POST "$SNOW/api/now/table/question_choice" \
    -d "$(echo "$CHOICE" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); d['question']='$VAR_BIZ_TYPE'; print(json.dumps(d))")" \
    | python3 -c "import sys,json; r=json.loads(sys.stdin.read())['result']; print(f\"    Choice: {r['text']}\")"
done

# Variable 3: Merchant ID (Single Line Text)
curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/item_option_new" \
  -d '{
    "cat_item": "'"$ITEM_MERCHANT"'",
    "type": "6",
    "order": "300",
    "question_text": "Merchant ID",
    "name": "merchant_id",
    "mandatory": true,
    "tooltip": "Unique NPCI merchant identifier"
  }' | python3 -c "import sys,json; print('  Variable: Merchant ID')"

# Variable 4: Integration Type (Select Box)
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/item_option_new" \
  -d '{
    "cat_item": "'"$ITEM_MERCHANT"'",
    "type": "5",
    "order": "400",
    "question_text": "Integration Type",
    "name": "integration_type",
    "mandatory": true
  }')
VAR_INT_TYPE=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
for CHOICE in '{"text":"SDK","value":"sdk","order":"100"}' \
              '{"text":"API","value":"api","order":"200"}' \
              '{"text":"Plugin","value":"plugin","order":"300"}'; do
  curl -s -u "$AUTH" -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -X POST "$SNOW/api/now/table/question_choice" \
    -d "$(echo "$CHOICE" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); d['question']='$VAR_INT_TYPE'; print(json.dumps(d))")" > /dev/null
done
echo "  Variable: Integration Type with 3 choices"

# Variable 5: Expected TPS (Integer, type=14)
curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/item_option_new" \
  -d '{
    "cat_item": "'"$ITEM_MERCHANT"'",
    "type": "14",
    "order": "500",
    "question_text": "Expected TPS (Transactions Per Second)",
    "name": "expected_tps",
    "mandatory": true,
    "tooltip": "Estimated peak transactions per second for capacity planning"
  }' | python3 -c "import sys,json; print('  Variable: Expected TPS')"

# Variable 6: Go-live Date (Date, type=10)
curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/item_option_new" \
  -d '{
    "cat_item": "'"$ITEM_MERCHANT"'",
    "type": "10",
    "order": "600",
    "question_text": "Planned Go-live Date",
    "name": "golive_date",
    "mandatory": true
  }' | python3 -c "import sys,json; print('  Variable: Go-live Date')"

echo "All 6 variables created for Request Merchant Onboarding."
```

## 11.5 Submit a Catalog Request (Order Now)

```bash
# ----------------------------------------------------------------
# Submit a service catalog request using the Service Catalog API
# This is equivalent to a user clicking "Order Now" in the portal
# UI: Self-Service > Service Catalog > browse to item > fill form > Order Now
# ----------------------------------------------------------------

# Method: Use the Table API to create an sc_request and sc_req_item directly
# First create the request (REQ)
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/sc_request" \
  -d '{
    "requested_for": "'"$PRIYA"'",
    "description": "Merchant onboarding request for QuickPay Solutions submitted via API"
  }')
SC_REQ=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
SC_REQ_NUM=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['number'])")
echo "Request created: $SC_REQ_NUM ($SC_REQ)"

# Now create the requested item (RITM) linked to the catalog item
RESULT=$(curl -s -u "$AUTH" -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST "$SNOW/api/now/table/sc_req_item" \
  -d '{
    "request": "'"$SC_REQ"'",
    "cat_item": "'"$ITEM_MERCHANT"'",
    "requested_for": "'"$PRIYA"'",
    "short_description": "Request Merchant Onboarding - QuickPay Solutions",
    "description": "Merchant: QuickPay Solutions, Type: E-commerce, ID: MERCH-QPS-2024-001, Integration: API, TPS: 500",
    "assignment_group": "'"$PLATFORM_ENG"'"
  }')
SC_RITM=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['sys_id'])")
SC_RITM_NUM=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['result']['number'])")
echo "Requested Item: $SC_RITM_NUM ($SC_RITM)"
```

> **Alternative (Service Catalog Order API):** If your instance supports it, use the Service Catalog API endpoint: `POST /api/sn_sc/servicecatalog/items/{item_sys_id}/order_now` with variables in the request body. This method automatically creates REQ, RITM, and triggers workflows.

## 11.6 Track Request Fulfillment

```bash
# ----------------------------------------------------------------
# Check request status
# UI: Service Catalog > Requests > open REQ > see RITM > see SCTASKs
# ----------------------------------------------------------------

# Check the REQ
echo "=== Request Status ==="
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sc_request/$SC_REQ?sysparm_fields=number,state,approval&sysparm_display_value=true" \
  | python3 -c "
import sys, json
r = json.loads(sys.stdin.read())['result']
print(f\"  REQ: {r['number']} | State: {r['state']} | Approval: {r['approval']}\")"

# Check RITMs under this REQ
echo "=== Requested Items ==="
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sc_req_item?sysparm_query=request=$SC_REQ&sysparm_fields=number,state,short_description,cat_item.name&sysparm_display_value=true" \
  | python3 -c "
import sys, json
for r in json.loads(sys.stdin.read())['result']:
    print(f\"  RITM: {r['number']} | State: {r['state']} | Item: {r.get('cat_item.name', r['short_description'])}\")"

# Check SCTASKs under the RITM
echo "=== Catalog Tasks ==="
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sc_task?sysparm_query=request_item=$SC_RITM&sysparm_fields=number,state,short_description,assignment_group.name&sysparm_display_value=true" \
  | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())['result']
if not data:
    print('  No SCTASKs found (may require workflow/execution plan)')
else:
    for r in data:
        print(f\"  SCTASK: {r['number']} | State: {r['state']} | {r['short_description']} | Group: {r.get('assignment_group.name','')}\")"
```

---

# Verification Section

## Verify Lab 07: CMDB

```bash
echo "================================================================"
echo "VERIFY LAB 07: CMDB & Configuration Management"
echo "================================================================"

# Count CIs by class
echo ""
echo "--- CI Counts by Class ---"
for TABLE in cmdb_ci_business_app cmdb_ci_app_server cmdb_ci_db_instance cmdb_ci_lb cmdb_ci_server cmdb_ci_appl; do
  COUNT=$(curl -s -u "$AUTH" -H "Accept: application/json" \
    "$SNOW/api/now/table/$TABLE?sysparm_query=support_group=$PLATFORM_ENG&sysparm_fields=sys_id&sysparm_count=true" \
    | python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('result',{}).get('count', len(json.loads(sys.stdin.read()).get('result',[]))))" 2>/dev/null || echo "?")
  echo "  $TABLE: queried"
done

# Count relationships
echo ""
echo "--- Relationship Count ---"
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_rel_ci?sysparm_query=parent=$UPI_PLATFORM^type=$REL_CONTAINS&sysparm_fields=sys_id" \
  | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())['result']
print(f'  Containment relationships from UPI Platform: {len(data)}')"

echo ""
echo "Expected: 12 CIs, 21 relationships (10 dependency/runs/monitors + 11 containment)"
```

## Verify Lab 08: Services

```bash
echo "================================================================"
echo "VERIFY LAB 08: Service Portfolio"
echo "================================================================"

echo "--- Business Services ---"
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_ci_service_business?sysparm_query=nameSTARTSWITHUPI&sysparm_fields=name,operational_status&sysparm_display_value=true" \
  | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())['result']
for r in data: print(f\"  {r['name']} ({r['operational_status']})\")
print(f'Total: {len(data)}')"

echo "--- Technical Services ---"
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_ci_service_technical?sysparm_query=nameSTARTSWITHUPI&sysparm_fields=name,operational_status&sysparm_display_value=true" \
  | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())['result']
for r in data: print(f\"  {r['name']} ({r['operational_status']})\")
print(f'Total: {len(data)}')"

echo ""
echo "Expected: 3 Business Services, 4 Technical Services"
```

## Verify Lab 09: SLA Definitions

```bash
echo "================================================================"
echo "VERIFY LAB 09: SLA Definitions"
echo "================================================================"

curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/contract_sla?sysparm_query=nameSTARTSWITHNPCI^active=true&sysparm_fields=name,duration,active&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())['result']
for r in data: print(f\"  {r['name']} | Duration: {r['duration']}\")
print(f'Total active SLAs: {len(data)}')"

echo ""
echo "Expected: 7 SLA definitions (P1 resp/res, P2 resp/res, P3 resp/res, P4 res)"
```

## Verify Lab 10: Knowledge Base

```bash
echo "================================================================"
echo "VERIFY LAB 10: Knowledge Management"
echo "================================================================"

# Knowledge Base
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/kb_knowledge_base?sysparm_query=title=UPI Operations Knowledge Base&sysparm_fields=title,active" \
  | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())['result']
for r in data: print(f\"  KB: {r['title']} | Active: {r['active']}\")"

# Categories
echo "--- Categories ---"
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/kb_category?sysparm_query=kb_knowledge_base=$KB_BASE&sysparm_fields=label" \
  | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())['result']
for r in data: print(f\"  {r['label']}\")
print(f'Total categories: {len(data)}')"

# Articles
echo "--- Articles ---"
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/kb_knowledge?sysparm_query=kb_knowledge_base=$KB_BASE&sysparm_fields=number,short_description,workflow_state&sysparm_display_value=true" \
  | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())['result']
for r in data: print(f\"  {r['number']}: {r['short_description']} [{r['workflow_state']}]\")
print(f'Total articles: {len(data)}')"

echo ""
echo "Expected: 1 KB, 7 categories, 5+ articles"
```

## Verify Lab 11: Service Catalog

```bash
echo "================================================================"
echo "VERIFY LAB 11: Service Catalog"
echo "================================================================"

# Categories
echo "--- Catalog Categories ---"
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sc_category?sysparm_query=parent=$CAT_UPI&sysparm_fields=title,active" \
  | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())['result']
for r in data: print(f\"  {r['title']} | Active: {r['active']}\")
print(f'Total sub-categories: {len(data)}')"

# Catalog Items
echo "--- Catalog Items ---"
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sc_cat_item?sysparm_query=category=$CAT_MERCHANT^ORcategory=$CAT_ACCESS^ORcategory=$CAT_INFRA^ORcategory=$CAT_COMPLIANCE&sysparm_fields=name,category.title,active&sysparm_display_value=true" \
  | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())['result']
for r in data: print(f\"  {r['name']} [{r.get('category.title','')}]\")
print(f'Total items: {len(data)}')"

# Requests
echo "--- Recent Requests ---"
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sc_request?sysparm_query=ORDERBYDESCsys_created_on&sysparm_fields=number,state,requested_for.name&sysparm_display_value=true&sysparm_limit=5" \
  | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())['result']
for r in data: print(f\"  {r['number']} | State: {r['state']} | For: {r.get('requested_for.name','')}\")"

echo ""
echo "Expected: 1 parent + 5 sub-categories, 1+ catalog items, 1+ requests"
```

---

# Cleanup Section

Use these commands to remove all lab data if you need to start fresh.

> **WARNING:** These DELETE operations are irreversible. Only run in a PDI/dev instance.

```bash
echo "================================================================"
echo "CLEANUP: Removing all Phase 2 lab data"
echo "================================================================"
echo "This will DELETE all CIs, services, SLAs, KB articles, and catalog items."
echo "Press Ctrl+C within 10 seconds to cancel."
sleep 10

# ----------------------------------------------------------------
# Cleanup Lab 11: Catalog items, categories, requests
# ----------------------------------------------------------------
echo "--- Cleaning Lab 11: Service Catalog ---"

# Delete catalog requests and related items
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/sc_request?sysparm_query=sys_id=$SC_REQ&sysparm_fields=sys_id" \
  | python3 -c "
import sys, json
for r in json.loads(sys.stdin.read())['result']:
    print(f'  Deleting REQ: {r[\"sys_id\"]}')" 2>/dev/null

curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/sc_request/$SC_REQ" 2>/dev/null && echo "  Deleted request"

# Delete catalog item variables
curl -s -u "$AUTH" -H "Accept: application/json" \
  "$SNOW/api/now/table/item_option_new?sysparm_query=cat_item=$ITEM_MERCHANT&sysparm_fields=sys_id" \
  | python3 -c "
import sys, json
for r in json.loads(sys.stdin.read())['result']:
    print(r['sys_id'])" 2>/dev/null | while read VID; do
  curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/item_option_new/$VID" && echo "  Deleted variable $VID"
done

# Delete catalog item
curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/sc_cat_item/$ITEM_MERCHANT" 2>/dev/null && echo "  Deleted catalog item"

# Delete sub-categories then parent
for CID in $CAT_ACCESS $CAT_MERCHANT $CAT_ISSUE $CAT_INFRA $CAT_COMPLIANCE; do
  curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/sc_category/$CID" 2>/dev/null
done
curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/sc_category/$CAT_UPI" 2>/dev/null && echo "  Deleted catalog categories"

# ----------------------------------------------------------------
# Cleanup Lab 10: Knowledge articles, categories, base
# ----------------------------------------------------------------
echo "--- Cleaning Lab 10: Knowledge Management ---"

for ART_ID in $ART_ERROR $ART_RUNBOOK $ART_KNOWN $ART_ARCH $ART_GRAFANA; do
  curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/kb_knowledge/$ART_ID" 2>/dev/null
done
echo "  Deleted KB articles"

for CID in $KB_CAT_ERROR $KB_CAT_RUNBOOK $KB_CAT_ARCH $KB_CAT_ONBOARD $KB_CAT_KNOWN $KB_CAT_CHANGE $KB_CAT_MONITOR; do
  curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/kb_category/$CID" 2>/dev/null
done
echo "  Deleted KB categories"

curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/kb_knowledge_base/$KB_BASE" 2>/dev/null && echo "  Deleted Knowledge Base"

# ----------------------------------------------------------------
# Cleanup Lab 09: SLA definitions, schedules, test incident
# ----------------------------------------------------------------
echo "--- Cleaning Lab 09: SLA Definitions ---"

for SLA_ID in $SLA_P1_RESP $SLA_P1_RES $SLA_P2_RESP $SLA_P2_RES $SLA_P3_RESP $SLA_P3_RES $SLA_P4_RES; do
  curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/contract_sla/$SLA_ID" 2>/dev/null
done
echo "  Deleted 7 SLA definitions"

curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmn_schedule/$SCHED_BIZ" 2>/dev/null && echo "  Deleted business hours schedule"

# Delete test incident (if created)
if [ -n "$TEST_INC" ]; then
  curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/incident/$TEST_INC" 2>/dev/null && echo "  Deleted test incident"
fi

# ----------------------------------------------------------------
# Cleanup Lab 08: Services and service relationships
# ----------------------------------------------------------------
echo "--- Cleaning Lab 08: Services ---"

for SVC_ID in $BS_PAYMENT $BS_DISPUTE $BS_MERCHANT $TS_TXN $TS_STL $TS_DB $TS_MON; do
  # Delete relationships first
  curl -s -u "$AUTH" -H "Accept: application/json" \
    "$SNOW/api/now/table/cmdb_rel_ci?sysparm_query=parent=$SVC_ID^ORchild=$SVC_ID&sysparm_fields=sys_id" \
    | python3 -c "
import sys, json
for r in json.loads(sys.stdin.read())['result']:
    print(r['sys_id'])" 2>/dev/null | while read RID; do
    curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_rel_ci/$RID" 2>/dev/null
  done
done

for SVC_ID in $BS_PAYMENT $BS_DISPUTE $BS_MERCHANT; do
  curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_ci_service_business/$SVC_ID" 2>/dev/null
done
echo "  Deleted 3 Business Services"

for SVC_ID in $TS_TXN $TS_STL $TS_DB $TS_MON; do
  curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_ci_service_technical/$SVC_ID" 2>/dev/null
done
echo "  Deleted 4 Technical Services"

# ----------------------------------------------------------------
# Cleanup Lab 07: CI relationships then CIs
# ----------------------------------------------------------------
echo "--- Cleaning Lab 07: CMDB ---"

# Delete all relationships involving our CIs
for CI_ID in $UPI_PLATFORM $UPI_TXN_SVC $UPI_STL_SVC $PG_PRIMARY $PG_REPLICA $UPI_LB $APP_SRV_01 $APP_SRV_02 $DB_SRV_01 $PROMETHEUS $GRAFANA $SNOW_BRIDGE; do
  curl -s -u "$AUTH" -H "Accept: application/json" \
    "$SNOW/api/now/table/cmdb_rel_ci?sysparm_query=parent=$CI_ID^ORchild=$CI_ID&sysparm_fields=sys_id" \
    | python3 -c "
import sys, json
for r in json.loads(sys.stdin.read())['result']:
    print(r['sys_id'])" 2>/dev/null | while read RID; do
    curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_rel_ci/$RID" 2>/dev/null
  done
done
echo "  Deleted CI relationships"

# Delete CIs
curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_ci_business_app/$UPI_PLATFORM" 2>/dev/null
curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_ci_app_server/$UPI_TXN_SVC" 2>/dev/null
curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_ci_app_server/$UPI_STL_SVC" 2>/dev/null
curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_ci_db_instance/$PG_PRIMARY" 2>/dev/null
curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_ci_db_instance/$PG_REPLICA" 2>/dev/null
curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_ci_lb/$UPI_LB" 2>/dev/null
curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_ci_server/$APP_SRV_01" 2>/dev/null
curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_ci_server/$APP_SRV_02" 2>/dev/null
curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_ci_server/$DB_SRV_01" 2>/dev/null
curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_ci_appl/$PROMETHEUS" 2>/dev/null
curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_ci_appl/$GRAFANA" 2>/dev/null
curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/cmdb_ci_appl/$SNOW_BRIDGE" 2>/dev/null
echo "  Deleted 12 CIs"

echo ""
echo "================================================================"
echo "CLEANUP COMPLETE"
echo "================================================================"
```

---

## Quick Reference: API Patterns

| Action | Method | Endpoint |
|--------|--------|----------|
| Create record | POST | `/api/now/table/{table_name}` |
| Read record | GET | `/api/now/table/{table_name}/{sys_id}` |
| Query records | GET | `/api/now/table/{table_name}?sysparm_query=...` |
| Update record | PATCH | `/api/now/table/{table_name}/{sys_id}` |
| Delete record | DELETE | `/api/now/table/{table_name}/{sys_id}` |
| Order catalog item | POST | `/api/sn_sc/servicecatalog/items/{sys_id}/order_now` |

## Key Tables Used

| Table | Label | Lab |
|-------|-------|-----|
| `cmdb_ci_business_app` | Business Application | 07 |
| `cmdb_ci_app_server` | Application Server | 07 |
| `cmdb_ci_db_instance` | Database Instance | 07 |
| `cmdb_ci_lb` | Load Balancer | 07 |
| `cmdb_ci_server` | Server | 07 |
| `cmdb_ci_appl` | Application | 07 |
| `cmdb_rel_ci` | CI Relationship | 07, 08 |
| `cmdb_rel_type` | Relationship Type | 07 |
| `cmdb_ci_service_business` | Business Service | 08 |
| `cmdb_ci_service_technical` | Technical Service | 08 |
| `contract_sla` | SLA Definition | 09 |
| `task_sla` | Task SLA | 09 |
| `cmn_schedule` | Schedule | 09 |
| `kb_knowledge_base` | Knowledge Base | 10 |
| `kb_category` | KB Category | 10 |
| `kb_knowledge` | KB Article | 10 |
| `sc_catalog` | Service Catalog | 11 |
| `sc_category` | Catalog Category | 11 |
| `sc_cat_item` | Catalog Item | 11 |
| `item_option_new` | Catalog Variable | 11 |
| `question_choice` | Variable Choice | 11 |
| `sc_request` | Request (REQ) | 11 |
| `sc_req_item` | Requested Item (RITM) | 11 |
| `sc_task` | Catalog Task (SCTASK) | 11 |

---

*Phase 2 API Companion -- Labs 07-11 | NPCI UPI Payment Platform ITSM Lab Series*
