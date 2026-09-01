# Lab 6: Bridge-to-Bridge Network Communication

## Objectives

- Understand network isolation between Docker bridge networks
- Learn how to route traffic between two separate bridge networks
- Understand the gateway container pattern

---

## Prerequisites

- Completed Lab 5 (Docker Networking)
- Understanding of bridge networks and IP addresses

---

## The Scenario

- You have two separate networks: `frontend` (10.0.1.0/24) and `backend` (10.0.0.0/24)
- By default, containers on different bridge networks CANNOT communicate with each other
- Docker creates a private "bubble" for each network
- Containers inside one bubble are completely invisible to containers inside the other bubble

### The Problem

```
  frontend (10.0.1.0/24)          backend (10.0.0.0/24)
  +------------------+          +------------------+
  |  s2 (10.0.1.2)   |          |  s1 (10.0.0.2)   |
  |                   |   XXX   |                   |
  |  Cannot reach s1  | ------> |  Cannot reach s2  |
  +------------------+          +------------------+

  These networks are completely isolated from each other!
```

- This isolation is a security feature, not a bug
- In a real application, you might want frontend web servers on one network and backend databases on another
- They stay isolated unless you explicitly allow communication between them

---

## The Solution: Gateway Container

- A container connected to BOTH networks can act as a router
- It receives packets on one network interface
- It forwards them out through the other interface
- This is the same concept as a home router connecting your private network to the internet

```
  frontend (10.0.1.0/24)          backend (10.0.0.0/24)
  +------------------+          +------------------+
  |  s2 (10.0.1.2)   |          |  s1 (10.0.0.2)   |
  +--------+---------+          +---------+--------+
           |                               |
           |    +--------------------+     |
           |    |   gw (Gateway)     |     |
           +--->| eth0: 10.0.1.3     |<----+
                | eth1: 10.0.0.3     |
                +--------------------+
                (Connected to BOTH networks)
```

- The gateway has one "foot" in each network
- When s2 wants to reach s1, it sends the packet to the gateway
- The gateway then delivers that packet into the backend network

---

## Part 1: Understanding the Dockerfile

- Before building anything, look at the Dockerfile provided in this directory

```dockerfile
FROM httpd
RUN apt-get update
RUN apt-get install -y iputils-ping
RUN apt-get install -y inetutils-traceroute
RUN apt-get install -y iproute2
RUN apt-get install -y curl telnet dnsutils vim
```

- The base `httpd` (Apache) image is minimal — it only contains what is needed to serve web pages
- It does NOT include network troubleshooting tools like `ping`, `traceroute`, or `ip`
- We add these tools on top of `httpd` so we can debug the network from inside each container
- Each `RUN` line installs a specific package:

| Package                 | What it gives us                        |
|-------------------------|-----------------------------------------|
| `iputils-ping`          | `ping` command                          |
| `inetutils-traceroute`  | `traceroute` command                    |
| `iproute2`              | `ip route` command (for routing tables) |
| `curl telnet dnsutils`  | HTTP, TCP, and DNS testing              |
| `vim`                   | Text editor inside the container        |

---

## Part 2: Build the Image and Create Networks

### Step 2.1 — Build the custom image

Make sure you are in the `Lab` directory where the Dockerfile is located:

```bash
cd /path/to/07-Containers/Lab
ls Dockerfile.nhttpd   # Verify the Dockerfile exists here
```

Now build the image:

```bash
docker build -f Dockerfile.nhttpd . -t nhttpd
```

