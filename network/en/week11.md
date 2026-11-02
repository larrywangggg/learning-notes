# COMP3310 Week 11: Security Part 3

> This week wraps up the security topic: Onion Routing → WiFi security → DoS/DDoS → nation-level backdoors.

---

## 1. VPN's Privacy Flaw → Onion Routing

**Where VPN isn't good enough**: however good the encryption is, **traffic metadata is still exposed** — who is communicating with whom is plain to see. The tunnel endpoint (corporate edge router) can see the real unwrapped traffic and source/destination addresses. Tunnel-mode VPN is the same, just "which two devices are communicating" is obvious.

**Core idea of Onion Routing**: since one layer of encryption isn't enough, **wrap encryption layer upon layer**.

- Origin: not created by open-source freedom fighters, but by the **US Naval Research Labs**, later handed to DARPA (and patented); after the original concept was published it evolved into TOR / the dark web
- The client **randomly picks 3 nodes**: Guard (first hop), Middle (responsible for randomisation/hiding), Exit (delivers the traffic to the server)

### Setup process: negotiating session keys hop by hop (an exam scoring point)

> ⚠️ The slides say "collect public keys of 3 nodes", but in reality it's **built hop by hop (telescoping)**, not getting three public keys in one go. This detail is a scoring point when answering exam questions.

```
1. The client connects to Guard, uses its public key to negotiate the Guard session key (K_guard)
2. Through the Guard tunnel, connect to Middle, negotiate the Middle session key (K_middle)
3. Through the Guard+Middle tunnel, connect to Exit, negotiate the Exit session key (K_exit)

When sending: three layers of encryption with K_exit + K_middle + K_guard (plus the application layer's own encryption)

Guard  → only knows the source, not the destination
Exit   → only knows the destination, not the source
Middle → only knows Guard and Exit
No one sniffing along the way can reconstruct "who is communicating with whom"
```

### Additional mechanisms

- **9 Directories of Nodes**: federated, exchanging signed verification information every hour — similar to the P2P bootstrap problem
- A circuit is **only used for 10 minutes** before being rebuilt automatically, shortening the sniffing window
- Resilient to evil nodes: the layered encryption means nodes can only see fragments
- The directory is a web service and can be blocked by national firewalls → bypass with **bridge/relay nodes** (not in the directory, must be obtained privately)

### Known weaknesses

| Weakness | Explanation |
|------|------|
| **Exit node can see the destination** | You still need application-layer encryption; compromising the exit node is an attack surface |
| **Timing analysis** | Simultaneously observing the client's outbound traffic and the target server's inbound traffic, if the timing lines up you can establish evidence of communication. **Layered encryption can't prevent this** |
| **Mitigation** | Garlic routing — bundle multiple messages together to buffer/reroute and scramble the timing, but you can't buffer for too long, so the effect is limited |

### Onion Routing vs MPLS (important comparison)

Onion routing is "like a circuit" but **only pins down 3 nodes**; between the nodes it's still handled by ordinary internet routing (can route around failures), and it only fails when one of the 3 nodes dies.

**MPLS**: sets up the **whole path** in advance, every path-element is pinned down, and if any link dies it fails → far more fragile than onion routing.

---

## 2. Post-VPN: Cloud-based Alternatives

VPNs are complex, burdensome, need configuration changes, aren't optimised, and don't scale. Three outsourced options:

| Option | Explanation |
|------|------|
| **Cloudflare Tunnels** | Uses its global data centres as meeting points, traffic goes over its private network, hiding the communication relationship from the outside — but you have to **trust Cloudflare** |
| **Twingate** | Dynamically generated VPNs, the two ends discover each other and connect via a rendezvous point; fine-grained access control can be layered on top of the VPN (VPN + firewall) |
| **Tailscale** | Mesh-based VPN |

Twingate/Tailscale can run on a NAS or home storage/media centre, giving global access without configuring a VPN on the edge router.

---

## 3. WiFi Security

**Why WiFi needs encryption more than wired**: wired gets physical protection from "you can't touch the cable"; with wireless **anyone can listen**, and every frame is visible to everyone.

### The bootstrap problem and the handshake flow

**Core problem**: the client has to prove to the AP that it knows the PSK, but **can't send it in plaintext** (anyone can hear a broadcast).

**Solution**: each side independently computes the **PTK (Pairwise Transient Key, the session key)** from `MAC addresses + nonce + SSID password`, exchanging only the computed results and nonces, never the password itself.

