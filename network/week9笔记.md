# COMP3310 Week 9：拥塞控制 · 流控 · 网络管理

---

## Part A：拥塞与流量控制

### 一、定位

课程进入最后大主题"When Good Networks Go Bad"。前面所有协议设计都建立在"网络是你一个人用的"这个童话假设上。现实是全球共享，所以要谈 **congestion（拥塞）** 和 **flow control（流控）**。讨论范围：Network layer + Transport layer，主要是 TCP，UDP 只在它"惹事"时被提一下。

---

### 二、Sliding Window 回顾（铺垫）

**Sender Window W**：未 ACK 的字节数，目标是填满管道。

```
W ≈ 2 × Bandwidth × delay（BDP，带宽时延积）

例：100Mb/s + 50ms 单向延迟 → W = 10Mb ≈ 1MB ≈ 1000 个 10kb 段
    这 1000 个段此刻就"在路上"
```

**最原始的 Receiver 模型：**
- 只 buffer 一个段
- 不是按序的就 drop，ACK 仍然指向"我还在等的那个"
- Sender 单计时器超时 → 全部重传未 ACK 的 → 简单但极其低效

---

### 三、Flow Control（流控，针对 Receiver）

**问题**：Sender 拼命塞，Receiver 应用层处理不过来（典型场景：高清视频流到小设备）。

**Receiver Window WIN**：Receiver 在 ACK 里报告自己剩余 buffer 大小。

| 名字 | 谁的 | 作用 |
|------|------|------|
| W | Sender | 基于 BDP，理论上能塞多少 |
| WIN | Receiver | 告诉 Sender "我还有多少 buffer" |
| CWND | Sender | 基于网络反馈估计的"安全发送量" |

**Sender 实际使用：`min(W, WIN, CWND)` 作为有效窗口。**

> **常考点**：WIN 和 CWND 没有任何关系。WIN 是 Receiver 的 buffer 状态，CWND 是 Sender 对网络容量的估计。

由于路径上有大量段在飞，WIN 报告回来时已经是"半个 RTT 前"的状态——你看到的反馈天然滞后。

---

### 四、Congestion（拥塞）

**一个必须纠正的概念：**"链路拥塞"是错误说法。链路是有固定时钟的传送带，100Mb/s 就是 100Mb/s，不会"装更多"。真正拥塞的是**路由器的 buffer**（多入一出 → output buffer 溢出 → 丢包）。

**Congestion Collapse（拥塞崩溃）正反馈循环：**

```
负载上升 → buffer 填满 → 延迟暴涨
→ buffer 溢出 → 丢包
→ Receiver 请求重传 → Sender 重传
→ 网络里塞满"老数据的重传"，新数据进不来
→ Goodput（有效吞吐）→ 0
```

> "我如果不遵守拥塞控制是不是能多抢点带宽？"——不能。物理打不过，你只会让自己丢更多包。

---

### 五、Fairness vs Efficiency

| 策略 | 含义 | 总吞吐 |
|------|------|--------|
| Fair（每流 0.5） | 所有流平等分配 | 1.5 |
| Efficient（饿死 AC） | 最大化总吞吐 | 2.0 |
| Optimal（轻微饿死 AC=0.25） | 高吞吐且不完全饿死任何人 | 2.0 |

**Max-Min Fairness**：最大化最小者。做法：所有流从 0 开始一起涨，谁先把瓶颈链路占满就锁定该值，剩余容量给还没饱和的流继续涨。

> ⚠️ 讲师承认 PPT 数字加起来不对（学生当场指出）。考试如果碰到这种题，自己重算别迷信幻灯片。

---

### 六、控制律分类

| 维度 | 选项 |
|------|------|
| 开/闭环 | Open（预留电路，如 ATM）/ Closed（基于反馈） |
| 主导方 | Host-driven / Network-driven（policing 强但僵硬） |
| 分配方式 | Rate-based / Window-based |

**TCP = Closed-loop, Host-driven, Window-based。**

---

### 七、AIMD（核心机制）

**Additive Increase, Multiplicative Decrease：**
- 没拥塞 → 慢慢加（每 RTT +1 段）
- 一拥塞 → 砍半（×0.5）

