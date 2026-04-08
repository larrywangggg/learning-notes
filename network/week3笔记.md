# Network Week 3 笔记

**本周主线：** Space Wireless → LAN 概念与设计哲学 → 媒介访问控制（MAC）→ Ethernet → Wi-Fi

---

## 一、卫星通信（Space Wireless）

### 1.1 卫星通信的演变

| 阶段 | 描述 |
|------|------|
| 早期（被动反射）| 卫星相当于"大型空中反射镜"，地面电磁波打上去再反射回另一处，无需复杂电子系统 |
| 现代（主动转发）| 卫星接收上行信号（Uplink），在星上放大/处理/变频，再发回地面（Downlink）|
| 星间链路 | 卫星之间直接通信（激光链路），减少对地面站的依赖，实现跨洋路由 |

通信模式：
- **Satellite-to/from-ground：** 地面站 ↔ 卫星 ↔ 地面站
- **Satellite-to-satellite：** 星间中继，不必每跳都回地面
- **Mixed-mode：** 地面链路与卫星链路混合使用

### 1.2 轨道类型对比

| 轨道 | 高度 | 公转周期 | 延迟（RTT）| 特点 |
|------|------|----------|------------|------|
| LEO（低地球轨道）| ~400–1,200 km | ~90 min | ~20–40 ms | 低延迟，但卫星移动快，需跟踪，需大量卫星 |
| MEO（中地球轨道）| 2,000–20,000 km | ~2–12 h | 中等 | GPS 常用 |
| GEO（地球同步轨道）| 36,000 km | 24 h | ~250 ms | 从地面看"固定"，覆盖范围大，但延迟高 |

**GEO 延迟分析：** 单程约 36,000 km，信号以约光速传播，单程约 120 ms，往返约 250 ms。对视频尚可接受，对实时交互（游戏、视频通话）体验较差。

**LEO 优势：** 距离近、延迟低（Starlink 约 20–40 ms RTT）；真空中光速比光纤快约 50%，某些超长距离路径（如纽约→东京）走星间链路可能比走海底光缆更快。

> **例子（Starlink 工程细节）：**
> - **Phased Array 天线：** 用户端天线无需机械转动，通过电子方式"虚拟转向"，实时追踪过顶卫星
> - **星间激光链路：** 卫星间直接通信，无需每次中转地面站，支持跨洋传输
> - **Direct-to-Cell：** 新一代服务允许普通手机直接通过卫星发收短信，逐步向语音扩展

### 1.3 什么时候需要卫星

| 场景 | 原因 |
|------|------|
| 偏远/农村地区 | 地面基础设施铺设成本过高或不可行 |
| 海上/航空 | 目标持续移动，超出地面基站覆盖范围 |
| 灾区/应急 | 地面网络损坏，卫星作为紧急恢复通道 |
| 临时部署 | 工地/野外/军事场景，需要快速开通 |
| 全球覆盖服务 | GPS、气象观测、遥感成像、全球广播 |
| 超长距离低延迟 | LEO 星间链路在特定路径上可能优于海底光缆 |

**不适合用卫星的情况：**
- 城市密集区（已有光纤/4G/5G，成本更低）
- 对超低延迟极敏感且本地可建地面网络
- 需要高容量且长期稳定（地面网络容量/成本更优）

卫星通常是地面网络的**补充**，而非替代。

---

## 二、LAN（局域网）

### 2.1 LAN 的正确理解

传统按距离分类（LAN/MAN/WAN）过于武断，真正重要的是两个概念：

**Administrative Domain（管理域）：**
- LAN 内所有设备遵守同一套介质、编码、调制、硬件标准
- 由同一个组织/管理者统一控制
- 不是"范围小"，而是"同一个主人管的、规则统一的网络"

**Broadcast Domain（广播域）：**
- 该域内任何设备发出的广播帧，可以被域内所有其他设备接收
- 类比：在教室里喊一句话，所有人都听得到，目标那人回应，其余人忽略

> LAN 是设备接入网络的**起点**：你访问任何互联网服务，数据首先从本地 LAN 出发。

### 2.2 LAN 的历史演进

1. **Point-to-point：** 最早两台设备之间单独连线，简单但无法扩展
2. **Shared medium / Bus topology：** 所有设备接到同一条公共总线，信号被所有人"看到"，适合多设备共享
3. **Switched Ethernet：** 现代主流，交换机在中间转发，每条链路变为 point-to-point

