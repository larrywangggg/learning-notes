# The Gopher Protocol

## What it is

Gopher is an Internet information retrieval protocol (RFC 1436) invented in 1991 by Mark McCahill's team at the University of Minnesota; it matured earlier than HTTP/HTML and was for a time the de facto standard of the "Internet library".

---

## Core mechanism

Gopher is an application-layer protocol running over TCP (port 70), just as HTTP runs on 80.

```
Application layer  →  Gopher (defines the selector format, menu format)
Transport layer  →  TCP (reliable transfer, segmentation, reassembly)
Network layer  →  IP
```

The interaction flow is extremely simple:

```
Client  →  TCP connection to port 70
        →  sends a selector (one line of text, may be empty, ending with CRLF)
Server  →  returns a block of text, ending with a line containing only "."
        →  closes the connection
```

No headers, no status codes, no cookies.

**Concrete example**: accessing a Gopher server's root menu

```
# Client sends (empty selector, meaning request the root directory)
\r\n

# Server returns (menu format: type + display name + selector + host + port)
1University of Minnesota    /                gopher.tc.umn.edu  70
1Computer Science Dept      /cs              gopher.tc.umn.edu  70
0README                     /README.txt      gopher.tc.umn.edu  70
.
```

The first character of a line is the type code: `1` = directory, `0` = text file, `7` = search, `9` = binary file.

---

## Mental model: file system vs hypertext

| | Gopher | HTTP/HTML |
|---|---|---|
| Information structure | Strict tree menus, like a file system | Arbitrary hyperlink graph |
| Link location | Links live in menu files, separate from content | Links embedded within documents |
| Content types | Plain text, files, search | Anything (images, scripts, multimedia…) |
| Navigation | Choose menu items level by level | Jump freely |
| Protocol complexity | Extremely low (selector + text block) | High (methods, headers, status codes…) |

**Key insight**: Gopher's hierarchy is defined by the server, and users can only walk within the tree the server prescribes. HTML handed linking power to content creators; Gopher didn't.

---

## Why it died

1. **February 1993**: the University of Minnesota announced fees for Gopher servers
2. **April 1993**: CERN placed the WWW (HTTP + HTML) in the public domain, free
3. Commercialisation halted Gopher's expansion, and developers flocked to the Web

> On port numbers: Gopher uses 70, HTTP uses 80. 70 < 80 happens to match the historical fact that Gopher came before HTTP, which makes it easy to remember.

---

## Significance today

**Gopherspace is still alive**: a niche community of enthusiasts maintains Gopher servers, accessible with clients such as Lagrange and Kristall.

**Security research — SSRF exploitation**: the `gopher://` URL scheme is still exploited in Server-Side Request Forgery (SSRF) attacks. Because Gopher can construct arbitrary TCP byte streams, attackers can use it to bypass HTTP restrictions and send raw requests directly to internal network services.

```
# A malicious URL constructed by an attacker, making the server request internal Redis
gopher://127.0.0.1:6379/_%2A1%0D%0A%248%0D%0Aflushall%0D%0A
# The content actually sent to Redis after decoding:
# *1\r\n$8\r\nflushall\r\n
```

**Protocol design textbook**: it is a classic example of a "minimalist protocol", and its comparison with HTTP often appears in networking courses.

---

## Sources

- https://datatracker.ietf.org/doc/html/rfc1436
- https://en.wikipedia.org/wiki/Gopher_(protocol)
- https://boston.conman.org/2019/01/12.2
- https://www.ils.unc.edu/callee/gopherpaper.htm
- https://dev.to/dotcomboom/the-gopher-protocol-in-brief-1d88