```
1. The AP broadcasts a nonce (may contain a timestamp)
2. The client computes the session key from MACs + nonces + password,
   replies + MIC (Message Integrity Code, a tamper-proof signature)
3. The AP does the same computation to confirm, and after accepting sends down the GTK (group/broadcast key) etc. + MIC
4. The client replies ACK + MIC
```

### Why there are absurdly many keys

- A unicast session key can't be used for broadcast/multicast (can't send the same content repeatedly) → a separate **GTK** is needed
- The PTK (64 bytes) is split into KCK / KEK / TK / MIC Tx/Rx keys; the GTK (32 bytes) is split into several more; above them there's also the PMK (≈PSK), GMK, MSK
- These temporal keys are **continuously and dynamically recomputed**, not done once on connecting

### Enterprise authentication — 802.1X

- Uses **EAP** (Extensible Authentication Protocol), can run over 802.11 and 802.3
- The backend is usually **RADIUS**; each client uses its own credentials (e.g. student number + password), **no shared PSK**
- The AP only does pass-through, handing authentication to the backend server

### Evolution of WiFi encryption (key scoring points)

| Stage | Key points | How it was broken |
|------|--------|---------|
| **WEP** | Single key, fixed RC4 | A few minutes of sniffing is enough to compute the key. **Don't use it** |
| **WPA** | PSK = "personal" / 802.1X = "enterprise"; TKIP (per-frame key); later improved to **CCMP** (Counter Mode CBC-MAC Protocol) | Mainly broken via handshake flaws in **WPS** (the "one-click join" button) |
| **WPA2** (~2010) | Stronger encryption and protection | **KRACK** (Key Reinstallation Attack, via ACK) and **KR00K** (via null/disassociation frames) |
| **WPA3** (2018) | Stronger key agreement (SAE) | Broken by **Dragonblood** within ~1.5 years: needs huge computing power, but usable if you have money and resources |

> **Golden rule of encryption**: there must never be predictable plaintext content. The null frames of disassociation and the predictable weather reports in WWII Enigma are counterexamples — predictable plaintext + ciphertext → reverse-derive the key.

### What WiFi still can't defend against

- **No protocol can verify an AP's identity**: you can't ask an AP "are you entitled to broadcast 'ANU-Secure'?". An attacker starts a fake AP on a phone with the same SSID, and if you're not careful you connect to it
- Once on the path they can snoop on/tamper with encrypted traffic, do **SSL stripping** (unless **HSTS** enforces high-grade SSL), and **protocol downgrade attacks** (negotiating WPA3 down to WPA1 during the SSL handshake)

---

## 4. Denial of Service (DoS)

**Essence**: doesn't care what you transmit, **just wants to make you unavailable** — through **resource exhaustion** (bandwidth / router CPU & memory / server CPU & memory & disk). **Encryption can't save you here**.

### DDoS scale

- Single-machine attacks are easy to trace/block → use a **botnet**: hacked IoT devices (cameras, baby monitors, NVRs…) are far more numerous and more useful than PCs
- Akamai records **~10 million** gigabit-scale attacks per year (about 1000 per hour)
- **2016 the first 1 Tb/s attack**: 100,000+ wireless cameras (Canon default admin URL + nobody changed default passwords, firmware was modified)
- **Tb-scale attacks frequent since 2017**
- **2018.02.28 GitHub attack**: peak **1.35 Tb/s** (normally <100 Gb/s). Note the X axis is in **minutes** — paid IDS/IPS appliances detected it automatically within seconds, coordinated dozens of upstream routers to **black-hole** (discard) the traffic, and it was largely quelled in ~10 minutes. The attack packets had similar patterns, so firewall rules matched easily

### Main attack vectors

| Vector | Explanation |
|------|------|
| **UDP flood** | UDP doesn't politely slow down like TCP, it just blasts away regardless (IoT cameras using RTSP are an example) |
| **Ping of Death** | Fragmented ICMP with modified headers, >64 KB after reassembly → memory overflow, directly crashing the host/NIC |
| **SYN flood** | Send SYN, receive SYN/ACK, then **don't reply with ACK**; the server keeps state for each pending connection → resource exhaustion. Mitigation: **SYN cookies** (only create state after receiving the ACK) |

### Amplification attacks (small request, large response)

Two dimensions of amplification:

| Dimension | Example |
|------|------|
| **Host multiplier** | Botnet: many devices sending together |
| **Packet multiplier + spoofing** | SMURF: ping a broadcast address with the source address forged as the target → the whole network's replies smash into the target |
| | DNS: 32-byte request → several MB response (e.g. requesting a zone file) |
| | HTTP/FTP/NFS: 1 request pulls a 10 GB file |
| | **Memcache**: a database accelerator that should only run over UDP on internal networks, yet thousands were exposed on the public Internet with a bug → reflecting the whole database, extremely strong amplification |

### Spoofing and Ingress Filtering

**Spoofing** = forging the source IP, so other machines do the work for you and it's extremely hard to trace.

**Ingress filtering (the root fix)**: the ISP checks source IPs at its internet boundary — if an IP should come from the left interface but comes in from the right, it's forged, drop it. **Only that ISP itself can do it**.

**Why it's generally not enabled**:
- Extra cost/work
- **Only protects others, not its own customers** — a classic case where the cost-benefit doesn't add up

> DoS mitigation is **financially worthwhile** for ISPs (so they're willing to do it), while ingress filtering **isn't worthwhile** (so they don't) — the two motivations are exactly opposite. This is why the lecturer wants you to "stay cynical about the ISP industry".

### Mitigations

- **CDN**: don't be a single target, spread out the traffic
- **Edge router / attack detection**: efficient packet dropping, filtering by country
- **Upstream provider support**: route changes, dedicated DDoS handling systems (like the one GitHub used)
- **Deploy ingress filtering everywhere** (and while you're at it, change the default passwords on those cameras)

---

## 5. Nation-level Backdoors (Tinfoil Hat vs Black Hat)

"Good encryption = bad national security?" Methods that NSA and other three-letter agencies have been accused of:

| Method | Explanation |
|------|------|
| Modifying OS/VPN code | E.g. OpenVPN being "infiltrated" — a piece of code lets sending a specific bit pattern drastically reduce encryption strength |
| Modifying encryption algorithms | Making random number generators "not so random" (predictable RNG → smaller key space → brute-forceable) |
| Precomputing keys | Limited key space + enough storage (ANU supercomputer 20 PB, national research network 100 PB) → turn all public/private key pairs into lookup tables, then brute-force look up |
| Attacking firmware/motherboards | Adding suspicious tiny chips to router boards, disguised as resistors |
| **Harvest-then-decrypt** | If it can't be decrypted today, store it first and decrypt it in 10 years when computing power is sufficient — who can afford to store it? Governments can |

**The IPv6 and IPSec dilemma**: IPv6 originally wanted to **mandate IPSec** (full encryption + global PKI), but one of IPv6's big motivations was precisely supporting huge numbers of **ultra-low-power IoT devices**, which **can't run IPSec** → it had to be made **voluntary**. This is the reality of "half-fixed".

---

## Review Focus

**Must know:**

1. **Onion Routing hop-by-hop circuit building (telescoping)**: not getting 3 public keys at once, but negotiating session keys hop by hop; each node only knows the adjacent addresses
2. **Why layered encryption can't defend against timing analysis**: traffic timing can be correlated by external observers
3. **WiFi handshake**: how the PTK is derived from MAC + nonce + password, avoiding transmitting the password in plaintext
4. **How WPA/WPA2/WPA3 were broken**: WPS flaws, KRACK, KR00K, Dragonblood
5. **Golden rule of encryption**: predictable plaintext + ciphertext → reverse-derive the key (the lesson of Enigma)
6. **WiFi AP identity can't be verified**: anyone can forge an SSID, protocol downgrade attacks
7. **SYN flood and SYN cookies** mitigation mechanism
8. **Two dimensions of amplification attacks**: host multiplier (botnet) + packet multiplier (DNS/Memcache etc.)
9. **Why ingress filtering isn't deployed at scale**: a cost-benefit problem — it only protects others, not its own customers
10. **Harvest-then-decrypt**: store ciphertext first, decrypt when computing power suffices; this is a real method of nation-level actors

**Understanding is enough:**

- Limitations of garlic routing in scrambling timing
- The division of roles among 802.1X / EAP / RADIUS (the AP is only pass-through)
- Why the PTK is split into multiple keys (unicast vs broadcast/multicast need different keys)
- Why IPv6's mandatory IPSec → was made voluntary (IoT devices can't run it)
- The differences between Cloudflare Tunnels / Twingate / Tailscale (just know each one's trust assumptions)
