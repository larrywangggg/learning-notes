# Interstellar Spacecraft and Deep Space Communication

---

## NASA Deep Space Network (DSN) Signal Analysis

### Uplink transmit power vs. everyday appliances

DSN ground station transmit power comes in several tiers:

- 34-metre aperture antenna: **20 kW** (X band)
- 70-metre large antenna (e.g. DSS-43 Canberra station): **400 kW** (S band)

| Device | Power |
|---|---|
| LED bulb | ~1 W |
| Microwave oven | ~1,000 W (1 kW)|
| DSN 34m antenna | 20,000 W (20 kW)|
| DSN 70m antenna (peak)| 400,000 W (400 kW)|

The strongest DSN transmitter is **400 times** a microwave oven, and **400,000 times** an LED bulb.

But transmit power is only part of it — what's really impressive is the antenna gain. 20 kW focused by the 70-metre dish gives an Effective Isotropic Radiated Power (EIRP) as high as **10¹⁰ W** (10 billion watts), equivalent to compressing the power into a beam as wide as a strand of hair aimed at the target.

---

### How weak is the returning signal?

Taking Voyager 1 (2017) as an example, the downlink signal strength is about **−160 dBm**:

$$-160\ \text{dBm} = 10^{-160/10}\ \text{mW} = 10^{-16}\ \text{W} \approx 0.1\ \text{femtowatts (fW)}$$

Compared with the 20 kW uplink transmission = $2 \times 10^4$ W:

$$\frac{2 \times 10^4}{10^{-16}} = 2 \times 10^{20}$$

**Uplink vs. downlink: a difference of about 20 orders of magnitude.** The signal Earth sends out is a hundred quintillion times stronger than what it receives.

The DSN can fish the signal out of the noise thanks to liquid-helium-cooled maser amplifiers, extremely narrow receive bandwidth and advanced error-correcting codes.

---

### What's the data rate of the most distant spacecraft?

**Voyager 1** (currently the most distant human-made object):

- About **24 billion km** from Earth (~160 AU), one-way signal travel takes about **22 hours**
- For reference: the Moon is 1.3 light-seconds, the Sun 8 light-minutes, Voyager is **1300 times** the Sun's distance
- Downlink data rate: **160 bps** (up to 1.4 kbps when playing back plasma wave data)

What does 160 bps mean?
- Your Wi-Fi is about 100 Mbps, **600,000 times** Voyager
- A 200 KB JPEG would take Voyager about **3 hours** to transmit
- Send a command, and waiting for the response takes **44 hours** (one-way 22h × 2)

---

### Why do different antennas/spacecraft differ so much?

The core reason is that **free-space path loss** grows with the square of distance. Double the distance, and the signal power decays to 1/4.

Mars is about 0.5–2.5 AU, Voyager is at 160 AU — a 100-fold difference in distance, a 10,000-fold difference in power (4 orders of magnitude), which directly determines the upper limit of the usable data rate.

In addition, the DSN supports a single antenna simultaneously receiving signals from up to 4 spacecraft (MSPA capability), so antennas pointing towards Mars on the DSN Now page have multiple clickable options.

---

## Free-Space Path Loss: Why the Square of Distance?

Essentially this isn't a "loss", but the inevitable result of **conservation of energy + geometric spreading**.

### Derivation from first principles

The electromagnetic waves emitted by an antenna propagate outward, with energy evenly distributed over a sphere centred on the emission point with radius $r$:

$$A = 4\pi r^2$$

The total transmit power $P_t$ stays constant (conservation of energy), so the power density per unit area is:

$$S(r) = \frac{P_t}{4\pi r^2}$$

Double the distance → sphere area becomes 4 times → the same energy is spread thinly over 4 times the area → power per unit area becomes **1/4**. This is the whole origin of the inverse square: **in three-dimensional space the area of a sphere is proportional to $r^2$**.

### How much power does the receiver actually get? (Friis formula)

The receiving antenna has a physical aperture $A_r$, and the power it intercepts from a wave field with power density $S$ is:

$$P_r = S \cdot A_r = \frac{P_t}{4\pi r^2} \cdot A_r$$

After replacing aperture area with antenna gain:

$$\frac{P_r}{P_t} = G_t \cdot G_r \cdot \left(\frac{\lambda}{4\pi r}\right)^2$$

The $\left(\frac{\lambda}{4\pi r}\right)^2$ in the brackets is the **free-space path loss factor**, inversely proportional to $r^2$.

### Intuitive analogy

Shining a torch at a wall:
- Shining right up against the wall: small spot, bright
- Step back twice as far: spot area becomes **4 times**, brightness becomes **1/4**
- Step back ten times as far: brightness becomes **1/100**

The total number of photons doesn't decrease, they're just spread over a larger area. Radio waves are exactly the same.

### Why does the DSN use high-gain antennas?

In the Friis formula $G_t$ and $G_r$ are both multipliers. **High-gain antennas "compress" energy into a narrow beam**, equivalent to enlarging the virtual aperture, compensating for the spreading loss brought by $r^2$.

The combination of the DSN 70-metre dish + Voyager's 3.7-metre antenna, with the gains at both ends multiplied, is what makes it possible to receive a 160 bps signal from 24 billion km away — essentially it's a game against $r^2$.
