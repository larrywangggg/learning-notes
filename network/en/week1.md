# Network Week 1 Notes

---

## 1. Overall Course Structure

This course is a complete network architecture course from the physical layer to the application layer, then on to global routing and network operations, in 8 stages:

| Stage | Topic | Content |
|------|------|------|
| 1 | Communication fundamentals | Basic principles of encoding, transmitting and recovering information |
| 2 | Transmission media | How copper, optical fibre and wireless signals work and their characteristics |
| 3 | LANs and layering | Ethernet, WiFi, WAN, OSI/TCP-IP layered models |
| 4 | Internet core protocols | IPv4/IPv6, UDP, TCP (addressing, reliability, congestion control) |
| 5 | Application layer | DHCP, DNS, Web, real-time communication, P2P, IoT |
| 6 | Global interconnection | Routing protocols, cross-network communication |
| 7 | Network problems and security | Congestion, monitoring, security protection |
| 8 | Real-world networks | Actual deployment and engineering practice |

**Overall logic:** Physical layer → Data link layer → Network layer → Transport layer → Application layer → Global routing → Operations and security → Engineering applications

---

## 2. Circuit Switching

### Core idea

First establish a **dedicated path**; during the call, the resources belong exclusively to that connection. Also called **connection-oriented**.

### Setup process

- **Hop-by-hop setup**: every intermediate switch must allocate resources
- Control signals can travel:
  - **in-band**: control signals travel on the same line as the data
  - **out-of-band**: control signals travel on a separate signalling network (e.g. SS7)

> **Example:** Making an intercity phone call, from your home → local exchange → long-distance exchange → the other party's exchange → the other party; every segment is "connected" in advance, and this path won't be used by anyone else for the whole call.

### Advantages

- Guaranteed fixed quality (QoS)
- Dedicated bandwidth, stable delay
- Suitable for voice calls

### Disadvantages

- **Wastes capacity**: the channel stays occupied when idle and can't be given to others
- **High cost to scale**: resources must be explicitly allocated/released, and trunk links easily become congestion points

  > **Example:** 10 phone lines can carry at most 10 calls at once; the 11th person has to wait.

- **Single point of failure**: the network must maintain end-to-end state; if one segment breaks, resources must be released and the whole circuit re-established

### History: the automatic exchange (1888–1892)

Strowger invented the automatic exchange, moving from human operators to mechanical automatic switching.

**Key idea: Smart clients, dumb network**
- The terminal (phone) is responsible for dialling
- The network is only responsible for connecting according to rules

Phone numbers are allocated **hierarchically by geography**, which is scalable — this is where the idea of hierarchical IP address design later came from.

---

## 3. Multiplexing

**Problem**: when the trunk is full, either expand capacity by buying lines, or share the lines more efficiently.  
**Solution**: Multiplexing = multiple signals sharing one physical link.

### Three kinds of multiplexing

| Method | Principle |
|------|------|
| **Space-division multiplexing (SDM)** | Physically different lines |
| **Frequency-division multiplexing (FDM)** | Different signals occupy different frequency bands |
| **Time-division multiplexing (TDM)** | Different signals take turns occupying time slots |

### Analogue TDM

Principle: all input channels **take turns** occupying the output line.

Suppose there are 4 input lines; the system samples them cyclically:
```
Input:  1, 2, 3, 4, 1, 2, 3, 4 ...
Output: 1 2 3 4 1 2 3 4 1 2 3 4 ...
```
Early implementations used a mechanical rotating arm, equivalent to a switch rotating at a fixed rate.

### Circuit switching vs TDM vs packet switching

| Type | How it's used | Efficiency |
|------|----------|------|
| Circuit switching (Circuits) | Exclusive for the whole duration | Low (idle waste) |
| TDM (Cells) | Fixed time slots in turn | Medium |
| Packet switching (Packets) | Send only when there's data, compete on demand | High |

**Logic of the historical evolution:** circuit switching in the telephone era → capacity waste discovered → multiplexing introduced → further developed into packet switching → finally evolved into the Internet

---

## 4. Communication Fundamentals: Signals and Transmission

### The essence of communication

Communication = **expressing information through changes in energy**; whether current, light, sound waves or electromagnetic waves, they all transmit patterns of energy change.

### Problems encountered in transmission

| Phenomenon | Essence |
|------|------|
| Attenuation | Energy weakens with distance |
| Noise | Random energy superimposed on the signal |
| Delay distortion | Different frequencies propagate at different speeds |
| Frequency cut-offs | High- or low-frequency components are filtered out |
| Frequency-specific attenuation | Different frequencies suffer different amounts of loss |

### The simplest encoding: On-Off Keying (OOK)

Use "on/off" to represent "1/0":
```
on = 1, off = 0
Waveform: ▁▔▁▔▁▁▔▔  →  0 1 0 1 0 0 1 1
```

### Why can't speed be increased indefinitely?

**Intuition:** faster = narrower pulses  
**Problems:**
1. The narrower the pulse → the shorter its duration → the less total energy → the more easily it's drowned by noise
2. An ideal square wave needs infinitely many high-frequency components (an infinitely wide spectrum), which is physically impossible

### Nature is Analogue

- There are no truly "vertical edges" in nature
- All signals have a rise time; edges get "smoothed out"
- The knife-edge experiment: light at a sharp edge produces diffraction ripples, because a sharp edge contains infinitely high frequencies, which physical systems can't support

### The relationship between time domain and frequency domain (Fourier transform)

**Narrower pulse ↔ wider spectrum** (the duality between time domain and frequency domain)