为什么必须是 AI + MD？

| 组合 | 结果 |
|------|------|
| 慢增 + 慢减 | 收敛慢，浪费容量 |
| 快增 + 快减 | 震荡剧烈，不稳定 |
| 快增 + 慢减 | 公平性差，强者通吃 |
| **慢增 + 快减** | **博弈论意义上收敛到公平 + 高效** |

产生的典型流量曲线就是 **TCP Sawtooth（锯齿波）**——Wireshark 抓一次长距离传输就能看到。

---

### 八、拥塞信号来源

| 信号 | 优点 | 缺点 |
|------|------|------|
| Packet loss | 明确 | 已经晚了（buffer 已满） |
| Packet delay | 早期预警 | 推断而非确证，对 jitter 敏感（手机切基站时尤其坑） |
| ECN（路由器显式标记） | 早期且零额外流量 | 全路径设备都得支持，部署率至今很低 |

---

### 九、ACK Clocking（自时钟机制）

高速链 → 低速链时，packets 在路由器排队后被"拉长"输出，ACK 也以慢链速率返回。Sender 看到 ACK 间隔变大，就知道该减速。

TCP 用 **ACK 到达节奏**作为发包触发器——这是隐式的反馈回路，不需要额外测时间。由此引出 CWND（Congestion Window）：实际发送量上限，通常 < W。

---

### 十、Slow Start

冷启动时 CWND 该设多少？AI 太慢（1000 个 RTT 才填满），所以用 Slow Start：

```
初始 CWND = 1
每 RTT 翻倍（1, 2, 4, 8, 16...）
直到出现丢包 → MD 砍半
设 ssthresh = ½ × CWND@loss
之后进入 AI 阶段（每 RTT +1）
```

> 讲师吐槽："叫 Slow Start 但其实是指数增长，名字是反的。"

---

### 十一、TCP 变种演进

| 版本 | 关键特性 |
|------|---------|
| Tahoe / Reno（90s） | 经典 AIMD + Slow Start + Fast Retransmit |
| Vegas | 用 RTT 变化预测拥塞，提前退让。问题：被 Reno 打死（Reno 不让步，Vegas 主动让，结果 Vegas 拿不到带宽） |
| BIC / CUBIC | 三阶曲线，更激进的探测，Linux 默认 |
| BBR（Google） | 测瓶颈带宽 + RTT，心跳式探测（不是锯齿），YouTube 在用，但和其他 TCP 共存时是否"友好"还有争议 |

Wikipedia 列了 20+ 种 TCP，每种在不同场景表现不一，不存在"绝对最优"。

---

### 十二、丢包恢复优化（概览）

| 机制 | 描述 |
|------|------|
| **Fast Retransmit** | 收到 3 个 dup-ACK → 不等 timeout，立刻重传丢失的那一段 |
| **Fast Recovery** | 重传后不退回 Slow Start，只做 MD 然后继续——保住 ACK clock |
| **NewReno** | 识别 partial ACK，一个 RTT 内能修多个丢包 |
| **SACK** | Receiver 直接告诉 Sender 收到了哪些段，Sender 精准重传 |

> 详见 Part B 完整演进路径。

---

### 十三、ECN（路由器协助）

机制极简，零额外流量：

```
1. 路由器发现 output buffer 快满 → 在 IP header 标记 ECN bit
2. Receiver 看到 → 在返回的 TCP segment（ACK 或正常包）里回标
3. Sender 看到 → 主动 MD
```

要求路径上**所有路由器 + 两端 host** 都支持，至今普及率惨淡。

---

## Part B：TCP 丢包恢复演进详解

### 起点：原始 TCP（蠢到什么程度）

假设 CWND = 1000 个段，第 3 个段丢了：

```
Sender 发:   1 2 [3] 4 5 6 7 ... 1000
Receiver 收: 1 2     4 5 6 7 ... 1000  （4-1000 全部被 drop！）
Receiver ACK: ACK=3, ACK=3, ACK=3 ...  （一直说"我等3"）
Sender:      超时后重传 3, 4, 5, 6, ..., 1000
```

