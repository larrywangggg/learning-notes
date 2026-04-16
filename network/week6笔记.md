# Network Week 6 笔记

---

## 一、本周主线

应用层协议需要**主动选择**传输层协议，没有默认最优解：

| 需求 | 适合 |
|------|------|
| 短消息、快速 request/response、低 server state | UDP |
| 长会话、大量数据、可靠性、复杂交互 | TCP |

TCP 只是字节流，应用层还需自己定义消息的开始和结束（帧边界）。

---

## Part A：Web 与 HTTP

### 二、Web 的本质

Tim Berners-Lee 在 CERN 提出用 HTML 做超文本链接、用 HTTP 传输资源，形成 World Wide Web。

**关键认知：网页不是一个文件**，而是一个 HTML 主文件 + 大量附属对象（CSS、JS、图片、字体）。浏览器通过发出**多个 HTTP 请求**来拼出一个完整页面。

### 三、URL 结构

```
scheme://user:password@host:port/path?query#fragment
```

| 组成 | 含义 | 例子 |
|------|------|------|
| scheme | 协议 | http, https, ftp, mailto |
| host | 服务器地址 | www.google.com |
| port | 端口（默认 HTTP:80, HTTPS:443）| :8080 |
| path | 资源路径 | /search |
| query | 传给服务端程序的参数 | ?q=dns&lang=en |
| fragment | 页内跳转锚点（不发给服务器）| #section-2 |

> **注意**：URL 中的 `?query` 不只是"文件路径"，常常在触发服务端逻辑；URL 里嵌明文用户名密码是安全隐患。

### 四、静态 vs 动态内容

| 类型 | 原理 | 例子 |
|------|------|------|
| 静态 | 服务器直接返回文件 | HTML 文档、图片 |
| 动态（服务端）| 服务器执行程序后生成内容 | CGI、数据库查询 |
| 动态（客户端）| 服务器发数据，浏览器 JS 本地渲染 | Google Maps、SPA |

现代主流是**客户端动态**：减轻服务器压力，Google Maps 就是按需请求地图 tile、图层、交通数据，持续交互更新。

### 五、HTTP 工作流程（8 步）

```
1. 解析 URL
2. DNS 解析 hostname → IP
3. 建立 TCP 连接到 host:port
4. 发送 HTTP 请求
5. 接收响应内容
6. 关闭 TCP 连接
7. 解包响应
8. 浏览器渲染
```

简化记忆：**定位（URL+DNS）→ 传输（TCP+HTTP）→ 呈现（渲染）**

### 六、HTTP 请求与响应

**请求方法（Methods）：**

| 方法 | 含义 |
|------|------|
| GET | 获取资源 |
| HEAD | 只取响应头（不含 body，用于缓存验证）|
| POST | 提交数据 |
| PUT/DELETE | 写/删文件（安全风险大，基本废弃）|

**响应状态码：**

| 范围 | 含义 | 常见例子 |
|------|------|----------|
| 2xx | 成功 | 200 OK |
| 3xx | 重定向 | 301 永久移动；302 临时移动 |
| 4xx | 客户端错误 | 400 Bad Request；403 Forbidden；404 Not Found |
| 5xx | 服务端错误 | 500 Internal Error；503 Unavailable |

> **重点**：状态码的文字描述（如 "Found" vs "Moved Temporarily"）不规范，三位数字才是权威。

HTTP 是文本协议，本质就是写在 TCP 字节流上的协议语言。用 `telnet` 手工连 web server 发送 `GET / HTTP/1.1` 可以看到真实响应。

### 七、HTTP Headers

**客户端 → 服务端：**

| Header | 作用 |
|--------|------|
| User-Agent | 浏览器/设备信息，服务端据此返回不同内容 |
| Accept, Accept-Encoding | 声明客户端能处理的格式 |
| Cookie, Authorization | 状态维持与认证 |
| Host | 同一 IP 上多个虚拟主机的区分依据 |
| Referer | 请求来源页面 |

**服务端 → 客户端：**

| Header | 作用 |
|--------|------|
| Content-Type, Content-Length | 描述响应体 |
| Location | 3xx 重定向目标 |
| Set-Cookie | 写入 Cookie |
| Last-Modified, Expires, ETag | 缓存控制 |

### 八、HTTP 无状态与 Cookie

HTTP 是**无状态**协议：每个请求原则上独立，服务器不为所有客户端长期维护状态。