### 2.3 LAN 设计哲学

**核心原则：简单、快，把复杂性留给上层。**

| 设计选择 | 原因 |
|----------|------|
| 不保证可靠交付（No guaranteed delivery）| 底层尽力发送（best-effort），可靠性由 TCP 等上层处理 |
| 不内建复杂纠错 | 出错通常直接丢包，由上层重传；但有 CRC 做基本差错检测 |
| 不为特定场景优化（实时/批传输/安全）| LAN 是通用基础设施，不为单一用途定制 |
| 优先关注 Performance | 高速率、低延迟、高吞吐是 LAN 的核心追求 |

**LAN 是硬件主导的系统**，硬件倾向于简洁、稳定、可规模化，而不是复杂逻辑判断。

---

## 三、Frame（帧）

### 3.1 为什么要有 Frame

LAN 不是随意传 bit，而是把 bit 组织成 **Frame（帧）**，每个帧必须说明：

| 字段 | 作用 |
|------|------|
| Destination | 去哪（目标 MAC 地址）|
| Source | 从哪来（源 MAC 地址）|
| 边界标识 | 帧从哪里开始、到哪里结束 |
| 长度 | 帧有多长 |
| Payload | 实际数据 |
| Checksum（CRC）| 基本差错检测 |

**帧长度的限制：**
- **不能无限长：** 会独占链路、消耗接收缓冲区、错误累积
- **不能无限短：** header/trailer 开销占比太高，效率低；对于 CSMA/CD，太短的帧无法覆盖碰撞检测所需时间

### 3.2 字节填充（Byte Stuffing / Escape）

如果帧边界符号（flag）出现在 payload 中，接收方会误判帧结束。解决方法是**转义（escape）**：

```
原始数据：... FLAG ...
发送时：  ... ESC FLAG ...   ← 用 ESC 转义
接收方：  遇到 ESC 则将下一字节视为数据，不作边界处理
```

这个思想在很多协议中反复出现（如 PPP、HDLC）。

### 3.3 Ethernet Frame 结构

```
| Preamble | SFD | Dest MAC | Src MAC | [802.1Q Tag] | Type/Length | Payload | FCS |
|  7 bytes |1byte|  6 bytes | 6 bytes |   4 bytes    |   2 bytes   | 46-1500B|4byte|
```

- **Preamble：** 7 字节的 `10101010...` 序列，用于唤醒接收方、锁定时钟和速率（像"敲锣"让接收端准备好）
- **SFD（Start of Frame Delimiter）：** 1 字节，标志帧数据开始
- **802.1Q Tag：** 可选，用于 VLAN 标记（4 字节）
- **Type/Length：** 标识上层协议类型（如 0x0800 = IPv4）或帧长度
- **FCS（Frame Check Sequence）：** CRC-32 校验，检测传输错误

---

## 四、MAC（媒介访问控制）

### 4.1 MAC 的双重含义

1. **MAC Address（MAC 地址）：** 网络接口的硬件身份标识，48 位，全球唯一
   - 识别的是**网络接口（interface）**，不是整台电脑
   - 格式：`AA:BB:CC:DD:EE:FF`，前 24 位是厂商 OUI
   - 广播地址：`FF:FF:FF:FF:FF:FF`

2. **Media Access Control（媒介访问控制）：** 多设备如何公平共享同一介质的规则

### 4.2 为什么需要 MAC 协议

多路复用策略对比：

| 方式 | 原理 | 问题 |
|------|------|------|
| TDM（时分）| 固定时间片轮流 | 空闲时浪费带宽 |
| FDM（频分）| 固定频段分配 | 频谱利用率低 |
| SDM（空分）| 物理隔离 | 成本高 |
| **Statistical Multiplexing** | 有需要就发，配套访问控制 | 需要解决碰撞 |

LAN 采用 **Statistical Multiplexing**：不预先固定分配，谁有数据谁发，但必须有机制防止混乱。

---

## 五、随机接入协议（Random Access）

### 5.1 ALOHA

**原理：** 想发就发，发完后等 ACK；未收到 ACK 则假设发生碰撞，随机等待后重传。