- `-f Dockerfile.nhttpd` tells Docker which Dockerfile to use (since it's not named `Dockerfile`)
- `-t nhttpd` tags the resulting image as `nhttpd`
- The build may take a minute the first time as it downloads packages

Verify the image was created:

```bash
docker images nhttpd
```

- You should see `nhttpd` listed with a recent creation timestamp

### Step 2.2 — Create the two networks

```bash
docker network create frontend --subnet 10.0.1.0/24
docker network create backend  --subnet 10.0.0.0/24
```

- We specify explicit subnets so we know exactly which IP addresses will be assigned
- Without `--subnet`, Docker picks a random range and the IPs become unpredictable
- Unpredictable IPs make the routing steps later harder to follow

Verify both networks exist:

```bash
docker network ls
```

- You should see `frontend` and `backend` listed with driver `bridge`

Inspect each network to confirm the subnet:

```bash
docker network inspect frontend
docker network inspect backend
```

- Look for the `"Subnet"` field under `IPAM.Config`
- Confirm they match `10.0.1.0/24` and `10.0.0.0/24` respectively

---

## Part 3: Create the Backend and Frontend Containers

### Step 3.1 — Start the containers

```bash
docker run --name s1 --network backend  --cap-add=NET_ADMIN -d nhttpd
docker run --name s2 --network frontend --cap-add=NET_ADMIN -d nhttpd
```

WHY `--cap-add=NET_ADMIN`?

- Containers run with a limited set of Linux "capabilities" by default
- This is a security mechanism built into the Linux kernel
- `NET_ADMIN` is the specific capability that allows a process to modify the kernel's routing table
- Without it, the `ip route add` command we run later would fail with a "permission denied" error

### Step 3.2 — Verify container IPs

```bash
docker inspect s1 | grep IPAddress
docker inspect s2 | grep IPAddress
```

- s1 should have an IP in the `10.0.0.x` range (backend network)
- s2 should have an IP in the `10.0.1.x` range (frontend network)
- Docker typically assigns `.2` as the first container IP, so expect:
  - s1: `10.0.0.2`
  - s2: `10.0.1.2`

### Step 3.3 — Prove the isolation (expected failure)

Try pinging s1 from s2 right now, before the gateway is set up:

```bash
docker exec -it s2 bash
ping 10.0.0.2
```

- This SHOULD fail — you will see `Network is unreachable` or the ping will time out with no replies
- This confirms the network isolation is working correctly
- Press `Ctrl+C` to stop the ping
- Type `exit` to leave the container

---

## Part 4: Create the Gateway Container

### Step 4.1 — Start the gateway on the backend network

```bash
docker run -d --name gw --network backend nhttpd
```

- The gateway starts connected only to the backend network
- We do NOT add `--cap-add=NET_ADMIN` here
- The gateway does not need to modify its own routing table
- It already has routes to both networks through its two interfaces

### Step 4.2 — Connect the gateway to the frontend network

```bash
docker network connect frontend gw
```

- `docker network connect` adds a second network interface to a running container
- After this command, `gw` has two interfaces: one facing backend, one facing frontend
- You can do this to a running container without restarting it

### Step 4.3 — Verify the gateway has two IPs

```bash
docker inspect gw | grep -A 5 '"Networks"'
```

Or for a cleaner view:

```bash
docker inspect gw --format '{{json .NetworkSettings.Networks}}' | python3 -m json.tool
```

- You should see two entries — one for `backend` and one for `frontend`
- Each entry has its own IP address:

```
docker inspect gw shows:

Networks:
  backend:  IP = 10.0.0.3
  frontend: IP = 10.0.1.3

The gateway has a "foot" in each network!
```

- Note these IPs down — you will need them in the next step

---

## Part 5: Add Routes to Enable Communication

- Even though the gateway is connected to both networks, s1 and s2 do not automatically know to use it
- We must manually tell each container: "When you want to reach that other network, send the traffic to the gateway"
- This is exactly how your laptop works — when you want to reach the internet, your OS has a default route pointing to your home router

### The routing logic

| Container | Wants to reach     | Route to add                              |
|-----------|--------------------|-------------------------------------------|
| s2        | 10.0.0.0/24 (backend) | send via 10.0.1.3 (gw's frontend IP)  |
| s1        | 10.0.1.0/24 (frontend) | send via 10.0.0.3 (gw's backend IP)  |

### Step 5.1 — Add a route on s2 (frontend container)

```bash
docker exec -it s2 bash
ip route add 10.0.0.0/24 via 10.0.1.3
exit
```

- This tells s2: "Any packet destined for the 10.0.0.0/24 subnet should be forwarded to 10.0.1.3"
- `10.0.1.3` is the gateway's IP on the frontend side

Verify the route was added:

```bash
docker exec s2 ip route
```

- You should see a line like: `10.0.0.0/24 via 10.0.1.3 dev eth0`

### Step 5.2 — Add a route on s1 (backend container)

```bash
docker exec -it s1 bash
ip route add 10.0.1.0/24 via 10.0.0.3
exit
```

- This tells s1: "Any packet destined for the 10.0.1.0/24 subnet should be forwarded to 10.0.0.3"
- `10.0.0.3` is the gateway's IP on the backend side

Verify the route was added:

```bash
docker exec s1 ip route
```

- You should see a line like: `10.0.1.0/24 via 10.0.0.3 dev eth0`

### Traffic flow diagram

```
s2 (10.0.1.2) wants to reach s1 (10.0.0.2):

  Step 1: s2 checks its routing table
          "10.0.0.0/24 via 10.0.1.3" --> send to gateway

  Step 2: gw receives the packet on its 10.0.1.3 interface (frontend side)
          gw looks up 10.0.0.2 --> it is on the backend network
          gw forwards the packet out its 10.0.0.3 interface (backend side)

  Step 3: s1 receives the packet at 10.0.0.2
          s1 sends the reply back via its route:
          "10.0.1.0/24 via 10.0.0.3" --> send to gateway

  s2 <--> gw <--> s1
```

---

## Part 6: Test the Connection

### Step 6.1 — Ping from s2 to s1

```bash
docker exec -it s2 bash
ping 10.0.0.2
```

- The ping should succeed now
- You will see replies from `10.0.0.2`
- Press `Ctrl+C` to stop

### Step 6.2 — Test HTTP with curl

```bash
curl 10.0.0.2
```

- This should return the Apache default HTML page from s1
- This confirms that not just ICMP (ping) but also TCP traffic is being routed through the gateway

### Step 6.3 — Trace the path with traceroute

```bash
traceroute 10.0.0.2
```

- You should see TWO hops:
  - Hop 1: `10.0.1.3` — the gateway (frontend side)
  - Hop 2: `10.0.0.2` — s1 (the destination)
- This visually confirms the gateway is in the middle of the path

```bash
exit
```

### Step 6.4 — Ping from s1 to s2

```bash
docker exec -it s1 bash
ping 10.0.1.2
```

- This should also succeed
- Both directions work because both containers now have routes pointing to the gateway
- Press `Ctrl+C`, then `exit`

---

## Part 7: Docker Compose Alternative

- Manually creating networks, containers, and routes works for learning but is tedious in real projects
- Docker Compose lets you declare the entire setup in a single YAML file
- The `docker-compose.yml` in this directory shows a simpler example:

```yaml
---
services:
  myapp1:
    image: nagabhushanamn/myapp
    ports:
      - 8081:8080
    networks:
      - my-bridge-net

  myapp2:
    image: nagabhushanamn/myapp
    ports:
      - 8082:8080
    networks:
      - my-bridge-net

networks:
  my-bridge-net:
    driver: bridge
    # Optionally, match the previous example
    # ipam:
    # config:
    # - subnet: "10.0.0.0/19"
    # gateway: "10.0.0.1"
```

Key points about this Compose file:

- Both `myapp1` and `myapp2` are placed on the same `my-bridge-net` network, so they can reach each other directly without a gateway
- The `networks:` section at the bottom defines the network — Docker creates it automatically when you run `docker compose up`
- The commented-out `ipam` block shows how you would specify a fixed subnet, similar to the `--subnet` flag used manually above
- In a multi-network Compose setup, you can list multiple networks under a service and Docker will attach the container to all of them
- This is how you would declare a gateway service in Compose

To run the Compose example:

```bash
docker compose up -d
docker compose ps
docker compose down
```

---

## Cleanup

Remove all containers and networks created in this lab:

```bash
docker rm -f s1 s2 gw
docker network rm frontend backend
```

Verify cleanup:

```bash
docker ps -a        # s1, s2, gw should not appear
docker network ls   # frontend, backend should not appear
```

---

## Key Takeaways

- Docker bridge networks are isolated by default — containers on different bridge networks cannot communicate without explicit routing
- A gateway container connected to multiple networks can forward traffic between them, acting just like a physical router
- Each container that needs to reach another network must have a manual `ip route add` entry pointing at the gateway's IP on the shared network
- The `--cap-add=NET_ADMIN` flag is required for containers that modify their own routing tables
- In production, you would use Docker Compose (with shared networks), Docker Swarm overlay networks, or Kubernetes networking instead of manual IP routes

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `ip route add` fails with "Operation not permitted" | Container missing NET_ADMIN capability | Recreate with `--cap-add=NET_ADMIN` |
| Ping says "Network is unreachable" | Missing route to destination subnet | Add route: `ip route add <subnet> via <gateway_ip>` |
| Ping sends but gets no reply | Route exists one-way only (asymmetric) | Add the return route on the destination container |
| `docker build` fails | Not in the correct directory or wrong Dockerfile name | `cd` to the `Lab` directory and use `-f Dockerfile.nhttpd` |
| Gateway can't forward packets | IP forwarding disabled in container | Run `docker exec gw sysctl net.ipv4.ip_forward` — should show `1` (Docker enables this by default) |

---

## Challenges

**Challenge 1 — Add a third network**

- Create a third network called `dmz` with subnet `10.0.2.0/24`
- Start a new container `s3` on it
- Connect the gateway to `dmz` as well
- Add routes on s1, s2, and s3 so that all three containers can ping each other
- Hint: the gateway will need a third interface, and each container needs two route entries (one for each of the other two subnets)

**Challenge 2 — Trace the path**

- Run `traceroute` from s2 to s1
- How many hops do you see?
- What are the IP addresses at each hop?
- Can you explain what each hop represents?

**Challenge 3 — Asymmetric routing**

- Remove the route from s1 only (use `ip route del 10.0.1.0/24`)
- Now test:
  - Can s2 ping s1? (try `docker exec s2 ping 10.0.0.2`)
  - Can s1 ping s2? (try `docker exec s1 ping 10.0.1.2`)
- Which direction still works and which does not?
- Explain WHY the result is asymmetric
- Think about what happens to the reply packet when the route is missing

> **Hint — how ping works**: Ping is a request-reply protocol. s2 sends an ICMP Echo Request to s1. s1 must then send an ICMP Echo Reply BACK to s2. For the reply to reach s2, s1 needs a route to s2's network. If s1's route to 10.0.1.0/24 is removed, it can still *receive* the request (the gateway forwards it), but it has no way to send the *reply* back. This same principle applies to TCP — a connection requires packets flowing in BOTH directions (SYN → SYN-ACK → ACK).

**Challenge 4 — Direct connection vs gateway pattern**

- Instead of using a gateway, try running `docker network connect backend s2` so that s2 is directly on both networks
- Can s2 now reach s1 without any manual routes?
- Compare this approach to the gateway pattern
- When would you choose the gateway pattern over simply connecting a container to both networks?
