# Exam-style Questions

---

## **1. Why does the IETF standards process look for 'rough consensus and running code'?**

**"Rough consensus"** — not unanimous agreement, just no significant unresolved objections. This prevents any single party from blocking a standard indefinitely, while still ensuring broad agreement.

**"Running code"** — the standard must be implementable and actually implemented. This prevents standards from being purely theoretical constructs that look good on paper but fail in practice.

Together they ensure standards are both practically achievable and broadly acceptable — avoiding the failure mode of either "perfect spec, nobody implements it" or "one vendor's implementation becomes the de facto standard without agreement."

---

## **2. Which IP header fields and ICMP packets are important for traceroute? How does it use them?**

**IP header field — TTL (Time To Live)**:
- Traceroute sends packets with TTL=1, 2, 3… incrementing each probe
- Each router decrements TTL by 1; when TTL hits 0, the router drops the packet

**ICMP packets**:
- Routers send back **ICMP Time Exceeded (Type 11)** when they drop a TTL=0 packet — this reveals the router's IP and RTT
- The destination sends back **ICMP Port Unreachable (Type 3)** or a TCP RST when the packet finally arrives — this signals traceroute to stop

Traceroute reconstructs the path hop-by-hop by deliberately expiring packets at each router and collecting the ICMP responses.

---

## **3. What is the role of a port identifier for an internet connection? How does it also get used by a NAT device?**

**Normal role**: ports provide transport-layer multiplexing — multiple applications on the same IP address can have simultaneous connections. The 4-tuple `(src IP, src port, dst IP, dst port)` uniquely identifies each connection.

**NAT's additional use**: a NAT device has one public IP but many internal clients. It maintains a translation table:
```
(internal IP : internal port)  ↔  (public IP : unique port)
```
The NAT rewrites both IP address and port number on every packet in both directions. The port number stops being just a "which application" identifier — it becomes the NAT's way of tracking which internal host owns which external connection. Effectively NAT is stealing port number space to solve the IP address shortage problem.

---

## **4. Is every payload of an IP packet a Transport Protocol? What does that even mean?**

No. The IP header has a **Protocol field** that identifies what's inside:

| Value | Protocol |
|---|---|
| 1 | ICMP |
| 6 | TCP |
| 17 | UDP |
| 41 | IPv6 encapsulated in IPv4 |
| 89 | OSPF (routing protocol) |

ICMP and routing protocols like OSPF sit directly on top of IP without using TCP or UDP — they are not transport protocols. "Transport protocol" specifically means something that provides end-to-end communication between applications (TCP/UDP). IP can carry many other things that serve completely different purposes.

---

## **5. Why should we use Path-MTU Discovery? What happens if the path changes during the exchange?**

**Why PMTUD**: different links along a path have different MTUs (e.g. Ethernet = 1500 bytes, some tunnels = less). If you send a packet larger than a link's MTU, it must be fragmented — or dropped if the DF (Don't Fragment) bit is set. Fragmentation is inefficient and problematic.

PMTUD finds the largest packet size the entire path can handle without fragmentation:
1. Send packets with DF bit set
2. Receive **ICMP Fragmentation Needed (Type 3, Code 4)** from routers that can't forward the packet
3. Reduce packet size until no more ICMP errors come back

**If the path changes mid-connection**: the new path may have a smaller MTU. Packets start getting dropped silently if a router has DF-bit handling issues ("ICMP black holes") — the connection stalls with no obvious error. The fix is to periodically re-run PMTUD or use conservative packet sizes from the start.