**随机等待的原因：** 如果两个设备都在同时重传，会再次碰撞；随机等待让它们错开。

| 优点 | 缺点 |
|------|------|
| 极简单，无需中央调度 | 负载高时碰撞率高 |
| 适合低负载/偶发传输 | 网络繁忙时吞吐急剧下降 |
| 去中心化，易扩展 | 最大信道利用率约 18%（纯 ALOHA）|

**Slotted ALOHA：** 将时间划分为等长时隙，所有设备只能在时隙开始时发送，碰撞概率减半，最大利用率约 37%。

> **例子：** 早期夏威夷大学用无线电网络连接各岛，ALOHA 即由此命名（1970s）。现代 IoT 低功耗传感器网络（如 LoRa 的 ALOHA-like 接入）也使用类似机制。

### 5.2 CSMA（Carrier Sense Multiple Access）

**核心改进：先监听，再发送。**

```
发送前 → 监听信道是否空闲
  空闲 → 立即发送整个帧
  忙碌 → 等待，直到空闲再尝试
```

**为什么仍会发生碰撞？—— 传播延迟（Propagation Delay）**

```
A ─────────────────── B
A 开始发（A 听到空闲）
B 也开始发（B 听到空闲，因为 A 的信号还没传到 B）
→ A 和 B 的信号在线缆中间碰撞
```

关键结论：**你监听到的只是"此刻你这里"的状态，无法感知远端刚开始的发送。**

**Bandwidth × Delay Product（带宽延迟积）：**
- 带宽越高 + 延迟越大 → 线缆中"在途"的数据越多 → 碰撞管理越难

**最小帧长要求：**
- 发送方必须在帧发送期间检测到碰撞信号
- 最坏情况：远端在你刚开始发时也开始发，碰撞发生后碰撞信号需要传回来
- 因此：**最小帧发送时间 ≥ 2 × 单向传播延迟**

> **例子：** 100 m 长的以太网电缆，信号传播约 0.5 μs；往返约 1 μs；以 10 Mbps 传输，1 μs 内能发 10 bit，所以帧至少要超过 10 bit，实际标准定为 64 字节（考虑更大网络）。

### 5.3 CSMA/CD（Collision Detection，有线）

在 CSMA 基础上加入**边发边听**：发送期间持续监听，一旦检测到碰撞立即：
1. 发送 **Jam 信号**（通知所有节点发生碰撞）
2. 停止发送
3. 执行 **Binary Exponential Backoff** 后重传

**Binary Exponential Backoff（二进制指数退避）：**

| 第 n 次碰撞 | 等待窗口 | 随机等待范围 |
|------------|----------|-------------|
| 1 | 0–1 个时隙 | 0 或 1 |
| 2 | 0–3 个时隙 | 0–3 |
| 3 | 0–7 个时隙 | 0–7 |
| n | 0–(2ⁿ−1) 个时隙 | 随机选一个 |
| 16 次后 | — | 放弃，报错 |

退避窗口随碰撞次数指数增长，分散了重试时间，减少再次碰撞概率。

**适用范围：** 主要用于传统有线 Ethernet（10BASE-T、100BASE-TX）。在 switched Ethernet 中每条链路是 point-to-point，几乎不再发生碰撞，CSMA/CD 已基本退出使用。

### 5.4 CSMA/CA（Collision Avoidance，无线）

无线环境无法做 Collision Detection（发射时本机信号太强，无法同时监听远端微弱信号），因此改为**避免碰撞**：

```
监听信道是否空闲
  空闲 → 等待 DIFS（分布式帧间间隔）+ 随机 Backoff 时间 → 再发送
  忙碌 → 等待，直到空闲后再开始退避计时
发送完 → 等待 ACK 确认
```

**Wi-Fi（802.11）使用 CSMA/CA。**

### 5.5 无线特有问题

**Hidden Terminal Problem（隐藏终端）：**

```
A ──→ B ←── C
A 和 C 互相听不到对方，却都能和 B 通信
→ A 和 C 同时发给 B → 在 B 处发生碰撞
```

**Exposed Terminal Problem（暴露终端）：**

```
A ←── B ──→ C ──→ D
B→A 和 C→D 本可以同时进行
但 B 能听到 C 正在发，误以为信道忙而等待 → 带宽浪费
```

**解决方案：RTS/CTS（MACA 协议）**

