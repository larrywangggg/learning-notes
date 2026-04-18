# Exam-style Questions

## **T1: Why do we care about the frequency view of things?**

The time domain shows signal waveforms, but the frequency domain reveals what actually limits communication:
- Channel bandwidth is a frequency-domain concept — it directly determines maximum data rate (Nyquist/Shannon)
- Noise, interference, and signal attenuation are all frequency-dependent phenomena
- Technologies like FDM and WiFi channel allocation only make sense when viewed in the frequency domain

---

## **T1: What are the benefits of a communications circuit, and what are the downsides, compared to using some shared communication channel approach?**

| | Circuit | Shared Channel |
|---|---|---|
| Pros | Guaranteed bandwidth, predictable low latency, good for real-time (voice) | High resource utilisation, handles bursty traffic well via statistical multiplexing |
| Cons | Bandwidth wasted when idle, connection setup overhead | Variable latency, contention and collision issues |

---

## **T1: Could you have a 35-position QAM? And what would it look like? If yes, would it be efficient? If no, what values are better suited?**

Technically yes, practically no. QAM constellations are typically rectangular grids with power-of-2 positions (16, 64, 256…) because:
- Equal numbers of I and Q bits map cleanly onto a square grid
- 35 points cannot form a uniform rectangular grid, making demodulation more complex with worse BER performance
- 32-QAM or 64-QAM would always be preferred instead

---

## **T2: Why does copper become less useful over longer distances? What causes those problems? How can we fix them?**

Three compounding problems:
- **Attenuation**: signal power decays exponentially with distance, worse at high frequencies
- **Skin effect**: high-frequency current concentrates at the wire surface, increasing effective resistance
- **Crosstalk**: electromagnetic coupling between adjacent pairs accumulates over length

Fixes:
- Repeaters/amplifiers (used in DSL)
- Fibre replacement (eliminates the problem entirely)
- Bring fibre closer to the user (FTTC/FTTP), shortening the copper segment
