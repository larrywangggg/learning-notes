# Network Week 2 Notes

**This week's topic:** Physical Media — Copper → Fibre → Wireless → Last Mile

> Core idea: network performance is ultimately determined by the physical medium. Choosing a medium is a trade-off between **performance / cost / deployment difficulty / maintenance / coverage**.

---

## 1. Copper

### 1.1 Why copper

| Advantage | Explanation |
|------|------|
| Ubiquity | Already laid at large scale all over the world |
| Good conductivity | Transmits electrical signals efficiently |
| Low cost | Simple to process, cheap raw material |
| Soft | Easy to bend for cabling |
| Mature technology | 100+ years of experience |

In theory aluminium, steel, ceramics and even wet string can carry signals — the essence of communication is signal propagation, not "it must be copper".

### 1.2 Physical problems of copper

**(a) Resistive loss (Attenuation / Insertion Loss)**

$$R = \rho \frac{L}{A}$$

The longer and thinner the wire, the greater the resistance and the more the signal attenuates.

**(b) Skin Effect**

High-frequency current flows only on the **surface** of the conductor, so the effective cross-section shrinks and resistance rises. The higher the frequency, the worse the attenuation. This is the root cause of DSL's poor performance in high-frequency bands.

**(c) Antenna Effect**

A straight wire is essentially an antenna:
- It picks up external electromagnetic interference (EMI/RFI)
- It leaks its own signal outward
- It produces **crosstalk** with adjacent wires

So copper problems are often not "the wire is broken" but "the wire is picking up someone else's signal".

### 1.3 Power Line Communication (PLC)

Superimpose data signals on existing power lines:

| Scenario | Speed | Distance |
|------|------|------|
| ISP → home | < 1 Mbps | km scale |
| In-building Powerline Adapter | ~100 Mbps | tens of metres |

> **Example:** Home Powerline Adapters plug into two sockets and use the house's electrical wiring directly as a network cable — extending the signal from the router to another room without extra cabling.

### 1.4 Coaxial Cable

Structure (from inside to outside):
```
Centre conductor (Signal) → Insulation (Dielectric) → Shield → Outer jacket (Jacket)
```

**Pros:** the shield blocks external interference, good signal quality  
**Cons:** each cable has only one signal channel, not suitable for full duplex; relatively expensive

Common types:

| Type | Use |
|------|------|
| RG-58 | Early 10BASE-2 Ethernet |
| RG-6 | Cable TV |
| RG-59 | CCTV surveillance |

### 1.5 Spatial Division Multiplexing

Multiple wires transmit in parallel, each carrying one data stream:
- Pros: enables **Full Duplex** (different wires for sending/receiving), bandwidth adds up
- Cons: the more adjacent wires, the worse the crosstalk

> **Example:** HDMI contains multiple differential data pairs + a clock pair; USB 3.0 has 5 or more pairs of conductors working in parallel.

### 1.6 Differential Signalling

**Core idea:** use two wires to carry the positive/inverted versions of the same signal, and the receiver takes the difference.

```
wire1: +V + noise
wire2: -V + noise
difference: (+V + noise) - (-V + noise) = 2V   ← noise cancels
```

As long as the noise acts on both wires simultaneously, it's automatically cancelled.

### 1.7 Twisted Pair

Noise usually comes from one direction — if the two wires are parallel, the one closer to the noise is affected more.

**Solution:** twist the two wires together (twisting) → the two wires take turns being closer to/further from the noise source, so on average the interference is almost equal → after differential subtraction the noise is almost eliminated.

```
/\/\/\/\/\/\/\/\
```

> **Example:** Each pair in a network cable has a different twist rate (twists per metre), and Cat5e and Cat6 have different twist parameters; this is one reason higher-category cables resist crosstalk better.

**UTP (Unshielded Twisted Pair):** the most common medium in modern networks.

### 1.8 Cable Categories

| Category | Bandwidth | Max rate | Typical application |
|------|------|----------|----------|
| Cat 3 | 16 MHz | 10–100 Mbps | Old telephone/Ethernet |
| Cat 5e | 100 MHz | 1 Gbps | Mainstream home/office |
| Cat 6 | 250 MHz | 10 Gbps (short distance) | Data centres/high performance |
| Cat 6A | 500 MHz | 10 Gbps (100m) | Enterprise networks |
| Cat 7 | 600 MHz | 10 Gbps | Data centres |
| Cat 8 | 2000 MHz | 40 Gbps | Short-distance high-speed interconnect |