维持登录状态的两种方式：
1. URL 中嵌 Session Token
2. **Cookie**：服务端通过 `Set-Cookie` 写入，客户端自动在同域请求中带上

| Cookie 类型 | 特点 |
|------------|------|
| Session Cookie | 关闭浏览器即删除 |
| Persistent Cookie | 有过期时间，持久存储 |
| Secure Cookie | 仅 HTTPS 传输 |

**第三方 Cookie 跨站追踪机制：**

```
你访问 ANU 首页
  → 页面内嵌 Facebook 图标
  → 浏览器向 Facebook 请求该图标
  → Facebook 给你种一个 Cookie
你之后访问堪培拉时报
  → 同一 Cookie 被带上
  → Facebook 知道你同时访问了两个网站
```

Cookie 不只是"保持登录"，也是跨网站追踪（tracking）的基础设施。

### 九、Web 性能

#### 9.1 HTTP/1.0 的问题

每个资源一个 TCP 连接：三次握手 + 数据传输 + 四次挥手，大量时间用在连接建立/拆除上。

#### 9.2 三种改进方案

| 方案 | 机制 | 缺点 |
|------|------|------|
| 并行（Parallelism）| 同时开多个 TCP 连接 | 资源消耗大，突发流量 |
| 持久连接（HTTP/1.1）| 一条 TCP 复用多个请求 | 仍需等前一响应完成 |
| 流水线（Pipelining）| 连续发出多个请求 | 队头阻塞（Head-of-Line Blocking）|

**Head-of-Line Blocking**：前面的对象卡住，后面的全部排队等待。Web 性能优化很多时候不是提高带宽，而是**减少等待和连接开销**。

#### 9.3 真实网页性能

![Real World Performance](./images/week6/realworld_performance.png)

一个真实网页（如 ANU 首页）会触发 100+ 个资源请求。页面内容构成：
- **图片**：bytes 占比最大
- **JavaScript**：请求数量多
- **CSS / Fonts**：影响渲染
- **HTML 本身**：反而只占很小一部分

每个资源加载分多个阶段：DNS → TCP connect → SSL → 等待服务器响应 → 下载内容。页面加载慢不只是因为"网速慢"，而是 RTT、对象数量、TCP/HTTP 行为、页面设计共同造成的。

> **额外发现**：现代网页中大量资源来自第三方服务（Google Analytics、Facebook、DoubleClick），不仅拖慢页面速度，也会带来额外的 cookie/tracking。

### 十、Caching / Proxy / CDN

#### 核心思路

现代网页资源多、重复访问多、远程往返代价高，三层缓存解决不同范围的问题：

| 层次 | 覆盖范围 | 填充方式 |
|------|----------|----------|
| **Browser Cache** | 单个用户 | 按需（访问后缓存）|
| **Proxy Cache** | 组织/校园网用户群体 | 按需（共享缓存）|
| **CDN** | 全球用户 | 主动预推送（Push before request）|

#### HTTP 缓存控制 Headers

| Header | 作用 |
|--------|------|
| Expires | 指定资源有效期，到期前直接用缓存 |
| Last-Modified | 资源最后修改时间 |
| ETag | 资源版本指纹（比时间更精确）|
| If-Modified-Since | 条件请求：没变化就别重传 |
| If-None-Match | 条件请求：基于 ETag 验证 |
| Range | 部分获取（流媒体按段拉取）|

**Conditional GET** 是节省流量的核心：带条件询问服务器，没变就直接用缓存，变了才下载新版。

#### Proxy Cache

Proxy 把一条端到端连接拆成两段：`客户端 ↔ Proxy ↔ 源服务器`。

工作流程：
```
第一次请求：浏览器 → Proxy → 源服务器（Proxy 存副本）
第二次请求：浏览器 → Proxy（直接返回缓存）→ 不访问源服务器
```

优势：
- 提升客户端速度（物理距离更近）
- 降低外网流量和源服务器负载
- 可做安全扫描（检查可执行文件、脚本）
- 可做访问控制（组织策略）

局限：
- 加密流量（HTTPS）看不到内容，难以缓存/检查
- 动态内容（个性化页面）无法共享缓存
- 缓存空间会被大量一次性访问的冷门资源填满

#### CDN（内容分发网络）

CDN 是**主动把热门内容推送到离用户更近的节点**，再用 DNS 把用户导向最近节点。Akamai 1996 年开创了这个模式。

> **区分**：Proxy Cache = 拉取后顺手留着；CDN = 热门内容事先部署好

### 十一、HTTP 版本演进

