# Exam-Style Questions — Answers

## **Why can't DHTs handle wildcard/regex/general searches in P2P?**

Because a DHT's lookup mechanism relies on **exact-key hashing**. A key is mapped onto the ring via a hash function (e.g. SHA-1) to a specific node; to retrieve it, you hash the *same exact key* and go straight to that node. The entire efficiency of a DHT depends on knowing the precise key in advance.

The fatal property (for searching) is that hashing **destroys any semantic or lexicographic relationship between keys**. `"cat"` and `"cats"` hash to completely unrelated positions on the ring. Therefore:

- **Wildcards (`cat*`)**: you don't know which concrete keys match, so you can't pre-compute their hashes and can't locate them. The only way would be to enumerate every possible completion or scan the whole network — exactly the O(N) flooding a DHT is designed to avoid.
- **Regex / range queries**: same problem. Hashing destroys locality, so a range like `[a-c]*` is scattered randomly across the hash space. No single node "owns a contiguous range of keys" in any meaningful semantic sense.

In short: a DHT gives you `lookup(exact_key) → value` — it's a distributed *hash table*, not a distributed *index*. Supporting fuzzy search requires building an inverted index or a different structure (e.g. prefix hash trees, order-preserving DHT variants) on top, which is no longer native DHT functionality.

---

## **Why are MQTT packets so compact and simple (compared to HTTP)?**

Because the design goals are completely different. MQTT targets **IoT / constrained environments**: low bandwidth, high latency, unreliable networks, battery-powered weak devices (sensors, microcontrollers). Every byte and every parse operation is a cost.

Sources of the compactness:

- **Fixed header as small as 2 bytes**: 1 byte for packet type + flags, then a variable-length "remaining length" field. Compare that to HTTP's pile of ASCII text headers (`Content-Type:`, `User-Agent:`, `Host:`, …), routinely hundreds of bytes.
- **Binary, not text-based**: no parsing of newlines, no handling of dozens of optional header fields. Parsing logic stays trivial, so a weak MCU can handle it.
- **State lives on the connection, not in every packet**: MQTT uses a long-lived connection, with subscription and session state held at the broker. HTTP (especially stateless) repeats full context (cookies, auth headers, etc.) on every request — huge redundancy.

Fewer bytes = less bandwidth = less power = less CPU. For a sensor expected to run for years on a coin cell, this is a survival issue.

---

## **Why does MQTT offer multiple levels of QoS?**

Because **different messages have wildly different reliability needs, and reliability isn't free** (extra round-trips, acknowledgement packets, state storage). A single fixed reliability level would either waste resources or fail to meet requirements. The three levels:

- **QoS 0 (at most once)**: fire and forget, no acknowledgement. Suited to high-frequency, disposable telemetry — e.g. a temperature reading every second; losing one or two doesn't matter, a fresh value arrives next tick. Zero overhead.
- **QoS 1 (at least once)**: delivery confirmed, but duplicates possible (a lost PUBACK triggers retransmission). Suited to "must not lose, but can tolerate duplicates" — the application handles idempotency.
- **QoS 2 (exactly once)**: a four-way handshake guarantees no loss and no duplication. Suited to critical, non-repeatable commands — e.g. "charge a payment", "open the gate once". Highest cost (two round-trips).

Letting the application choose per scenario gives the user control over the **reliability vs overhead** trade-off — especially important on constrained networks.

---

## **Why is there separate, potentially different QoS on each side of the broker (producer→broker, broker→consumer)?**

Because these are **two independent transfers** — the broker sits in the middle and decouples publishers from subscribers. MQTT isn't an end-to-end protocol; it's hop-by-hop:

- First hop: the publisher pushes a message to the broker at some QoS.
- Second hop: the broker distributes the message at **each subscriber's own QoS, declared when that subscriber subscribed**.

The reliability needs of the two hops can genuinely differ. In practice the **effective delivery QoS is the minimum of the publish QoS and the subscription QoS** (QoS is "downgraded" to the min on delivery).

Example: a sensor publishes at QoS 1. Subscriber A is a dashboard subscribed at QoS 0 (doesn't care about loss); subscriber B is an alarm system subscribed at QoS 1 (must not lose). For the same message, broker→A runs at QoS 0 and broker→B runs at QoS 1. Each consumer gets the reliability it needs and can afford, independently. This is exactly the value of pub/sub decoupling — the publisher needn't know who the downstream subscribers are or what reliability each one requires.

---

## **In what circumstances is it useful for a broker to "retain" an MQTT-published message?**

Retain means the broker stores the **last** message flagged with the retain bit for a given topic, so that any **new subscriber** receives that latest value *immediately* on subscribing, instead of waiting for the next publish.

Useful in **state-type / low-frequency-update** scenarios:

- **Device state**: e.g. a switch state `home/livingroom/light = ON`. Such state might change only once every few hours. Without retain, a newly launched app would have to wait until someone next toggles the light to learn the current state. With retain, it gets the current state the instant it subscribes.
- **Configuration / metadata**: a topic carrying a current threshold, version number, etc., where a new client needs to know "what the current value is" right away.
- **Online status (with Last Will)**: `device/123/status = online`, combined with the Last Will message to display presence/availability.

Counter-example (don't retain): a high-frequency telemetry stream (temperature every second). Retaining it is pointless — a new subscriber gets fresh data next tick anyway, and storing a stale value can even be misleading.

Rule of thumb: retain is valuable when the message represents a **"current state / latest value" rather than a one-off event in a stream**, updates are sparse, and new subscribers need to know the present state immediately.