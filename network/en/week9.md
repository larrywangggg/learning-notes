# COMP3310 Week 9: Congestion Control · Flow Control · Network Management

---

## Part A: Congestion and Flow Control

### 1. Positioning

The course enters its last big topic, "When Good Networks Go Bad". All the earlier protocol designs were built on the fairy-tale assumption that "the network is used by you alone". In reality it's shared globally, so we have to talk about **congestion** and **flow control**. Scope of discussion: Network layer + Transport layer, mainly TCP; UDP is mentioned only when it "causes trouble".

---

### 2. Sliding Window Recap (groundwork)

**Sender Window W**: the number of unACKed bytes; the goal is to fill the pipe.

```
W ≈ 2 × Bandwidth × delay (BDP, bandwidth-delay product)

E.g.: 100Mb/s + 50ms one-way delay → W = 10Mb ≈ 1MB ≈ 1000 10kb segments
    These 1000 segments are "on the road" right now
```

**The most primitive Receiver model:**
- Buffers only one segment
- Drops anything out of order, and the ACK still points to "the one I'm still waiting for"
- Sender's single timer times out → retransmit everything unACKed → simple but extremely inefficient

---

### 3. Flow Control (aimed at the Receiver)

**Problem**: the Sender stuffs data in as hard as it can, and the Receiver's application layer can't keep up (typical scenario: HD video streamed to a small device).

**Receiver Window WIN**: the Receiver reports its remaining buffer size in the ACK.

| Name | Whose | Role |
|------|------|------|
| W | Sender | Based on BDP, how much can theoretically be stuffed in |
| WIN | Receiver | Tells the Sender "how much buffer I have left" |
| CWND | Sender | The "safe sending amount" estimated from network feedback |

**What the Sender actually uses: `min(W, WIN, CWND)` as the effective window.**

> **Common exam point**: WIN and CWND have nothing to do with each other. WIN is the Receiver's buffer state, CWND is the Sender's estimate of network capacity.

Because many segments are in flight along the path, by the time WIN is reported back it already reflects the state "half an RTT ago" — the feedback you see inherently lags.

---

### 4. Congestion

**A concept that must be corrected:** "link congestion" is a wrong way to put it. A link is a conveyor belt with a fixed clock; 100Mb/s is 100Mb/s, it won't "fit more". What really gets congested is the **router's buffer** (many in, one out → output buffer overflows → packet loss).

**The Congestion Collapse positive feedback loop:**

```
Load rises → buffers fill → delay soars
→ buffers overflow → packet loss
→ Receiver requests retransmission → Sender retransmits
→ The network fills up with "retransmissions of old data", and new data can't get in
→ Goodput (effective throughput) → 0
```

> "If I don't obey congestion control, can I grab a bit more bandwidth?" — No. You can't beat physics; you'll only make yourself lose more packets.

---

### 5. Fairness vs Efficiency

| Strategy | Meaning | Total throughput |
|------|------|--------|
| Fair (0.5 per flow) | All flows allocated equally | 1.5 |
| Efficient (starve AC) | Maximise total throughput | 2.0 |
| Optimal (slightly starve AC=0.25) | High throughput without completely starving anyone | 2.0 |

**Max-Min Fairness**: maximise the minimum. Method: all flows start from 0 and rise together; whichever first saturates a bottleneck link is locked at that value, and the remaining capacity goes to the flows not yet saturated, which keep rising.

> ⚠️ The lecturer admitted the numbers on the slide don't add up (a student pointed it out on the spot). If you meet this kind of question in the exam, recompute it yourself rather than trusting the slides blindly.

---

### 6. Classification of Control Laws

| Dimension | Options |
|------|------|
| Open/closed loop | Open (reserved circuits, e.g. ATM) / Closed (feedback-based) |
| Who leads | Host-driven / Network-driven (policing is strong but rigid) |
| Allocation method | Rate-based / Window-based |

**TCP = Closed-loop, Host-driven, Window-based.**

---

### 7. AIMD (the core mechanism)

**Additive Increase, Multiplicative Decrease:**
- No congestion → increase slowly (+1 segment per RTT)
- Congestion → cut in half (×0.5)

