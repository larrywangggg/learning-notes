# 分布式系统 & DevOps 核心概念

## 一、什么是分布式系统

**定义**：多台机器协作，对外表现为一个系统。

**为什么要分布式？** 单机有天花板：

| 问题 | 后果 |
|------|------|
| 算力/内存/磁盘有限 | 无法处理大规模请求 |
| 单点故障 | 服务全挂 |
| 无法横向扩展 | 流量高峰扛不住 |

分布式系统解决：**scalability**（可扩展）、**availability**（高可用）、**fault tolerance**（容错）、**performance**（性能）。

**为什么分布式难？** 引入了额外复杂性：
- 机器之间网络随时可能断
- 节点随时可能挂
- 多份数据副本，哪份算最新？
- 请求超时后 retry，会不会重复写入？
- 扩容时数据如何迁移？

---

## 二、核心概念

### 1. Replication（复制）

同一份数据存多份副本，分布在不同节点。

**目的**：提高可用性和容灾能力。

**例子**：PostgreSQL 主从复制。一个 primary 节点挂了，replica 可以被提升（promote）为新的 primary，服务不中断。Cassandra 默认 replication factor = 3，同一行数据会存在 3 个节点上，任意 1 个节点宕机不影响读写。

**代价**：
- 存储成本增加
- 写入需要同步多个副本，延迟可能增加
- 需要处理数据一致性问题

---

### 2. Partitioning / Sharding（分片）

把不同的数据拆到不同机器上（与 replication 相反——replication 是同一份数据复制多份）。

**类比**：
- Replication = 把同一本书印 3 本，放 3 个书架
- Sharding = 把一本书拆成上中下三册，分放 3 个书架

**例子**：一张 1 亿行的用户表，按 user_id 分片：
- Shard A：user_id 1 ~ 3000 万
- Shard B：user_id 3000 万 ~ 6000 万
- Shard C：user_id 6000 万 ~ 1 亿

**目的**：分担存储和查询压力，支持横向扩展。

**代价**：跨 shard 的 join 和事务变得困难；shard key 选不好会导致热点（某一个 shard 特别忙）。

> 生产系统通常两者结合：先 sharding，每个 shard 再做 replication。

---

### 3. Vertical Scaling vs Horizontal Scaling

| | Vertical Scaling（纵向扩展）| Horizontal Scaling（横向扩展）|
|---|---|---|
| 方式 | 升级单台机器配置（更多 CPU/内存/磁盘）| 增加更多机器 |
| 优点 | 简单，无需改动架构 | 理论上无上限，适合大规模 |
| 缺点 | 有硬件上限；贵；单点风险不变 | 系统复杂，数据同步、请求路由更难 |

Kafka、Cassandra 的核心卖点之一是对 horizontal scaling 友好。

---

### 4. Availability（高可用）

服务在部分组件故障时是否仍然可用。

**例子**：
- 一个 3 节点的 Cassandra cluster，1 个节点宕机后，其他 2 个节点仍可响应请求 → 高可用
- 一个没有 replica 的单节点数据库，宕机后服务立即不可用 → 单点故障（SPOF）

可用性通常用 SLA 百分比表示：99.9%（三个九）= 每年最多约 8.7 小时停机；99.99%（四个九）= 每年约 52 分钟。

---

### 5. Fault Tolerance（容错）

系统在部分组件出故障时，仍能继续工作的能力。

**例子**：
- Kafka：一个 broker 挂了，topic 的其他副本（replica）仍可提供服务
- 多 AZ 部署：AWS 某个 Availability Zone 出问题，流量自动切换到其他 AZ

与高可用关系密切，fault tolerance 更强调"面对故障时的设计"，高可用更强调"服务可用的程度"。

---

### 6. Failover（故障切换）

主节点故障时，系统自动切换到备用节点。

**例子**：
- PostgreSQL：primary 宕机 → 监控系统检测到 → 将某个 replica promote 为新 primary → 连接切换 → 恢复服务
- DNS failover：主区域不健康时，DNS 自动指向备用区域

**关键指标**：RTO（Recovery Time Objective，恢复目标时间）——failover 需要多长时间。

---

### 7. Consistency（一致性）

当一份数据在多台机器上都有副本时，所有节点看到的数据是否一致。

**例子**：用户在 Node A 上更新了邮箱，Node B 上读到的还是旧邮箱 → 出现了不一致。

