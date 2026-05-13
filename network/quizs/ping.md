# ping 快速参考

## 一句话定义

ping 是最基础的网络诊断工具：向目标发一个"你在吗"的包，看对方能不能回应、回应要多久。

**心智模型：声呐**

```
声呐：发出声波 → 碰到物体反弹 → 计算时间 → 判断距离和是否存在
ping：发出 ICMP 包 → 目标回包   → 计算时间 → 判断连通性和延迟
```

ping 用的协议是 ICMP（Internet Control Message Protocol），不是 TCP 也不是 UDP，是网络层的控制协议。它不建立连接，只发一个 echo request，等对方回一个 echo reply。

---

## 读懂 ping 输出

```
$ ping api.github.com

PING api.github.com (4.237.22.34): 56 data bytes
64 bytes from 4.237.22.34: icmp_seq=0 ttl=112 time=12.345 ms
64 bytes from 4.237.22.34: icmp_seq=1 ttl=112 time=11.892 ms
64 bytes from 4.237.22.34: icmp_seq=2 ttl=112 time=13.201 ms
^C
--- api.github.com ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 11.892/12.479/13.201/0.537 ms
```

| 字段 | 含义 | 怎么判断好坏 |
|------|------|------------|
| `icmp_seq` | 第几个包（从 0 开始） | 序号不连续 = 有丢包 |
| `ttl=112` | 包还能经过多少跳路由器 | Linux 初始 64，Windows 128，每过一跳减 1；可估算跳数 |
| `time=12ms` | 往返延迟（RTT） | 同城 <10ms，跨国 50–200ms，>500ms 很慢 |
| `packet loss` | 丢包率 | 0% 正常，>5% 有问题，>20% 严重 |
| `stddev` | 延迟抖动 | 越小越稳定，高抖动导致语音/视频卡顿 |

---

## 常用命令

### 基础用法

```bash
# 最简单的 ping（macOS/Linux 默认不停，Ctrl+C 中断）
ping google.com

# 只 ping 指定次数
ping -c 4 google.com

# ping IPv6 地址
ping6 google.com
# 或
ping -6 google.com
```

### 控制行为

```bash
# 加快频率（默认 1 秒一次，改为 0.2 秒）
ping -i 0.2 google.com

# 指定包大小（默认 56 字节，测大包网络表现）
ping -s 1400 google.com

# 指定每个包的超时时间（等待 2 秒没响应就算超时）
ping -W 2 google.com

# 组合：只 ping 10 次，每次等 1 秒，包大小 512 字节
ping -c 10 -i 1 -s 512 google.com
```

### 诊断场景

```bash
# 场景1：服务挂了？先判断是网络问题还是应用层问题
ping your-server.com
# 通   → 网络没问题，是应用层出了事，接着用 curl 诊断
# 不通 → 网络层有问题，或对方屏蔽了 ICMP

# 场景2：验证 DNS 解析是否正确（第一行会显示解析到的 IP）
ping my-domain.com

# 场景3：持续监控，看网络是否稳定（观察偶发丢包或延迟 spike）
ping -i 1 8.8.8.8

# 场景4：测量到某个地区的延迟
ping tokyo.server.com

# 场景5：测试本机网络栈是否正常（ping 回环地址）
ping 127.0.0.1

# 场景6：测试局域网网关是否通（先确认本机 → 网关这段）
ping 192.168.1.1
```

---

## 5 种典型结果

```bash
# 1. 正常
64 bytes from 1.1.1.1: icmp_seq=0 ttl=57 time=5.2 ms

# 2. 完全不通（域名解析成功，但主机不响应或防火墙屏蔽 ICMP）
Request timeout for icmp_seq 0

# 3. 域名解析失败（DNS 有问题）
ping: cannot resolve xyz.invalid: Name or service not known

# 4. 网络根本不通（连路由器都到不了）
ping: sendto: Network is unreachable

# 5. 丢包（icmp_seq 序号出现断层）
64 bytes from 1.1.1.1: icmp_seq=0 ttl=57 time=5.2 ms
64 bytes from 1.1.1.1: icmp_seq=1 ttl=57 time=5.1 ms
                                   ↑ icmp_seq=2 缺失 = 丢了一个包
64 bytes from 1.1.1.1: icmp_seq=3 ttl=57 time=5.3 ms
```

> **重要认知：ping 超时 ≠ 服务挂了。** 防火墙可以屏蔽 ICMP 同时放行 TCP 80/443。ping 不通但 `curl` 正常是完全可能的。

---

## 常用 Flag 速查

| Flag | 作用 | 示例 |
|------|------|------|
| `-c <n>` | 只发 n 个包 | `ping -c 4 google.com` |
| `-i <sec>` | 发包间隔（秒） | `ping -i 0.5 google.com` |
| `-s <bytes>` | 指定包大小 | `ping -s 1400 google.com` |
| `-W <sec>` | 每包超时时间 | `ping -W 2 google.com` |
| `-t <ttl>` | 设置 TTL 值 | `ping -t 10 google.com` |
| `-6` | 强制 IPv6 | `ping -6 google.com` |
| `-4` | 强制 IPv4 | `ping -4 google.com` |

---

## ping vs 其他诊断工具的分工

| 工具 | 能诊断什么 | 不能诊断什么 |
|------|-----------|------------|
| `ping` | IP 层连通性、延迟、丢包 | 应用层是否正常（HTTP、数据库等） |
| `traceroute` | 数据包经过哪些路由器、哪一跳延迟高 | 应用层问题 |
| `curl` | HTTP 应用层是否正常 | 网络层的丢包和路由问题 |
| `nslookup / dig` | DNS 解析是否正确 | 网络连通性 |

**诊断顺序：**

```
ping 127.0.0.1      → 本机网络栈正常？
ping 192.168.1.1    → 本机到网关通？
ping 8.8.8.8        → 能到公网？
ping google.com     → DNS 解析正常？
curl https://...    → 应用层服务正常？
```

---

## TTL 推断跳数

TTL 初始值因系统而异：

| 操作系统 | 默认 TTL |
|---------|---------|
| Linux | 64 |
| macOS | 64 |
| Windows | 128 |
| 网络设备（Cisco 等） | 255 |

收到的 TTL = 初始值 - 经过的跳数。例如收到 `ttl=112`，对方是 Windows（128），则经过了 128 - 112 = **16 跳**。