Why must it be AI + MD?

| Combination | Result |
|------|------|
| Slow increase + slow decrease | Slow convergence, wasted capacity |
| Fast increase + fast decrease | Violent oscillation, unstable |
| Fast increase + slow decrease | Poor fairness, the strong take all |
| **Slow increase + fast decrease** | **Converges to fair + efficient in the game-theoretic sense** |

The typical traffic curve it produces is the **TCP Sawtooth** — capture one long-distance transfer in Wireshark and you'll see it.

---

### 8. Sources of Congestion Signals

| Signal | Pros | Cons |
|------|------|------|
| Packet loss | Unambiguous | Already too late (the buffer is full) |
| Packet delay | Early warning | Inferred rather than confirmed, sensitive to jitter (especially nasty when a phone switches base stations) |
| ECN (explicit marking by routers) | Early, with zero extra traffic | Every device on the path must support it; deployment is still very low |

---

### 9. ACK Clocking (self-clocking mechanism)

Going from a high-speed link → a low-speed link, packets queue at the router and are output "stretched out", and ACKs also return at the slow link's rate. When the Sender sees the ACK spacing grow, it knows to slow down.

TCP uses **the rhythm of ACK arrivals** as the trigger for sending packets — an implicit feedback loop, with no need to measure time separately. This leads to CWND (Congestion Window): the upper limit on the amount actually sent, usually < W.

---

### 10. Slow Start

What should CWND be set to at a cold start? AI is too slow (1000 RTTs to fill), so Slow Start is used:

```
Initial CWND = 1
Double every RTT (1, 2, 4, 8, 16...)
Until packet loss occurs → MD cuts it in half
Set ssthresh = ½ × CWND@loss
Then enter the AI phase (+1 per RTT)
```

> The lecturer quipped: "It's called Slow Start but it's actually exponential growth; the name is backwards."

---

### 11. Evolution of TCP Variants

| Version | Key features |
|------|---------|
| Tahoe / Reno (90s) | Classic AIMD + Slow Start + Fast Retransmit |
| Vegas | Uses RTT changes to predict congestion and backs off early. Problem: beaten to death by Reno (Reno doesn't yield, Vegas yields voluntarily, so Vegas can't get bandwidth) |
| BIC / CUBIC | Cubic curve, more aggressive probing, Linux default |
| BBR (Google) | Measures bottleneck bandwidth + RTT, heartbeat-style probing (not a sawtooth), used by YouTube, but whether it's "friendly" when coexisting with other TCPs is still debated |

Wikipedia lists 20+ kinds of TCP, each performing differently in different scenarios; there's no "absolute optimum".

---

### 12. Loss Recovery Optimisations (overview)

| Mechanism | Description |
|------|------|
| **Fast Retransmit** | On receiving 3 dup-ACKs → don't wait for the timeout, immediately retransmit the lost segment |
| **Fast Recovery** | After retransmitting, don't fall back to Slow Start; just do MD and continue — keeps the ACK clock |
| **NewReno** | Recognises partial ACKs, can repair multiple losses within one RTT |
| **SACK** | The Receiver tells the Sender directly which segments it received, and the Sender retransmits precisely |

> See Part B for the complete evolution path.

---

### 13. ECN (router assistance)

An extremely simple mechanism with zero extra traffic:

```
1. A router finds its output buffer nearly full → marks the ECN bit in the IP header
2. The Receiver sees it → echoes the mark in the returning TCP segment (ACK or normal packet)
3. The Sender sees it → proactively does MD
```

It requires **all routers on the path + both end hosts** to support it; adoption is still dismal.

---

## Part B: TCP Loss Recovery Evolution in Detail

### Starting point: original TCP (how dumb it was)

Suppose CWND = 1000 segments and the 3rd segment is lost:

```
Sender sends:   1 2 [3] 4 5 6 7 ... 1000
Receiver gets:  1 2     4 5 6 7 ... 1000  (4-1000 all dropped!)
Receiver ACKs:  ACK=3, ACK=3, ACK=3 ...  (keeps saying "I'm waiting for 3")
Sender:         after the timeout, retransmits 3, 4, 5, 6, ..., 1000
```

