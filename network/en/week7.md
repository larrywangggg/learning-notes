# COMP3310 Week 7 — IoT/MQTT & P2P/DHT

- **Corresponding slides**: T5d - IoT, T5e - P2P
- **Corresponding recordings**: Mon 20 Apr (IoT & MQTT), Tue 21 Apr (P2P & DHT)
- **Position in the stack**: Application Layer — the last two application-layer topics

---

## Part 1: IoT and MQTT

### 1. Background to choosing a transport protocol

When designing an application you must choose a transport-layer protocol:

- **TCP**: large file transfers, long sessions, reliability needed (e.g. HTTP)
- **UDP**: short messages, low latency, simple request/response (e.g. RTP)

These protocols run fine on "normal-sized" computers, but when devices become extremely small (IoT), everything needs to be reconsidered.

### 2. What IoT (Internet of Things) is

The core idea of IoT: connect any device to the Internet.

**Device scale from large to small:**

- **Large devices**: smart fridges (can scan food, transparent screens), washing machines (completion reminders, energy monitoring), remotely controllable power strips (each socket controlled independently, supports schedules/triggers), colour-changing light bulbs (built-in CPU + WiFi)
- **Medium devices**: Raspberry Pi (a general-purpose computer with an OS, can run multiple programs in parallel), Arduino (single-program microcontroller)
- **Small devices**: ESP32 (with camera, SD card slot, can do AI) — Markus brought physical ones to show in the recording
- **Tiny devices**: chips smaller than a coin that can sit on a fingertip, be scattered across fields (smart dust), or be injected into the bloodstream

> **Recording supplement**: Markus mentioned he brought a variety of devices to show in class. The ESP32-S3 is smaller and more powerful than the old ESP32, and with a daughter board it can become a complete security camera. He personally uses it for a wildlife tracking camera: a passive infrared sensor as the trigger, with the ESP32 handling capture and WiFi mesh transmission.

**The Smart Dust concept**: tiny chips scattered on the ground detect people passing via pressure sensing. Each person's gait is as unique as a fingerprint and can distinguish individuals.

**IoT application scenarios (M2M, large-scale):**

- Predictive maintenance of industrial equipment (detecting anomalies in temperature, pressure, noise)
- Agriculture (from one sensor per farm → one sensor per plant, a few dollars each)
- Water quality monitoring (Tasmanian oyster farm case: a chemical leak from an upstream farm was discovered by tracing back through sensor data)
- Traffic flow, V2V (vehicle-to-vehicle) and V2I (vehicle-to-infrastructure) communication
- Military applications

### 3. The "Phone Home" problem

Almost all IoT devices rely on a "phone home" mechanism:

- The device is behind NAT → needs dynamic DNS → the vendor runs a central server
- Every brand has its own App and proprietary protocol
- Your phone ends up with dozens of Apps to control different devices

**Risk cases (expanded on at length in the recording):**

| Case | Problem |
|------|------|
| Insteon going bust | Servers shut down, users couldn't control their light bulbs and power strips |
| Nike self-lacing shoes | Server outage → couldn't check for firmware updates → shoes "bricked" |
| European luxury car RFID unlock | The showroom was a Faraday cage, couldn't reach the server, couldn't open the car door |
| Ring doorbell cameras | The CEO sold police access to users' camera data |
| Smart baby cot | Hacked: no limit on speaker volume + no limit on the rocking motor |
| Baby monitor | Hacked, strangers talking to other people's babies |
| Pet feeder | During COVID technicians couldn't get into the server room → server outage → pets went unfed |
| Eight Sleep smart bed | Same vulnerability as the baby cot, could remotely fold up the user |
| Car OTA updates | Updates reset all systems including the parking brake, requiring the car to be parked on flat ground |

### 4. Why is IoT "different"?

Five big challenges + one implicit challenge:

1. **Scale**: the number of devices can reach billions. N devices → N² relationships. 1 billion devices × 1 byte/s = 10 Gbps of data
2. **Power**: the smaller the device, the more constrained. Energy harvesting technologies: solar, kinetic, thermal, RF
3. **Networking**: low power = short range + infrequent transmission. Mesh networks, limiting transmission needs
4. **Timeliness**: a nuclear reactor vs the outdoor temperature have completely different needs
5. **Reliability**: add it where needed, stay lightweight. State changes vs continuous reporting
6. **Flexibility**: uses are unpredictable, so arbitrary applications must be supported

### 5. Overview of IoT protocols