**Pattern:** higher category → more bandwidth → higher rate, but more expensive, stiffer cable, and more troublesome installation.

Naming rules for shielded versions:

| Symbol | Meaning |
|------|------|
| U | Unshielded |
| F | Foil |
| S | Braided Shield |

E.g. `S/FTP` = outer braided shield + foil shield on each pair; best performance but most expensive and stiffest.

### 1.9 Propagation delay problems

Electricity propagates in copper at about 2/3 the speed of light. At high transmission speeds:
- Pairs of different lengths → **skew** → the receiver can't correctly reconstruct the signal
- It also causes **propagation delay** and **collision problems**

---

## 2. DSL (Digital Subscriber Line)

### 2.1 Basic concept

DSL = transmitting Internet data over the existing **PSTN (Public Switched Telephone Network)** copper phone lines, without laying new cable.

```
Telephone exchange (Exchange)
       │
       │ Copper (original phone line)
       │
     Your home
```

Standards are set by the **ITU (International Telecommunication Union)**, with standard numbers such as G.992, G.993, etc.

### 2.2 Comparison of DSL types

| Type | Downstream | Upstream | Distance limit | Characteristics |
|------|------|------|----------|------|
| ADSL | 10 Mbps | 1 Mbps | ~4 km | Asymmetric, mainstream for homes |
| ADSL2 | 12 Mbps | 3.5 Mbps | ~4 km | Improved version |
| ADSL2+ | 24 Mbps | 3.5 Mbps | ~3 km | Most common old broadband |
| VDSL | 52 Mbps | 16 Mbps | ~1 km | Fast but short distance |
| VDSL2 | 200 Mbps | 100 Mbps | ~500 m | Needs fibre support (FTTN) |
| G.fast | 1 Gbps | 500 Mbps | ~100 m | Extremely short distance |
| XG.fast | 10 Gbps | — | ~130 m | Experimental |

**Core pattern:** the shorter the copper, the higher the usable frequency band and the faster the rate.

### 2.3 Why Asymmetric

- **Commercial reason:** home users download far more than they upload
- **Technical reason:** the pair going to your home is basically used only by you (upstream), but the bundle entering the exchange is shared by many users (downstream); the exchange transmits with more power, giving downstream the advantage

### 2.4 How DSL works: DMT multi-carrier

DSL uses **DMT (Discrete Multi-Tone)** technology, cutting the spectrum into a large number of small subchannels:

- Each subchannel is about **4.3125 kHz** wide (4 kHz for short)
- Each subchannel uses **QAM** modulation (encoding amplitude + phase simultaneously)
- Each symbol adaptively carries 2–16 bits according to the subchannel's signal-to-noise ratio (SNR)
- All subchannels work in parallel, adding up to the total rate

**Spectrum allocation (ADSL as an example):**
```
|  POTS   |  Upstream  |        Downstream         |
0      4kHz  138kHz               ~1.1 MHz
```

- POTS (Plain Old Telephone Service): 0–4 kHz, traditional voice
- Upstream: 25 kHz–138 kHz
- Downstream: 138 kHz–a few MHz

**Why are subchannels about 4 kHz?**
1. Compatible with the 4 kHz voice bandwidth, convenient for allocation
2. Each subchannel can be adapted individually (lower its speed or turn it off if noisy)
3. Matches FFT/DSP computation, efficient hardware implementation (symbol rate ≈ 4000 sym/s)

> **Example:** The ADSL band is about 1.1 MHz, with subchannels 4.3125 kHz wide → about 256 subcarriers transmitting in parallel. When a subchannel corresponds to an AM radio station's frequency, its SNR is ruined and the modem automatically lowers its speed or turns it off (called a notch).

**Network equipment:**
- Home side: **DSL modem** (digital signal ↔ analogue phone-line signal)
- Exchange side: **DSLAM (DSL Access Multiplexer)**, which aggregates many home DSL lines before connecting to the fibre backbone

### 2.5 Copper frequency limits (Copper Limit)

