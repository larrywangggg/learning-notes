# MQTT Lab Review Notes

> These notes map the hands-on lab phenomena from this week to exam-style questions. Every point has "evidence I verified myself", not rote memorisation.
> Environment: macOS + local broker (`mosquitto -v`) + `mosquitto_pub` / `mosquitto_sub` + Wireshark.

---

## 0. Basics: three programs + the working model

| Program | Role | Behaviour |
|---|---|---|
| `mosquitto` | **broker** (server side) | Listens on port 1883, accepts all connections, stores subscriptions, forwards messages |
| `mosquitto_pub` | Publisher | Connect → send one message → **disconnect immediately** (like a sensor waking up, pushing once, then sleeping) |
| `mosquitto_sub` | Subscriber | Connect → **stays attached** receiving messages until Ctrl-C |

**Core model**: publishers and subscribers **never communicate directly**, everything is relayed through the broker. The same message appearing twice in the capture (pub→broker, broker→sub) is the evidence — this is pub/sub **decoupling**.

Common flags: `-h` host, `-t` topic, `-m` message (pub), `-q` QoS, `-r` retain (pub), `-v` verbose (sub), `-p` port (default 1883).

---

## 1. Why are MQTT packets so compact and simple? (compared with HTTP)

**Because the target scenario is IoT / constrained environments**: low bandwidth, high latency, weak devices, battery-powered. Every byte and every parse is a cost.

Where the compactness comes from:
- The fixed header is a minimum of **2 bytes** (1 byte type+flags, a variable-length remaining length starting at 1 byte). HTTP is a pile of ASCII text headers, easily hundreds of bytes.
- **Binary protocol**, not text, parsing is extremely simple, weak MCUs can handle it.
- **State lives on the connection** (subscriptions and sessions exist on the broker side), unlike HTTP where every request carries full context.

**Capture evidence**: a QoS 0 PUBLISH is only a few dozen bytes; acknowledgement packets (PubAck etc.) are only a few bytes — single bits are used as flags.

---

## 2. Messages are an instant stream, the broker stores no history by default

**Experiment**:
```bash
# Publish first when nobody is subscribed
mosquitto_pub -h localhost -t "3311/larrywang" -m "msg1"
# Only then subscribe
mosquitto_sub -h localhost -t "3311/#" -v
```
**Result: msg1 is not received.**

**Why**: when the broker receives a PUBLISH, it only forwards it to clients "subscribed at this moment", and discards it immediately after forwarding. When msg1 was sent nobody was subscribed, so it evaporated on the spot.

> Corresponding lab wording: "messages are deleted by the broker as soon as possible after publishing."

---

## 3. retain: making a topic's "latest value" visible to future subscribers

**Experiment**:
```bash
mosquitto_pub -h localhost -t "3311/larrywang" -m "msg2" -r   # with -r
mosquitto_sub -h localhost -t "3311/#" -v                      # subscribe only afterwards
```
**Result: msg2 is received.** The only variable is `-r`.

**Mechanism**:
- The broker keeps the **last** retained message for each topic.
- Any **new subscriber**, as soon as it connects, immediately receives this latest value, without waiting for the next publish.
- Resubscribing **receives it again and again** (it sticks around), unlike ordinary messages that self-destruct after reading.

**Overwriting and clearing**:
- Sending another new message with `-r` → **overwrites** the old retained one.
- Sending an **empty message** with `-r`: `mosquitto_pub ... -m "" -r` → **deletes** that topic's retained message.

**When it's useful**: state-type/low-frequency data (switch state, configuration, online status). A device that's just come online needs to know immediately "what the current state is".
**When it shouldn't be used**: high-frequency telemetry streams (temperature sent every second), retaining is pointless and may even mislead.

---

## 4. Wildcards `+` and `#`

Two rules:
- **`+`**: matches **exactly one level** (single-level placeholder). `a/+/c` matches `a/x/c`, doesn't match `a/x/y/c`.
- **`#`**: matches **that level and all levels below**, **can only be placed at the end**. `a/#` matches `a`, `a/x`, `a/x/y`…
  - Key detail: the `#` in `a/#` also counts as matching the `a` node **itself** (this is why in the experiment `larrywang/+/kitchen/#` received `heater/kitchen`, which has only 3 levels).
  - `#` by default **doesn't match** topics starting with `$` (e.g. `$SYS`), to avoid being flooded by broker-internal messages.

**Topic tree used for testing** (deliberately asymmetric levels):
```
larrywang/light/kitchen/ceiling
larrywang/light/kitchen/wall
larrywang/light/bedroom/ceiling
larrywang/heater/kitchen
larrywang/heater/bedroom
```