| 版本 | 关键改进 |
|------|----------|
| HTTP/1.0 | 基础 GET/HEAD/POST，每资源一个连接 |
| HTTP/1.1 | 持久连接（Keep-Alive）、流水线 |
| HTTP/2 | 请求优先级、Header 压缩（HPACK）、Server Push、多路复用 |
| HTTP/3 | 基于 QUIC（UDP），内置 TLS，消除 TCP 队头阻塞 |

**HTTP/3 关键点**：Google 2012 年开发 QUIC，2021 年 RFC 正式化。QUIC = UDP + 可靠性 + 安全层，减少握手轮次，目前约占互联网流量 1/3。

**HTTP 被"滥用"为通用传输的原因**：防火墙基本不封 80/443 端口，所以 SOAP、REST、AJAX、实时音视频全都往 HTTP 上堆——不是因为技术最优，而是因为能**穿透防火墙**。

---

## Part B：实时通信

### 十二、什么是"实时"

实时没有统一标准，取决于应用能容忍的上限：

| 维度 | 视频 | 音频 | 控制信号 |
|------|------|------|----------|
| 丢包容忍度 | 高（丢 90% 还凑合）| 低（丢 10% 就难以理解）| 极低（"停刀"消息不能丢）|
| 延迟容忍度 | 中 | 低 | 极低 |

| 应用类型 | 特点 | 常用协议 |
|----------|------|----------|
| Streaming（单向流媒体）| 可接受较大延迟，能预缓冲 | TCP/HTTP/CDN |
| Interactive Real-time（视频会议）| 低延迟优先 | UDP/RTP |

### 十三、为什么实时通信困难

Internet 是 **best-effort** 网络：只尽力转发，不保证延迟、不保证送达、不保证顺序。

实时通信面临三大问题：

| 问题 | 定义 |
|------|------|
| **Latency（延迟）**| 包从发送端到接收端的基本传播时延 |
| **Jitter（抖动 / PDV）**| 不同包的到达时间不一致，延迟的随机波动 |
| **Packet Loss（丢包）**| 包在网络中消失，或到达太晚被应用丢弃 |

> **Latency vs Jitter**：Latency 是整体慢；Jitter 是忽快忽慢。Jitter 典型值约 15ms，大致等于一帧视频时长（60fps ≈ 16ms/帧）。

**"等效丢包"**：有些包物理上已到达接收端，但超过了 `maximum acceptable delay`（最大可接受播放延迟），对应用来说等同于丢失。

### 十四、接收端缓冲区

接收端建立 `receive buffer + playout buffer` 来平滑 jitter，将乱序到达的包排列成稳定的播放流。

**核心 trade-off：**

| 缓冲区大小 | 延迟 | 抗 Jitter 能力 |
|------------|------|----------------|
| 大 | 高 | 强（容忍更大波动）|
| 小 | 低 | 弱（稍有延迟就丢帧）|

实时性（低延迟）和平滑性（抗抖动）是互相拉扯的。

### 十五、补救机制

| 机制 | 原理 | 备注 |
|------|------|------|
| **重传（Retransmission）** | 检测到丢包后请求重发 | 需要额外 RTT，实时场景通常太慢；组播场景例外（邻近节点代发）|
| **弹性缓冲（Elastic Buffer）** | 丢包多时扩大缓冲、播放变慢；网络恢复后收缩、快速追赶 | Zoom 上人物动作突然"变快"的原因 |
| **前向纠错（FEC）** | 发送端提前附带冗余信息，接收端本地重建丢失内容 | 用额外带宽换低延迟可靠性，适合 RTT 大或无线环境 |
| **码率自适应（Codec Adaptation）** | 网络差时降低码率/分辨率 | YouTube 自动切换到 360p 的原因 |
| **并行传输** | 在后续帧中附带前一帧的低质量副本 | 低码率备份保底 |

#### FEC 原理

FEC（Forward Error Correction）= **提前把"修复材料"一起发出去**，不等丢包后再重传。

最简单的例子：
```
发送 P1, P2, P3 和冗余包 R = P1 XOR P2 XOR P3
若接收端丢了 P2，则 P2 = P1 XOR P3 XOR R（本地恢复）
```

**Adaptive FEC**：根据网络状况动态调整冗余比例：
- 网络稳定 → 少发冗余，节省带宽
- 网络变差 → 多发冗余，提高恢复能力
- 通过 RTCP 反馈（丢包率、延迟、抖动）驱动调整