三个核心问题：
1. Receiver 把 4-1000 全扔了——它们其实都到了，但因为乱序就被丢，逼着 Sender 重发一遍
2. Sender 等 timeout 才反应——timeout 通常是几倍 RTT，这段时间 ACK clock 断了
3. Timeout 后重新 Slow Start（CWND=1）→ 性能腰斩还要从头爬

---

### 优化 1：Receiver 多 buffer 一点

乱序到的段先存着，不直接丢。

```
Sender 发:   1 2 [3] 4 5 6 7
Receiver 收: 1 2     4 5 6 7  （4-7 存进 buffer）
Receiver ACK: ACK=3, ACK=3, ACK=3, ACK=3  （还是说"我等3"，但段没扔）
```

光这一步就省下了"4-7 不用重传"的浪费。但 Sender 还不知道 4-7 已经到了——引出下一步。

---

### 优化 2：Fast Retransmit（快速重传）

**核心洞察**：duplicate ACK 不是噪音，是信号。

```
ACK=3
ACK=3  ← duplicate #1
ACK=3  ← duplicate #2
ACK=3  ← duplicate #3  ← 触发 Fast Retransmit
```

**规则**：收到 3 个 dup-ACK → 不等 timer → 立刻只重传丢失的那一个段。

**为什么是 3 个？**

| dup-ACK 数量 | 判断 |
|-------------|------|
| 1 个 | 可能只是网络乱序 |
| 2 个 | 还是可能乱序 |
| 3 个 | 基本确定真丢了 |

**为什么只重传那一个？** 后续 dup-ACK 还在涌来，说明 4, 5, 6, 7 确实到了 Receiver，不用全发一遍。

**收益**：反应时间从"timeout（几倍 RTT）"缩短到"3 个 dup-ACK（约 1 个 RTT）"。

---

### 优化 3：Fast Recovery（快速恢复）

**问题**：Fast Retransmit 之后，该不该 Slow Start？

**老逻辑（Tahoe）**：任何丢包 → 假定严重拥塞 → CWND 砍到 1 → Slow Start 重来。

**Fast Recovery（Reno 引入）**：

洞察：dup-ACK 还在源源不断地来 = ACK clock 没断 = 网络还在跑 = 不是雪崩级拥塞。

做法：
1. MD：`ssthresh = CWND/2`，`CWND = ssthresh`（砍半但不归零）
2. 跳过 Slow Start，直接进入 Additive Increase
3. 重传丢的段后，继续往前发新数据

```
CWND
 │    Tahoe                      Reno
 │   ╱╲                         ╱╲
 │  ╱  ╲___╱╲                  ╱  ╲___╱╲___╱
 │ ╱  (Slow Start 回来)        ╱  (直接 AI 继续)
 └─────────────────────────────────────────► Time
```

Reno 在丢包后保持高速运行，性能比 Tahoe 高一个档次。

---

### 优化 4：NewReno（一个 RTT 内多丢包）

**Reno 的痛点**：一个窗口内丢了两个段（seq 3 和 seq 7）：

```
Sender 发:  1 2 [3] 4 5 6 [7] 8 9 10
Receiver 收: 1 2     4 5 6     8 9 10
```

Fast Retransmit 触发，重传 3。Receiver 收到 3 后：

```
Receiver ACK: ACK=7  ← 这叫 "partial ACK"
```

Reno 看到 ACK 从 3 跳到 7，以为"事情解决了"，退出 Fast Recovery。结果 8, 9, 10 又 dup-ACK 一波，又触发一次 MD——CWND 被砍两次，性能崩。

**NewReno 的修复**：识别 partial ACK（ACK 推进了但还没追上 Fast Retransmit 触发时的最高 seq）：
- 不退出 Fast Recovery
- 立即重传下一个被怀疑丢的段（seq 7）
- 继续等下一个 ACK

一个 RTT 内能修多个丢包，且只做一次 MD。

**局限**：NewReno 仍然在"猜"——每个 RTT 修一个洞，丢了 5 个段要 5 个 RTT 填完。

---

### 优化 5：SACK（Selective ACK）—— 终于不猜了

Receiver 直接告诉 Sender "我具体收到了哪些"：

