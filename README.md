# 学习笔记

个人技术学习仓库，用来记录和练习正在学的内容。每个主题一个目录，里面主要是笔记；`fast/` 里还有一个可运行的小例子。这些材料用于学习，不是生产项目。

本页按仓库里的实际文件导航。中文稿在前；某一行有英文链接，表示那一份有对应英文稿。`network/en/` 目前有周笔记 week1–11，以及 MQTT、gopher、interstellar-spacecraft、ping。`network/quizs/` 里的 lab、curl、cheatsheet 没有放进 `network/en/`。Week 6 的 HTML 和 Markdown 周笔记是不同文件。

_更新日期：2026-11-05_

## 主题入口

| 主题 | 中文 | English |
| --- | --- | --- |
| 计算机体系结构 | [Set 1](computer-architecture/set1.md) | [Set 1](computer-architecture/en/set1.md) |
| 计算机网络 | [Week 1](network/week1笔记.md) | [Week 1](network/en/week1.md) |
| 关系数据库 | [什么是数据库](relational_db/中文笔记/1.什么是DB.md) | [What Is a Database](relational_db/1.what_is_db.en.md) |
| FastAPI | [数据模型与数据库层](fast/fast_api_notes/中文笔记/fastapi_db_schema中文.md) | [Data models](fast/fast_api_notes/fastapi_db_schema.en.md) |
| Git / Linux | [Git 常用指令](git/git_notes/中文笔记/git_cheatsheet中文.md) | [Git cheatsheet](git/git_notes/git_cheatsheet.md) |
| Agent | [Agent](agent/agent.md) | — |
| 分布式系统 | [核心概念](distributed_system/distributed_system_basics.md) | — |
| RAG | [基础概念](rag/基础概念.md) | — |

## 计算机体系结构

笔记标题为 COMP2300，Set 1–9。中文是 `computer-architecture/setN.md`，英文是 `computer-architecture/en/setN.md`。图片在 [computer-architecture/images](computer-architecture/images)，按 set1–set9 分子目录，中英文共用。

| Set | 笔记中的主题 | 中文 | English |
| --- | --- | --- | --- |
| 1 | 课程导论、信息表示、构建块 | [set1](computer-architecture/set1.md) | [set1](computer-architecture/en/set1.md) |
| 2 | 组合电路 | [set2](computer-architecture/set2.md) | [set2](computer-architecture/en/set2.md) |
| 3 | 时序电路、存储器与有限状态机 | [set3](computer-architecture/set3.md) | [set3](computer-architecture/en/set3.md) |
| 4 | Von Neumann 模型、ARM ISA、单周期微架构 | [set4](computer-architecture/set4.md) | [set4](computer-architecture/en/set4.md) |
| 5 | 多周期微架构、FSM 控制器、微程序 | [set5](computer-architecture/set5.md) | [set5](computer-architecture/en/set5.md) |
| 6 | 函数、栈、内存映射、异常与 I/O、功耗 | [set6](computer-architecture/set6.md) | [set6](computer-architecture/en/set6.md) |
| 7 | micro:bit、特权级与中断、局部性与 Cache | [set7](computer-architecture/set7.md) | [set7](computer-architecture/en/set7.md) |
| 8 | 流水线、冒险与分支预测 | [set8](computer-architecture/set8.md) | [set8](computer-architecture/en/set8.md) |
| 9 | ILP、乱序执行（Scoreboard、ROB、寄存器重命名） | [set9](computer-architecture/set9.md) | [set9](computer-architecture/en/set9.md) |

## 计算机网络

周笔记标题里使用 Network Week / COMP3310。中文是 `network/weekN笔记.md`，英文是 `network/en/weekN.md`。配图在 [network/images](network/images)，现有 week4、week5、week6、week8、week10，中英文 Markdown 共用。

