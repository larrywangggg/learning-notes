# Network Week 3 Notes

**This week's thread:** Space Wireless → LAN concepts and design philosophy → Media Access Control (MAC) → Ethernet → Wi-Fi

---

## 1. Satellite Communication (Space Wireless)

### 1.1 The evolution of satellite communication

| Stage | Description |
|------|------|
| Early (passive reflection) | The satellite is like a "giant mirror in the sky"; electromagnetic waves from the ground hit it and reflect back to another place, with no complex electronics needed |
| Modern (active relaying) | The satellite receives the upstream signal (Uplink), amplifies/processes/frequency-converts it on board, then sends it back to the ground (Downlink) |
| Inter-satellite links | Satellites communicate directly (laser links), reducing dependence on ground stations and enabling transoceanic routing |

Communication modes:
- **Satellite-to/from-ground:** ground station ↔ satellite ↔ ground station
- **Satellite-to-satellite:** inter-satellite relaying, no need to return to the ground at every hop
- **Mixed-mode:** ground links and satellite links used together

### 1.2 Comparison of orbit types

| Orbit | Altitude | Orbital period | Delay (RTT) | Characteristics |
|------|------|----------|------------|------|
| LEO (low Earth orbit) | ~400–1,200 km | ~90 min | ~20–40 ms | Low delay, but satellites move fast, need tracking, and many are needed |
| MEO (medium Earth orbit) | 2,000–20,000 km | ~2–12 h | Medium | Commonly used by GPS |
| GEO (geosynchronous orbit) | 36,000 km | 24 h | ~250 ms | "Fixed" as seen from the ground, large coverage, but high delay |

**GEO delay analysis:** about 36,000 km one way; the signal travels at about the speed of light, about 120 ms one way and about 250 ms round trip. Acceptable for video, but a poor experience for real-time interaction (games, video calls).

**LEO advantage:** short distance, low delay (Starlink about 20–40 ms RTT); light in vacuum is about 50% faster than in fibre, so on some very long paths (e.g. New York → Tokyo) inter-satellite links may be faster than submarine cables.

> **Example (Starlink engineering details):**
> - **Phased Array antenna:** the user antenna doesn't need to rotate mechanically; it "steers virtually" by electronic means, tracking overhead satellites in real time
> - **Inter-satellite laser links:** satellites communicate directly without relaying through a ground station each time, supporting transoceanic transmission
> - **Direct-to-Cell:** a new generation of service lets ordinary phones send and receive texts directly via satellite, gradually extending to voice

### 1.3 When satellites are needed

| Scenario | Reason |
|------|------|
| Remote/rural areas | Laying ground infrastructure is too costly or infeasible |
| Maritime/aviation | The target is constantly moving, beyond ground base station coverage |
| Disaster/emergency | The ground network is damaged; satellite serves as an emergency recovery channel |
| Temporary deployment | Construction sites/field/military scenarios that need quick activation |
| Global coverage services | GPS, weather observation, remote sensing imaging, global broadcasting |
| Very long distance low delay | LEO inter-satellite links may beat submarine cables on certain paths |

**When satellites aren't suitable:**
- Dense urban areas (fibre/4G/5G already exist, lower cost)
- Extremely sensitive to ultra-low delay and a ground network can be built locally
- High capacity needed with long-term stability (ground networks are better in capacity/cost)

Satellites are usually a **supplement** to ground networks, not a replacement.

---

## 2. LAN (Local Area Network)

### 2.1 Understanding LANs correctly

The traditional classification by distance (LAN/MAN/WAN) is too arbitrary; what really matters are two concepts:

**Administrative Domain:**
- All devices in the LAN follow the same set of media, encoding, modulation and hardware standards
- Controlled uniformly by the same organisation/administrator
- Not "small range", but "a network owned by the same owner with uniform rules"

**Broadcast Domain:**
- A broadcast frame sent by any device in the domain can be received by all other devices in the domain
- Analogy: shout something in a classroom and everyone hears it; the target person responds and everyone else ignores it

> The LAN is the **starting point** of a device's access to the network: whatever Internet service you access, the data first leaves from the local LAN.

### 2.2 The historical evolution of LANs

