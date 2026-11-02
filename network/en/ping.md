# ping Quick Reference

## One-sentence definition

ping is the most basic network diagnostic tool: send the target an "are you there" packet, and see whether it can respond and how long the response takes.

**Mental model: sonar**

```
Sonar: emit a sound wave → bounces off an object → compute the time → judge distance and presence
ping: send an ICMP packet → target replies   → compute the time → judge connectivity and latency
```

The protocol ping uses is ICMP (Internet Control Message Protocol), neither TCP nor UDP, but a network-layer control protocol. It doesn't establish a connection, it just sends an echo request and waits for the other side to return an echo reply.

---

## Reading ping output

```
$ ping api.github.com

PING api.github.com (4.237.22.34): 56 data bytes
64 bytes from 4.237.22.34: icmp_seq=0 ttl=112 time=12.345 ms
64 bytes from 4.237.22.34: icmp_seq=1 ttl=112 time=11.892 ms
64 bytes from 4.237.22.34: icmp_seq=2 ttl=112 time=13.201 ms
^C
--- api.github.com ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 11.892/12.479/13.201/0.537 ms
```

| Field | Meaning | How to judge good or bad |
|------|------|------------|
| `icmp_seq` | Which packet (starting from 0) | Non-consecutive sequence numbers = packet loss |
| `ttl=112` | How many more router hops the packet can pass through | Linux starts at 64, Windows 128, minus 1 per hop; can be used to estimate hop count |
| `time=12ms` | Round-trip latency (RTT) | Same city <10ms, international 50–200ms, >500ms is very slow |
| `packet loss` | Packet loss rate | 0% normal, >5% problematic, >20% severe |
| `stddev` | Latency jitter | Smaller is more stable, high jitter causes voice/video stuttering |

---

## Common commands

### Basic usage

```bash
# The simplest ping (macOS/Linux run nonstop by default, Ctrl+C to interrupt)
ping google.com

# Ping only a given number of times
ping -c 4 google.com

# Ping an IPv6 address
ping6 google.com
# or
ping -6 google.com
```

### Controlling behaviour

```bash
# Increase the frequency (default once per second, changed to 0.2 seconds)
ping -i 0.2 google.com

# Specify packet size (default 56 bytes, test network behaviour with large packets)
ping -s 1400 google.com

# Specify the timeout per packet (no response after waiting 2 seconds counts as a timeout)
ping -W 2 google.com

# Combined: ping only 10 times, waiting 1 second each, packet size 512 bytes
ping -c 10 -i 1 -s 512 google.com
```

### Diagnostic scenarios

```bash
# Scenario 1: is the service down? First determine whether it's a network problem or an application-layer problem
ping your-server.com
# Reachable   → the network is fine, something's wrong at the application layer, continue diagnosing with curl
# Unreachable → there's a network-layer problem, or the other side blocks ICMP

# Scenario 2: verify DNS resolution is correct (the first line shows the resolved IP)
ping my-domain.com

# Scenario 3: continuous monitoring, to see whether the network is stable (watch for occasional loss or latency spikes)
ping -i 1 8.8.8.8

# Scenario 4: measure latency to a particular region
ping tokyo.server.com

# Scenario 5: test whether the local network stack is working (ping the loopback address)
ping 127.0.0.1

# Scenario 6: test whether the LAN gateway is reachable (first confirm the local machine → gateway segment)
ping 192.168.1.1
```

---

## 5 typical results

```bash
# 1. Normal
64 bytes from 1.1.1.1: icmp_seq=0 ttl=57 time=5.2 ms

# 2. Completely unreachable (domain resolved successfully, but the host doesn't respond or a firewall blocks ICMP)
Request timeout for icmp_seq 0

# 3. Domain resolution failed (DNS problem)
ping: cannot resolve xyz.invalid: Name or service not known

# 4. Network not reachable at all (can't even reach the router)
ping: sendto: Network is unreachable

# 5. Packet loss (gap in icmp_seq numbers)
64 bytes from 1.1.1.1: icmp_seq=0 ttl=57 time=5.2 ms
64 bytes from 1.1.1.1: icmp_seq=1 ttl=57 time=5.1 ms
                                   ↑ icmp_seq=2 missing = one packet lost
64 bytes from 1.1.1.1: icmp_seq=3 ttl=57 time=5.3 ms
```

> **Important insight: ping timeout ≠ service down.** A firewall can block ICMP while allowing TCP 80/443. It's entirely possible for ping to fail while `curl` works fine.

---

## Common Flag quick reference

| Flag | Purpose | Example |
|------|------|------|
| `-c <n>` | Send only n packets | `ping -c 4 google.com` |
| `-i <sec>` | Interval between packets (seconds) | `ping -i 0.5 google.com` |
| `-s <bytes>` | Specify packet size | `ping -s 1400 google.com` |
| `-W <sec>` | Timeout per packet | `ping -W 2 google.com` |
| `-t <ttl>` | Set the TTL value | `ping -t 10 google.com` |
| `-6` | Force IPv6 | `ping -6 google.com` |
| `-4` | Force IPv4 | `ping -4 google.com` |

---

## Division of labour between ping and other diagnostic tools

| Tool | What it can diagnose | What it can't diagnose |
|------|-----------|------------|
| `ping` | IP-layer connectivity, latency, packet loss | Whether the application layer works (HTTP, databases, etc.) |
| `traceroute` | Which routers packets pass through, which hop has high latency | Application-layer problems |
| `curl` | Whether the HTTP application layer works | Network-layer packet loss and routing problems |
| `nslookup / dig` | Whether DNS resolution is correct | Network connectivity |

**Diagnostic order:**

```
ping 127.0.0.1      → local network stack OK?
ping 192.168.1.1    → local machine to gateway reachable?
ping 8.8.8.8        → can reach the public Internet?
ping google.com     → DNS resolution OK?
curl https://...    → application-layer service OK?
```

---

## Inferring hop count from TTL

The initial TTL value varies by system:

| Operating system | Default TTL |
|---------|---------|
| Linux | 64 |
| macOS | 64 |
| Windows | 128 |
| Network devices (Cisco etc.) | 255 |

Received TTL = initial value - number of hops passed. For example, receiving `ttl=112` with the other side being Windows (128) means it passed through 128 - 112 = **16 hops**.