```
Sender 发:  1 2 [3] 4 5 [6] 7 8 [9] 10
Receiver 收: 1 2     4 5     7 8     10

ACK 携带:
  ACK number = 3  （我还在等 3）
  SACK blocks = [4-5], [7-8], [10-10]
```

Sender 看一眼就明白：只要补 3, 6, 9。一个 RTT 内全部精准重传。

**关键限制（期末考点）**：TCP option 字段只有 40 bytes，一个 SACK block 占 8 bytes（起始 + 结束 seq），加上 option header 2 bytes，最多放 **4 个 block**（实际常常是 3 个，因为还要给 timestamp option 留位置）。

**Sender 侧的变化**：
- 每个未 ACK 段一个 timer（不再是全局一个 timer）
- 根据 SACK 信息精准判断哪些丢、哪些到
- 重传决策几乎是算法上最优

**协商**：TCP 三次握手时双方在 SYN 里带 SACK-permitted option。现在主流系统（Linux/Windows/macOS/BSD）默认全开。

---

### 五代演进对比

| 版本 | 丢包探测 | 重传策略 | 一个 RTT 修几个丢包 | 主要缺陷 |
|------|---------|---------|------------------|---------|
| 原始 TCP | Timeout | 重传所有未 ACK | 1（且要等 timeout） | 极慢，ACK clock 断 |
| Tahoe | 3 dup-ACK | Fast Retransmit | 1 | 丢包后 Slow Start，性能崩 |
| Reno | 3 dup-ACK | Fast Retransmit + Fast Recovery | 1 | 一窗口多丢包会多次 MD |
| NewReno | 3 dup-ACK + partial ACK | 同上 + 持续 FR | 多个（每 RTT 一个） | 还是在猜 |
| SACK | 3 dup-ACK + SACK block | 精准重传 | 多个（一次性） | header 限 4 个 block |

**核心底层逻辑**：保住 ACK clock 比什么都重要。Timeout = ACK clock 死了 = 必须冷启动 → 灾难。Fast Retransmit / Fast Recovery / SACK 的共同目标：在丢包发生时让 ACK 流不断。

---

### 容易混淆的点（期末防雷）

1. **Fast Retransmit ≠ Fast Recovery**
   - Fast Retransmit = "什么时候重传 + 传什么"（基于 3 dup-ACK）
   - Fast Recovery = "重传之后怎么调 CWND"（不回 Slow Start，只 MD）
   - Tahoe 有 Fast Retransmit 但没 Fast Recovery，Reno 两个都有

2. **dup-ACK 触发条件是"3 个"，不是"第 3 次"**：实际上是第 4 个相同 seq 的 ACK 到达时触发（原始 + 3 dup）

3. **SACK 不替代累积 ACK**：ACK number 字段还是累积 ACK，SACK 是 option，额外告诉你不连续收到了哪些。为了向后兼容。

---

## Part C：网络测量与 SNMP（Week 9-2）

### 一、为什么需要测量和监控

Speedtest 类工具的局限：只是端到端测量，变量太多（WiFi 干扰、距离、天气、共用人数、对端位置...），无法判断网络**哪一段**出了问题。

真正想知道的：
- 哪里拥塞、有没有错误、硬件软件是否正常
- 改动之后是变好还是变坏（没有 before/after 就无法验证）
- 包是否到达了正确的应用、路由是否符合预期

**两个真实故事（说明监控的价值）：**

1. CSIRO 两个园区之间的微波链路性能逐渐下降，排查到最后发现天线罩里筑了蚂蚁窝——"bug in the network"字面意义上的 bug。

2. 中日视频会议每 60 秒一次画面卡顿。最终定位到 Seattle 一个路由器——工程师为了申请采购新设备，每 60 秒 SNMP 查询一次，这个查询本身就让繁忙的路由器丢了 90% 流量。**教训：监控本身不能给被监控设备添加负担（SNMP 轻量化的核心动机）。**

---

### 二、现有反馈机制为什么不够

ECN、ICMP、TCP ACK 这些都是应用层端到端的 measure：
- 只告诉你"出了问题"，不告诉你沿路哪个点出问题
- 不告诉你好消息（比如"这条链路 30% 负载零错误"）
- 因为非对称路由，通常只能反映一个方向

结论：必须直接和路径上的设备对话——只有它们持有我们需要的数据。