1. **Point-to-point:** originally a separate wire between two devices, simple but unscalable
2. **Shared medium / Bus topology:** all devices attach to the same common bus, the signal is "seen" by everyone, suitable for sharing among many devices
3. **Switched Ethernet:** the modern mainstream, with a switch forwarding in the middle; each link becomes point-to-point

### 2.3 LAN design philosophy

**Core principle: simple, fast, leave complexity to the upper layers.**

| Design choice | Reason |
|----------|------|
| No guaranteed delivery | The lower layer sends with best effort; reliability is handled by upper layers such as TCP |
| No built-in complex error correction | Errors usually just cause packet drops, retransmitted by upper layers; but CRC does basic error detection |
| Not optimised for specific scenarios (real-time/bulk transfer/security) | The LAN is general-purpose infrastructure, not customised for a single use |
| Focus on Performance first | High rate, low delay and high throughput are the core goals of a LAN |

**A LAN is a hardware-dominated system**; hardware tends toward simplicity, stability and scalability rather than complex logical decisions.

---

## 3. Frames

### 3.1 Why Frames are needed

A LAN doesn't transmit bits arbitrarily; it organises bits into **Frames**, and each frame must state:

| Field | Purpose |
|------|------|
| Destination | Where it's going (destination MAC address) |
| Source | Where it's from (source MAC address) |
| Boundary markers | Where the frame starts and ends |
| Length | How long the frame is |
| Payload | The actual data |
| Checksum (CRC) | Basic error detection |

**Limits on frame length:**
- **Can't be infinitely long:** it would monopolise the link, consume receive buffers, and accumulate errors
- **Can't be infinitely short:** header/trailer overhead would be too large a share, low efficiency; for CSMA/CD, frames that are too short can't cover the time needed for collision detection

### 3.2 Byte Stuffing / Escape

If the frame boundary symbol (flag) appears in the payload, the receiver will wrongly conclude the frame has ended. The solution is **escaping**:

```
Original data: ... FLAG ...
When sending:  ... ESC FLAG ...   ← escaped with ESC
Receiver:      on seeing ESC, treat the next byte as data, not a boundary
```

This idea appears repeatedly in many protocols (e.g. PPP, HDLC).

### 3.3 Ethernet Frame structure

```
| Preamble | SFD | Dest MAC | Src MAC | [802.1Q Tag] | Type/Length | Payload | FCS |
|  7 bytes |1byte|  6 bytes | 6 bytes |   4 bytes    |   2 bytes   | 46-1500B|4byte|
```

- **Preamble:** a 7-byte `10101010...` sequence used to wake the receiver and lock onto the clock and rate (like "striking a gong" to get the receiver ready)
- **SFD (Start of Frame Delimiter):** 1 byte, marks the start of the frame data
- **802.1Q Tag:** optional, used for VLAN tagging (4 bytes)
- **Type/Length:** identifies the upper-layer protocol type (e.g. 0x0800 = IPv4) or the frame length
- **FCS (Frame Check Sequence):** CRC-32 check, detects transmission errors

---

## 4. MAC (Media Access Control)

### 4.1 The two meanings of MAC

1. **MAC Address:** the hardware identity of a network interface, 48 bits, globally unique
   - It identifies a **network interface**, not the whole computer
   - Format: `AA:BB:CC:DD:EE:FF`; the first 24 bits are the vendor OUI
   - Broadcast address: `FF:FF:FF:FF:FF:FF`

2. **Media Access Control:** the rules for how multiple devices share the same medium fairly

### 4.2 Why a MAC protocol is needed

Comparison of multiplexing strategies:

| Method | Principle | Problem |
|------|------|------|
| TDM (time division) | Fixed time slots in turn | Bandwidth wasted when idle |
| FDM (frequency division) | Fixed frequency band allocation | Low spectrum utilisation |
| SDM (space division) | Physical isolation | High cost |
| **Statistical Multiplexing** | Send when needed, paired with access control | Collisions must be resolved |

LANs use **Statistical Multiplexing**: no fixed allocation in advance; whoever has data sends, but there must be a mechanism to prevent chaos.

---

## 5. Random Access Protocols

### 5.1 ALOHA