| Protocol | Characteristics |
|------|------|
| CoAP | Based on HTTP/UDP, security layer too heavy, rarely used |
| DDS | Based on IP multicast |
| Matter | Emerging smart home standard, runs on top of WiFi/Thread/Zigbee etc. |
| AMQP | Broker-based message queueing |
| MQTT | The focus of this course, a Broker-based PubSub model |

Many protocols use the **PubSub (publish/subscribe)** model rather than traditional Client/Server or Broadcast.

### 6. The PubSub model

Core idea: separate the "publishing" of data from its "consumption".

- **Publishers (sensors etc.)**: just push data to the Broker, without knowing/caring who's listening
- **Broker (intermediary)**: receives data, forwards it to all subscribers, then deletes it as soon as possible
- **Subscribers (consumers)**: register interest with the Broker and wait for pushes

Key point: there's no direct connection between publishers and subscribers. The Broker does all the routing work. Both sides are called "clients" in the MQTT documentation.

### 7. The MQTT protocol in detail

**Basic information:**

- Originally Message-Queueing Telemetry Transport (IBM 1990s)
- No longer queues (mostly), and not limited to telemetry
- v3.1 runs on TCP; v5 (2018) started supporting UDP, Zigbee etc. (MQTT-SN)
- Standardised by OASIS (not the IETF)
- Essentially a key/value database that deletes data as soon as possible

#### 7.1 Topic structure

A Topic is a hierarchical key: `topic/subtopic/sub-sub-topic/...`

Examples:
```
Sensors/Paddock-A/Moisture/Sensor-1 = 93%
Sensors/Paddock-B/Temperature/Sensor-3 = 28C
PizzaPreferences/HouseMate/Malcolm = "vegetarian, but no olives"
```

The Value can be: a number, a string, a file, a JSON object, etc. Topics don't need to be created in advance; just write to them.

#### 7.2 Subscription wildcards

- **`#`** (placed at the end): matches everything at that level and below
  - `Sensors/#` → all data from all sensors
  - `Sensors/Paddock-A/#` → all sensors under Paddock-A
- **`+`**: replaces a single level
  - `Sensors/+/Moisture/+` → all moisture sensors in all locations

> **Recording supplement (student question)**: `+` matches only one level and doesn't reach down into lower sublevels. If there are further sublevels under Sensor-1, `+` won't match them; use `#` in that case. When designing a topic structure, think in advance about how consumers will slice it.

#### 7.3 $SYS/# — Broker system information

- System status information published by the Broker itself, including: version, uptime, number of clients, message statistics, bandwidth statistics, etc.
- The fields aren't standardised (each broker implementation differs), and the update frequency is low (maybe once every 60s)
- Irony: using MQTT to monitor the health of the MQTT broker itself isn't reliable — when the broker has problems, it won't update `$SYS`

#### 7.4 MQTT packet structure

Very compact, bit-oriented:

- **Header**: message type (4 bit), DUP flag, QoS (2 bit), Retain flag
- Variable-length header + variable-length payload
- Only 16 message types

**Main messages:**

- `CONNECT` / `DISCONNECT` (+ ACK)
- `PINGREQ` / `PINGRESP` (application-layer heartbeat, not ICMP)
- `PUBLISH` (used in both directions: source→broker and broker→subscriber)
- `SUBSCRIBE` / `UNSUBSCRIBE` (+ ACK)
- `PUBACK` / `PUBREC` / `PUBREL` / `PUBCOMP` (QoS-related)

#### 7.5 QoS (Quality of Service)

Three levels, with increasing overhead:

**QoS 0 — Fire and Forget**
- Deleted immediately after sending, no acknowledgement
- `Client → PUBLISH → Broker`, done

**QoS 1 — At Least Once**
- Delivery guaranteed, but may be duplicated
- `Client → PUBLISH → Broker → PUBACK → Client`
- If the PUBACK is lost, the Client resends (with the DUP flag)

**QoS 2 — Exactly Once**
- Delivery guaranteed, no duplicates guaranteed, 4-step handshake
- `Client → PUBLISH → Broker → PUBREC → Client → PUBREL → Broker → PUBCOMP → Client`
- `PUBREL` is the signal "you may now distribute this to all subscribers"
- The highest cost: energy, time, storage

