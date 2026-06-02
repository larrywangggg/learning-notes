# COMP3310 Week 11：安全 Part 3

> 本周是安全主题收尾：Onion Routing → WiFi 安全 → DoS/DDoS → 国家级后门。

---

## 一、VPN 的隐私缺陷 → Onion Routing

**VPN 不够好的点**：加密做得再好，**流量元数据仍然暴露**——谁在跟谁通信看得清清楚楚。隧道端点（corporate edge router）能看到解包后的真实流量、源/目的地址。Tunnel-mode VPN 也一样，只是"哪两台设备在通信"很明显。

**Onion Routing 的核心思路**：既然一层加密不够，那就**层层套加密**。

- 起源：不是开源自由斗士搞的，而是 **US Naval Research Labs**，后来交给 DARPA（并申请了专利），原始概念公开发表后演化成 TOR / dark web
- 客户端**随机挑 3 个节点**：Guard（守卫，第一跳）、Middle（中间，负责随机化/隐藏）、Exit（出口，把流量送到 server）

### 建立过程：逐跳协商 session key（考试采分点）

> ⚠️ 幻灯片说"collect public keys of 3 nodes"，但实际是**逐跳建立的（telescoping）**，不是一次性拿到三把公钥。考试答题时这个细节是采分点。

```
1. 客户端连 Guard，拿公钥协商 Guard 会话密钥（K_guard）
2. 通过 Guard 隧道，连 Middle，协商 Middle 会话密钥（K_middle）
3. 通过 Guard+Middle 隧道，连 Exit，协商 Exit 会话密钥（K_exit）

发包时：用 K_exit + K_middle + K_guard 三层加密（再加应用层自身加密）

Guard  → 只知道源，不知道目的
Exit   → 只知道目的，不知道源
Middle → 只知道 Guard 和 Exit
沿途任何人嗅探都无法还原"谁跟谁通信"
```

### 额外机制

- **9 个 Directories of Nodes**（节点目录）：federated，每小时交换签名验证信息——类似 P2P 的 bootstrap 问题
- 一条 circuit **只用 10 分钟**就自动重建，缩短嗅探窗口
- 对 evil node 有韧性：层层加密让节点只能看到片段
- 目录是个 web service，可被国家防火墙封锁 → 用 **bridge/relay nodes**（不在目录里，需私下获取）绕过

### 已知弱点

| 弱点 | 说明 |
|------|------|
| **Exit node 能看到目的地** | 你仍然需要做应用层加密；攻破 exit node 有攻击面 |
| **Timing analysis（时序分析）** | 同时观察客户端出口流量和目标 server 入口流量，时间对得上就能建立通信证据。**层层加密也防不住** |
| **缓解手段** | Garlic routing——打包多条消息一起 buffer/重路由打乱时序，但无法 buffer 太久，效果有限 |

### Onion Routing vs MPLS（重要对比）

Onion routing "像电路"但**只钉死 3 个节点**，节点之间仍由普通 internet routing 处理（可绕过故障），只有当 3 个节点之一挂掉才会失败。

**MPLS**：预先建立**整条路径**，每个 path-element 都钉死，任一环节死掉就失败 → 远比 onion routing 脆弱。

---

## 二、Post-VPN：云化替代方案

VPN 复杂、负担重、需改配置、不优化、不 scale。三个外包方案：

| 方案 | 说明 |
|------|------|
| **Cloudflare Tunnels** | 借其全球数据中心当 meeting point，流量走它的私有网，对外隐藏通信关系——但你得**信任 Cloudflare** |
| **Twingate** | 动态生成的 VPN，两端通过 rendezvous point 互相发现并建连；VPN 之上还能叠加细粒度访问控制（VPN + 防火墙） |
| **Tailscale** | 基于 mesh 的 VPN |

Twingate/Tailscale 能跑在 NAS、家用存储/媒体中心上，无需在 edge router 配 VPN 就能全球访问。

---

## 三、WiFi 安全

**为什么 WiFi 比有线更需要加密**：有线靠"摸不到线"获得物理保护，无线**任何人都能监听**，且每一帧对所有人可见。

### Bootstrap 难题与握手流程

**核心问题**：客户端要向 AP 证明自己知道 PSK，但**不能明文发送**（广播谁都能听）。

**解法**：双方各自用 `MAC 地址 + nonce + SSID 密码` 算出 **PTK（Pairwise Transient Key，会话密钥）**，只交换计算结果和 nonce，不发密码本身。