| Requirement | pattern | Result |
|---|---|---|
| (a) All lights | `larrywang/light/#` | 3 light entries, no heater ✓ |
| (b) All of a type in a room | `larrywang/light/kitchen/+` | The 2 kitchen lights ✓ |
| (c) **All switches in a room regardless of type** | (see the pitfall below) | ⚠️ Can't be expressed robustly |
| (d) Everything I published | `larrywang/#` | All ✓ |

### (c) That pitfall — the essence of the whole exercise
"kitchen" is level 3 in the light subtree and also level 3 in the heater subtree, but the **total depth differs**; with a different design (`room/type`) it would even move to level 2. **MQTT wildcards match strictly by "level position"**; once the same semantic concept appears at non-fixed level depths, **no single pattern can robustly express** "everything in this room". `larrywang/+/kitchen/#` happened to work this time because the tree happened to be shaped just right.

**Design takeaway**: level order is a design decision to think through in advance. If "querying by room" is common, fix room at the same level (`uniid/<room>/<type>/<pos>`), so that `uniid/<room>/#` expresses it cleanly.

---

## 5. Why offer multiple QoS levels? Why can the two sides differ? (physical Wireshark evidence)

**Because different messages have different reliability needs, and reliability has a cost** (extra round trips, acknowledgements, state). It gives applications control to make trade-offs by scenario.

Capture (one message each with `-q 0/1/2`, filter `mqtt && !(mqtt.topic contains "$SYS")`):

| QoS | Handshake packets | Packet count | Guarantee | Cost / use |
|---|---|---|---|---|
| 0 | `Publish` (no id, no acknowledgement) | 1 | at most once | Zero overhead, may be lost. High-frequency telemetry |
| 1 | `Publish(id)` + `PubAck(id)` | 2 | at least once | 1 acknowledgement, may duplicate. Needs idempotency |
| 2 | `Publish` → `PubRec` → `PubRel` → `PubComp` (all with id) | 4 | exactly once | Two round trips, most expensive. Payments/opening gates |

**Key observations**:
- **Packet count rising in steps 1→2→4** = higher reliability, higher overhead.
- **`(id=N)` packet identifier**: QoS 0 doesn't have one; QoS 1/2 always do — it's what ties subsequent acknowledgement packets to the original PUBLISH. The presence or absence of this id is itself the packet-level difference between QoS 0 vs 1/2.

**Why QoS can differ on the two sides of the broker**:
MQTT is **hop-by-hop**, not end-to-end. The broker decouples the two transmission legs:
- First leg: the publisher sends to the broker with some QoS.
- Second leg: the broker distributes according to **the QoS each subscriber declared**.
- Effective QoS = `min(publish QoS, subscribe QoS)` (downgraded to the lower one on distribution).

Example: a sensor publishes at QoS 1; the dashboard subscribes at QoS 0 (doesn't care about loss), the alert system subscribes at QoS 1 (can't lose any) → the same message goes broker→dashboard at 0 and broker→alerts at 1. The publisher needn't know who's downstream or what each wants. This is exactly the value of pub/sub decoupling.

---

## 6. Why can't a DHT handle wildcard/regex/generalised search? (isomorphic to MQTT wildcards)

A DHT locates by **exact hashing**: `lookup(exact_key) → value`. Hashing **destroys the semantic/lexicographic relationship between keys** (`cat` and `cats` land in unrelated places), so:
- Wildcard `cat*`: without knowing the specific key, you can't compute the hash in advance to locate it, and can only scan the whole network (exactly the O(N) that a DHT is meant to avoid).
- Regex/range: hashing destroys locality, ranges are scattered across the hash space, and no node is "responsible for a contiguous semantic interval".

**Connection to this week**: DHT and MQTT wildcards are **the same kind of problem** —
> **Query capability is locked in by how the data is organised.** A DHT organises by hash → only exact lookups; MQTT organises by fixed levels → only wildcards by level position. To support more flexible queries, either change how the data is organised or build a separate index on top. The native mechanism can't do it.

---

## 7. What $SYS is

`$SYS` = **system**. A reserved topic prefix by MQTT convention, which the broker uses to **report its own status** (connection count, load, bytes sent/received, uptime…), published automatically and periodically by the broker; clients can only subscribe, not publish. Starting with `$` means "special, non-business", and the wildcard `#` doesn't match it by default.

```bash
mosquitto_sub -h localhost -t '$SYS/#' -v   # note the single quotes, $ is a shell special character
```
Watching the `$SYS/broker/load/...` series best reflects the current server load.