**Principle:** send whenever you want, then wait for an ACK; if no ACK is received, assume a collision occurred, wait a random time, and retransmit.

**Reason for the random wait:** if two devices retransmit at the same time, they'll collide again; a random wait staggers them.

| Pros | Cons |
|------|------|
| Extremely simple, no central scheduling needed | High collision rate under high load |
| Suitable for low load/occasional transmission | Throughput drops sharply when the network is busy |
| Decentralised, easy to scale | Maximum channel utilisation about 18% (pure ALOHA) |

**Slotted ALOHA:** time is divided into equal-length slots, and all devices can only send at the start of a slot; the collision probability is halved and the maximum utilisation is about 37%.

> **Example:** In the early days the University of Hawaii used a radio network to connect the islands, and ALOHA is named after this (1970s). Modern low-power IoT sensor networks (such as LoRa's ALOHA-like access) also use similar mechanisms.

### 5.2 CSMA (Carrier Sense Multiple Access)

**Core improvement: listen first, then send.**

```
Before sending → listen whether the channel is idle
  Idle → send the whole frame immediately
  Busy → wait until idle, then try again
```

**Why do collisions still happen? — Propagation Delay**

```
A ─────────────────── B
A starts sending (A hears idle)
B also starts sending (B hears idle, because A's signal hasn't reached B yet)
→ A's and B's signals collide in the middle of the cable
```

Key conclusion: **what you hear is only the state "here, at this moment"; you can't perceive a transmission that has just started at the far end.**

**Bandwidth × Delay Product:**
- Higher bandwidth + larger delay → more data "in flight" in the cable → harder collision management

**Minimum frame length requirement:**
- The sender must detect the collision signal while the frame is being sent
- Worst case: the far end starts sending just as you start; after the collision, the collision signal has to travel back
- Therefore: **minimum frame transmission time ≥ 2 × one-way propagation delay**

> **Example:** On a 100 m Ethernet cable, the signal propagates in about 0.5 μs; the round trip is about 1 μs; at 10 Mbps, 10 bits can be sent in 1 μs, so the frame must be longer than 10 bits; the actual standard is set at 64 bytes (allowing for larger networks).

### 5.3 CSMA/CD (Collision Detection, wired)

Building on CSMA, add **listening while sending**: keep listening during transmission, and as soon as a collision is detected, immediately:
1. Send a **Jam signal** (notifying all nodes that a collision occurred)
2. Stop sending
3. Perform **Binary Exponential Backoff** and then retransmit

**Binary Exponential Backoff:**

| nth collision | Wait window | Random wait range |
|------------|----------|-------------|
| 1 | 0–1 slots | 0 or 1 |
| 2 | 0–3 slots | 0–3 |
| 3 | 0–7 slots | 0–7 |
| n | 0–(2ⁿ−1) slots | Choose one at random |
| After 16 times | — | Give up, report an error |

The backoff window grows exponentially with the number of collisions, spreading out retry times and reducing the probability of another collision.

**Scope of use:** mainly in traditional wired Ethernet (10BASE-T, 100BASE-TX). In switched Ethernet every link is point-to-point and collisions almost never happen, so CSMA/CD has basically fallen out of use.

### 5.4 CSMA/CA (Collision Avoidance, wireless)

A wireless environment can't do Collision Detection (while transmitting, the station's own signal is too strong to simultaneously hear the weak remote signal), so it switches to **avoiding collisions**:

```
Listen whether the channel is idle
  Idle → wait DIFS (Distributed Inter-Frame Space) + a random Backoff time → then send
  Busy → wait until idle, then start the backoff timer
After sending → wait for an ACK
```

**Wi-Fi (802.11) uses CSMA/CA.**

### 5.5 Problems specific to wireless

**Hidden Terminal Problem:**

```
A ──→ B ←── C
A and C can't hear each other, but both can communicate with B
→ A and C send to B at the same time → collision at B
```

**Exposed Terminal Problem:**

```
A ←── B ──→ C ──→ D
B→A and C→D could have happened simultaneously
but B hears C sending, wrongly thinks the channel is busy and waits → bandwidth wasted
```

**Solution: RTS/CTS (the MACA protocol)**