| Technology | Frequency range | Typical distance |
|------|----------|----------|
| ADSL | ~1 MHz | 4 km |
| ADSL2+ | ~2.2 MHz | 3 km |
| VDSL2 | ~12 MHz | 500 m |
| G.fast | ~100 MHz | 100 m |

**Root cause:** copper is equivalent to a combination of resistance + inductance + capacitance, which naturally forms a low-pass filter:
- Skin effect → resistance increases at high frequency
- Capacitance → high-frequency signals leak
- Inductance → impedance increases at high frequency

Conclusion: the higher the frequency, the worse the attenuation and the shorter the usable distance. This is the fundamental physical bottleneck of DSL performance.

### 2.6 DSL upgrade technologies

| Technology | Function |
|------|------|
| G.inp | Error recovery mechanism, reduces the impact of external noise |
| G.vector | Predicts and cancels crosstalk between multiple copper pairs, raising the rate to ~100 Mbps@500m |
| G.fast | Uses the ~100 MHz band, 1 Gbps, but distance only ~100 m |

---

## 3. Fibre

### 3.1 Advantages of fibre

| Comparison | Copper | Fibre |
|--------|------|------|
| Frequency range | Hundreds of MHz | THz scale |
| Typical bandwidth | Gbps | Tbps |
| EMI resistance | Poor | Completely immune |
| Transmission distance | km scale (DSL) | Tens to thousands of km |
| Attenuation | Relatively high | Extremely low (about 0.2 dB/km) |

### 3.2 How it works: Total Internal Reflection

**Refractive Index:**
$$n = \frac{c}{v}$$

- $c$ = speed of light in vacuum ≈ 300,000 km/s
- $v$ = speed of light in the material

The higher a material's refractive index, the slower light travels in it. When light passes from a high-index material into a low-index one, if the angle of incidence exceeds the **critical angle**, the light is **totally reflected** and no longer refracts out.

**Fibre structure:**
```
Outer jacket (Jacket) — mechanical protection
    Cladding (Cladding, n₂) — low refractive index, reflects light back
        Core (Core, n₁) — high refractive index (n₁ > n₂), the light transmission channel
```

Light undergoes total internal reflection in the core and propagates along the fibre:
```
/\/\/\/\/\/\/\/\/\/\/\
```

### 3.3 Modes and modal distortion

**Each propagation path = one mode.** Multiple paths have different lengths and arrive at different times, causing pulse broadening:

```
Input: │█│  →  Output: │████│
```

This is called **Modal Distortion**, which causes signal overlap and lower rates.

### 3.4 Comparison of fibre types

| Type | Core diameter | Characteristics | Use |
|------|----------|------|------|
| Step-index multimode | 50–100 μm | Multiple paths, severe modal distortion | Short distance (rarely used now) |
| Graded-index multimode | 50–62.5 μm | Graded refractive index, less distortion | Data centres (~300 m–2 km) |
| Single-mode | ~9 μm | Only one path allowed, almost no distortion | Backbone, intercity, undersea (50–100+ km) |

**How Graded-Index works:** the refractive index is high at the centre of the core and low at the edge. Light on curved paths travels faster in the low-index outer region, so the path is longer but also faster, eventually arriving at the same time as the straight path; modal distortion is greatly reduced.

**Why Single-mode is expensive:**
- The core is extremely thin (~9 μm, about 1/10 the diameter of a hair) → needs a laser light source (not LED)
- Splicing requires extremely high precision
- Fibre manufacturing is more complex

### 3.5 Fibre Splicing

**Fusion Splicing:** align the end faces of two fibres, heat and melt them with an electric arc, and weld them together permanently.

- Extremely low joint loss (about 0.02 dB)
- A heat-shrink sleeve is applied for protection afterwards
- Almost indistinguishable from a continuous fibre

**Key distinction:**
- **Splice:** a branching point in the path; the fibre is physically continuous, no plug, no power needed
- **Termination:** a connector installed at the end of the fibre (e.g. at the ONT), pluggable

Junctions need only a splice; not every branching point needs a termination, greatly reducing cost.

### 3.6 Fibre signal attenuation and repeaters

**Natural transmission distance:**
- Multimode fibre (MMF): about 1–2 km
- Single-mode fibre (SMF): about 50–100 km

