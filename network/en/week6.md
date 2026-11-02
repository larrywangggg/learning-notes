# Network Week 6 Notes

---

## 1. This Week's Thread

Application-layer protocols must **actively choose** a transport-layer protocol; there's no default optimum:

| Need | Suits |
|------|------|
| Short messages, fast request/response, low server state | UDP |
| Long sessions, large amounts of data, reliability, complex interaction | TCP |

TCP is just a byte stream; the application layer still has to define where messages start and end (frame boundaries) itself.

---

## Part A: The Web and HTTP

### 2. The Essence of the Web

At CERN, Tim Berners-Lee proposed using HTML for hypertext links and HTTP to transfer resources, forming the World Wide Web.

**Key insight: a web page is not one file**, but a main HTML file + many attached objects (CSS, JS, images, fonts). The browser assembles a complete page by issuing **multiple HTTP requests**.

### 3. URL Structure

```
scheme://user:password@host:port/path?query#fragment
```

| Component | Meaning | Example |
|------|------|------|
| scheme | Protocol | http, https, ftp, mailto |
| host | Server address | www.google.com |
| port | Port (default HTTP:80, HTTPS:443) | :8080 |
| path | Resource path | /search |
| query | Parameters passed to the server-side program | ?q=dns&lang=en |
| fragment | In-page anchor (not sent to the server) | #section-2 |

> **Note**: the `?query` in a URL isn't just a "file path"; it often triggers server-side logic. Embedding a plaintext username and password in a URL is a security risk.

### 4. Static vs Dynamic Content

| Type | Principle | Example |
|------|------|------|
| Static | The server returns a file directly | HTML documents, images |
| Dynamic (server-side) | The server runs a program to generate content | CGI, database queries |
| Dynamic (client-side) | The server sends data, browser JS renders locally | Google Maps, SPAs |

The modern mainstream is **client-side dynamic**: it relieves server load. Google Maps requests map tiles, layers and traffic data on demand, continuously updating through interaction.

### 5. The HTTP Workflow (8 steps)

```
1. Parse the URL
2. DNS resolves hostname → IP
3. Establish a TCP connection to host:port
4. Send the HTTP request
5. Receive the response content
6. Close the TCP connection
7. Unpack the response
8. Browser renders
```

Simplified to remember: **locate (URL+DNS) → transfer (TCP+HTTP) → present (render)**

### 6. HTTP Requests and Responses

**Request Methods:**

| Method | Meaning |
|------|------|
| GET | Retrieve a resource |
| HEAD | Retrieve only the response headers (no body, used for cache validation) |
| POST | Submit data |
| PUT/DELETE | Write/delete files (big security risk, basically obsolete) |

**Response status codes:**

| Range | Meaning | Common examples |
|------|------|----------|
| 2xx | Success | 200 OK |
| 3xx | Redirection | 301 Moved Permanently; 302 Moved Temporarily |
| 4xx | Client error | 400 Bad Request; 403 Forbidden; 404 Not Found |
| 5xx | Server error | 500 Internal Error; 503 Unavailable |

> **Key point**: the textual descriptions of status codes (e.g. "Found" vs "Moved Temporarily") aren't standardised; the three-digit number is what's authoritative.

HTTP is a text protocol; it's essentially a protocol language written onto a TCP byte stream. Manually connecting to a web server with `telnet` and sending `GET / HTTP/1.1` shows you the real response.

### 7. HTTP Headers

**Client → server:**

| Header | Purpose |
|--------|------|
| User-Agent | Browser/device info; the server returns different content based on it |
| Accept, Accept-Encoding | Declare the formats the client can handle |
| Cookie, Authorization | State maintenance and authentication |
| Host | Distinguishes multiple virtual hosts on the same IP |
| Referer | The page the request came from |

**Server → client:**

| Header | Purpose |
|--------|------|
| Content-Type, Content-Length | Describe the response body |
| Location | Target of a 3xx redirect |
| Set-Cookie | Write a Cookie |
| Last-Modified, Expires, ETag | Cache control |

### 8. HTTP Statelessness and Cookies

HTTP is a **stateless** protocol: in principle each request is independent, and the server doesn't maintain long-term state for all clients.

Two ways to maintain login state:
1. Embed a Session Token in the URL
2. **Cookie**: the server writes it via `Set-Cookie`, and the client automatically includes it in requests to the same domain