```
1. 发送方 → RTS（Request to Send）→ 接收方
2. 接收方 → CTS（Clear to Send）→ 发送方（广播）
3. 听到 CTS 的节点：保持安静（即使没听到 RTS）
4. 发送方 → 发送数据
5. 接收方 → ACK
```

RTS/CTS 让"隐藏节点"通过听到 CTS 知道信道被占用，从而避免碰撞。代价是增加了握手开销，适合大帧；小帧则直接发送效率更高。

### 5.6 Contention-Free Access（无竞争接入）

与随机接入相对的另一类方案：**轮流发送**。

| 方法 | 原理 |
|------|------|
| TDM | 固定时隙分配 |
| Token Ring | 持有 token 才能发送，发完传给下一个 |

**优点：** 高负载下行为可预测，无碰撞，延迟有上界。  
**缺点：** Token 丢失时整个网络停止；扩展性差；对拓扑变化敏感。

Token Ring 是重要历史技术（IBM 802.5 标准），但今天已基本被 Ethernet 替代。

---

## 六、Ethernet

### 6.1 Ethernet 的核心优势

- **便宜、规模化、简单、向后兼容**
- 从共享总线演化至 switched，保持标准稳定
- 相比 carrier-grade 技术（ATM 等）更轻量，不强调 SLA

### 6.2 Ethernet 的演化

| 阶段 | 介质 | MAC 机制 | 备注 |
|------|------|----------|------|
| 10BASE-2/5 | 同轴电缆 | CSMA/CD | 总线拓扑，所有人共享 |
| 10BASE-T | 双绞线 + Hub | CSMA/CD | 物理星型但逻辑仍是总线 |
| 100BASE-TX | 双绞线 + Switch | CSMA/CD（很少触发）| 交换机引入 |
| 1000BASE-T+ | 双绞线/光纤 + Switch | 全双工，几乎无碰撞 | 每链路 point-to-point |

**现代 Ethernet = Switched + Full Duplex，CSMA/CD 基本不再需要。**

### 6.3 Auto-Negotiation

设备接入交换机时自动协商：
- **Speed：** 10/100/1000/10G Mbps
- **Duplex：** Half / Full
- **Crossover：** MDI/MDI-X 自动识别
- **Power：** PoE（Power over Ethernet）

> **注意：** Auto-negotiation 在现实中并非总是完美，一端强制固定速率而另一端 auto-negotiate 可能导致 duplex mismatch（一端 full duplex，另一端 half duplex），表现为大量碰撞和性能极差。排障时必查此项。

### 6.4 交换机（Switch）的工作原理

交换机核心逻辑：**学习 MAC 地址，决定转发**。

```
帧进入端口 port X，源 MAC = AA:BB:CC
→ 交换机记录：AA:BB:CC 在 port X（MAC Table）

目标 MAC = DD:EE:FF
→ 查 MAC Table：已知 DD:EE:FF 在 port Y → 转发到 port Y
→ 未知 → 泛洪（Flood）到所有端口（除入端口）

广播帧（FF:FF:FF:FF:FF:FF）→ 永远泛洪到所有端口
```

MAC Table 有老化时间（aging），长时间未收到来自某 MAC 的帧会被删除。

### 6.5 STP（Spanning Tree Protocol）

**问题：** 交换机之间成环 → 未知单播泛洪或广播会无限复制 → **Broadcast Storm（广播风暴）**

**STP（802.1D）解决方案：** 在逻辑上将交换网络裁剪成一棵无环树。

```
1. 选举 Root Bridge（Bridge ID 最小者，通常是优先级最低或 MAC 最小）
2. 每个非 Root Bridge 计算到 Root 的最短路径（Root Port）
3. 每段链路选出一个 Designated Port
4. 剩余端口进入 Blocking 状态（逻辑断开）
5. 拓扑变化时重新收敛
```

**关键理解：** STP 不是让物理环消失，而是让逻辑转发表现为无环树。物理冗余链路仍然存在，拓扑变化后会激活备用链路。

RSTP（802.1w）是快速版，收敛时间从分钟级降至秒级。

### 6.6 VLAN（802.1Q）

**问题：** 同一物理交换网络中需要流量隔离（不同部门、不同安全级别）。

**802.1Q VLAN Tag（4 字节，插入 Ethernet 帧中）：**