**两个管理边界：**
- **Interior（自己的管理域）**：有权限，可以在每台设备上装 agent，随便查
- **Exterior（域外）**：无权限，甚至"知道某设备存在"本身就是信息泄露

---

### 三、SNMP 设计目标

- 覆盖所有设备（路由器、交换机、AP、打印机、摄像头、服务器...）
- **轻量级**——agent 不做计算、不存历史、没有绝对时钟
- 设备承压时仍能工作
- 可扩展的全局命名（应对厂商各异的参数）
- 既支持 query/response，也支持 command/control（通过 set 变量）
- 安全性"以后再说"（后来确实拖了很多年）

---

### 四、SNMP 四个组成部分

| 组件 | 角色 | 说明 |
|------|------|------|
| SNMP protocol | 协议本身 | 定义消息格式和 PDU |
| **Agent** | **Server（反直觉）** | 跑在被监控设备上，维护轻量数据库 |
| **Manager** | **Client** | 运行在 NMS 上，发起查询 |
| **MIB** | 数据模型 | 描述 agent 数据库结构，由 SMI 组织 |

**Proxy agent**：用来桥接不支持 SNMP 的设备（把摄像头数据"映射"进 SNMP 世界）。

---

### 五、Agent 的"轻"如何实现

只有这些原始数据类型：counter / gauge / timeticks / string / OID

| 功能 | Agent 做不做 | 谁来做 |
|------|------------|--------|
| 计算速率 | ❌ 不做 | Manager 自己减、自己除 |
| 存历史 | ❌ 不存 | Manager 自己存、自己画图 |
| 绝对时钟 | ❌ 没有 | 只有"开机至今"的相对时间 |

**TimeTicks = 1/100 秒**：32 位整数 × 10ms 恰好 1 年 wrap 一次，所以一年问一次都不会重复。

---

### 六、协议运作

- 基于 **UDP**（connectionless），用 request ID 匹配请求和响应
- Agent 监听 **161**，Manager 监听 **162**（接收 trap）

**5 种 PDU（v1）**：GetRequest / GetNextRequest / SetRequest / GetResponse / Trap

**6 个标准 Trap：**

| # | Trap 名称 | 触发条件 | 严重性 |
|---|----------|---------|--------|
| 1 | linkDown | 某个接口挂了（网线拔了、端口故障） | 警告 |
| 2 | linkUp | 某个接口恢复了 | 信息 |
| 3 | **coldStart** | 设备**意外重启**（崩溃后自动恢复） | 严重 |
| 4 | warmStart | 设备**预期内重启**（管理员手动 reboot） | 信息 |
| 5 | authenticationFailure | 有人尝试访问 agent 但认证失败 | 安全警告 |
| 6 | **egpNeighbourLoss** | EGP/BGP 邻居丢失（失去外部路由对等体） | 严重 |

**coldStart vs warmStart 的区分很重要：**
- warmStart：你刚才 ssh 进去敲了 reboot，设备重启完发 warmStart——预期内，无所谓
- coldStart：你没让它重启，它自己重启了，意味着设备崩溃过——可能是软件 bug、电源、过热、被攻击

**为什么 egpNeighbourLoss 单独列出：** 链路本身可能还活着（linkDown 没触发），但 BGP 邻居不再说话了——整个网络可能瞬间和互联网失联。"足以让大多数网管陷入恐慌"。

**Trap 的坑**：Trap 走 UDP 且单向无确认，丢了就丢了。现代实践通常是 trap 做实时告警 + 周期性轮询（polling）做兜底。SNMPv2 引入 InformRequest（带确认的 trap），但 v1 只有这 6 个 trap。

---

### 七、Counter vs Gauge（重要的语义陷阱）

#### 本质区别

| 维度 | Counter | Gauge |
|------|---------|-------|
| 测量对象 | 累积事件（已发生过的总数） | 当前状态（此刻的量） |
| 方向 | 只增不减 | 可增可减 |
| 类比 | 汽车**总里程表** | 汽车**油量表** |
| 典型例子 | 接口收发包总数、字节总数、错误总数 | 内存使用率、队列长度、CPU 温度 |
| 到达最大值 | **wrap 回 0**（从头开始，不通知） | **latch 在最大值**（停在那不动） |
| 大小 | Counter32 / Counter64 | Gauge32（标准里没有 Gauge64） |