```
1. AP 广播一个 nonce（可能含时间戳）
2. Client 用 MACs + nonces + password 算出 session key，
   回传 + MIC（Message Integrity Code，防篡改签名）
3. AP 做同样计算确认，接受后下发 GTK（group/broadcast key）等 + MIC
4. Client 回 ACK + MIC
```

### 为什么 key 多到离谱

- 单播会话密钥不能用于广播/多播（不能重复发同一内容）→ 需要单独的 **GTK**
- PTK（64 bytes）拆成 KCK / KEK / TK / MIC Tx/Rx keys；GTK（32 bytes）又拆几把；上面还有 PMK（≈PSK）、GMK、MSK
- 这些 temporal key 是**持续动态重算的**，不是连上一次就完事

### Enterprise 认证 — 802.1X

- 用 **EAP**（Extensible Authentication Protocol），可跑在 802.11 和 802.3 上
- 后端通常是 **RADIUS**；每个 client 用自己的凭证（如学号 + 密码），**无共享 PSK**
- AP 只做 pass-through，把认证转交给后端服务器

### WiFi 加密演进史（重点采分）

| 阶段 | 关键点 | 怎么被破 |
|------|--------|---------|
| **WEP** | 单密钥，固定 RC4 | 几分钟嗅探即可算出密钥。**别用** |
| **WPA** | PSK = "personal" / 802.1X = "enterprise"；TKIP（per-frame key）；后改进为 **CCMP**（Counter Mode CBC-MAC Protocol） | 主要经 **WPS**（"一键加入"按钮）握手缺陷被破 |
| **WPA2**（~2010） | 更强加密与防护 | **KRACK**（Key Reinstallation Attack，经 ACK）和 **KR00K**（经 null/disassociation 帧） |
| **WPA3**（2018） | 更强密钥协商（SAE） | ~1.5 年内被 **Dragonblood** 破：需巨量算力，但有钱有资源就能用 |

> **加密黄金法则**：绝不能有可预测的明文内容。disassociation 的 null 帧、WWII Enigma 里可预测的天气预报都是反例——可预测明文 + 密文 → 逆推密钥。

### WiFi 仍然防不住的

- **没有任何协议能验证 AP 身份**：你无法问 AP"你有资格广播 'ANU-Secure' 吗？"。攻击者用手机起一个假 AP 叫同名 SSID，你不留神就连上去
- 上了路径就能 snoop/篡改加密流量、**SSL stripping**（除非 **HSTS** 强制高等级 SSL）、**协议降级攻击**（SSL 握手时把 WPA3 谈成 WPA1）

---

## 四、Denial of Service（DoS）

**本质**：不在乎你传什么，**就是要让你不可用**——靠**资源耗尽**（带宽 / 路由器 CPU & 内存 / 服务器 CPU & 内存 & 磁盘）。**加密在这里救不了你**。

### DDoS 规模

- 单机攻击易被追踪/封锁 → 用 **botnet**：被黑的 IoT 设备（摄像头、婴儿监视器、NVR…）远比 PC 多且好用
- Akamai 每年记录 **~1000 万次** gigabit 级攻击（约每小时 1000 次）
- **2016 首个 1 Tb/s 攻击**：10 万+ 无线摄像头（Canon 默认 admin URL + 没人改默认密码，固件被改）
- **2017 起 Tb 级攻击频繁**
- **2018.02.28 GitHub 攻击**：峰值 **1.35 Tb/s**（平时 <100 Gb/s）。注意 X 轴是**分钟**——靠付费的 IDS/IPS 设备秒级自动检测，协调上游几十台路由器 **black-hole**（黑洞丢弃）流量，~10 分钟基本平息。攻击包模式相似，所以防火墙规则好匹配

### 主要攻击向量

| 向量 | 说明 |
|------|------|
| **UDP flood** | UDP 不像 TCP 会礼貌减速，不管不顾狂发（IoT 摄像头走 RTSP 即是） |
| **Ping of Death** | 分片 + 改 header 的 ICMP，重组后 >64 KB → 内存溢出，直接搞崩主机/网卡 |
| **SYN flood** | 发 SYN 收 SYN/ACK 后**不回 ACK**，server 为每个挂起连接保留状态 → 资源耗尽。缓解：**SYN cookies**（收到 ACK 后才建状态） |

### 放大攻击（小请求大响应）