```
| Dest MAC | Src MAC | 0x8100 | PCP(3b) | DEI(1b) | VID(12b) | Type | Payload | FCS |
                     ← TPID  →←————————— TCI ————————————→
```

- **VID（VLAN ID）：** 0–4095，标识帧属于哪个 VLAN
- **PCP（Priority Code Point）：** 3 位 QoS 优先级
- 同一物理网络上可创建最多 4094 个独立广播域

> **例子：** 企业网络中，财务部门（VLAN 10）和研发部门（VLAN 20）的设备连接在同一台交换机上，但互相不能直接通信，必须经过三层路由（Router/L3 Switch）才能跨 VLAN 访问。

### 6.7 Link Aggregation（链路聚合，802.1AX/LACP）

多条物理链路捆绑为一条逻辑链路：
- 提升带宽（多条 1G → 逻辑 2/4/8G）
- 提供冗余（一条断了，流量自动切换到其他链路）
- LACP（Link Aggregation Control Protocol）动态协商

### 6.8 Jumbo Frames

| 类型 | Payload 上限 |
|------|-------------|
| 标准 Ethernet | 1500 bytes |
| Jumbo Frame | 约 9000 bytes（9000 MTU）|

**为什么需要 Jumbo Frame：**
- 10 Gbps 下，1500B 帧约每 1.2 μs 处理一帧 → CPU 中断频率极高
- 更大帧 → 更少帧数 → 更低 CPU 开销 → 更高有效吞吐
- 主要用于存储网络（iSCSI）、数据中心互联等大流量场景

---

## 七、Wi-Fi（无线局域网）

### 7.1 Wi-Fi ≠ 无线 Ethernet

Wi-Fi 继承了 Ethernet 的 frame、MAC、地址、广播域等**概念**，但无线环境远比有线复杂，机制差异显著：

| 对比项 | Ethernet | Wi-Fi |
|--------|----------|-------|
| 碰撞检测 | CSMA/CD（边发边听）| CSMA/CA（避免碰撞）|
| 信道共享 | 同一线段上的设备 | 同一频道覆盖范围内所有设备 |
| 隐藏终端 | 不存在 | 存在（需 RTS/CTS 解决）|
| 媒介 | 物理线缆，边界明确 | 电磁波，范围动态变化 |
| ACK | 无链路层 ACK | 每帧都有 ACK 确认 |

### 7.2 Wi-Fi 的关键技术

| 技术 | 作用 |
|------|------|
| CSMA/CA | 基本媒介访问控制 |
| OFDM（正交频分复用）| 将信道分成多个子载波并行传输，抗多径干扰 |
| MIMO（多输入多输出）| 多根天线同时收发，提高吞吐和抗干扰 |
| DSSS（直接序列扩频）| 早期 802.11b，抗干扰 |
| 速率自适应 | 信号质量差时自动降低调制阶数（如 QAM256 → QAM16）|
| 功率控制 | 动态调整发射功率，减少干扰 |

### 7.3 Wi-Fi 频段对比

**2.4 GHz：**
- 信道带宽 20 MHz，总共 13 个信道（各地区不同）
- 相邻信道大量重叠，非重叠信道仅 3 个：**1 / 6 / 11**
- 设备密集（手机、Bluetooth、微波炉、无绳电话均在此频段）→ 干扰严重
- 穿墙能力强，覆盖范围更大

**5 GHz：**
- 信道更多（约 25 个非重叠 20 MHz 信道）
- 可组合为 40/80/160 MHz 宽信道，容量大幅提升
- 设备相对少，干扰小
- 穿墙能力弱，覆盖范围较小

**6 GHz（Wi-Fi 6E/7）：**
- 1200 MHz 新频段，非重叠信道极多
- 几乎无历史遗留干扰

**实用结论：能用 5 GHz 就用 5 GHz；密集环境优先考虑 6 GHz。**

### 7.4 Wi-Fi 标准演进