#### Counter 的核心陷阱：Wrap

**Counter32 最大值 = 2³² - 1 = 4,294,967,295（约 42.9 亿）**，到顶后下一次递增直接变 0，没有任何通知。

```
T=0:    ifInOctets = 4,294,967,290
T=5min: ifInOctets = 1,005
```

差值是多少？两种可能：
- **情况 A（wrap 了）**：真实流量 = (2³² - 4294967290) + 1005 = 6 + 1005 = **1011 字节**
- **情况 B（wrap 整圈还多）**：真实流量 ≈ 4.3 GB

Manager 根据接口速率来判断：100Mbps 接口 5 分钟最多 ≈ 3.75GB，情况 B 物理上不可能，确定是 A。

**Counter32 为什么不够用：** 10Gbps 接口跑满 → 每 **3.4 秒** wrap 一次。5 分钟内 wrap 了 87 次，完全无法重建真实流量。

SNMPv2 引入 **Counter64**（满 10Gbps 需要约 585 年才 wrap 一次），对应 MIB 对象：
- `ifInOctets`（IF-MIB, Counter32）→ 千兆以上慎用
- `ifHCInOctets`（IF-MIB, Counter64，HC = High Capacity）→ 现代环境必用

#### Gauge 的核心陷阱："等值"不代表"没变化"

```
T=0:    disk_used = 500 GB
T=5min: disk_used = 500 GB
```

三种可能：
- 情况 A：这 5 分钟磁盘真的没人动
- 情况 B：5 分钟内写了 10GB，又删了 10GB，净变化为 0
- 情况 C：多次写入删除，净变化恰好为 0

Manager 完全无法区分。**Gauge 的"静止"不可信。**

**结论：**
- 监控"当前状态"（够不够、满不满）→ Gauge ✅
- 统计"累积发生了多少事" → Counter ✅
- 用 Gauge 推算写入总量 → ❌

MIB 设计者经常两个一起放：
- 当前队列长度 → Gauge（`ifOutQLen`）
- 历史发送总包数 → Counter（`ifOutUcastPkts`）

#### 从 Counter 计算速率（实战）

```python
t1, c1 = time(), snmp_get('ifInOctets')   # t1=0, c1=1000
sleep(60)
t2, c2 = time(), snmp_get('ifInOctets')   # t2=60, c2=8500

delta = c2 - c1
if delta < 0:
    delta += 2**32  # 处理 Counter32 wrap（Counter64 用 2**64）

rate_bps = delta * 8 / (t2 - t1)
```

**三个坑：**
1. 采样间隔不能太长——Counter32 + 高速链路 wrap 信息丢失
2. 采样间隔不能太短——给 agent 增加负担（还记得 Seattle 路由器的故事吗）
3. `delta < 0` 也可能是**设备重启**，不一定是 wrap——配合 `sysUpTime` 判断：如果 uptime 比上次采样还短，说明重启过，这段数据丢弃

---

### 八、安全演进

| 版本 | 年份 | 关键点 |
|------|------|--------|
| v1 | 1990 | 用"community string"做认证，**明文密码**。public（只读）/ private（读写） |
| v2c | 1996 | 加了 GetBulk、manager-to-manager、TCP、64 位 counter；c 代表 community，安全又没修 |
| v3 | 2002 | 从 v1 分支重写；支持 integrity / authentication / privacy 三层 |

**v3 的三个安全级别：**

| 级别 | 说明 |
|------|------|
| noAuthNoPriv | 只匹配用户名 |
| authNoPriv | 消息摘要认证（验完整性） |
| authPriv | 认证 + 加密（最强） |

> 讲师吐槽："S 本来代表 Simple，v3 之后已经完全不 simple 了。"

**安全提示**：SNMPv1/v2 agent 绝不应暴露到外网——容易被扫、是攻击面。

---

### 九、MIB、ASN.1 与 OID

**ASN.1（1980 年代，比 XML 早 40 年）**：Type-Length-Value 形式描述数据结构。基本类型：INTEGER、OCTET STRING、OBJECT IDENTIFIER 等。