Three core problems:
1. The Receiver threw away 4-1000 — they all actually arrived, but were dropped because they were out of order, forcing the Sender to send them all again
2. The Sender only reacts after a timeout — the timeout is usually several RTTs, during which the ACK clock is broken
3. After the timeout it restarts Slow Start (CWND=1) → performance is halved and has to climb from scratch

---

### Optimisation 1: Receiver buffers a bit more

Out-of-order segments are stored first rather than dropped directly.

```
Sender sends:   1 2 [3] 4 5 6 7
Receiver gets:  1 2     4 5 6 7  (4-7 stored in the buffer)
Receiver ACKs:  ACK=3, ACK=3, ACK=3, ACK=3  (still saying "I'm waiting for 3", but the segments weren't thrown away)
```

This step alone saves the waste of "4-7 needn't be retransmitted". But the Sender doesn't yet know 4-7 have arrived — leading to the next step.

---

### Optimisation 2: Fast Retransmit

**Core insight**: duplicate ACKs aren't noise, they're a signal.

```
ACK=3
ACK=3  ← duplicate #1
ACK=3  ← duplicate #2
ACK=3  ← duplicate #3  ← triggers Fast Retransmit
```

**Rule**: on receiving 3 dup-ACKs → don't wait for the timer → immediately retransmit only the one lost segment.

**Why 3?**

| Number of dup-ACKs | Judgement |
|-------------|------|
| 1 | Possibly just network reordering |
| 2 | Still possibly reordering |
| 3 | Basically certain it's really lost |

**Why retransmit only that one?** Subsequent dup-ACKs are still pouring in, showing that 4, 5, 6, 7 really reached the Receiver, so there's no need to send them all again.

**Benefit**: reaction time shrinks from "timeout (several RTTs)" to "3 dup-ACKs (about 1 RTT)".

---

### Optimisation 3: Fast Recovery

**Problem**: after Fast Retransmit, should we Slow Start?

**Old logic (Tahoe)**: any packet loss → assume severe congestion → cut CWND to 1 → restart with Slow Start.

**Fast Recovery (introduced by Reno)**:

Insight: dup-ACKs keep streaming in = the ACK clock isn't broken = the network is still running = it's not avalanche-level congestion.

Method:
1. MD: `ssthresh = CWND/2`, `CWND = ssthresh` (cut in half but not to zero)
2. Skip Slow Start and go straight into Additive Increase
3. After retransmitting the lost segment, keep sending new data

```
CWND
 │    Tahoe                      Reno
 │   ╱╲                         ╱╲
 │  ╱  ╲___╱╲                  ╱  ╲___╱╲___╱
 │ ╱  (back via Slow Start)    ╱  (continue straight with AI)
 └─────────────────────────────────────────► Time
```

Reno keeps running at high speed after packet loss, performing a notch above Tahoe.

---

### Optimisation 4: NewReno (multiple losses within one RTT)

**Reno's pain point**: two segments lost within one window (seq 3 and seq 7):

```
Sender sends:   1 2 [3] 4 5 6 [7] 8 9 10
Receiver gets:  1 2     4 5 6     8 9 10
```

Fast Retransmit triggers and retransmits 3. After the Receiver gets 3:

```
Receiver ACKs: ACK=7  ← this is called a "partial ACK"
```

Reno sees the ACK jump from 3 to 7, thinks "the problem's solved", and exits Fast Recovery. Then 8, 9, 10 produce another wave of dup-ACKs, triggering another MD — CWND is cut twice and performance collapses.

**NewReno's fix**: recognise partial ACKs (the ACK advanced but hasn't caught up to the highest seq at the time Fast Retransmit was triggered):
- Don't exit Fast Recovery
- Immediately retransmit the next segment suspected lost (seq 7)
- Keep waiting for the next ACK

It can repair multiple losses within one RTT, doing only one MD.

**Limitation**: NewReno is still "guessing" — it repairs one hole per RTT, so losing 5 segments takes 5 RTTs to fill.

---

### Optimisation 5: SACK (Selective ACK) — finally no more guessing

The Receiver tells the Sender directly "exactly which ones I received":