**Sources of attenuation:** Rayleigh scattering, material absorption, joint loss, bending loss. Fibre has several low-loss "transmission windows"; commonly used wavelengths: 1310 nm and 1550 nm.

**Ways to extend distance:**

| Method | Principle | Pros | Cons |
|------|------|------|------|
| Regenerate / OEO | Light → electrical → decode → re-encode → light | Signal fully restored, no noise accumulation | Expensive, complex, needs power |
| Amplify (EDFA) | Amplify the optical signal directly | Cheap, no optical-electrical conversion | Also amplifies noise |

**EDFA (Erbium Doped Fibre Amplifier):** erbium is doped into the fibre and a pump laser excites the erbium atoms; signal light passing through is amplified directly. One is placed about every 80–100 km.

> **Example:** A trans-Pacific submarine cable (Japan → USA, about 9,000 km) contains about 80–100 optical amplifiers, all on the seabed, basically unmaintained for decades. Australia once ran an experiment: the signal left Melbourne, went around via Sydney and Perth and back to Melbourne, a total of 10,358 km, and could still be transmitted at 100 Gbps.

### 3.7 Where fibre capacity comes from

**WDM (Wavelength Division Multiplexing):** send light of many different wavelengths (colours) simultaneously in the same fibre; each wavelength is an independent data channel.

```
λ₁ (1530nm) ──┐
λ₂ (1534nm) ──┤
λ₃ (1538nm) ──┼──→ single fibre ──→ ...
...           ──┤
λₙ            ──┘
```

- **CWDM (Coarse WDM):** about 8–18 wavelengths
- **DWDM (Dense WDM):** up to 80–160 wavelengths, 100 Gbps per wavelength → **16 Tbps** per fibre

**Other capacity-boosting techniques:**
- Multi-core fibre: one fibre contains 7/19 independent cores
- Pre-distortion compensation: the transmitter distorts the signal in advance so it returns to normal after fibre transmission

**Laboratory records:**
- 2012: 1 Pb/s over 50 km
- 2017: 10.2 Pb/s over 11 km
- 2021: 319 Tb/s over 2,900 km (practical long distance)

Global Internet traffic in 2020 was about 375,000 PB/month ≈ **1.4 Pb/s** — in theory it could fit into a single fibre.

---

## 4. Wireless

### 4.1 Wireless ≠ Wi-Fi

Wireless communication covers the whole electromagnetic spectrum:

| Technology | Frequency | Characteristics |
|------|------|------|
| ELF (Extremely Low Frequency) | 3–30 Hz | Submarine communication |
| AM broadcasting | ~1 MHz | Long distance, poor sound quality |
| FM broadcasting | 88–108 MHz | City coverage, good sound quality |
| TV broadcasting | 100–800 MHz | — |
| Wi-Fi | 2.4/5/6 GHz | Short-range high-speed |
| Millimetre wave (mmWave) | 30–300 GHz | 5G high band |

Free Space Optics is also wireless: the Heliograph (mirror reflections), the Photophone (invented by Bell), laser communication (Gbps scale), LiFi (data via flickering LEDs), infrared remote controls.

### 4.2 Comparison of AM and FM modulation