FEC 的代价：额外带宽开销；对突发连续丢包效果有限。

### 十六、实时传输协议栈

| 协议 | 职责 | 特点 |
|------|------|------|
| **RTP** | 承载实时媒体数据 | 跑在 UDP 之上；头部含序列号、时间戳、SSRC；支持唇音同步、多语言 |
| **RTCP** | RTP 的控制与反馈 | 奇数端口（RTP 偶数端口）；上报丢包率、延迟、jitter；驱动发送端调整码率/FEC |
| **SIP** | 建立/终止通话 | 类似 HTTP 的文本协议；用于 VoIP；Zoom/WhatsApp/Teams 均不用 SIP，各有私有协议 |
| **SDP** | 协商媒体参数 | 协商编解码器、分辨率等；配合 SIP 使用 |
| **RTSP** | 单向流媒体控制 | 支持 PLAY/PAUSE/SEEK；常见于监控摄像头 |
| **DASH** | 基于 HTTP 的自适应流媒体 | 无服务端状态；可复用 HTTP 缓存/CDN；YouTube 灰色进度条 = 预取缓冲 |

**完整视频会议协议分工：**
```
SIP  → 建立/结束 call
SDP  → 协商媒体参数（编解码器、分辨率）
RTP  → 传输音视频媒体流
RTCP → 传输反馈，驱动自适应调整
```

### 十七、Streaming vs Interactive Real-time

| 维度 | Streaming（单向流媒体）| Interactive（视频会议）|
|------|----------------------|----------------------|
| 方向 | 单向 pull | 双向 |
| 延迟容忍 | 高（可 buffer 数秒）| 低（<150ms 体验好）|
| 丢包响应 | 降码率、buffer 补偿 | 必须实时处理 |
| 带宽不足时 | 暂停 + 重新填充缓冲 | 降质量 / 卡顿 |
| 常用协议 | DASH/HTTP/CDN | RTP/UDP |

**RTSP vs DASH**：RTSP 协议上更"优雅"（类 HTTP 操作集：OPTIONS/DESCRIBE/SETUP/PLAY），但现实中 YouTube/Netflix 都选 DASH over HTTP，原因是：HTTP 能穿防火墙、有成熟的 CDN/proxy 生态、HTML5 内建播放器。

> **核心结论**：从协议设计最优看，也许不该都用 HTTP；从现实部署最方便看，HTTP 经常赢。

### 十八、丢包的根本原因

**A. 网络中真的丢失：**
- **拥塞/队列溢出**：路由器 buffer 满，后来的包被直接丢弃
- **链路带宽不足**：带宽或路由器处理能力跟不上
- **路径变化**：包走不同路径，某些包被重路由、碎片化，到达异常
- **无线误码**：信号弱/干扰导致比特损坏，下层纠错失败则整包丢弃

**B. 到达但已无用（等效丢包）：**
- **Jitter 过大**：延迟波动超出 playout buffer 范围
- **超过播放截止时间**：物理上已到接收端，但已错过播放窗口
- **接收端 buffer 过小**：socket buffer 满、应用线程来不及处理
- **系统主动丢弃**：OS 或应用为保持低延迟，主动丢弃晚到的包

---

## 十九、知识点速查

### HTTP 核心概念

| 概念 | 要点 |
|------|------|
| 网页结构 | HTML 主文件 + 多个附属对象 |
| HTTP stateless | 每个请求独立，靠 Cookie/Token 维持状态 |
| 持久连接 | HTTP/1.1：一条 TCP 复用多请求 |
| 队头阻塞 | Pipelining 中前面对象卡住，后面全等 |
| 缓存验证 | ETag/If-None-Match；Last-Modified/If-Modified-Since |
| CDN | DNS 引导用户到最近节点；预先推送热门内容 |
| HTTP/3 | QUIC over UDP，内置 TLS，消除 TCP 队头阻塞 |

### Realtime 核心概念

| 概念 | 要点 |
|------|------|
| Latency | 整体传播延迟 |
| Jitter | 延迟的随机波动（忽快忽慢）|
| 等效丢包 | 到得太晚 = 对应用等于丢失 |
| Buffer trade-off | 大缓冲低丢包高延迟；小缓冲低延迟高丢包 |
| FEC | 提前发冗余，本地恢复；用带宽换延迟 |
| RTP/RTCP | RTP 传内容；RTCP 传反馈 |
| SIP | 建立/结束通话信令（不传媒体）|
| DASH | HTTP 上的自适应流媒体 |