> **Example:** A 1 ns pulse has a spectral width on the order of 1 GHz. To transmit on a channel with 1 GHz bandwidth, the signal's time resolution is only about 1 ns.

### Digital vs analogue

| Digital | Analogue |
|------|------|
| Easy to copy, easy to regenerate, highly noise-resistant | Exists naturally, continuous, can't have sharp edges |

Digital signals are man-made constructs, and physical propagation is inevitably an analogue wave, so digital communication must go through **modulation → filtering → regeneration/recovery**.

**Core constraint:** the faster you want to transmit, the wider the spectrum you need; but link spectrum is limited, so the transmission rate is physically limited (Nyquist theorem, Shannon capacity).

---

## 5. Modulation

### Why is modulation needed?

Information signals (such as voice) have very low frequencies (tens of Hz to a few kHz); transmitting them directly has two problems:
- The antenna would need to be extremely long (antenna length ≈ wavelength/4, and 1 kHz corresponds to a wavelength of about 300 km)
- Multiple signals in the same frequency band interfere with each other

**Solution:** "move" the information signal onto a high-frequency carrier for transmission.

### AM (Amplitude Modulation)

Principle: **vary the amplitude of the carrier** to carry information.

$$s(t) = (1 + m(t)) \cdot \sin(2\pi f_c t)$$

- $m(t)$: the information signal (e.g. voice)
- $f_c$: the carrier frequency (e.g. 666 kHz)

```
Information signal (low frequency, slowly varying)  →  controls  →  amplitude of the high-frequency carrier
Big wave envelope = information, small ripples = carrier
```

> **Example:** AM radio (535 kHz ~ 1605 kHz); each channel is assigned a carrier frequency. Tuning means selecting a different $f_c$. When demodulating, the radio extracts the amplitude changes to restore the sound.

### Three basic modulation methods

| Modulation | What changes | Application |
|----------|----------|------|
| AM | Amplitude | AM broadcasting |
| FM | Frequency | FM broadcasting |
| PM | Phase | Foundation of modern digital communication |

Modern communication (WiFi, 4G/5G) uses more complex modulation such as **QAM** (varying amplitude and phase simultaneously) and **OFDM** (multiple carriers).

---

## 6. DTMF (Dual-Tone Multi-Frequency)

### Principle

The telephone keypad system represents each key with **the superposition of two sine waves of different frequencies**.

| | 1209 Hz | 1336 Hz | 1477 Hz |
|--|---------|---------|---------|
| **697 Hz** | 1 | 2 | 3 |
| **770 Hz** | 4 | 5 | 6 |
| **852 Hz** | 7 | 8 | 9 |
| **941 Hz** | * | 0 | # |

> **Example:** Key `5` → the two tones 770 Hz + 1336 Hz sound simultaneously;  
> Key `9` → 852 Hz + 1477 Hz are emitted.

### Why use two frequencies?

- A single frequency is easily falsely triggered by noise
- Only two frequencies (one from the low group, one from the high group) uniquely determine a key, giving strong interference resistance

### Recognition process

```
Press key → emit tones at two frequencies → exchange receives → Fourier transform analyses the spectrum → look up the table to get the key
```

### Dial-up Modem

Same principle: digital data → converted into sounds of different frequencies/modulation → transmitted over the phone line → the receiver restores the digital data.

That "beep—hiss—screech" sound is different frequencies and modulation methods transmitting data.

---

## 7. Line Encoding

### NRZ (Non-Return to Zero)

- `1` = high level, `0` = low level
- Simple, but **no clock recovery capability**: with consecutive identical bits the signal doesn't change, and the receiver can't determine bit boundaries

```
Data:  0  1  1  0  0  0  1
NRZ:  ___|‾‾‾|‾‾‾|___|___|___|‾‾‾
```

### NRZI (Non-Return to Zero Inverted)

- **Flip** on a `1`, **no change** on a `0`
- Solves the synchronisation problem for consecutive `1`s, but there are still no transitions for consecutive `0`s

### Manchester Encoding

**Core rule: every bit must have a level transition in the middle.**

Ethernet standard rules:
- `0` → high level → low level (`‾|_`)
- `1` → low level → high level (`_|‾`)

```
Data:     0      1      0      1
Man:  [‾|_]  [_|‾]  [‾|_]  [_|‾]
```

### Why is Manchester needed?

It solves the **clock recovery** problem:
- NRZ consecutive `0`s: `_________` → the receiver doesn't know where the bit boundaries are
- Manchester consecutive `0`s: `‾|_ ‾|_ ‾|_` → every bit has a transition, and the receiver uses the transitions to recover the clock

### Pros and cons of Manchester

**Pros:**
- **Self-clocking**: every bit has a transition, from which the receiver can recover the clock
- **Strong noise resistance**: detecting "whether there's a change" is more reliable than detecting "an absolute voltage value"
- **No DC bias**: the average voltage is close to 0, friendly to transformer-coupled lines

**Cons:**
- **Doubles the bandwidth**: 1 bit → 2 signal changes, so a 10 Mbps data rate needs 20 Mbaud of signal bandwidth

> **Example:** 10BASE-T Ethernet (10 Mbps) uses Manchester encoding. Later high-speed Ethernet (100 Mbps, 1 Gbps) switched to more efficient encodings such as 4b/5b, 8b/10b and PAM4.

### Comparison of the three encodings

| Encoding | Clock recovery | Bandwidth efficiency | Application |
|------|----------|----------|------|
| NRZ | None | High | Short, simple links |
| NRZI | Partial (only for 1s) | High | USB, optical fibre |
| Manchester | Fully self-clocking | Low (×2) | 10BASE-T Ethernet |