**OID 树（全局唯一，类似 DNS）：**

```
.(root) → iso(1) → org(3) → dod(6) → internet(1)
                                          ├── directory(1)
                                          ├── mgmt(2) → mib-2(1) → system(1)
                                          │                       → interfaces(2)
                                          │                       → ip(4)
                                          │                       → tcp(6)
                                          ├── experimental(3)
                                          └── private(4)  ← 厂商扩展（打印机墨水量之类）
```

- 大部分 Internet 标准对象 = `1.3.6.1.2.1.x.y.z`
- 厂商扩展 = `1.3.6.1.4.x.y.z`

**MIB 对象示例：**

```
ifNumber OBJECT-TYPE
    SYNTAX  INTEGER
    ACCESS  read-only
    STATUS  mandatory
    ::= { interfaces 1 }
```

即 `1.3.6.1.2.1.2.1`。ifNumber 只读很合理——给它写值不会真长出一个新网口。

---

### 十、表（Table）与 GetNext

ASN.1 本身没有"表"这种结构，但需要（每个接口的 IP/状态/包数/错误率...）。

解法：每个表格单元都有自己的 OID，行按 index 展开。Manager 不知道有几行，用 **GetNext 按字典序遍历**：

```
Get(Interface.1.ipAddress)     → 150.203.1.1
GetNext(Interface.1.ipAddress) → Interface.2.ipAddress
...一直走到 OID 跳出当前 table 就停
```

**问题**：来回包太多。v2 引入 **GetBulk**，一次拉一整块，但回包不能超过单个 UDP 包（~64KB），否则报 tooBig。

---

### 十一、SNMP 在广域网外的处境

SNMP 主要用于自己管理域内，跨域监控基本靠"人"（合同、求人、装探针）。

**替代/补充方案：**

| 工具 | 说明 |
|------|------|
| Port mirroring | 交换机镜像端口抓包 |
| 物理层 snooping | 在缆线上插光/电传感器 |
| Looking Glass | 运营商公开的远程路由器查询界面（BGP 查询、ping、traceroute） |
| perfSONAR | 学术界协作部署的探针 beacon 网络，生成跨机构的"延迟/带宽/丢包矩阵" |

---

### 十二、常用工具

- **MRTG / Cacti / Nagios**：按时间画流量图
- **Network Weathermap**（PHP，读 MRTG 数据）：按空间画拓扑负载图
- **厂商自带工具**：按机柜面板布局画端口状态

---

## 复习重点

### 拥塞控制（必须会）

1. **W vs WIN vs CWND 三窗口分清楚**，WIN 和 CWND 完全无关
2. 拥塞发生在**路由器 buffer**，不是链路
3. AIMD 为什么必须是"慢加快减"
4. Slow Start → AI → MD 的状态转换
5. Fast Retransmit 触发条件 = **3 个 dup-ACK**
6. Fast Retransmit ≠ Fast Recovery（Tahoe 有前者没后者，Reno 两个都有）
7. SACK 解决了 Sender 的"猜"的问题，header 最多 4 个 block
8. ECN 的工作流程（IP header 标记 → Receiver 回传 → Sender MD）
9. Max-Min Fairness 的定义和 4 流路由网络例子（可能出计算题）

### SNMP（必须会）

1. SNMP 四组件，**agent 是 server、manager 是 client**（反直觉）
2. v1/v2c/v3 区别，尤其 v3 的三个安全级别
3. 5 种 PDU + 6 种标准 Trap（冷热启动的区分、egpNeighbourLoss 的含义）
4. **Counter vs Gauge 的语义差异**：Counter 两次相等可信，Gauge 两次相等不可信
5. Counter32 的 wrap 问题 → Counter64 的引入原因（10Gbps 满载 3.4 秒 wrap 一次）
6. OID 树结构，能读 `1.3.6.1.2.1.x` 这种地址
7. GetNext 用于遍历表，GetBulk 的引入原因

### SNMP（理解即可）

- ASN.1 语法细节（知道存在、知道哪里查就行）
- TimeTicks 为什么是 1/100 秒（段子，不会考）
- perfSONAR、Looking Glass（知道是什么、用在哪里）
