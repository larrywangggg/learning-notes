# MQTT 实验复习笔记

> 本笔记把本周 lab 的动手实验现象，对应到 exam-style 考题。每一条都有「亲手验证的证据」，不是死记。
> 环境：macOS + 本地 broker（`mosquitto -v`）+ `mosquitto_pub` / `mosquitto_sub` + Wireshark。

---

## 0. 基础：三个程序 + 工作模型

| 程序 | 角色 | 行为 |
|---|---|---|
| `mosquitto` | **broker**（服务端） | 在 1883 端口监听，接收所有连接，存订阅关系，转发消息 |
| `mosquitto_pub` | 发布者 | 连接 → 发一条 → **立即断开**（像传感器醒来推一次就睡） |
| `mosquitto_sub` | 订阅者 | 连接 → **一直挂着**收消息，直到 Ctrl-C |

**核心模型**：发布者和订阅者**从不直接通信**，全靠 broker 中转。抓包里同一条消息出现两次（pub→broker、broker→sub）就是证据 —— 这就是 pub/sub **解耦**。

常用 flag：`-h` host，`-t` topic，`-m` message（pub），`-q` QoS，`-r` retain（pub），`-v` verbose（sub），`-p` port（默认 1883）。

---

## 1. 为什么 MQTT 报文这么紧凑简单？（对比 HTTP）

**因为目标场景是 IoT / 受限环境**：低带宽、高延迟、弱设备、电池供电。每个字节、每次解析都是成本。

紧凑来源：
- 固定头部最小 **2 字节**（1 字节类型+标志，1 字节起变长的剩余长度）。HTTP 是一堆 ASCII 文本头部，动辄几百字节。
- **二进制协议**，不是文本，解析极简，弱 MCU 扛得住。
- **状态在连接上**（订阅关系、会话存在 broker 端），不像 HTTP 每个请求都带满上下文。

**抓包证据**：QoS 0 的一条 PUBLISH 才几十字节；确认包（PubAck 等）只有几个字节 —— 单个 bit 当 flag 用。

---

## 2. 消息是即时流，broker 默认不存历史

**实验**：
```bash
# 没人订阅时先发
mosquitto_pub -h localhost -t "3311/larrywang" -m "msg1"
# 然后才订阅
mosquitto_sub -h localhost -t "3311/#" -v
```
**结果：收不到 msg1。**

**为什么**：broker 收到 PUBLISH，只转发给「此刻正在订阅」的客户端，转发完立即丢弃。发 msg1 时无人订阅，当场蒸发。

> 对应 lab 原话："messages are deleted by the broker as soon as possible after publishing."

---

## 3. retain：让 topic 的「最新值」对未来订阅者可见

**实验**：
```bash
mosquitto_pub -h localhost -t "3311/larrywang" -m "msg2" -r   # 带 -r
mosquitto_sub -h localhost -t "3311/#" -v                      # 之后才订阅
```
**结果：收到 msg2。** 唯一变量就是 `-r`。

**机制**：
- broker 为每个 topic 留底**最后一条** retained 消息。
- 任何**新订阅者**一连上，立即收到这条最新值，不用干等下一次发布。
- 重新订阅会**反复收到**它（赖着不走），不像普通消息阅后即焚。

**覆盖与清除**：
- 再发一条带 `-r` 的新消息 → **覆盖**旧的留底。
- 发**空消息**带 `-r`：`mosquitto_pub ... -m "" -r` → **删除**该 topic 的留底。

**何时有用**：状态型/低频数据（开关状态、配置、在线状态）。新上线设备需要立即知道「现在是什么状态」。
**何时不该用**：高频遥测流（温度每秒一发），留底没意义、还可能误导。

---

## 4. 通配符 `+` 和 `#`

两条规则：
- **`+`**：匹配**恰好一层**（单层占位）。`a/+/c` 匹配 `a/x/c`，不匹配 `a/x/y/c`。
- **`#`**：匹配**该层及以下所有层**，**只能放末尾**。`a/#` 匹配 `a`、`a/x`、`a/x/y`…
  - 关键细节：`a/#` 的 `#` 连 `a` 节点**本身**也算匹配（实验里 `larrywang/+/kitchen/#` 收到了只有 3 层的 `heater/kitchen` 就是这个原因）。
  - `#` 默认**不匹配** `$` 开头的主题（如 `$SYS`），避免被 broker 内部消息淹没。

**测试用的主题树**（故意层级不对称）：
```
larrywang/light/kitchen/ceiling
larrywang/light/kitchen/wall
larrywang/light/bedroom/ceiling
larrywang/heater/kitchen
larrywang/heater/bedroom
```