| 周 | 笔记中的主线 | 中文 | English |
| --- | --- | --- | --- |
| 1 | 电路交换、复用、调制、线路编码 | [week1](network/week1笔记.md) | [week1](network/en/week1.md) |
| 2 | 物理介质：铜缆、光纤、无线、Last Mile | [week2](network/week2笔记.md) | [week2](network/en/week2.md) |
| 3 | 卫星、LAN、MAC、Ethernet、Wi-Fi | [week3](network/week3笔记.md) | [week3](network/en/week3.md) |
| 4 | 协议分层、封装、IPv4、分片、IPv6 | [week4](network/week4笔记.md) | [week4](network/en/week4.md) |
| 5 | 传输层、DHCP、DNS | [week5](network/week5笔记.md) | [week5](network/en/week5.md) |
| 6 | Web / HTTP、实时通信 | [week6](network/week6笔记.md) | [week6](network/en/week6.md) |
| 7 | IoT/MQTT 与 P2P/DHT | [week7](network/week7笔记.md) | [week7](network/en/week7.md) |
| 8 | 路由 | [week8](network/week8笔记.md) | [week8](network/en/week8.md) |
| 9 | 拥塞控制、流控、网络管理 | [week9](network/week9笔记.md) | [week9](network/en/week9.md) |
| 10 | 网络安全 | [week10](network/week10笔记.md) | [week10](network/en/week10.md) |
| 11 | 安全 Part 3 | [week11](network/week11笔记.md) | [week11](network/en/week11.md) |

Week 6 另有两份 HTML，和上表的 Markdown 分开：[中文 week6.html](network/week6.html)、[英文 week6_en.html](network/week6_en.html)。

### 专题笔记

| 主题 | 中文 | English |
| --- | --- | --- |
| MQTT | [MQTT笔记](network/MQTT笔记.md) | [MQTT](network/en/MQTT.md) |
| Gopher | [gopher](network/gopher.md) | [gopher](network/en/gopher.md) |
| 星际航天器 | [星际航天器](network/quizs/星际航天器.md) | [interstellar-spacecraft](network/en/interstellar-spacecraft.md) |
| ping | [ping](network/quizs/ping.md) | [ping](network/en/ping.md) |

### quizs

`network/quizs/` 本身没有英文目录。ping 与星际航天器的英文在 `network/en/`，见上表。实验题原文是英文，没有中文稿，也没有 lab1、lab6。

| 文件 | 说明 |
| --- | --- |
| [lab2](network/quizs/lab2.md) | 英文试题 |
| [lab3](network/quizs/lab3.md) | 英文试题 |
| [lab4](network/quizs/lab4.md) | 英文试题 |
| [lab5](network/quizs/lab5.md) | 英文试题 |
| [lab7](network/quizs/lab7.md) | 英文试题 |
| [lab8](network/quizs/lab8.md) | 英文试题 |
| [curl](network/quizs/curl.md) | 中文速查，无 `network/en/` 副本 |
| [cheatsheet.html](network/quizs/cheatsheet.html) | 速查页，无 `network/en/` 副本 |
| [cheatsheet.pdf](network/quizs/cheatsheet.pdf) | 速查 PDF，无 `network/en/` 副本 |

## 关系数据库

中文在 `relational_db/中文笔记/`，英文在 `relational_db/` 根目录（速查表的英文文件名是 `cheatsheet.md`）。配图在 [relational_db/images](relational_db/images)。

| 主题 | 中文 | English |
| --- | --- | --- |
| 什么是数据库 | [1](relational_db/中文笔记/1.什么是DB.md) | [1](relational_db/1.what_is_db.en.md) |
| 关系模型与 SQL DDL | [2](relational_db/中文笔记/2.relational_db_model_and_sql中文.md) | [2](relational_db/2.relational_db_model_and_sql.en.md) |
| SQL 入门 | [3](relational_db/中文笔记/3.sql入门.md) | [3](relational_db/3.sql_intro.en.md) |
| ER 图 | [4](relational_db/中文笔记/4.ER图中文.md) | [4](relational_db/4.ER_diagram.en.md) |
| 函数依赖 | [5](relational_db/中文笔记/5.functional_dependencies中文.md) | [5](relational_db/5.functional_dependencies.en.md) |
| 范式 | [6](relational_db/中文笔记/6.normal_forms中文.md) | [6](relational_db/6.normal_forms.en.md) |
| 关系代数 | [7](relational_db/中文笔记/7.关系代数.md) | [7](relational_db/7.relational_algebra.en.md) |
| 查询优化 | [8](relational_db/中文笔记/8.查询优化.md) | [8](relational_db/8.query_optimization.en.md) |
| 数据库安全 | [9](relational_db/中文笔记/9.数据库安全.md) | [9](relational_db/9.database_security.en.md) |
| 事务与并发 | [10](relational_db/中文笔记/10.事务与并发控制.md) | [10](relational_db/10.transactions_and_concurrency.en.md) |
| NoSQL | [11](relational_db/中文笔记/11.NoSQL中文.md) | [11](relational_db/11.NoSQL.en.md) |
| PostgreSQL 入门 | [中文](relational_db/中文笔记/postgre入门中文.md) | [English](relational_db/postgres_intro.en.md) |
| psql | [中文](relational_db/中文笔记/psql_cheatsheet中文.md) | [English](relational_db/psql_cheatsheet.en.md) |
| Python / Java 中使用 PostgreSQL | [中文](relational_db/中文笔记/psql_in_python_java.md) | [English](relational_db/psql_in_python_java.en.md) |
| 速查表 | [中文](relational_db/中文笔记/cheatsheet中文.md) | [English](relational_db/cheatsheet.md) |

