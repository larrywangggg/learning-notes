# Why Engineering Practice Tends to Prefer SSH over HTTPS

## 1. Clarifying a Common Misconception

When discussing Git, servers, and automation systems, it is common to hear statements such as “these scenarios use SSH 100% of the time.”  
From a strictly technical perspective, this statement is not entirely accurate.

- **HTTPS is often technically viable at the protocol level**
- **SSH is not always the only possible option**

However, in **engineering practice**, SSH has become the *de facto standard*.  
The reason lies not in raw capability, but in **maintainability, security, and suitability for automation**.

---

## 2. Fundamental Differences Between SSH and HTTPS

### 2.1 Design Goals of HTTPS

HTTPS is primarily designed for:

- human users
- interactive authentication
- short-lived credentials (passwords or tokens)
- browser-based and API-driven access

Its core strengths include:

- usability
- immediate authentication
- compatibility with web-based workflows

---

### 2.2 Design Goals of SSH

SSH is designed with a different focus:

- machine-to-machine communication
- long-lived, stable identity authentication
- non-interactive, automation-friendly access

SSH does not primarily answer the question:

> “Who are you right now?”

Instead, it answers:

> **“Is this machine authorised to act on your behalf?”**

---

## 3. Why SSH Becomes the Default in Key Engineering Scenarios

### 3.1 Private Git Repositories (Collaboration and Automation)

In Git-based workflows:

- HTTPS with tokens:
  - is technically valid
  - requires token storage, rotation, and management
- SSH keys:
  - are bound to machines
  - require no interactive input
  - provide long-term, stable authentication

SSH aligns better with engineering requirements in scenarios involving:

- team collaboration
- multiple development machines
- CI/CD pipelines
- unattended execution environments

As a result, SSH becomes the more natural choice in collaborative and automated Git workflows.

---

### 3.2 Cloud Servers and VPS Environments

In server environments:

- there is no browser
- there is no OAuth login flow
- interactive password entry is not assumed

The fundamental access mechanism is defined as:

```text
ssh user@host
```

In these contexts:

- HTTPS is not merely “less recommended”
- it is **fundamentally unsuitable**

As a result, SSH is effectively the only practical solution for accessing servers in real-world deployments.

---

### 3.3 Enterprise Git and Private Infrastructure

In enterprise environments, the primary concerns typically include:

- security governance
- controlled access management
- auditability
- device-level identity management

SSH keys provide several important advantages in such settings:

- they can be precisely bound to a specific device rather than a temporary login session
- they can be individually revoked when an employee leaves or a device is decommissioned
- revocation does not affect access from other authorised devices or team members

By contrast, HTTPS tokens are more commonly associated with:

- user-level credentials
- temporary authorisation mechanisms
- short-lived access contexts

For these reasons, HTTPS tokens are generally unsuitable as infrastructure-level identity mechanisms.  
Consequently, SSH is typically treated as the default and more governance-aligned solution for enterprise Git platforms and private infrastructure.

---

### 3.4 CI/CD and Automation Systems

CI/CD systems exhibit several defining characteristics:

- the absence of a human user
- no capability for interactive input (e.g. passwords)
- short-lived, ephemeral execution environments

Under these conditions, authentication mechanisms must satisfy the following requirements:

- automated injection
- zero human intervention
- secure rotation and centralised management

SSH keys are well suited to these requirements because they:

- can be safely injected as secrets into runtime environments
- support stable machine-to-machine authentication
- rely on mature, widely adopted tooling

Although API tokens may also be used in some cases, SSH typically introduces less operational friction and more predictable behaviour in automated pipelines.

---

### 3.5 Remote Development, Containers, and Tunnelling Scenarios

SSH provides functionality beyond remote login, including:

- port forwarding (SSH tunnels)
- secure file transfer (scp, rsync)
- remote command execution

These capabilities fall outside the design scope of HTTPS.  
As a result, SSH plays a foundational role in:

- remote development environments
- containerised and distributed system debugging
- secure internal service access via tunnels

In these scenarios, SSH functions as a **core infrastructure connectivity layer**, rather than merely a mechanism for transferring code.

---

## 4. An Engineering-Oriented Summary

From an engineering perspective, the roles of the two approaches can be summarised as follows:

> **HTTPS is better suited for interaction between humans and systems**  
> **SSH is better suited for interaction between systems and systems**

As systems evolve toward:

- multi-machine architectures
- automated execution
- unattended operation
- infrastructure-scale deployment

SSH increasingly becomes an implicit assumption rather than an explicit design choice.

---

## 5. A Practical Perspective for Individual Developers

For individual developers working on:

- personal projects
- single-user GitHub repositories
- occasional push and pull operations

HTTPS is entirely sufficient.

However, from a long-term engineering growth perspective:

- SSH is a **low-cost, high-return foundational skill**
- not immediately mandatory
- but effectively unavoidable in more complex environments

---

## 6. Conclusion

SSH is not preferred because it is the only possible option, but because it:

- aligns more closely with how engineering systems operate
- integrates naturally with automation and infrastructure
- introduces minimal friction in complex environments

For these reasons, SSH has become the de facto standard in modern engineering practice.