#### Strong Consistency（强一致性）
写入成功后，后续任何节点读到的一定是最新值。

- 优点：语义清晰，对业务安全
- 缺点：延迟更高，系统设计更复杂
- 例子：关系型数据库（PostgreSQL）的 ACID 事务

#### Eventual Consistency（最终一致性）
写入后不保证所有节点立刻同步，但最终会一致。

- 优点：性能更好，可用性更高
- 缺点：存在短暂的"脏读"风险
- 例子：Cassandra、DNS 更新传播（改了 DNS 记录后需要等待 TTL 过期才全局生效）

---

### 8. CAP Theorem

分布式系统遇到 **网络分区（Partition）** 时，不可能同时完全满足：
- **C**onsistency（一致性）
- **A**vailability（可用性）
- **P**artition Tolerance（分区容错）

由于网络分区在生产环境中无法避免（P 必须保证），系统设计实际上是在 **C 和 A 之间取舍**：

| 系统类型 | 倾向 | 例子 |
|------|------|------|
| CP | 一致性 > 可用性 | 传统关系型数据库、ZooKeeper |
| AP | 可用性 > 一致性 | Cassandra、DynamoDB |

> 分布式系统没有"全满分"，所有设计都是 trade-off。

---

### 9. Idempotency（幂等性）

同一个操作执行一次和执行多次，结果相同。

**为什么重要？** 因为网络超时后 client 会 retry。如果操作不幂等，retry 就会产生重复副作用。

| 操作 | 是否幂等 | 原因 |
|------|------|------|
| `PUT /users/1 { status: "disabled" }` | ✅ 是 | 多次执行结果不变 |
| `POST /orders { item: "coffee" }` | ❌ 否 | 每次都会创建一个新订单 |
| `DELETE /sessions/abc123` | ✅ 是 | 删除后再删，结果相同（不存在了） |

**实现方式**：通常使用 **idempotency key**（幂等键）。客户端每次请求携带唯一 key，服务端记录已处理的 key，重复请求直接返回之前的结果而不重复执行。

---

### 10. Observability（可观测性）

知道系统现在的状态，出问题时能快速定位。三大支柱：

| 类型 | 内容 | 例子 |
|------|------|------|
| **Logs** | 程序事件记录 | 报错信息、请求日志、状态变化 |
| **Metrics** | 可量化指标 | CPU 使用率、请求延迟、错误率、队列深度 |
| **Traces** | 跨服务调用链路 | 一个 HTTP 请求经过了哪些微服务、每一步耗时多少 |

**例子**：一个 API 请求变慢了，靠 traces 可以看到是调用链中哪一步（数据库查询？外部 API 调用？）引起了延迟，而不是只看到"整体慢了"。

---

### 11. Single Point of Failure（单点故障）

某个组件挂了就导致整个系统挂掉。消灭 SPOF 是分布式系统设计的重要目标之一。

**常见 SPOF 场景及解决方案**：
- 只有 1 个数据库 primary → 加 replica + failover
- 只有 1 个 load balancer → 部署多个 LB，DNS 层做冗余
- 只有 1 个 config service → 加副本，或用分布式配置中心（如 Consul、etcd）
- 跨 AZ 只在 1 个 AZ 有服务 → 多 AZ 部署

---

## 三、相关技术定位

### Kafka — Event Streaming Platform

高吞吐、可持久化的消息系统，用于系统间**解耦**和**异步处理**。

和传统消息队列（如 RabbitMQ）的核心区别：消息消费后**不删除**，默认保留 7 天，任何 consumer 可以随时回放历史消息。

---

#### Producer / Consumer / Topic

最简单的理解：Kafka 像一个**广播电台**。

- **Topic** 是"频道"（比如"订单事件频道"、"用户行为频道"）
- **Producer** 是往频道里播内容的人（发消息）
- **Consumer** 是收听频道的人（读消息）

**实际场景**：电商下单流程

用户点击"下单"后，订单服务不需要自己去调用库存服务、通知服务、积分服务——只需要往 Kafka 的 `order-created` topic 里写一条消息。其他服务各自订阅这个 topic，独立处理：

```
用户下单
  → 订单服务写数据库，同时发消息到 Kafka topic: order-created
       ├── 库存服务（消费）→ 扣减库存
       ├── 通知服务（消费）→ 发短信/邮件给用户
       ├── 积分服务（消费）→ 给用户加积分
       └── 数据分析服务（消费）→ 记录销售数据
```