## FastAPI

[fast/README.md](fast/README.md) 说明示例程序（JWT、上传、feed）怎么安装和运行。笔记的中文在 `fast/fast_api_notes/中文笔记/`，英文是同目录下的 `*.en.md`。配图在 [fast/fast_api_notes/images](fast/fast_api_notes/images)。

| 主题 | 中文 | English |
| --- | --- | --- |
| uv | [中文](fast/fast_api_notes/中文笔记/uv笔记.中文.md) | [English](fast/fast_api_notes/uv_notes.en.md) |
| dict | [中文](fast/fast_api_notes/中文笔记/dict中文.md) | [English](fast/fast_api_notes/dict.en.md) |
| URL、请求与响应 | [中文](fast/fast_api_notes/中文笔记/url_request_response中文.md) | [English](fast/fast_api_notes/url_request_response.en.md) |
| 数据模型与数据库层 | [中文](fast/fast_api_notes/中文笔记/fastapi_db_schema中文.md) | [English](fast/fast_api_notes/fastapi_db_schema.en.md) |
| SQLAlchemy Session | [中文](fast/fast_api_notes/中文笔记/session中文.md) | [English](fast/fast_api_notes/session.en.md) |
| SQLAlchemy 关系 | [中文](fast/fast_api_notes/中文笔记/sqlalchemy关系中文.md) | [English](fast/fast_api_notes/sqlalchemy_relationships.en.md) |
| lifespan | [中文](fast/fast_api_notes/中文笔记/asynccontextmanager中文.md) | [English](fast/fast_api_notes/asynccontextmanager.en.md) |
| Alembic | [中文](fast/fast_api_notes/中文笔记/Alembic中文.md) | [English](fast/fast_api_notes/Alembic.en.md) |
| JWT | [中文](fast/fast_api_notes/中文笔记/JWT中文.md) | [English](fast/fast_api_notes/JWT.en.md) |
| UploadFile | [中文](fast/fast_api_notes/中文笔记/uploadfile中文.md) | [English](fast/fast_api_notes/uploadfile.en.md) |

## Git 与 Linux

中文在 `git/git_notes/中文笔记/`，英文在 `git/git_notes/`。

| 主题 | 中文 | English |
| --- | --- | --- |
| Git 常用指令 | [中文](git/git_notes/中文笔记/git_cheatsheet中文.md) | [English](git/git_notes/git_cheatsheet.md) |
| SSH | [中文](git/git_notes/中文笔记/SSH中文.md) | [English](git/git_notes/SSH.md) |
| Ed25519 SSH | [中文](git/git_notes/中文笔记/ed25519_SSH中文.md) | [English](git/git_notes/ed25519_SSH.md) |
| Linux 基础命令 | [中文](git/git_notes/中文笔记/Linux基础.md) | [English](git/git_notes/Linux_basics.md) |
| nano | [中文](git/git_notes/中文笔记/nano基础.md) | [English](git/git_notes/nano_basics.md) |

## Agent

目前只有中文笔记。

| 笔记 | 链接 |
| --- | --- |
| Agent 循环 | [agent.md](agent/agent.md) |
| Harness | [harness.md](agent/harness.md) |
| Harness 四层 | [harness_layers.md](agent/harness_layers.md) |
| 本地模型与 API | [llm_local_vs_api.md](agent/llm_local_vs_api.md) |

## 分布式系统

目前只有中文笔记。

| 笔记 | 链接 |
| --- | --- |
| 分布式系统与 DevOps 核心概念 | [distributed_system_basics.md](distributed_system/distributed_system_basics.md) |
| Infrastructure as Code | [iac.md](distributed_system/iac.md) |

## RAG

目前只有中文笔记：[基础概念](rag/基础概念.md)（本地 RAG 与 LlamaIndex）。