```
1. Sender → RTS (Request to Send) → receiver
2. Receiver → CTS (Clear to Send) → sender (broadcast)
3. Nodes that hear the CTS: stay quiet (even if they didn't hear the RTS)
4. Sender → sends the data
5. Receiver → ACK
```

RTS/CTS lets "hidden nodes" know the channel is occupied by hearing the CTS, thus avoiding collisions. The cost is added handshake overhead, suitable for large frames; for small frames, sending directly is more efficient.

### 5.6 Contention-Free Access

Another class of schemes, as opposed to random access: **taking turns to send**.

| Method | Principle |
|------|------|
| TDM | Fixed slot allocation |
| Token Ring | Only the holder of the token can send; after sending it passes it to the next |

**Pros:** predictable behaviour under high load, no collisions, bounded delay.  
**Cons:** the whole network stops if the token is lost; poor scalability; sensitive to topology changes.

Token Ring is an important historical technology (IBM 802.5 standard), but today it has basically been replaced by Ethernet.

---

## 6. Ethernet

### 6.1 Ethernet's core advantages

- **Cheap, scalable, simple, backward compatible**
- Evolved from a shared bus to switched while keeping the standard stable
- Lighter-weight than carrier-grade technologies (ATM etc.), without emphasis on SLAs

### 6.2 The evolution of Ethernet

| Stage | Medium | MAC mechanism | Notes |
|------|------|----------|------|
| 10BASE-2/5 | Coaxial cable | CSMA/CD | Bus topology, shared by everyone |
| 10BASE-T | Twisted pair + Hub | CSMA/CD | Physically a star but logically still a bus |
| 100BASE-TX | Twisted pair + Switch | CSMA/CD (rarely triggered) | Switches introduced |
| 1000BASE-T+ | Twisted pair/fibre + Switch | Full duplex, almost no collisions | Each link point-to-point |

**Modern Ethernet = Switched + Full Duplex; CSMA/CD is basically no longer needed.**

### 6.3 Auto-Negotiation

When a device connects to a switch it automatically negotiates:
- **Speed:** 10/100/1000/10G Mbps
- **Duplex:** Half / Full
- **Crossover:** automatic MDI/MDI-X detection
- **Power:** PoE (Power over Ethernet)

> **Note:** Auto-negotiation isn't always perfect in reality; one end forced to a fixed rate while the other auto-negotiates may cause a duplex mismatch (one end full duplex, the other half duplex), showing up as lots of collisions and very poor performance. Always check this when troubleshooting.

### 6.4 How a Switch works

The core logic of a switch: **learn MAC addresses, decide forwarding**.

```
Frame enters port X, source MAC = AA:BB:CC
→ the switch records: AA:BB:CC is on port X (MAC Table)

Destination MAC = DD:EE:FF
→ look up the MAC Table: DD:EE:FF known to be on port Y → forward to port Y
→ unknown → Flood to all ports (except the ingress port)

Broadcast frame (FF:FF:FF:FF:FF:FF) → always flooded to all ports
```

The MAC Table has an aging time; an entry is deleted if no frame from that MAC is received for a long time.

### 6.5 STP (Spanning Tree Protocol)

**Problem:** loops between switches → unknown unicast floods or broadcasts are copied endlessly → **Broadcast Storm**

**STP (802.1D) solution:** logically prune the switched network into a loop-free tree.

```
1. Elect the Root Bridge (the one with the smallest Bridge ID, usually lowest priority or smallest MAC)
2. Each non-Root Bridge computes the shortest path to the Root (Root Port)
3. Each link segment elects one Designated Port
4. The remaining ports enter the Blocking state (logically disconnected)
5. Reconverge when the topology changes
```

**Key understanding:** STP doesn't make physical loops disappear; it makes logical forwarding behave as a loop-free tree. Physical redundant links still exist, and backup links are activated after topology changes.

RSTP (802.1w) is the rapid version, reducing convergence time from minutes to seconds.

### 6.6 VLAN (802.1Q)

**Problem:** traffic isolation is needed within the same physical switched network (different departments, different security levels).

**802.1Q VLAN Tag (4 bytes, inserted into the Ethernet frame):**