| Cookie type | Characteristics |
|------------|------|
| Session Cookie | Deleted when the browser closes |
| Persistent Cookie | Has an expiry time, stored persistently |
| Secure Cookie | Transmitted only over HTTPS |

**How third-party cookies track across sites:**

```
You visit the ANU home page
  → the page embeds a Facebook icon
  → the browser requests that icon from Facebook
  → Facebook plants a Cookie on you
You later visit the Canberra Times
  → the same Cookie is sent along
  → Facebook knows you visited both websites
```

Cookies aren't just for "staying logged in"; they're also the infrastructure for cross-site tracking.

### 9. Web Performance

#### 9.1 The problem with HTTP/1.0

One TCP connection per resource: three-way handshake + data transfer + four-way teardown, with lots of time spent setting up/tearing down connections.

#### 9.2 Three improvements

| Approach | Mechanism | Drawback |
|------|------|------|
| Parallelism | Open multiple TCP connections at once | High resource consumption, bursty traffic |
| Persistent connections (HTTP/1.1) | One TCP connection reused for multiple requests | Still has to wait for the previous response to finish |
| Pipelining | Issue several requests in a row | Head-of-Line Blocking |

**Head-of-Line Blocking**: if an earlier object gets stuck, everything behind it queues up and waits. Web performance optimisation is often not about raising bandwidth, but **reducing waiting and connection overhead**.

#### 9.3 Real-world web page performance

![Real World Performance](../images/week6/realworld_performance.png)

A real web page (such as the ANU home page) triggers 100+ resource requests. Page content makeup:
- **Images**: the largest share of bytes
- **JavaScript**: many requests
- **CSS / Fonts**: affect rendering
- **The HTML itself**: actually only a small part

Each resource load has several phases: DNS → TCP connect → SSL → waiting for the server response → downloading the content. Slow page loads aren't just due to a "slow network", but to RTT, the number of objects, TCP/HTTP behaviour and page design together.

> **Additional finding**: many resources on modern web pages come from third-party services (Google Analytics, Facebook, DoubleClick), which not only slow pages down but also bring extra cookies/tracking.

### 10. Caching / Proxy / CDN

#### Core idea

Modern web pages have many resources, lots of repeat visits, and expensive remote round trips; three layers of caching solve problems at different scopes:

| Layer | Coverage | How it's filled |
|------|----------|----------|
| **Browser Cache** | A single user | On demand (cached after access) |
| **Proxy Cache** | A group of users in an organisation/campus network | On demand (shared cache) |
| **CDN** | Users worldwide | Proactively pushed in advance (Push before request) |

#### HTTP cache-control Headers

| Header | Purpose |
|--------|------|
| Expires | Specifies the resource's validity period; use the cache directly until it expires |
| Last-Modified | Time the resource was last modified |
| ETag | Resource version fingerprint (more precise than time) |
| If-Modified-Since | Conditional request: don't resend if unchanged |
| If-None-Match | Conditional request: validate based on ETag |
| Range | Partial retrieval (streaming media pulled in segments) |

**Conditional GET** is the core of saving traffic: ask the server with a condition; if nothing changed, use the cache directly; only if it changed, download the new version.

#### Proxy Cache

A proxy splits one end-to-end connection into two segments: `client ↔ Proxy ↔ origin server`.

Workflow:
```
First request: browser → Proxy → origin server (Proxy keeps a copy)
Second request: browser → Proxy (returns the cache directly) → origin server not accessed
```

Advantages:
- Faster for clients (physically closer)
- Lower external traffic and origin server load
- Can do security scanning (checking executables, scripts)
- Can do access control (organisational policy)

Limitations:
- Encrypted traffic (HTTPS) content can't be seen, hard to cache/inspect
- Dynamic content (personalised pages) can't share a cache
- Cache space gets filled by lots of obscure resources accessed only once

#### CDN (Content Delivery Network)

A CDN **proactively pushes popular content to nodes closer to users**, then uses DNS to direct users to the nearest node. Akamai pioneered this model in 1996.

> **Distinction**: Proxy Cache = keep it while you're at it after fetching; CDN = popular content deployed in advance

### 11. Evolution of HTTP Versions