**QoS levels can be mixed:**
- The publishing side and subscribing side can use different QoS levels
- E.g.: a sensor publishes at QoS 0 (saves power), and a nuclear reactor control system subscribes at QoS 2 (guaranteed delivery)
- Or: a sensor uses QoS 2 to make sure the broker receives it, and the boss's phone uses QoS 0 to just take a look
- Note: some brokers don't support mixed mode

#### 7.6 Retain (retained messages) — Last Known Good

**Problem**: a door sensor only sends a state change once a day, so a new subscriber joining may have to wait a long time to receive the first message.

**Solution**: set the Retain flag when publishing. The Broker keeps this message, and a new subscriber receives the last retained message as soon as it connects.

- Retained messages are persisted in the broker's file system and survive restarts
- They're not deleted automatically — you must explicitly write an empty value to clear them

> **Recording supplement (student question)**: retained messages are never cleared automatically; to delete one you must actively overwrite it with an empty value. For a door sensor, each state change overwrites the previous retained message, and this kind of scenario generally uses QoS 2 to make sure state changes are written reliably.

#### 7.7 Last Will and Testament

A sensor presets a "will" message when it first connects. When:

- The Broker receives no heartbeat within the KeepAlive period, or
- The TCP connection drops without a proper MQTT `DISCONNECT`

the Broker considers the connection lost and publishes the preset will message to notify all subscribers.

Example will message: `"Service temporarily down; contact x@y.com"`

#### 7.8 Clean Session vs Persistent Session

- **Clean Session (default)**: treated as a brand-new client on connecting; only receives retained messages
- **Persistent Session**: asks the broker to remember all your subscriptions and unreceived messages (QoS 1/2)
  - After reconnecting, the broker pushes all the messages you missed (burst)
  - Very demanding on the broker — it has to store all relevant messages

### 8. MQTT in the smart home

- **Passive monitoring**: all sensors (light level, temperature, humidity, motion, etc.) publish to MQTT → plot trend charts
- **Active control**: controlled devices (lights, heating, curtains, door locks) subscribe to command topics → controllers (physical switches, Apps, voice assistants) publish commands

**Key design**: controllers don't publish directly to the controlled device but relay through the broker, so the software layer can add logic in the middle.

**Rule engines and state machines:**

- **IFTTT / NodeRed**: simple "if X happens, then do Y" triggers
- **Home Assistant / OpenHAB**: full state machines that can combine historical data, weather forecasts, time and other dimensions of information to build complex scenarios

> **Recording supplement**: Markus showed an RF bridge — it connects to WiFi to receive MQTT commands, then controls devices that don't support MQTT, such as a TV, via 433MHz RF signals. MQTT doesn't have to be used end to end; it can be used for protocol bridging.

### 9. IoT security problems

> "The S in IoT stands for Security" (there is no S in IoT)

**Real-world problems:**

- Firmware v1.0 → never updated for ten years
- Default admin username and password never changed
- Standardised admin URLs that can be found by Googling
- Cloud gateways may disappear when the vendor goes bust
- A device gets compromised → becomes a foothold in the home network → lateral attacks

> **Recording supplement**: The Philips light bulb case — after the first bulb connects to WiFi, the second bulb searches for bulbs of the same brand and asks for the WiFi password **in plaintext**. An attacker can pose as a bulb of the same brand to get your home WiFi password.

**MQTT's own security mechanisms:**

- Username/password authentication
- Client Identifier (up to 64KB)
- RBAC (role-based access control)
- X.509 certificates
- Payload signing and integrity checking
- Encrypted connections

### 10. Smart home network protocols

**Short-range protocols:**

| Protocol | Characteristics |
|------|------|
| WiFi | High bandwidth, high power consumption |
| Bluetooth/BLE | Short range, low power |
| Zigbee | Longer range, good wall penetration, tens of kbps |
| Z-Wave | Zigbee competitor, fully proprietary |
| Thread | 802.15.4 + IPv6 mesh, led by Google and others |
| Matter | Upper-layer application protocol running on Thread/WiFi/BLE, an Apple/Google/Amazon/Samsung/IKEA alliance |

**Wide-area IoT networks:**

- **NB-IoT**: cellular networks (offered by Telstra/Optus), very long range
- **LoRaWAN**: ultra-low power, 20km range, ~10 kbps shared bandwidth, transmitters cost tens of Australian dollars
- **SigFox**: a proprietary version of LoRaWAN

---

## Part 2: P2P and DHT

### 1. Problems with the Client/Server model