```
Sender sends:   1 2 [3] 4 5 [6] 7 8 [9] 10
Receiver gets:  1 2     4 5     7 8     10

ACK carries:
  ACK number = 3  (I'm still waiting for 3)
  SACK blocks = [4-5], [7-8], [10-10]
```

The Sender understands at a glance: it only needs to fill in 3, 6, 9. All retransmitted precisely within one RTT.

**Key limitation (final exam point)**: the TCP option field is only 40 bytes; one SACK block takes 8 bytes (start + end seq), plus 2 bytes of option header, so at most **4 blocks** fit (in practice often 3, because room must be left for the timestamp option).

**Changes on the Sender side**:
- One timer per unACKed segment (no longer one global timer)
- Precisely judges which were lost and which arrived based on SACK information
- Retransmission decisions are almost algorithmically optimal

**Negotiation**: during the TCP three-way handshake both sides include the SACK-permitted option in the SYN. Mainstream systems (Linux/Windows/macOS/BSD) now enable it by default.

---

### Comparison of five generations of evolution

| Version | Loss detection | Retransmission strategy | Losses repaired per RTT | Main flaw |
|------|---------|---------|------------------|---------|
| Original TCP | Timeout | Retransmit all unACKed | 1 (and must wait for timeout) | Extremely slow, ACK clock broken |
| Tahoe | 3 dup-ACK | Fast Retransmit | 1 | Slow Start after loss, performance collapses |
| Reno | 3 dup-ACK | Fast Retransmit + Fast Recovery | 1 | Multiple losses in a window cause multiple MDs |
| NewReno | 3 dup-ACK + partial ACK | As above + sustained FR | Several (one per RTT) | Still guessing |
| SACK | 3 dup-ACK + SACK block | Precise retransmission | Several (all at once) | Header limited to 4 blocks |

**The core underlying logic**: keeping the ACK clock alive matters more than anything. Timeout = the ACK clock died = must cold start → disaster. The common goal of Fast Retransmit / Fast Recovery / SACK: keep the ACK stream flowing when losses happen.

---

### Points easily confused (final exam mine-clearing)