| Item | AM | FM |
|------|----|----|
| Modulation | Varies Amplitude | Varies Frequency |
| Frequency range | 535 kHz–1,605 kHz | 88 MHz–108 MHz |
| Coverage distance | Very far (ground wave hundreds of km, sky wave up to thousands of km) | Closer (30–100 km) |
| Interference resistance | Poor (noise changes amplitude) | Good (noise doesn't change frequency) |
| Sound quality | Poor (bandwidth about 4–5 kHz) | Good (bandwidth about 15 kHz) |

**Why AM travels far:** it uses medium wave; during the day the ground wave travels hundreds of km; at night it's reflected by the ionosphere (Skywave), reaching thousands of km.

**Relationship with DSL:** the AM broadcast band (0.5–1.7 MHz) overlaps the DSL band. Copper phone lines (hundreds of metres to several km long) act as huge antennas that pick up AM signals, lowering the SNR of the corresponding subchannels and forming spectral "notches".

### 4.3 The core frequency / distance / rate trade-off

| | Low frequency | High frequency |
|--|------|------|
| Propagation distance | Far | Near |
| Wall penetration | Strong (good diffraction) | Poor |
| Data rate | Low | High |
| Antenna size | Large | Small |
| Power consumption | Low | High |

Positioning of different wireless technologies:

| Technology | Rate | Distance | Typical use |
|------|------|------|----------|
| LoRa / SigFox | A few kbps | 10–50 km | IoT sensors |
| Bluetooth | 1–3 Mbps | 10 m | Short-range peripherals |
| ZigBee / Z-Wave | Hundreds of kbps | Tens of m | Smart home |
| Wi-Fi | Hundreds of Mbps–a few Gbps | Tens of m | Indoor access |
| 4G/5G | Tens–hundreds of Mbps | Several km | Mobile access |
| 5G mmWave | Several Gbps | Tens of m | Hotspot areas |

**Core conclusion:** long distance, high rate, low power — you can have at most two at the same time.

### 4.4 Physical factors affecting wireless propagation

- **Absorption:** gases, water vapour, vegetation and building materials absorb signal energy
- **Noise:** interference from other wireless devices
- **Distance:** power falls off with the square of distance ($P \propto 1/d^2$)
- **Reflection / Refraction / Diffraction:** reflection off buildings, diffraction around terrain, refraction by humidity
- **Multipath:** the same signal arrives at the receiver via different paths, and the superposition may cancel out (fading)

**Atmospheric Ducting:** high humidity over the sea makes the refractive index near the surface high and the air above low, forming a fibre-like "waveguide structure"; the signal is trapped between the two layers and can propagate more than 100–500 km. This explains why you can sometimes receive very distant FM stations.

### 4.5 Security implications of wireless as a Shared Medium

Wireless is a **broadcast medium**:
- Once sent, the signal spreads in all directions
- Anyone can listen in, and the sender can't detect it
- Wired networks are limited by physical access; wireless is by default more "exposed" than wired

### 4.6 Antennas

Antenna size is usually of the same order as the wavelength (about λ/4 or λ/2):
- AM broadcasting (λ ≈ 300 m) → broadcast towers tens of metres high
- Wi-Fi (λ ≈ 6 cm) → the antenna fits inside a phone

Directionality: Omnidirectional vs. Directional (e.g. dish antennas)

### 4.7 Link Budget

The core of wireless system design:

$$\text{Received power} = \text{Transmit power} + \text{Antenna gain} - \text{Free-space loss} - \text{Environmental loss}$$

The received power must be above the receiver's Receive Sensitivity to decode reliably.

### 4.8 Cellular networks and Handover

A phone monitors the signal strength of multiple base stations simultaneously and automatically switches to a stronger one while moving (**Handover / Handshake**), keeping the session uninterrupted.

- Different speed scenarios have different requirements (walking vs. high-speed rail)
- Wi-Fi campus roaming follows the same logic

Modern phones integrate multiple wireless systems (about 2–3 sets of RF chips):

| System | Frequency |
|------|------|
| 4G LTE | 800–2200 MHz |
| Wi-Fi | 2.4/5/6 GHz |
| Bluetooth | 2.4 GHz |
| GPS | 1200–1600 MHz |
| FM Radio | About 100 MHz |

### 4.9 Satellite communication

| Type | Orbit altitude | Delay | Characteristics |
|------|----------|------|------|
| GEO (geosynchronous orbit) | 36,000 km | ~250 ms RTT | Wide fixed coverage, high delay |
| MEO (medium Earth orbit) | 2,000–20,000 km | Medium | Commonly used by GPS |
| LEO (low Earth orbit) | 400–1,200 km | ~20–40 ms | Low delay, needs many satellites |

**Key technologies of Starlink (LEO constellation):**
- **Phased Array antenna:** the user terminal doesn't need to rotate mechanically; it steers virtually by electronic means, tracking overhead satellites in real time
- **Inter-satellite Links / Space Lasers:** satellites communicate directly by laser, reducing dependence on ground stations and enabling transoceanic transmission
- **Delay advantage:** light in vacuum is about 50% faster than in fibre, so in some extremely delay-sensitive scenarios going via LEO may be faster than a submarine cable
- **Direct-to-Cell:** the new generation lets phones connect to satellites directly (without an extra antenna), under development

**High-altitude relay layer (drones/balloons):** Google Loon balloons, Facebook solar drones, tethered balloons, acting as "temporary base stations", suitable for temporary coverage of disaster or remote areas.

### 4.10 Spectrum regulation

You can't just pick any frequency to transmit on. Each country has a spectrum management authority (Australia: ACMA) that manages:
- Band allocation (which band for which use)
- Power limits
- Emission/leakage requirements
- Licensing (some bands require a licence, others such as the ISM bands are open)

Wireless design has three layers of constraints: **Physics → Engineering → Regulation**

---

## 5. Last Mile and FTTx

### 5.1 What the Last Mile is

**Last Mile:** the final segment of the access network from the backbone / exchange to the end user (home/office).

**Why the Last Mile is hard:**
- Backbone: few nodes, high-performance fibre can be invested in centrally
- Last Mile: a huge number of endpoints (about 10–11 million in Australia), geographically dispersed, limited revenue per household, high civil works/maintenance/power costs

**The essence isn't "is it technically possible" but "is it worth it at scale, who pays, and how is it maintained".**

### 5.2 The geometric advantage of coverage area

The maximum distance of copper DSL is about 4 km:
- Coverage area = π × 4² ≈ 50 km²

Fibre can easily extend 40+ km:
- Coverage area = π × 40² ≈ 5,000 km²

Fibre makes the service radius of one switching node 10× larger → **coverage area 100× larger** → greatly reducing the number of nodes needed.

### 5.3 Detailed explanation of the FTTx schemes

FTTx = **Fibre To The X**, where X is where the fibre extends to.

---

#### FTTP / FTTH (Fibre to the Premises / Home)

Fibre laid directly to the user's door/indoors.

```
Backbone ──fibre──→ OLT ──fibre──→ Splitter ──fibre──→ ONT ──→ user devices
```

| Metric | Explanation |
|------|------|
| Typical rate | 100 Mbps–10 Gbps (depending on the provider) |
| Copper segment | None (all fibre) |
| Power requirement | The ONT is powered on the user side |
| Maintenance difficulty | Relatively simple (passive middle section) |
| Cost | Highest (construction to each home) |

**Pros:** best performance, most room for upgrades, not limited by copper distance, most future-oriented.  
**Cons:** highest initial construction cost, replacing the entire old copper network is enormously costly, requires in-home installation.

> **Example:** Australia's NBN FTTP upgrade program, standard in new residential estates. An **ONT (Optical Network Terminal)** is installed at the user's end, converting the optical signal into an Ethernet signal for the router.

---

#### FTTN (Fibre to the Node)

Fibre to a street-side "node cabinet" (the green box by the street), then the existing copper to each home.

```
Backbone ──fibre──→ Node (street cabinet) ──copper (hundreds of metres)──→ user's home
```

| Metric | Explanation |
|------|------|
| Copper segment | 100–600 m (much shorter than traditional DSL's 4 km) |
| Typical rate | 25–100 Mbps (depending on copper segment length) |
| Node equipment | Active (needs power, needs maintenance) |
| Cost | Medium (reuses old copper) |

**Pros:** greatly shortens the copper segment (4 km → about 300–500 m), significantly better performance than pure DSL; reuses existing copper infrastructure, fast to build.  
**Cons:** still affected by copper segment length (the further, the slower); the node cabinet is active equipment needing power and regular maintenance; performance ceiling lower than FTTP.

> **Example:** Australia's NBN deployed a lot of FTTN early on, as a compromise between speed and cost. Users still need a DSL modem at home, and the rate varies with the copper distance to the node cabinet; close ones can reach 100 Mbps, distant ones may get only 25 Mbps.

---

#### FTTC (Fibre to the Curb / Kerb)

Fibre extends to the kerb (about 10–100 m from the home), with a small distribution box (DPU) outside each home, leaving only the indoor segment on copper.

```
Backbone ──fibre──→ DPU (kerbside box) ──very short copper──→ user's home
```

| Metric | Explanation |
|------|------|
| Copper segment | About 10–100 m |
| Typical rate | 100–250 Mbps |
| Node equipment | Active (the DPU needs power, usually reverse-powered by the user's modem) |
| Cost | Medium-high |

**Pros:** extremely short copper segment, performance close to FTTP; no need to enter the user's home.  
**Cons:** every home needs a nearby DPU (active equipment); power and responsibility boundaries are complex (usually the user-side modem reverse-powers the DPU over the copper); many components, more tedious maintenance.

> **Example:** Australia's NBN FTTC scheme uses VDSL2 or G.fast over the very short copper segment to reach 100–250 Mbps. Users need to install an NCD (Network Connection Device) that supports Reverse Power Feed.

---

#### FTTB (Fibre to the Building / Basement)

Fibre to the building/basement or wiring closet, with each unit in the building connected via internal copper or Ethernet.

```
Backbone ──fibre──→ building wiring closet ──in-building copper/network cable──→ each user's unit
```

| Metric | Explanation |
|------|------|
| Copper segment | In-building wiring, usually < 100 m |
| Typical rate | 100 Mbps–1 Gbps (VDSL2 or Ethernet inside the building) |
| Applicable scenarios | Apartment blocks, office buildings |
| Cost | Relatively low (fibre only to the building, existing in-building wiring reused) |

**Pros:** suitable for high-density housing (apartment blocks); fibre only needs to reach the building, existing phone lines/Ethernet are reused inside, very low cost.  
**Cons:** ageing in-building copper may affect performance; the building wiring closet needs maintenance; in-building bandwidth is shared.

> **Example:** Australia's NBN FTTB scheme is designed specifically for apartment blocks. Fibre is brought into the basement, then VDSL2 runs over the building's existing phone lines to each unit, typically reaching 100 Mbps. This scheme avoids the huge cost of re-laying fibre inside every apartment block.

---

#### HFC (Hybrid Fibre Coaxial)

Fibre to a neighbourhood/estate node, then coaxial cable (coax) connecting multiple homes. Essentially it reuses existing Cable TV network infrastructure.

```
Backbone ──fibre──→ Optical Node ──coaxial cable──→ dozens of homes (shared)
```

| Metric | Explanation |
|------|------|
| Typical rate | Downstream 100 Mbps–1 Gbps, upstream relatively low |
| Shared structure | One coax segment connects multiple homes, rates drop at peak times |
| Cost | Relatively low (reuses Cable TV infrastructure) |
| Technical standard | DOCSIS (Data Over Cable Service Interface Specification) |

**Pros:** coaxial cable performs better than ordinary copper; extensively reuses the existing Cable TV network, low construction cost; fast deployment.  
**Cons:** **Shared medium** — multiple homes share one coax segment, so rates drop noticeably at peak times (8–10 pm); upstream bandwidth is usually narrow; maintaining old HFC systems is complex.

> **Example:** Australia's NBN HFC scheme is used heavily in areas of Sydney, Melbourne etc. that already have the Foxtel cable TV network. One Optical Node typically serves about 500 homes, distributed via coaxial cable. The DOCSIS 3.1 standard can theoretically reach 10 Gbps downstream, but in practice it's affected by the number of sharing users.

---

#### PON / GPON (Passive Optical Network / Gigabit PON)

An "efficient sharing" scheme for fibre access: a **Passive Splitter** in the optical path distributes the optical signal to multiple homes, with no powered equipment in between.

```
OLT ──single fibre──→ Passive Splitter (1:32/1:64) ──→ each home's ONT
       (central office)                                        (user side)
```

| Component | Full name | Location |
|------|------|------|
| OLT | Optical Line Terminal | Exchange |
| Splitter | Passive Optical Splitter | Kerbside/in building |
| ONT/ONU | Optical Network Terminal/Unit | User's home |

| Technical standard | Typical rate | Split ratio |
|----------|----------|--------|
| GPON | 2.5 Gbps downstream / 1.25 Gbps upstream (shared) | Up to 1:64 |
| XGS-PON | 10 Gbps downstream / 10 Gbps upstream | Up to 1:128 |
| NG-PON2 | 40 Gbps+ | — |

**Core idea:** replace active switching equipment with passive splitters, reducing the intermediate nodes that need power and maintenance, lowering cost.

**How upstream and downstream are separated:** the OLT broadcasts downstream, and each ONT only receives the data belonging to it (distinguished by time slot or wavelength); upstream, the OLT schedules centrally and each ONT sends in its assigned time slot (TDMA), avoiding collisions.

**Pros:** the middle section is completely passive, needs no power, minimal maintenance; high fibre utilisation (multiple homes share one trunk fibre); cost-effective, suitable for large-scale FTTP deployment.  
**Cons:** still a shared structure (multiple homes share the total bandwidth); design and troubleshooting are more complex than point-to-point fibre.

> **Example:** Australia's NBN FTTP scheme uses GPON, with one trunk fibre split to at most 32 homes. Splitters are usually in kerbside distribution boxes, completely passive, needing no power and minimal maintenance. The user-side ONT is provided by NBN, looks like a small router, and once powered you connect a router to get online.

---

### 5.4 Fixed Wireless Access

When laying fibre/copper isn't worthwhile, directional wireless links connect users.

```
Base station (connected to fibre backhaul) ──wireless──→ antenna at the user's home ──→ user's router
```

**Applicable scenarios:** remote/rural areas where population density can't justify the cost of laying fibre but satellite isn't needed.

**Pros:** no digging to every home; fast to bring online; relatively flexible coverage.  
**Cons:** an antenna must be installed on the user's roof/exterior wall; affected by terrain, weather and building obstruction; capacity affected by the number of users per base station; the tower itself needs fibre backhaul.

> **Example:** Australia's NBN Fixed Wireless scheme covers about 3% of the geographic area, mainly suburban and rural. Base stations are usually on hilltops or high ground, and users install a small directional antenna pointed at the base station. Actual rates are about 25–75 Mbps, delay about 15–30 ms.

---

### 5.5 Overall comparison of FTTx schemes

| Scheme | Copper segment | Typical rate | Cost | Applicable scenarios |
|------|--------|----------|------|----------|
| FTTP/FTTH | None | 100 Mbps–10 Gbps | Highest | New areas, long-term investment |
| FTTB | < 100 m (in building) | 100 Mbps–1 Gbps | Low | Apartment blocks, office buildings |
| FTTC | 10–100 m | 100–250 Mbps | Medium-high | Older urban residential areas |
| FTTN | 100–600 m | 25–100 Mbps | Medium | Reusing old copper infrastructure |
| HFC | Coax (shared) | 100 Mbps–1 Gbps | Low | Areas already covered by Cable TV |
| Fixed Wireless | Wireless (a few km) | 25–75 Mbps | Medium | Suburban/rural |
| LEO satellite | None | 50–200 Mbps | High | Extremely remote areas |

**Selection principle:** not choosing the most advanced, but the combination that best balances **cost / performance / existing infrastructure / maintainability**. This is also why Australia's NBN uses a mix of technologies.

---

## 6. Overall Comparison of the Three Media

| | Copper | Fibre | Wireless |
|--|------|------|------|
| Frequency ceiling | ~Hundreds of MHz | THz scale | Depends on band |
| Typical bandwidth | Mbps–Gbps | Tbps | Mbps–Gbps |
| EMI resistance | Poor (antenna effect) | Completely immune | Poor (shared medium) |
| Transmission distance | DSL: < 4 km | SMF: 50–100 km | Depends on frequency |
| Security | Fairly good (wired) | Very good | Poor (broadcast medium) |
| Deployment cost | Low (existing infrastructure) | High (high construction precision) | Medium |
| Maintenance | Oxidation, ageing, crosstalk | Bending, dust, difficult splicing | Strongly affected by environment |
| Suitable for Last Mile | DSL (short-term reuse) | FTTP (long-term investment) | Remote areas |

---

## 7. Core Conclusions

1. **The medium isn't neutral.** Different media actively determine network performance, cost and maintenance.
2. **The core enemies of copper:** resistive loss, skin effect, antenna effect, crosstalk. Differential signalling + twisting are the countermeasures.
3. **The essence of DSL:** QAM + FDM + many subchannels in parallel, rather than single-frequency transmission. Distance is the fundamental limit on performance.
4. **Fibre's power comes from:** the THz band + total internal reflection + multi-wavelength multiplexing (WDM/DWDM).
5. **The essence of wireless:** low frequencies go far but are slow, high frequencies are fast but short-range. Wireless is a shared broadcast medium, insecure by default.
6. **Last Mile design:** not choosing the fastest technology, but the combination that's most cost-effective overall and best fits existing infrastructure. The further fibre is pushed forward, the shorter the remaining copper segment and the higher the rate — this is the core logic of the FTTx family of schemes.