| 需求 | pattern | 结果 |
|---|---|---|
| (a) 所有灯 | `larrywang/light/#` | 3 条 light，不含 heater ✓ |
| (b) 某房间某类型全部 | `larrywang/light/kitchen/+` | kitchen 的 2 条灯 ✓ |
| (c) **某房间所有开关不分类型** | （见下方坑） | ⚠️ 无法稳健表达 |
| (d) 我发布的全部 | `larrywang/#` | 全部 ✓ |

### (c) 那个坑 —— 整个练习的精华
"kitchen" 在 light 子树里是第 3 层、在 heater 子树里也是第 3 层但**总深度不同**；换个设计（`room/type`）它甚至会跑到第 2 层。**MQTT 通配符严格按「层级位置」匹配**，一旦同一语义概念出现在不固定的层级深度，就**没有单一 pattern 能稳健表达**「这个房间的所有东西」。这次 `larrywang/+/kitchen/#` 凑巧对，是因为树长得刚好。

**设计启示**：层级顺序是个要提前想清楚的设计决策。若「按房间查」常见，就把 room 固定在同一层（`uniid/<room>/<type>/<pos>`），这样 `uniid/<room>/#` 就能干净表达。

---

## 5. 为什么提供多级 QoS？两侧为何可不同？（Wireshark 实物证据）

**因为不同消息对可靠性的需求不同，而可靠性有代价**（额外往返、确认、状态）。给应用按场景取舍的控制权。

抓包（`-q 0/1/2` 各发一条，过滤 `mqtt && !(mqtt.topic contains "$SYS")`）：

| QoS | 握手报文 | 报文数 | 保证 | 代价 / 适用 |
|---|---|---|---|---|
| 0 | `Publish`（无 id、无确认） | 1 | at most once 至多一次 | 零开销，可丢。高频遥测 |
| 1 | `Publish(id)` + `PubAck(id)` | 2 | at least once 至少一次 | 1 确认，可能重复。需幂等 |
| 2 | `Publish` → `PubRec` → `PubRel` → `PubComp`（全带 id） | 4 | exactly once 恰好一次 | 两轮往返，最贵。扣款/开闸 |

**关键观察**：
- **报文数 1→2→4 阶梯上升** = 可靠性越高、开销越大。
- **`(id=N)` 报文标识符**：QoS 0 没有；QoS 1/2 必有 —— 靠它把后续确认包跟原始 PUBLISH 对应起来。这个 id 的有无本身就是 QoS 0 vs 1/2 的报文级区别。

**为什么 broker 两侧 QoS 可不同**：
MQTT 是 **hop-by-hop**，不是端到端。broker 解耦了两段传输：
- 第一段：publisher 用某 QoS 发给 broker。
- 第二段：broker 按**每个订阅者各自声明的 QoS** 分发。
- 实际生效 QoS = `min(发布 QoS, 订阅 QoS)`（分发时降级取较低者）。

例：传感器 QoS 1 发布；仪表盘订 QoS 0（不在乎丢），告警系统订 QoS 1（不能丢）→ 同一消息 broker→仪表盘走 0、broker→告警走 1。发布者无需知道下游是谁、各自要什么。这正是 pub/sub 解耦的价值。

---

## 6. DHT 为什么搞不定通配/正则/泛化搜索？（与 MQTT 通配符同构）

DHT 的定位靠**精确哈希**：`lookup(exact_key) → value`。哈希**摧毁了 key 之间的语义/字典序关系**（`cat` 和 `cats` 落在无关位置），所以：
- 通配 `cat*`：不知具体 key，无法预先算哈希定位，只能全网扫描（恰是 DHT 要避免的 O(N)）。
- 正则/范围：哈希破坏局部性，范围在哈希空间里散落，没有节点「负责一段连续语义区间」。

**与本周的联系**：DHT 和 MQTT 通配符是**同一类问题** ——
> **查询能力被数据的组织结构锁死。** DHT 用哈希组织 → 只能精确查；MQTT 用固定层级组织 → 只能按层级位置通配。想支持更灵活的查询，要么改数据组织方式，要么在上层另建索引。原生机制做不到。

---

## 7. $SYS 是什么

`$SYS` = **system**。MQTT 约定的保留主题前缀，broker 用它**自报状态**（连接数、负载、收发字节、uptime…），由 broker 周期性自动发布，客户端只能订阅、不能发布。以 `$` 开头表示「特殊、非业务」，通配符 `#` 默认不匹配它。

```bash
mosquitto_sub -h localhost -t '$SYS/#' -v   # 注意单引号，$ 是 shell 特殊字符
```
看 `$SYS/broker/load/...` 系列最能反映当前 server load。