```
| Dest MAC | Src MAC | 0x8100 | PCP(3b) | DEI(1b) | VID(12b) | Type | Payload | FCS |
                     ← TPID  →←————————— TCI ————————————→
```

- **VID (VLAN ID):** 0–4095, identifies which VLAN the frame belongs to
- **PCP (Priority Code Point):** 3-bit QoS priority
- Up to 4094 independent broadcast domains can be created on the same physical network

> **Example:** In an enterprise network, devices of the finance department (VLAN 10) and the R&D department (VLAN 20) connect to the same switch but can't communicate directly; cross-VLAN access must go through layer-3 routing (Router/L3 Switch).

### 6.7 Link Aggregation (802.1AX/LACP)

Bundle multiple physical links into one logical link:
- Increases bandwidth (multiple 1G → logical 2/4/8G)
- Provides redundancy (if one breaks, traffic automatically switches to the other links)
- LACP (Link Aggregation Control Protocol) negotiates dynamically

### 6.8 Jumbo Frames

| Type | Payload limit |
|------|-------------|
| Standard Ethernet | 1500 bytes |
| Jumbo Frame | About 9000 bytes (9000 MTU) |

**Why Jumbo Frames are needed:**
- At 10 Gbps, a 1500B frame must be processed about every 1.2 μs → extremely high CPU interrupt frequency
- Larger frames → fewer frames → lower CPU overhead → higher effective throughput
- Mainly used in high-traffic scenarios such as storage networks (iSCSI) and data centre interconnects

---

## 7. Wi-Fi (Wireless LAN)

### 7.1 Wi-Fi ≠ wireless Ethernet

Wi-Fi inherits Ethernet **concepts** such as frames, MAC, addresses and broadcast domains, but the wireless environment is far more complex than wired, and the mechanisms differ significantly:

| Comparison | Ethernet | Wi-Fi |
|--------|----------|-------|
| Collision detection | CSMA/CD (listen while sending) | CSMA/CA (avoid collisions) |
| Channel sharing | Devices on the same segment | All devices within the coverage of the same channel |
| Hidden terminals | Don't exist | Exist (need RTS/CTS to solve) |
| Medium | Physical cable, clear boundaries | Electromagnetic waves, range changes dynamically |
| ACK | No link-layer ACK | Every frame is ACKed |

### 7.2 Key Wi-Fi technologies

| Technology | Function |
|------|------|
| CSMA/CA | Basic media access control |
| OFDM (Orthogonal Frequency Division Multiplexing) | Splits the channel into many subcarriers transmitted in parallel, resists multipath interference |
| MIMO (Multiple-Input Multiple-Output) | Multiple antennas send and receive simultaneously, raising throughput and interference resistance |
| DSSS (Direct Sequence Spread Spectrum) | Early 802.11b, interference resistance |
| Rate adaptation | Automatically lowers the modulation order when signal quality is poor (e.g. QAM256 → QAM16) |
| Power control | Dynamically adjusts transmit power to reduce interference |

### 7.3 Comparison of Wi-Fi bands

**2.4 GHz:**
- 20 MHz channel bandwidth, 13 channels in total (varies by region)
- Adjacent channels overlap heavily; there are only 3 non-overlapping channels: **1 / 6 / 11**
- Crowded with devices (phones, Bluetooth, microwave ovens and cordless phones all use this band) → severe interference
- Strong wall penetration, larger coverage

**5 GHz:**
- More channels (about 25 non-overlapping 20 MHz channels)
- Can be combined into 40/80/160 MHz wide channels, greatly increasing capacity
- Relatively few devices, little interference
- Weak wall penetration, smaller coverage

**6 GHz (Wi-Fi 6E/7):**
- A new 1200 MHz band with very many non-overlapping channels
- Almost no legacy interference

**Practical conclusion: use 5 GHz whenever you can; in dense environments prefer 6 GHz.**

### 7.4 Evolution of Wi-Fi standards