好处：订单服务不需要知道下游有哪些服务，下游加新服务不需要改订单服务代码。如果通知服务临时挂了，消息还在 Kafka 里，恢复后继续消费，不丢消息。

---

#### Partition（分区）

一个 Topic 可以有多个 Partition，每个 Partition 是一段独立的有序日志。

**为什么要分 Partition？** 单个 Partition 只能被一个 Consumer 处理，Partition 越多，并行处理能力越强。

**实际场景**：外卖平台的订单消息

假设 `order-created` topic 有 3 个 Partition：
```
Partition 0: [北京的订单]
Partition 1: [上海的订单]
Partition 2: [广州的订单]
```

3 个 Consumer 实例同时工作，每人处理一个城市的订单，互不干扰，吞吐量是单 Partition 的 3 倍。

**关键限制**：顺序只在单个 Partition 内保证。如果你需要同一个用户的操作按顺序处理，必须保证同一用户的消息进同一个 Partition（用 user_id 作为 key）：

```
# 同一个 user_id 的消息，经过 hash 后总是进同一个 Partition
producer.send("user-events", key="user_42", value="加入购物车")
producer.send("user-events", key="user_42", value="下单")
producer.send("user-events", key="user_42", value="支付")
# 以上三条消息保证顺序，因为同一个 key → 同一个 Partition
```

---

#### Offset（偏移量）

每条消息在 Partition 内都有一个唯一递增编号（从 0 开始），这就是 offset。Consumer 自己记录"我消费到哪了"。

**实际场景**：消费失败后重新处理

假设你的数据处理服务在处理第 500 条消息时崩溃了：

```
Partition 0: [0][1][2]...[498][499][500 ← 崩溃点][501][502]...
                                          ↑
                              consumer 记录的 offset = 499（已提交）
```

服务重启后，从 offset 500 开始重新消费，不会从头来，也不会跳过未处理的消息。

**更强大的用法（Replay）**：新上线一个推荐系统，需要分析过去 3 天的用户行为数据。不需要从数据库里捞，直接把 `user-behavior` topic 的 offset 重置到 3 天前，重新消费即可。

---

#### Consumer Group（消费者组）

多个 Consumer 实例组成一个 Group，Kafka 自动把 Partition 分配给 Group 内的各个 Consumer。

**实际场景**：扩容处理能力

双十一活动，订单量是平时的 10 倍，单个 Consumer 处理不过来：

```
# 平时：1 个 Consumer 处理 3 个 Partition
Consumer A → Partition 0, 1, 2

# 双十一扩容到 3 个 Consumer（同一个 Consumer Group）
Consumer A → Partition 0
Consumer B → Partition 1
Consumer C → Partition 2
# 处理速度提升 3 倍
```

**同一份数据，多个业务独立消费**：

`order-created` 这一份消息，库存服务和通知服务属于不同的 Consumer Group，各自维护自己的 offset，互不影响：

```
order-created topic
  ← Consumer Group: inventory-service（库存服务，消费到 offset 1000）
  ← Consumer Group: notification-service（通知服务，消费到 offset 980，稍慢一点）
  ← Consumer Group: analytics-service（分析服务，消费到 offset 500，批量处理）
```

---

#### 为什么 Kafka 高吞吐？

| 机制 | 类比 | 效果 |
|------|------|------|
| 顺序写磁盘 | 像流水线记账，不翻页查找 | 比随机写快 100 倍以上 |
| 批量发送/消费 | 像快递公司攒一车再发，而不是一件一件送 | 大幅减少网络请求次数 |
| Zero-copy | 数据不经过应用内存，直接磁盘→网卡 | 减少 CPU 拷贝开销 |
| Partition 并行 | 多条流水线同时工作 | 吞吐线性扩展 |

**实际场景**：LinkedIn（Kafka 的发明者）用 Kafka 每天处理超过 **7 万亿条消息**。Netflix 用 Kafka 追踪用户在所有设备上的实时行为用于推荐系统。

---

#### 典型使用场景总结