1. **Fast Retransmit ≠ Fast Recovery**
   - Fast Retransmit = "when to retransmit + what to send" (based on 3 dup-ACKs)
   - Fast Recovery = "how to adjust CWND after retransmitting" (don't return to Slow Start, only MD)
   - Tahoe has Fast Retransmit but not Fast Recovery; Reno has both

2. **The dup-ACK trigger condition is "3 of them", not "the 3rd time"**: it's actually triggered when the 4th ACK with the same seq arrives (the original + 3 dups)

3. **SACK doesn't replace the cumulative ACK**: the ACK number field is still a cumulative ACK, and SACK is an option that additionally tells you which non-contiguous ones were received. For backward compatibility.

---

## Part C: Network Measurement and SNMP (Week 9-2)

### 1. Why measurement and monitoring are needed

The limitations of Speedtest-type tools: they're only end-to-end measurements with too many variables (WiFi interference, distance, weather, number of people sharing, location of the far end...), and can't tell **which segment** of the network has a problem.

What we really want to know:
- Where there's congestion, whether there are errors, whether hardware and software are working
- Whether a change made things better or worse (without before/after you can't verify)
- Whether packets reached the right application, whether routing matches expectations

**Two true stories (showing the value of monitoring):**

1. The performance of a microwave link between two CSIRO campuses gradually degraded; troubleshooting finally found an ant nest built inside the antenna radome — a "bug in the network" in the literal sense.

2. A China–Japan video conference froze once every 60 seconds. It was finally traced to a router in Seattle — to justify purchasing new equipment, an engineer was SNMP-querying it every 60 seconds, and that query itself made the busy router drop 90% of its traffic. **Lesson: monitoring itself must not add a burden to the monitored device (the core motivation for SNMP being lightweight).**

---

### 2. Why existing feedback mechanisms aren't enough

ECN, ICMP and TCP ACKs are all application-level end-to-end measures:
- They only tell you "there's a problem", not which point along the way has the problem
- They don't tell you good news (e.g. "this link is at 30% load with zero errors")
- Because of asymmetric routing, they usually reflect only one direction

Conclusion: you must talk directly to the devices on the path — only they hold the data we need.

**Two administrative boundaries:**
- **Interior (your own administrative domain)**: you have permission, can install an agent on every device, and query freely
- **Exterior (outside the domain)**: no permission; even "knowing a device exists" is itself an information leak

---

### 3. SNMP design goals

- Cover all devices (routers, switches, APs, printers, cameras, servers...)
- **Lightweight** — the agent does no computation, stores no history, has no absolute clock
- Still works when the device is under stress
- Extensible global naming (to cope with vendors' differing parameters)
- Supports both query/response and command/control (by setting variables)
- Security "later" (and it was indeed put off for many years)

---

### 4. The four components of SNMP

| Component | Role | Explanation |
|------|------|------|
| SNMP protocol | The protocol itself | Defines message formats and PDUs |
| **Agent** | **Server (counterintuitive)** | Runs on the monitored device, maintains a lightweight database |
| **Manager** | **Client** | Runs on the NMS, initiates queries |
| **MIB** | Data model | Describes the structure of the agent's database, organised by SMI |

**Proxy agent**: used to bridge devices that don't support SNMP ("mapping" camera data into the SNMP world).

---

### 5. How the agent is kept "light"

Only these primitive data types: counter / gauge / timeticks / string / OID

| Function | Does the agent do it | Who does it |
|------|------------|--------|
| Compute rates | ❌ No | The Manager subtracts and divides itself |
| Store history | ❌ No | The Manager stores it and draws the graphs itself |
| Absolute clock | ❌ None | Only relative time "since boot" |

**TimeTicks = 1/100 second**: a 32-bit integer × 10ms wraps exactly once a year, so even asking once a year won't repeat.

---

### 6. How the protocol operates

- Based on **UDP** (connectionless), using a request ID to match requests and responses
- The Agent listens on **161**, the Manager listens on **162** (to receive traps)

**5 kinds of PDU (v1)**: GetRequest / GetNextRequest / SetRequest / GetResponse / Trap

**6 standard Traps:**

| # | Trap name | Trigger condition | Severity |
|---|----------|---------|--------|
| 1 | linkDown | An interface went down (cable unplugged, port failure) | Warning |
| 2 | linkUp | An interface recovered | Info |
| 3 | **coldStart** | The device **restarted unexpectedly** (automatic recovery after a crash) | Severe |
| 4 | warmStart | The device **restarted as expected** (admin manually rebooted) | Info |
| 5 | authenticationFailure | Someone tried to access the agent but authentication failed | Security warning |
| 6 | **egpNeighbourLoss** | An EGP/BGP neighbour was lost (external routing peer lost) | Severe |

**The coldStart vs warmStart distinction is important:**
- warmStart: you just ssh'd in and typed reboot; after restarting the device sends warmStart — expected, nothing to worry about
- coldStart: you didn't tell it to restart, it restarted by itself, meaning the device crashed — possibly a software bug, power, overheating, or an attack

**Why egpNeighbourLoss is listed separately:** the link itself may still be alive (linkDown didn't trigger), but the BGP neighbour is no longer talking — the whole network may instantly lose contact with the Internet. "Enough to send most network admins into a panic".

**The catch with Traps**: Traps go over UDP, one-way with no acknowledgement; if one's lost, it's lost. Modern practice is usually traps for real-time alerts + periodic polling as a backstop. SNMPv2 introduced InformRequest (a trap with acknowledgement), but v1 has only these 6 traps.

---

### 7. Counter vs Gauge (an important semantic trap)

#### The essential difference

| Dimension | Counter | Gauge |
|------|---------|-------|
| What it measures | Cumulative events (the total that has occurred) | Current state (the amount at this moment) |
| Direction | Only increases | Can increase or decrease |
| Analogy | A car's **odometer** | A car's **fuel gauge** |
| Typical examples | Total packets sent/received on an interface, total bytes, total errors | Memory usage, queue length, CPU temperature |
| On reaching the maximum | **Wraps back to 0** (starts over, without notification) | **Latches at the maximum** (stays there) |
| Size | Counter32 / Counter64 | Gauge32 (there's no Gauge64 in the standard) |

#### The core trap of Counters: Wrap

**The maximum of Counter32 = 2³² - 1 = 4,294,967,295 (about 4.29 billion)**; after reaching the top, the next increment goes straight to 0, without any notification.

```
T=0:    ifInOctets = 4,294,967,290
T=5min: ifInOctets = 1,005
```

What's the difference? Two possibilities:
- **Case A (it wrapped)**: actual traffic = (2³² - 4294967290) + 1005 = 6 + 1005 = **1011 bytes**
- **Case B (wrapped more than a full lap)**: actual traffic ≈ 4.3 GB

The Manager judges based on the interface speed: a 100Mbps interface can do at most ≈ 3.75GB in 5 minutes, so case B is physically impossible, and it's definitely A.

**Why Counter32 isn't enough:** a 10Gbps interface running flat out → wraps every **3.4 seconds**. In 5 minutes it wraps 87 times, making it completely impossible to reconstruct the actual traffic.

SNMPv2 introduced **Counter64** (at a full 10Gbps it takes about 585 years to wrap once), with the corresponding MIB objects:
- `ifInOctets` (IF-MIB, Counter32) → use with caution on gigabit and above
- `ifHCInOctets` (IF-MIB, Counter64, HC = High Capacity) → a must in modern environments

#### The core trap of Gauges: "equal values" don't mean "no change"

```
T=0:    disk_used = 500 GB
T=5min: disk_used = 500 GB
```

Three possibilities:
- Case A: nobody really touched the disk in these 5 minutes
- Case B: 10GB was written and then 10GB deleted within 5 minutes, net change 0
- Case C: multiple writes and deletes, with the net change happening to be 0

The Manager can't distinguish them at all. **A Gauge's "stillness" can't be trusted.**

**Conclusions:**
- Monitoring "current state" (is there enough, is it full) → Gauge ✅
- Counting "how many things have happened cumulatively" → Counter ✅
- Using a Gauge to estimate total writes → ❌

MIB designers often put the two together:
- Current queue length → Gauge (`ifOutQLen`)
- Historical total packets sent → Counter (`ifOutUcastPkts`)

#### Computing rates from Counters (in practice)

```python
t1, c1 = time(), snmp_get('ifInOctets')   # t1=0, c1=1000
sleep(60)
t2, c2 = time(), snmp_get('ifInOctets')   # t2=60, c2=8500

delta = c2 - c1
if delta < 0:
    delta += 2**32  # handle Counter32 wrap (use 2**64 for Counter64)

rate_bps = delta * 8 / (t2 - t1)
```

**Three pitfalls:**
1. The sampling interval can't be too long — Counter32 + high-speed link loses wrap information
2. The sampling interval can't be too short — it burdens the agent (remember the Seattle router story?)
3. `delta < 0` may also be a **device restart**, not necessarily a wrap — check with `sysUpTime`: if the uptime is shorter than at the previous sample, it restarted, so discard that segment of data

---

### 8. The evolution of security

| Version | Year | Key points |
|------|------|--------|
| v1 | 1990 | Uses a "community string" for authentication, a **plaintext password**. public (read-only) / private (read-write) |
| v2c | 1996 | Added GetBulk, manager-to-manager, TCP, 64-bit counters; c stands for community, security still not fixed |
| v3 | 2002 | Rewritten from the v1 branch; supports three layers: integrity / authentication / privacy |

**The three security levels of v3:**

| Level | Explanation |
|------|------|
| noAuthNoPriv | Only matches the username |
| authNoPriv | Message digest authentication (verifies integrity) |
| authPriv | Authentication + encryption (strongest) |

> The lecturer quipped: "The S originally stood for Simple; after v3 it's not simple at all."

**Security tip**: SNMPv1/v2 agents should never be exposed to the outside network — they're easily scanned and are an attack surface.

---

### 9. MIB, ASN.1 and OID

**ASN.1 (1980s, 40 years earlier than XML)**: describes data structures in Type-Length-Value form. Basic types: INTEGER, OCTET STRING, OBJECT IDENTIFIER, etc.

**The OID tree (globally unique, similar to DNS):**

```
.(root) → iso(1) → org(3) → dod(6) → internet(1)
                                          ├── directory(1)
                                          ├── mgmt(2) → mib-2(1) → system(1)
                                          │                       → interfaces(2)
                                          │                       → ip(4)
                                          │                       → tcp(6)
                                          ├── experimental(3)
                                          └── private(4)  ← vendor extensions (printer ink levels and the like)
```

- Most Internet standard objects = `1.3.6.1.2.1.x.y.z`
- Vendor extensions = `1.3.6.1.4.x.y.z`

**MIB object example:**

```
ifNumber OBJECT-TYPE
    SYNTAX  INTEGER
    ACCESS  read-only
    STATUS  mandatory
    ::= { interfaces 1 }
```

That is `1.3.6.1.2.1.2.1`. It makes sense for ifNumber to be read-only — writing a value to it won't actually grow a new network port.

---

### 10. Tables and GetNext

ASN.1 itself has no "table" structure, but one is needed (each interface's IP/status/packet count/error rate...).

Solution: each table cell has its own OID, and rows are expanded by index. The Manager doesn't know how many rows there are, so it uses **GetNext to traverse in lexicographic order**:

```
Get(Interface.1.ipAddress)     → 150.203.1.1
GetNext(Interface.1.ipAddress) → Interface.2.ipAddress
...keep going until the OID jumps out of the current table, then stop
```

**Problem**: too many round-trip packets. v2 introduced **GetBulk**, pulling a whole block at once, but the response can't exceed a single UDP packet (~64KB), otherwise it reports tooBig.

---

### 11. SNMP's situation beyond the wide area network

SNMP is mainly used within your own administrative domain; cross-domain monitoring basically relies on "people" (contracts, asking favours, installing probes).

**Alternative/supplementary schemes:**

| Tool | Explanation |
|------|------|
| Port mirroring | Switch mirror ports for packet capture |
| Physical-layer snooping | Inserting optical/electrical sensors on the cable |
| Looking Glass | Remote router query interfaces published by carriers (BGP queries, ping, traceroute) |
| perfSONAR | A network of probe beacons deployed collaboratively by academia, generating cross-institution "delay/bandwidth/loss matrices" |

---

### 12. Common tools

- **MRTG / Cacti / Nagios**: plot traffic graphs over time
- **Network Weathermap** (PHP, reads MRTG data): plot topology load maps by space
- **Vendor-supplied tools**: draw port status following the rack panel layout

---

## Review Priorities

### Congestion control (must know)

1. **Distinguish the three windows W vs WIN vs CWND**; WIN and CWND are completely unrelated
2. Congestion happens in **router buffers**, not links
3. Why AIMD must be "slow increase, fast decrease"
4. The state transitions Slow Start → AI → MD
5. Fast Retransmit trigger condition = **3 dup-ACKs**
6. Fast Retransmit ≠ Fast Recovery (Tahoe has the former but not the latter; Reno has both)
7. SACK solves the Sender's "guessing" problem; the header holds at most 4 blocks
8. The ECN workflow (IP header marking → Receiver echoes back → Sender MD)
9. The definition of Max-Min Fairness and the 4-flow routing network example (possible calculation question)

### SNMP (must know)

1. The four SNMP components; **the agent is the server, the manager is the client** (counterintuitive)
2. Differences between v1/v2c/v3, especially v3's three security levels
3. 5 kinds of PDU + 6 standard Traps (the cold/warm start distinction, the meaning of egpNeighbourLoss)
4. **The semantic difference between Counter and Gauge**: two equal Counter readings can be trusted, two equal Gauge readings can't
5. Counter32's wrap problem → the reason Counter64 was introduced (at full 10Gbps it wraps every 3.4 seconds)
6. The OID tree structure, being able to read addresses like `1.3.6.1.2.1.x`
7. GetNext for traversing tables, the reason GetBulk was introduced

### SNMP (understanding is enough)

- ASN.1 syntax details (know it exists, know where to look it up)
- Why TimeTicks are 1/100 second (an anecdote, won't be examined)
- perfSONAR, Looking Glass (know what they are and where they're used)