| Standard | Name | Max rate | Main technology |
|------|------|----------|----------|
| 802.11b | Wi-Fi 1 | 11 Mbps | DSSS, 2.4 GHz |
| 802.11a | Wi-Fi 2 | 54 Mbps | OFDM, 5 GHz |
| 802.11g | Wi-Fi 3 | 54 Mbps | OFDM, 2.4 GHz |
| 802.11n | Wi-Fi 4 | 600 Mbps | MIMO, 2.4/5 GHz |
| 802.11ac | Wi-Fi 5 | 3.5 Gbps | MU-MIMO, 5 GHz |
| 802.11ax | Wi-Fi 6/6E | 9.6 Gbps | OFDMA, 6 GHz |
| 802.11be | Wi-Fi 7 | 46 Gbps | Multi-Link |

### 7.5 Wi-Fi frame types

Wi-Fi frames are more complex than Ethernet's, with 4 MAC address fields (because frames may be forwarded via an AP, requiring BSSID/SA/DA/TA to be distinguished).

Three classes of frames:

| Type | Examples |
|------|------|
| **Control Frames** | RTS / CTS / ACK |
| **Management Frames** | Beacon / Probe / Authentication / Association |
| **Data Frames** | Actual user data |

### 7.6 The process of a client connecting to an AP

```
1. Scanning
   Active scanning: send a Probe Request → the AP replies with a Probe Response
   Passive scanning: listen for Beacons sent periodically by APs (containing SSID, rates, security info)

2. Authentication
   802.11 Open System Authentication (basic handshake)

3. Association
   The client sends an Association Request → the AP replies with an Association Response
   An AID (Association ID) is assigned and the session established

4. Data transfer
   Get an IP via DHCP → normal communication

5. Roaming
   Signal weakens while moving → the client actively, or the AP, triggers a switch to a stronger AP (Re-association)
```

### 7.7 Wi-Fi security

| Protocol | Status | Problems |
|------|------|------|
| WEP | Deprecated | Flawed RC4 implementation, crackable in minutes |
| WPA | Not recommended | TKIP still has vulnerabilities |
| WPA2 | Current mainstream | CCMP/AES encryption, KRACK vulnerability (2017) |
| WPA3 | Recommended | SAE handshake, stronger forward secrecy |

**An important privacy issue: Probe Requests leak historical SSIDs**

When a device looks for known Wi-Fi, it actively broadcasts Probe Requests containing the list of SSIDs it has connected to before. This means:
- Anyone can listen in on which networks your device has connected to
- Services such as Wigle.net have collected geolocation data for SSIDs worldwide
- Combined with historical SSIDs, one can infer which places a user has been

Modern systems (iOS 14+/Android 10+) have started using randomised MAC addresses and not actively sending Probes to mitigate this.

---

## 8. Summary of Core Knowledge Points

### Comparison of random access protocols

| Protocol | Mechanism | Applicable scenarios | Pros and cons |
|------|------|----------|--------|
| Pure ALOHA | Send any time, random backoff on collision | Low-load wireless | Simple; low utilisation (max ~18%) |
| Slotted ALOHA | Send at slot boundaries, random backoff on collision | Low-load wireless | Improved utilisation (max ~37%) |
| CSMA | Listen before sending | Wired | Fewer collisions; still collides due to propagation delay |
| CSMA/CD | Listen before sending, detect collisions while sending | Wired Ethernet | Detects collisions quickly; unusable for wireless |
| CSMA/CA | Listen, random backoff, then send | Wireless (Wi-Fi) | Avoids collisions; relatively high overhead |

### This week's core exam points

1. The delay/coverage/tracking trade-off of LEO vs GEO
2. When satellites are needed (can't reach / not worthwhile / will break / is moving / needs to be global)
3. The two key LAN concepts: **Administrative Domain** and **Broadcast Domain**
4. LAN design philosophy: simple + high performance, complexity moved up
5. Frame boundaries, and the relationship between minimum frame length and 2× propagation delay
6. The evolutionary logic of ALOHA → CSMA → CSMA/CD / CSMA/CA
7. The **Hidden Terminal** problem and the RTS/CTS solution
8. Ethernet: from shared bus to Switched + Full Duplex
9. **STP** solves layer-2 loops and broadcast storms (logical loop-free tree)
10. Wi-Fi ≠ wireless Ethernet; 2.4 GHz is crowded, 5 GHz is better
11. The privacy issue of Probe Requests leaking historical SSIDs
