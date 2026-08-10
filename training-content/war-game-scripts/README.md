# War Game / Fault Injection Scripts

Scripts for simulating production failures during M34 (MidStage) and M37 (Final) exercises.

## Safety

- All scripts are designed for a LOCAL training environment only
- Each script has a built-in cleanup/rollback mechanism
- Scripts create temporary files that are cleaned up automatically
- No permanent system changes are made

## Scripts

| Script | What It Simulates | Used In |
|--------|-------------------|---------|
| `simulate-service-down.sh` | Service crash (process killed) | M34, M37 |
| `simulate-disk-full.sh` | Disk space exhaustion | M34 |
| `simulate-slow-response.sh` | Network latency / slow endpoint | M34, M37 |
| `simulate-memory-leak.sh` | Memory leak via growing data | M37 |
| `simulate-db-connection-exhaustion.sh` | Database connection pool full | M37 |

## Usage

```bash
# Run a fault injection
bash simulate-service-down.sh start

# Observe the failure (participants investigate)
# ...

# Clean up after the exercise
bash simulate-service-down.sh stop
```