| Problem | Explanation |
|------|------|
| Centralised | Dependent on a specific service/provider |
| Fragile | Single point of failure, a honeypot for attacks |
| Inefficient | One server to many clients = bottleneck |
| Expensive to scale | Better service = more server nodes |
| Lacks privacy | What you access can be observed along the communication path |

### 2. Ideal properties of P2P

- **Decentralised**: a group of independent, equal nodes cooperating for mutual benefit
- **Robust**: no single point of failure
- **Efficient**: no bottleneck, optimised data transfer
- **Scalable**: large numbers of nodes
- **Self-organising**: plug and play
- **Anonymous**: very hard to achieve

### 3. P2P performance advantages

- **Client/Server**: 1 server → N receivers → time grows linearly with N
- **P2P**: split the file into N parts on N machines → aggregate bandwidth = N × each peer's bandwidth → time barely grows with N (approaches a constant)

**Exploiting asymmetric bandwidth:**

- Typical home broadband ratio 100/20 Mbps (downstream/upstream = 5:1)
- From 1 person you can only get 20 Mbps of upload speed
- But getting 20 Mbps each from 5 people = 100 Mbps, filling the downstream pipe

**The Bootstrap problem**: with Client/Server you know both ends. With P2P, how do you find other peers?

### 4. Napster (1999)

- The first P2P application to "go viral", over 100 million users within 1 year
- Background: MP3 compression + dial-up Internet + CD ripping
- **Architecture**: central index server + peer-to-peer file transfer
  1. The client indexes local music files → uploads to the central server
  2. Searching queries the central index → returns the IPs of machines that have the file
  3. Download the file directly from that machine
- **Pros**: simple, supports flexible searching
- **Fatal flaw**: central server = single point of failure + target for legal attack
- **Historical impact**: shut down by the courts → gave rise to iTunes → Spotify (the shift from buying to renting)

> **Recording supplement**: Napster's legal defence strategy was "we're just an innocent tool that helps criminals", which the lawyers and judges ultimately didn't buy. But it proved there was a huge market for digital music.

### 5. Gnutella (2000)

- The first generation of unstructured/decentralised P2P protocols
- **Architecture**: no central server, queries rely on flooding
  1. Send the query to all neighbours
  2. Neighbours forward it recursively
  3. When found, reply to the originator
- **Pros**: decentralised, highly robust, flexible queries
- **Cons**:
  - Unscalable, queries propagate slowly
  - A TTL is needed to limit how far queries propagate
  - More than half the traffic is query traffic (not file downloads)
  - Easily disrupted by malicious nodes (the music industry joined the network to launch large numbers of fake queries and poisoned content)

### 6. BitTorrent (2001)

Developed by Bram Cohen. Design goals:

1. **Safe fragmentation**: files split into small encrypted chunks, so holding some fragments won't get you held liable
2. **Exploit asymmetric bandwidth**: download from multiple uploaders simultaneously
3. **Fair incentives**: a gamified mechanism (tit-for-tat game); you can only download if you upload
4. **Use TCP efficiently**: lots of parameter tuning

#### 6.1 Core components

- **Tracker**: central directory (original version); tracks only peer identities, holds no file content, and only tells you some of the peers (e.g. 10-20)
- **.torrent file**: static metadata, containing the Tracker address, file information, and the index and SHA-1 hash of every piece
- **Piece**: a 256KB or 512KB file chunk
- **Sub-piece**: 16KB, used for parallel TCP downloading

#### 6.2 Role terminology

- **Swarm**: all participating peers
- **Seeder**: a peer that has the complete file (uploads only)
- **Leecher**: a peer that's downloading (uploads while downloading)

#### 6.3 Network efficiency design

- Downstream/upstream ≈ 4:1 → download from ~4 peers simultaneously
- Pieces are split into 16KB sub-pieces → downloaded in parallel across multiple peers → assembled into complete pieces
- Uses multiple parallel TCP connections to get around the performance bottleneck of a single connection

#### 6.4 The piece selection algorithm (4 phases)

1. **Strict**: once you start downloading a sub-piece of some piece, you must finish that piece first
2. **Rarest First (most important)**:
   - Prefer downloading the rarest piece in the swarm
   - Reasons: reduces seeder pressure, improves robustness (in case the seeder goes offline), speeds up distribution, increases your own value
   - The most common pieces are left until last
3. **Random Start**: when you've just joined you have nothing, so request any piece at random to quickly get something you can share
4. **Endgame**: when only the last one or two pieces remain, request them from all peers to speed up becoming a seeder