| 场景 | 具体例子 |
|------|------|
| **系统解耦** | 订单服务不直接调库存/通知，通过 Kafka 异步通知 |
| **流量削峰** | 秒杀活动瞬间涌入 10 万请求，先全写入 Kafka，后端按能力逐步消费，不被压垮 |
| **日志收集** | 100 台服务器的日志统一写入 Kafka，再流向 OpenSearch 做检索 |
| **数据同步** | 数据库变更（通过 CDC）写入 Kafka，实时同步到搜索引擎、数仓 |
| **事件溯源** | 用户操作全部记录为事件，需要时可以从任意时间点回放，重建系统状态 |
| **实时计算** | 用户点击行为实时写入 Kafka，Flink 消费后实时计算 DAU、转化率等指标 |

---

### Cassandra — 分布式 NoSQL 数据库

面向大规模写入和水平扩展设计，牺牲强一致性换高可用。

核心设计哲学：**写入永远不失败**。Cassandra 宁愿返回稍旧的数据，也不愿因为某个节点挂掉而拒绝服务。

---

#### 无 Master 节点（Peer-to-Peer）

传统数据库（如 PostgreSQL）有一个 Primary 节点负责所有写入，Primary 挂了就需要 failover，有一段时间不可用。

Cassandra 完全不同：**所有节点地位平等，任何节点都可以接受读写请求**。

**实际场景**：Instagram 的用户动态

Instagram 有超过 10 亿用户，每秒产生海量的"点赞/评论/关注"事件。如果用传统主从数据库，Primary 节点会成为瓶颈。Cassandra 的所有节点都能写入，加机器就能线性扩展写入能力，Instagram 正是因此选择了 Cassandra 作为其 feeds 存储。

```
# 传统主从：所有写入都压在 Primary 上
Client → Primary → replica1
                 → replica2

# Cassandra：任意节点都能写，写入压力分散
Client → Node A ─┐
Client → Node B  ├─ 互相同步
Client → Node C ─┘
```

---

#### Consistent Hashing（一致性哈希）

Cassandra 用哈希函数决定一条数据存在哪个节点上，不需要一张"路由表"来记录哪条数据在哪里。

**实际场景**：存储物联网传感器数据

一个工厂有 10 万个传感器，每个传感器每秒上报温度数据。Cassandra 用 `sensor_id` 做哈希，同一个传感器的所有数据自动落到同一组节点上，查询时直接定位，不需要扫全表：

```
hash("sensor_001") → 落到 Node A、B、C（replication factor=3）
hash("sensor_002") → 落到 Node B、C、D
hash("sensor_003") → 落到 Node C、D、A
```

新增节点时，只需要迁移部分数据，不需要重新分配所有数据（这是"一致性哈希"相比普通哈希的优势）。

---

#### Replication Factor & 写入流程

`replication_factor = 3` 表示每条数据写入 3 个不同节点。

**实际场景**：跨数据中心容灾

Netflix 用 Cassandra 存储用户观看历史，在多个 AWS Region 都有副本。即使整个 us-east-1 区域出问题，us-west-2 和 eu-west-1 的副本仍可提供服务，用户不会看到报错：

```
用户写入"观看了《纸牌屋》第 3 集"
  → 同时写入 us-east-1（Node A）
  → 同时写入 us-west-2（Node B）
  → 同时写入 eu-west-1（Node C）
任意一个区域挂掉，其他两个继续服务
```

**Consistency Level（一致性级别）**可以按需调整，写入时可以选择等待多少个副本确认：

| Consistency Level | 含义 | 适用场景 |
|---|---|---|
| `ONE` | 1 个节点写成功即返回 | 日志、监控数据，允许少量丢失 |
| `QUORUM` | 多数节点（如 3 中的 2）写成功才返回 | 大多数业务场景，平衡性能与可靠性 |
| `ALL` | 所有副本都写成功才返回 | 极少使用，性能差，一个节点挂就失败 |

---

#### 写入为什么快？

Cassandra 写入不直接改磁盘上的数据文件，而是：
1. 写入内存中的 **Memtable**（极快）
2. 同时追加写 **Commit Log**（顺序写，不随机 IO）
3. Memtable 满了后，批量刷到磁盘的 **SSTable**（不可变文件）

**实际场景**：Uber 的行程数据

Uber 每次行程会产生大量 GPS 位置更新（每隔几秒一条）。这类数据写多读少，对写入延迟敏感。Cassandra 的写入路径几乎全在内存操作，P99 写入延迟可以控制在个位数毫秒。

