# Exam-style Questions

---

## **3.1. How is statistical multiplexing different to TDM/FDM/SDM?**

TDM/FDM/SDM all pre-allocate resources:
- **TDM**: each user gets a fixed time slot, whether they have data or not
- **FDM**: each user gets a fixed frequency band, whether they use it or not
- **SDM**: each user gets a physically separate channel (e.g. separate wire)

**Statistical multiplexing** allocates bandwidth on demand — if you have data, you get the channel; if you're idle, someone else uses it. Bandwidth is shared dynamically based on actual traffic patterns.

Key trade-off: TDM/FDM guarantee latency and bandwidth (good for voice); statistical multiplexing wastes nothing when idle but introduces variable latency under congestion (good for bursty data like internet traffic).

---

## **3.2. Why frame-flags instead of just frame-length?**

Frame-length alone has a critical failure mode: **if you lose sync** (e.g. one byte gets corrupted or dropped), you misread the length field, and now every subsequent frame boundary is wrong — you can never recover without restarting the connection.

Frame-flags (sentinel values like `01111110` in HDLC) allow **re-synchronisation** — even after corruption, the receiver can scan the bitstream until it finds the next valid flag and resume from there.

The counter-argument for length fields is simplicity, but they require bit-stuffing/byte-stuffing anyway to handle the case where the flag pattern appears inside the data — so you pay a similar cost regardless.

---

## **3.3. What is the difference between Collision Avoidance and Collision Detection?**

**Collision Detection (CSMA/CD)** — used in wired Ethernet:
- Transmit, and simultaneously listen to the channel
- If you detect a collision while transmitting, stop immediately, send a jam signal, wait a random backoff time, retry
- Requires you to be able to hear your own collision — only works reliably on wired media

**Collision Avoidance (CSMA/CA)** — used in WiFi:
- Try to *prevent* collisions before they happen
- Listen before transmitting (carrier sense), wait for channel to be idle, then add a random backoff *before* transmitting
- Why? Wireless senders cannot reliably detect their own collisions (hidden node problem, half-duplex radio), so detection after the fact is not viable

Core difference: CD reacts *after* a collision occurs; CA tries to prevent one *before* transmitting.

---

## **3.4. Why is 2.4GHz channel spacing a problem but not 5GHz?**

**2.4GHz band**: only 83.5MHz of total spectrum, divided into 14 channels each 22MHz wide with 5MHz spacing. Channels heavily overlap — only channels 1, 6, and 11 are non-overlapping. Every other channel interferes with its neighbours. In a dense environment (apartment building, office), many APs all fight over 3 effective channels.

**5GHz band**: much wider total spectrum (~500MHz+ depending on country), with 20MHz channels and 20MHz spacing — giving **20+ non-overlapping channels**. Far less congestion, far less interference between neighbouring networks.

Additionally, 2.4GHz shares spectrum with Bluetooth, microwave ovens, baby monitors, and other ISM devices — making the interference problem even worse.