#### 6.5 Peer selection and the Choking mechanism

- Connect to the ~10 peers assigned by the tracker
- Actually download from 4 peers at a time (unchoke 4)
- Every **10 seconds** evaluate each peer's upload rate
- Every **30 seconds** "Optimistic Unchoking": randomly pick a choked peer and give it a chance
  - Measure its performance → compare with the current 4 → keep the best 4
  - Gives everyone a fair chance and reduces the impact of free-riders

#### 6.6 The Seeder phase

- After the download completes, enter the pure upload phase
- No longer look at your own download rate, but at the upload rate to other peers
- Goal: help more leechers become seeders as quickly as possible
- Prefer serving peers with good bandwidth → optimises overall distribution efficiency

> **Recording supplement (student question)**: some BT clients support cross-file credit — your contribution in other download tasks can earn you points in the current one. On identity spoofing: the BT ID is a random 160-bit number (pointless to forge), the IP address must be real (otherwise others can't connect to you), and poisoning requires passing every SHA-1 check (very difficult).

### 7. Distributed Hash Table (DHT)

#### 7.1 Motivation

The Tracker is a single point of failure. In 2005 Bram Cohen proposed Trackerless BitTorrent, using a DHT to replace the Tracker.

#### 7.2 Core idea

- Distribute the Tracker database across all peers
- Each peer can be a tracker node
- Nodes form an overlay network used for sharing metadata (not the files themselves)
- Each node only needs to know some of the other nodes

#### 7.3 DHT requirements

- Autonomous, decentralised, fault-tolerant, scalable
- Query resolution uses the fewest messages
- Can cope with churn (nodes frequently joining/leaving)

#### 7.4 Data assignment mechanism

Each piece has a KeyID and each node has a NodeID (the same number space, 160 bits in BT).

**Assignment rule**: a KeyID is assigned to its nearest successor NodeID.

Example (ID space [1, 150], 3 nodes with NodeID = 40, 90, 140):

- KeyID 45 → NodeID 90 (40 < 45 ≤ 90)
- KeyID 111 → NodeID 140 (90 < 111 ≤ 140)
- KeyID 149 → NodeID 40 (wrap around: 140 < 149, beyond the largest node → back to the first)

#### 7.5 Ring topology

Organise the ID space into a ring:

- Nodes are arranged on the ring by NodeID
- Each node is responsible for all KeyIDs between its predecessor and itself
- Initially each node only knows its predecessor and successor

#### 7.6 Query resolution

- **Simple way**: forward hop by hop along the ring → O(N) steps, O(2) neighbours
- **Optimised way**: each node additionally remembers some "shortcut nodes" (usually exponentially spaced) → O(log N) steps, O(log N) neighbours

> **Recording supplement**: with 16 nodes, you can have each node know the nodes 1, 2, 4 and 8 hops away from itself (exponential spacing), so that any query reaches its target in at most log₂(16) = 4 steps.

#### 7.7 Storage redundancy

A Key/Value isn't stored only on the responsible node; it's also replicated to the predecessor and successor nodes, so that data isn't lost if a node goes offline.

#### 7.8 Handling churn

- **A node leaves normally**: notify the predecessor and successor neighbours and hand over the data
- **A node crashes**: detected via ping timeout, and the neighbours take over its data
- **A new node joins**: find a boot peer → compute its own position on the ring → get the data it should be responsible for from its neighbours

#### 7.9 DHT limitations and applications

**Limitations**: supports only exact lookups, not fuzzy/wildcard queries (regular expressions over hashes are meaningless).

**Applications it has been extended to:**

- File systems, databases, naming systems (DNS-like), CDNs
- Communication/messaging systems, event notification
- Application-layer multicast, PubSub frameworks
- Electronic health records

> **Recording supplement**: Markus also mentioned that people have researched two-dimensional and even higher-dimensional DHT topologies (spheres, tori, 5-dimensional hypercubes) to suit particular geographic network distributions (such as clusters in Australia and Japan), but these are hard to draw on slides so only the one-dimensional ring was covered.

---

## Exam Points

> The recording explicitly mentioned: the guest lecture content (Jeff Huston next Tuesday) is also examinable.

- **IoT part**: the focus isn't memorising every protocol name, but understanding the design principles of MQTT — the PubSub model, QoS levels, and the roles of Retain / LWT / Clean Session.
- **P2P part**: the focus is BitTorrent's piece selection algorithm, the choking mechanism, and how a DHT replaces the Tracker.
