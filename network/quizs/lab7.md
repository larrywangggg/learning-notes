# Exam-style Questions

---

## **How does HTTP Persistence (of TCP connections) and Pipelining help improve performance?**

**Persistence** (HTTP/1.1 default — `Connection: keep-alive`):
- Without it: every request requires a new TCP connection — SYN, SYN-ACK, ACK, request, response, FIN. Enormous overhead for a page with 50 resources.
- With persistence: one TCP connection handles multiple requests sequentially. Eliminates repeated handshake RTTs and TCP slow-start penalties.

**Pipelining**:
- Without it: even on a persistent connection, you send request 1, wait for response 1, then send request 2 — pure sequential latency.
- With pipelining: send requests 1, 2, 3 without waiting for responses; responses come back in order. Eliminates per-request round-trip wait.

Combined effect: instead of `N × (handshake + request + response)`, you get approximately `1 × handshake + N × request/response` overlapped.

---

## **Why is HTTP parallelism (firing off lots of requests in parallel) a generally bad idea?**

Opening many parallel TCP connections to the same server causes:

- **TCP congestion control bypass**: each connection independently runs slow-start, collectively flooding the network with more traffic than congestion control was designed to allow
- **Server resource exhaustion**: each connection consumes server-side memory, file descriptors, and CPU — a client opening 50 parallel connections is effectively a mini DoS attack
- **Unfairness**: one aggressive client grabs disproportionate bandwidth at the expense of other users sharing the same network
- **Head-of-line blocking doesn't actually get fixed**: if the bottleneck is server processing, parallelism just creates a queue on the server side instead

HTTP/2 multiplexing solves the legitimate use case properly — multiple streams over one TCP connection — without the network abuse.

---

## **How can HTTP cookies be misused/"leveraged" by apparently friendly websites?**

**Third-party tracking cookies**: you visit `news.com`, which loads ads from `tracker.com`. `tracker.com` sets a cookie in your browser. Next you visit `shopping.com`, which also loads from `tracker.com` — your browser sends the same cookie. `tracker.com` now knows you visited both sites and builds a cross-site profile of your browsing behaviour, without you ever directly interacting with them.

**Session hijacking**: cookies contain session tokens. If transmitted over HTTP (not HTTPS), an attacker on the same network can intercept the cookie and replay it — authenticating as you without needing your password. This is why the `Secure` flag (HTTPS-only) and `HttpOnly` flag (no JavaScript access) exist.

**CSRF (Cross-Site Request Forgery)**: a malicious site tricks your browser into making a request to `bank.com` — your browser automatically attaches your `bank.com` cookie. The bank sees a valid authenticated request and executes it, even though it originated from a malicious third party. The `SameSite` cookie attribute was introduced specifically to block this.
