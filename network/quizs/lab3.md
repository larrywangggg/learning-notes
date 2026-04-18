# Exam-style Questions

---

## **Explain what dB, dBm and dBi mean, how are they different? Recall 1 Bels = 10 deciBels.**

**dB (decibel)** — a relative ratio between two power levels:
$$dB = 10 \log_{10}\left(\frac{P_{out}}{P_{in}}\right)$$
No absolute reference — only meaningful as a comparison. e.g. "this amplifier adds 3dB" means it doubles the power.

**dBm** — absolute power, referenced to 1 milliwatt:
$$dBm = 10 \log_{10}\left(\frac{P}{1mW}\right)$$
0 dBm = 1mW, 30 dBm = 1W. WiFi typically transmits at ~20 dBm. This is an absolute measure.

**dBi** — antenna gain, referenced to an ideal isotropic antenna (one that radiates equally in all directions):
- A higher dBi means the antenna focuses energy in a particular direction
- It's not extra power, just redistribution — like a torch vs a bare bulb

**Key difference**: dB is relative, dBm is absolute power, dBi is antenna directionality gain.

---

## **How can I make signals over copper/fibre/wireless go further? What challenges does that bring?**

| Medium | Methods | Challenges |
|---|---|---|
| Copper | Amplifiers, repeaters, thicker wire, shielding | Amplifiers also boost noise; repeaters add cost and failure points |
| Fibre | Optical amplifiers (EDFA), repeaters | Dispersion accumulates over distance; expensive infrastructure |
| Wireless | More transmit power, directional antennas (higher dBi), better receivers | Interference with other users, regulatory power limits, multipath fading |

General problem across all three: **you can boost signal, but noise comes with it**. SNR (Signal-to-Noise Ratio) is what actually limits you, not raw signal strength — this is what Shannon's theorem captures.

---

## **Can I build a wireless transmitter of any power at any frequency? What might stop me?**

No, three categories of constraints:

**Regulatory** — the biggest constraint in practice:
- Governments (ACMA in Australia, FCC in the US) license the spectrum
- Unlicensed bands (e.g. 2.4GHz ISM) have strict power limits (~100mW EIRP)
- Transmitting on licensed frequencies without a licence is illegal
- Some frequencies are reserved (military, emergency services, radio astronomy)

**Physical**:
- Higher frequencies → more free-space path loss, harder to penetrate walls
- Very high power → heat dissipation becomes an engineering problem
- Antenna design is frequency-dependent, you can't use one antenna for everything efficiently

**Interference**:
- High power transmitters drown out nearby receivers on the same or adjacent frequencies
- This is why spectrum is a regulated shared resource, not a free-for-all
