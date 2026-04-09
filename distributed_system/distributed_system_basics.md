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

**核心概念**：
- **Producer**：向 topic 写消息的服务
- **Consumer**：从 topic 读消息的服务
- **Topic**：消息分类，类似"频道"
- **Partition**：topic 的物理分片，同一 topic 可以有多个 partition 并行处理，提高吞吐
- **Offset**：consumer 在 partition 中读取到的位置游标，可以 replay

**为什么 Kafka 高吞吐？** 消息顺序写磁盘（比随机写快很多），partition 并行，consumer 可批量拉取。

**典型场景**：
- 订单系统写数据库后发 Kafka 事件，库存服务、通知服务分别消费 → 解耦
- 用户行为日志实时收集 → 数据分析 pipeline

---

### Cassandra — 分布式 NoSQL 数据库

面向大规模写入和水平扩展设计，牺牲强一致性换高可用。

**特点**：
- 无 master 节点，所有节点对等（peer-to-peer）
- 通过 consistent hashing 决定数据存放在哪个节点
- Replication factor 可配置（通常 3），数据写入多个副本
- 写入优先：写性能极强（追加 WAL，不做随机写）

**适合场景**：时序数据、IoT 传感器数据、用户行为日志、需要全球多数据中心写入的场景。

**不适合场景**：复杂 join、多表事务、强一致性业务（如金融交易）。

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
