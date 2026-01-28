# ER 图（Entity-Relationship）整理

本节总结 ER/EER 模型的核心概念、符号与建模要点，并结合图片示例理解。

---

## 1. ER 图的基本符号（Peter Chen, 1976）
- **实体（Entity）**：矩形
- **属性（Attribute）**：椭圆
- **主键属性（Key attribute）**：下划线
- **联系（Relationship）**：菱形

![ER 基本符号](images/ER%20diagram.png)

---

## 2. 实体、属性与属性类型
- **实体集**：现实世界中同类对象的集合（如 Student、Course）。
- **属性**：描述实体特征（如 name、id）。
- 常见属性类型：
  - **简单属性 / 复合属性**（如 Address 可拆分为 City/Street）
  - **单值 / 多值属性**（如 phone 可能多值）
  - **派生属性**（如 age 可由 dob 推导）

建模提示：
- 主键属性必须能唯一标识实体。
- 复合属性与多值属性在关系模型中通常需要拆表处理。

---

## 3. 关系（Relationships）
- **二元关系**最常见：实体之间的关联（如 Student–Enrol–Course）。
- 关系也可以有属性（如 EnrolDate、Grade）。

### 3.1 基数（Cardinality）
- **1:1**：一对一
- **1:N**：一对多
- **M:N**：多对多（通常需要中间关系/桥表）

### 3.2 参与约束（Participation）
- **全参与（Total）**：每个实体都必须参加该关系（双线）
- **部分参与（Partial）**：可参加可不参加（单线）

---

## 4. 弱实体（Weak Entity）
- **弱实体**依赖强实体存在，不能独立用自身属性唯一标识。
- 需通过**识别关系（Identifying relationship）**与强实体组合确定主键。

---

## 5. EER（扩展 ER）与继承
- **子类/超类（ISA）**：继承属性与关系。
- 可用于区分不同子类型（如 Student vs Staff）。

![EER 示例](images/EER%20example.png)

---

## 6. 从 ER 图到关系模型的直觉
- 实体 -> 表
- 1:N 关系 -> 在 N 端加外键
- M:N 关系 -> 独立关系表（含两个外键 + 关系属性）
- 弱实体 -> 主键包含强实体主键

---

## 一句话总结
ER 图通过实体、关系、属性与约束把现实世界抽象成结构化模型，是关系数据库设计的起点。