对比 PostgreSQL：每次写入需要找到数据在磁盘上的位置并原地修改（随机 IO），写入量大时性能显著下降。

---

#### 数据模型：按查询设计表（Query-Driven Design）

Cassandra 没有 JOIN，**表结构必须按照你的查询方式来设计**，这是和关系型数据库最大的思维转变。

**实际场景**：查询某用户的消息记录

在 PostgreSQL 里，你可能设计一张 `messages` 表，用 `WHERE user_id = ? ORDER BY created_at DESC` 查询。

在 Cassandra 里，表结构直接为这个查询服务：

```sql
CREATE TABLE messages_by_user (
    user_id   UUID,
    sent_at   TIMESTAMP,
    message   TEXT,
    PRIMARY KEY (user_id, sent_at)  -- user_id 是分区键，sent_at 是排序键
) WITH CLUSTERING ORDER BY (sent_at DESC);

-- 查询直接命中，不需要全表扫描
SELECT * FROM messages_by_user WHERE user_id = ? LIMIT 20;
```

同一个用户的所有消息存在同一个 Partition，按时间排好序，查询极快。

---

#### 适合 vs 不适合的场景

| 适合 | 不适合 |
|------|------|
| 时序数据（传感器、日志、监控指标） | 需要复杂 JOIN 的业务查询 |
| 用户行为/事件记录（点赞、浏览历史） | 多表事务（转账、库存扣减） |
| 大规模写入（每秒几十万次写） | 需要强一致性的场景（金融账务） |
| 全球多数据中心部署 | 数据模型经常变化、需要灵活 ad-hoc 查询 |
| 按已知 key 查单条或一批数据 | 需要聚合计算（SUM/GROUP BY 大量数据）|

**一句话判断**：如果你的系统**写多读少、数据量极大、需要高可用、查询模式固定**，考虑 Cassandra。如果你需要**事务、复杂查询、数据关系复杂**，用 PostgreSQL。

---

### PostgreSQL — 关系型数据库

ACID 事务强，SQL 生态成熟，适合业务系统核心数据存储。

**关键特性**：
- **MVCC**（Multi-Version Concurrency Control）：读不阻塞写，通过多版本实现并发控制
- **WAL**（Write-Ahead Log）：保证崩溃恢复，也是 replication 的基础
- **索引**：B-tree（默认）、GIN（全文搜索）、GiST 等
- **Streaming Replication**：异步/同步 replica，支持读写分离

**vs Cassandra**：

| | PostgreSQL | Cassandra |
|---|---|---|
| 一致性 | 强（ACID）| 最终一致（可调） |
| 扩展方式 | 垂直为主，水平难 | 水平扩展友好 |
| 写入性能 | 一般 | 极强 |
| 适合场景 | 业务事务、复杂查询 | 大规模写入、时序 |

---

### OpenSearch — 搜索与日志分析

基于 Elasticsearch 的分支，擅长全文搜索和日志聚合分析。

**适合场景**：
- 电商商品全文搜索
- 日志集中检索（ELK Stack 中的 E 换成 OpenSearch）
- 近实时聚合统计

**不适合**：作为主业务数据库（不支持事务，数据 schema 灵活但查询不如 SQL 直观）。

---

### ClickHouse — 列式分析数据库（OLAP）

**列式存储**：数据按列存，聚合查询（SUM、COUNT、AVG）只读需要的列，速度极快。

**适合场景**：报表、时间序列分析、用户行为漏斗分析、大规模 GROUP BY 查询。

**vs PostgreSQL**：

| | PostgreSQL (OLTP) | ClickHouse (OLAP) |
|---|---|---|
| 优化方向 | 事务、单行查询 | 聚合、批量分析查询 |
| 存储方式 | 行式 | 列式 |
| 写入方式 | 实时单行插入 | 批量写入 |

---

### Cadence — Workflow Orchestration

管理长流程异步任务，处理重试、状态追踪、超时。

**例子**：云数据库 provision 流程：
1. 接收创建请求
2. 调用云厂商 API 创建 VM
3. 等待 VM 启动（可能需要几分钟）
4. 安装数据库软件
5. 配置网络和安全组
6. 健康检查
7. 通知用户完成

每一步都可能失败，需要重试，不能用简单的 REST 调用链来实现。Cadence 将状态持久化，确保流程可靠执行。

---

## 四、DevOps 核心概念

### 什么是 DevOps