| 标准 | 名称 | 最大速率 | 主要技术 |
|------|------|----------|----------|
| 802.11b | Wi-Fi 1 | 11 Mbps | DSSS, 2.4 GHz |
| 802.11a | Wi-Fi 2 | 54 Mbps | OFDM, 5 GHz |
| 802.11g | Wi-Fi 3 | 54 Mbps | OFDM, 2.4 GHz |
| 802.11n | Wi-Fi 4 | 600 Mbps | MIMO, 2.4/5 GHz |
| 802.11ac | Wi-Fi 5 | 3.5 Gbps | MU-MIMO, 5 GHz |
| 802.11ax | Wi-Fi 6/6E | 9.6 Gbps | OFDMA, 6 GHz |
| 802.11be | Wi-Fi 7 | 46 Gbps | Multi-Link |

### 7.5 Wi-Fi 帧类型

Wi-Fi 帧比 Ethernet 更复杂，有 4 个 MAC 地址字段（因为帧可能经过 AP 转发，需区分 BSSID/SA/DA/TA）。

三类帧：

| 类型 | 示例 |
|------|------|
| **Control Frames（控制帧）**| RTS / CTS / ACK |
| **Management Frames（管理帧）**| Beacon / Probe / Authentication / Association |
| **Data Frames（数据帧）**| 实际用户数据 |

### 7.6 客户端连接 AP 的流程

```
1. 扫描（Scanning）
   主动扫描：发送 Probe Request → AP 回应 Probe Response
   被动扫描：监听 AP 定期发出的 Beacon（含 SSID、速率、安全信息）

2. Authentication（认证）
   802.11 Open System Authentication（基本握手）

3. Association（关联）
   客户端发 Association Request → AP 回 Association Response
   分配 AID（Association ID），建立会话

4. 数据传输
   DHCP 获取 IP → 正常通信

5. Roaming（漫游）
   移动中信号变弱 → 客户端主动或 AP 触发切换到更强的 AP（Re-association）
```

### 7.7 Wi-Fi 安全

| 协议 | 状态 | 问题 |
|------|------|------|
| WEP | 已废弃 | RC4 实现缺陷，数分钟可破解 |
| WPA | 不推荐 | TKIP 仍有漏洞 |
| WPA2 | 当前主流 | CCMP/AES 加密，KRACK 漏洞（2017）|
| WPA3 | 推荐 | SAE 握手，更强前向保密 |

**重要隐私问题：Probe Request 泄露历史 SSID**

设备在寻找已知 Wi-Fi 时，会主动广播 Probe Request，其中包含曾经连接过的 SSID 列表。这意味着：
- 任何人都可以监听你的设备曾经连过哪些网络
- Wigle.net 等服务收集了全球 SSID 地理位置数据
- 结合历史 SSID 可以推断用户去过哪些地方

现代系统（iOS 14+/Android 10+）已开始使用随机 MAC 地址和不主动发 Probe 来缓解此问题。

---

## 八、核心知识点总结

### 随机接入协议对比

| 协议 | 机制 | 适用场景 | 优缺点 |
|------|------|----------|--------|
| Pure ALOHA | 随时发，碰了随机退避 | 低负载无线 | 简单；利用率低（max ~18%）|
| Slotted ALOHA | 时隙边界发，碰了随机退避 | 低负载无线 | 利用率提升（max ~37%）|
| CSMA | 先听再发 | 有线 | 减少碰撞；仍因传播延迟发生碰撞 |
| CSMA/CD | 先听再发，边发边检测碰撞 | 有线 Ethernet | 快速发现碰撞；无线不可用 |
| CSMA/CA | 先听，随机退避，再发 | 无线（Wi-Fi）| 避免碰撞；开销较高 |

### 本周核心考点

1. LEO vs GEO 的延迟/覆盖/跟踪 trade-off
2. 何时需要卫星（到不了 / 不划算 / 会坏掉 / 在移动 / 要全球）
3. LAN 两个关键概念：**Administrative Domain** 和 **Broadcast Domain**
4. LAN 设计哲学：简单 + 高性能，复杂性上移
5. Frame 边界、最小帧长与 2×传播延迟的关系
6. ALOHA → CSMA → CSMA/CD / CSMA/CA 的演化逻辑
7. **Hidden Terminal** 问题与 RTS/CTS 解决方案
8. Ethernet：从共享总线走向 Switched + Full Duplex
9. **STP** 解决二层环路和广播风暴（逻辑无环树）
10. Wi-Fi ≠ 无线 Ethernet；2.4 GHz 拥挤，5 GHz 更好
11. Probe Request 泄露历史 SSID 的隐私问题