两种放大维度：

| 维度 | 例子 |
|------|------|
| **Host multiplier** | Botnet：很多设备一起发 |
| **Packet multiplier + spoofing** | SMURF：ping 广播地址，源地址伪造成 target → 全网回包砸向 target |
| | DNS：32 字节请求 → 数 MB 响应（如请求 zone file） |
| | HTTP/FTP/NFS：1 个请求拉 10 GB 文件 |
| | **Memcache**：数据库加速器，本应只在内网走 UDP，却有上千台暴露在公网且有 bug → 反射整个数据库，放大极猛 |

### Spoofing 与 Ingress Filtering

**Spoofing** = 伪造源 IP，让别的机器替自己干活、极难追踪。

**Ingress filtering（根治办法）**：ISP 在其 internet 边界检查源 IP——如果某 IP 本应来自左边接口却从右边进来，就是伪造，丢弃。**只有该 ISP 自己能做**。

**为什么普遍没启用**：
- 额外成本/工作
- **只保护别人、不保护自己客户**——典型成本收益算不过来

> DoS mitigation 对 ISP **财务上是划算的**（因此愿做），而 ingress filtering **不划算**（因此不做）——两者动机刚好相反。这是讲师让你"对 ISP 行业保持愤世嫉俗"的理由。

### 缓解手段

- **CDN**：别当单一靶子，分散流量
- **Edge router / 攻击检测**：高效丢包、按国家过滤
- **上游 provider 支持**：改路由、专用 DDoS 处理系统（如 GitHub 用的那套）
- **到处部署 ingress filtering**（顺手把那些摄像头的默认密码也改了）

---

## 五、国家级后门（锡箔帽 vs 黑帽）

"好的加密 = 坏的国家安全？" NSA 等三字母机构被指控的手段：

| 手段 | 说明 |
|------|------|
| 修改 OS/VPN 代码 | 如 OpenVPN 被"渗透"——某段代码可让发特定 bit pattern 就大幅降低加密强度 |
| 修改加密算法 | 让随机数生成器"没那么随机"（可预测 RNG → 密钥空间缩小 → 可暴力破解） |
| 预计算密钥 | 密钥空间有限 + 足够存储（ANU 超算 20 PB，全国研究网 100 PB）→ 把所有公私钥对查表化，再暴力查 |
| 攻击固件/主板 | 往路由器板上加可疑小芯片，伪装成电阻 |
| **Harvest-then-decrypt（先存后解）** | 今天解不了就先存着，10 年后算力够了再解——谁存得起？政府存得起 |

**IPv6 与 IPSec 的两难**：IPv6 本想**强制 IPSec**（全加密 + 全球 PKI），但 IPv6 的一大动因正是支持海量**超低功耗 IoT 设备**，它们**跑不动 IPSec** → 只好改成**自愿**。这就是"修了一半"的现实。

---

## 复习重点

**必须会：**

1. **Onion Routing 逐跳建链（telescoping）**：不是一次性拿 3 把公钥，是逐跳协商 session key；每个节点只知道相邻地址
2. **Timing analysis 为什么层层加密也防不住**：流量时序可被外部观测者关联
3. **WiFi 握手**：PTK 如何通过 MAC + nonce + password 派生，避免明文传输密码
4. **WPA/WPA2/WPA3 的破解方式**：WPS 缺陷、KRACK、KR00K、Dragonblood
5. **加密黄金法则**：可预测明文 + 密文 → 逆推密钥（Enigma 的教训）
6. **WiFi AP 身份无法验证**：任何人可以伪造 SSID，协议降级攻击
7. **SYN flood 与 SYN cookies** 缓解机制
8. **放大攻击两个维度**：host multiplier（botnet）+ packet multiplier（DNS/Memcache 等）
9. **Ingress filtering 为什么没有大规模部署**：成本收益问题——只保护别人，不保护自己客户
10. **Harvest-then-decrypt**：先存密文，等算力够了再解，这是国家级行为者的现实手段

**理解即可：**

- Garlic routing 打乱时序的局限性
- 802.1X / EAP / RADIUS 的角色分工（AP 只是 pass-through）
- PTK 拆分成多把 key 的原因（单播 vs 广播/多播需要不同 key）
- IPv6 强制 IPSec → 改成自愿的原因（IoT 设备跑不动）
- Cloudflare Tunnels / Twingate / Tailscale 的区别（知道各自的信任假设即可）