| Version | Key improvements |
|------|----------|
| HTTP/1.0 | Basic GET/HEAD/POST, one connection per resource |
| HTTP/1.1 | Persistent connections (Keep-Alive), pipelining |
| HTTP/2 | Request priorities, Header compression (HPACK), Server Push, multiplexing |
| HTTP/3 | Based on QUIC (UDP), built-in TLS, eliminates TCP head-of-line blocking |

**Key points of HTTP/3**: Google developed QUIC in 2012, formalised as an RFC in 2021. QUIC = UDP + reliability + a security layer, reducing handshake rounds; currently about 1/3 of Internet traffic.

**Why HTTP is "abused" as a general-purpose transport**: firewalls basically never block ports 80/443, so SOAP, REST, AJAX and real-time audio/video are all piled onto HTTP — not because it's technically optimal, but because it can **get through firewalls**.

---

## Part B: Real-Time Communication

### 12. What "Real-Time" Means

There's no single standard for real-time; it depends on the limit the application can tolerate:

| Dimension | Video | Audio | Control signals |
|------|------|------|----------|
| Loss tolerance | High (still passable with 90% lost) | Low (hard to understand with 10% lost) | Extremely low (a "stop the blade" message can't be lost) |
| Delay tolerance | Medium | Low | Extremely low |

| Application type | Characteristics | Common protocols |
|----------|------|----------|
| Streaming (one-way media) | Can accept larger delay, can pre-buffer | TCP/HTTP/CDN |
| Interactive Real-time (video conferencing) | Low delay first | UDP/RTP |

### 13. Why Real-Time Communication Is Hard

The Internet is a **best-effort** network: it only tries its best to forward, with no guarantees on delay, delivery or order.

Real-time communication faces three big problems:

| Problem | Definition |
|------|------|
| **Latency** | The basic propagation delay of a packet from sender to receiver |
| **Jitter (PDV)** | Arrival times of different packets are inconsistent; random fluctuation of delay |
| **Packet Loss** | Packets disappear in the network, or arrive too late and are discarded by the application |

> **Latency vs Jitter**: Latency is being slow overall; Jitter is being sometimes fast, sometimes slow. A typical jitter value is about 15ms, roughly one video frame's duration (60fps ≈ 16ms/frame).

**"Effective loss"**: some packets have physically reached the receiver but exceeded the `maximum acceptable delay` (the maximum acceptable playout delay), which for the application is equivalent to being lost.

### 14. Receiver Buffers

The receiver sets up a `receive buffer + playout buffer` to smooth out jitter, arranging out-of-order packets into a steady playout stream.

**Core trade-off:**

| Buffer size | Delay | Jitter resistance |
|------------|------|----------------|
| Large | High | Strong (tolerates bigger fluctuations) |
| Small | Low | Weak (frames dropped with even slight delay) |

Real-timeness (low delay) and smoothness (jitter resistance) pull against each other.

### 15. Remedial Mechanisms

| Mechanism | Principle | Notes |
|------|------|------|
| **Retransmission** | Request a resend after detecting loss | Needs an extra RTT, usually too slow for real-time; multicast is an exception (a nearby node resends) |
| **Elastic Buffer** | When loss is high, enlarge the buffer and slow playback; when the network recovers, shrink it and catch up quickly | Why people's movements suddenly "speed up" on Zoom |
| **Forward Error Correction (FEC)** | The sender attaches redundant information in advance, and the receiver reconstructs lost content locally | Trades extra bandwidth for low-delay reliability, suits high-RTT or wireless environments |
| **Codec Adaptation** | Lower the bitrate/resolution when the network is poor | Why YouTube automatically switches to 360p |
| **Parallel transmission** | Attach a low-quality copy of the previous frame to subsequent frames | Low-bitrate backup as a safety net |

#### How FEC works

FEC (Forward Error Correction) = **send the "repair materials" along in advance**, instead of waiting for loss and then retransmitting.

The simplest example:
```
Send P1, P2, P3 and the redundant packet R = P1 XOR P2 XOR P3
If the receiver loses P2, then P2 = P1 XOR P3 XOR R (recovered locally)
```

**Adaptive FEC**: dynamically adjust the redundancy ratio according to network conditions:
- Network stable → send less redundancy, saving bandwidth
- Network worse → send more redundancy, improving recoverability
- Driven by RTCP feedback (loss rate, delay, jitter)

The cost of FEC: extra bandwidth overhead; limited effectiveness against bursts of consecutive losses.

### 16. The Real-Time Transport Protocol Stack

| Protocol | Responsibility | Characteristics |
|------|------|------|
| **RTP** | Carries real-time media data | Runs on top of UDP; the header contains a sequence number, timestamp, SSRC; supports lip sync, multiple languages |
| **RTCP** | Control and feedback for RTP | Odd port (RTP uses even ports); reports loss rate, delay, jitter; drives the sender to adjust bitrate/FEC |
| **SIP** | Sets up/terminates calls | An HTTP-like text protocol; used for VoIP; Zoom/WhatsApp/Teams don't use SIP, each has its own proprietary protocol |
| **SDP** | Negotiates media parameters | Negotiates codecs, resolution, etc.; used together with SIP |
| **RTSP** | One-way streaming control | Supports PLAY/PAUSE/SEEK; common in surveillance cameras |
| **DASH** | HTTP-based adaptive streaming | No server-side state; can reuse HTTP caches/CDNs; YouTube's grey progress bar = prefetch buffer |

**Division of labour among protocols in a complete video conference:**
```
SIP  → set up/end the call
SDP  → negotiate media parameters (codec, resolution)
RTP  → carry the audio/video media streams
RTCP → carry feedback, driving adaptive adjustment
```

### 17. Streaming vs Interactive Real-time

| Dimension | Streaming (one-way media) | Interactive (video conferencing) |
|------|----------------------|----------------------|
| Direction | One-way pull | Two-way |
| Delay tolerance | High (can buffer several seconds) | Low (<150ms for a good experience) |
| Response to loss | Lower bitrate, buffer compensation | Must be handled in real time |
| When bandwidth is insufficient | Pause + refill the buffer | Lower quality / stuttering |
| Common protocols | DASH/HTTP/CDN | RTP/UDP |

**RTSP vs DASH**: RTSP is more "elegant" as a protocol (an HTTP-like set of operations: OPTIONS/DESCRIBE/SETUP/PLAY), but in reality YouTube/Netflix both chose DASH over HTTP, because: HTTP gets through firewalls, has a mature CDN/proxy ecosystem, and HTML5 has a built-in player.

> **Core conclusion**: from the standpoint of optimal protocol design, perhaps not everything should use HTTP; from the standpoint of what's most convenient to deploy in reality, HTTP often wins.

### 18. Root Causes of Packet Loss

**A. Really lost in the network:**
- **Congestion/queue overflow**: the router buffer is full and later packets are dropped outright
- **Insufficient link bandwidth**: bandwidth or router processing capacity can't keep up
- **Path changes**: packets take different paths, and some get rerouted or fragmented and arrive abnormally
- **Wireless bit errors**: weak signal/interference corrupts bits; if lower-layer error correction fails, the whole packet is discarded

**B. Arrived but useless (effective loss):**
- **Excessive jitter**: delay fluctuation exceeds the range of the playout buffer
- **Past the playout deadline**: physically at the receiver, but the playout window has been missed
- **Receiver buffer too small**: socket buffer full, application thread can't process in time
- **Deliberately discarded by the system**: the OS or application proactively drops late packets to keep delay low

---

## 19. Knowledge Point Quick Reference

### Core HTTP concepts

| Concept | Key points |
|------|------|
| Web page structure | Main HTML file + multiple attached objects |
| HTTP stateless | Each request is independent; state is maintained via Cookies/Tokens |
| Persistent connections | HTTP/1.1: one TCP connection reused for multiple requests |
| Head-of-line blocking | In pipelining, if an earlier object gets stuck, everything behind waits |
| Cache validation | ETag/If-None-Match; Last-Modified/If-Modified-Since |
| CDN | DNS directs users to the nearest node; popular content pushed in advance |
| HTTP/3 | QUIC over UDP, built-in TLS, eliminates TCP head-of-line blocking |

### Core real-time concepts

| Concept | Key points |
|------|------|
| Latency | Overall propagation delay |
| Jitter | Random fluctuation of delay (sometimes fast, sometimes slow) |
| Effective loss | Arriving too late = lost as far as the application is concerned |
| Buffer trade-off | Large buffer: low loss, high delay; small buffer: low delay, high loss |
| FEC | Send redundancy in advance, recover locally; trades bandwidth for delay |
| RTP/RTCP | RTP carries content; RTCP carries feedback |
| SIP | Signalling to set up/end calls (doesn't carry media) |
| DASH | Adaptive streaming over HTTP |