开发（Dev）与运维（Ops）的协作方式，通过自动化和工程化让软件更可靠、更快速地交付。

**核心原则**：
1. **自动化优于手工**：手工操作不可重复、容易出错
2. **环境可重复**：今天能部署，明天换个人也能部署
3. **开发关心生产**：merge 完代码不是终点，还要关心可部署性、可监控性、可排查性
4. **Infra 透明化**：工程师理解基础设施，而非将其视为黑盒

---

### CI/CD

**CI（Continuous Integration）**：代码频繁合并，每次合并自动触发 build、test、lint，尽早发现问题。

**CD（Continuous Delivery/Deployment）**：将通过 CI 的代码自动或半自动部署到环境中。

**典型流程**：
```
push code → trigger CI pipeline
  → run unit tests
  → run integration tests
  → build Docker image
  → push to registry
  → deploy to staging
  → (手动审批) → deploy to production
```

**工具**：GitHub Actions、Jenkins、GitLab CI、CircleCI。

---

### Infrastructure as Code（IaC）

用代码定义基础设施，而非手动点云平台页面。

**为什么重要**：
- **可重复**：同样的代码在 staging 和 production 部署出相同的环境
- **可版本控制**：infra 变更有 git history，可以 review、rollback
- **可审查**：PR review infra 变更，就像 review 业务代码一样
- **减少人为错误**：避免"某人手动改了配置，别人不知道"

**例子（Terraform）**：
```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  count         = 3  # 一行代码创建 3 台机器
}
```

---

### Monitoring & Alerting

**Monitoring**：持续采集系统状态指标（CPU、内存、延迟、错误率、磁盘）。

**Alerting**：指标超出阈值时自动通知（PagerDuty、Slack、邮件）。

**典型指标（以数据库服务为例）**：
- 查询延迟 p99 > 500ms → 告警
- 连接数 > 80% 上限 → 告警
- 磁盘使用率 > 85% → 告警
- Replication lag > 30s → 告警

---

### Incident Response

生产故障处理流程：

1. **发现**：告警触发或用户反馈
2. **止血**：先恢复服务（回滚、重启、切流量），再找原因
3. **确认范围**：影响了哪些用户、哪些功能
4. **修复 or 绕过**：临时方案先上，正式修复后跟进
5. **复盘**（Post-mortem）：无责复盘，分析 root cause，避免重现

**Runbook**：针对常见故障提前写好操作手册（先检查什么、如何 failover、如何扩容），减少故障时的决策压力。

---

## 五、DevOps 工具

| 工具 | 类型 | 核心用途 |
|------|------|------|
| **Terraform** | IaC | 声明式创建/管理云资源（VM、网络、数据库、LB） |
| **Ansible** | Configuration Management | 在已有机器上统一安装软件、下发配置、执行脚本 |
| **Jenkins** | CI/CD | 自动化流水线：build → test → deploy |
| **Docker** | 容器化 | 将应用及依赖打包成可移植的镜像，解决"我本地能跑"的问题 |
| **Kubernetes (K8s)** | 容器编排 | 管理大量 Docker 容器的部署、扩缩容、服务发现、滚动更新 |

**Terraform vs Ansible 区别**：
- Terraform：偏"创建基础设施"（把东西建出来）
- Ansible：偏"配置机器"（机器有了，把它变成想要的状态）

---

## 六、关键对比速查

| 对比 | A | B | 选择依据 |
|------|---|---|------|
| PostgreSQL vs Cassandra | 强一致、ACID、SQL | 高可用、横向扩展、最终一致 | 需要事务 → PG；需要大规模写入/分布式 → Cassandra |
| PostgreSQL vs ClickHouse | OLTP（事务、单行）| OLAP（聚合、分析）| 业务系统 → PG；报表/分析 → CH |
| Replication vs Sharding | 同一份数据复制多份 | 不同数据分放不同机器 | 高可用 → replication；扩展存储/查询 → sharding |
| Kafka vs 直接调 API | 异步解耦 | 同步耦合 | 允许延迟、需要解耦 → Kafka；需要实时响应 → 直接调 |
| Vertical vs Horizontal | 升级单机 | 加更多机器 | 短期快 → vertical；长期大规模 → horizontal |
| Strong vs Eventual Consistency | 读一定是最新值 | 短暂可能读到旧值 | 金融/账务 → strong；社交/日志 → eventual |
