# SQL 入门（Week 3：查询为核心）

目标：用 SQL 可靠地表达“问题”，并避免常见错误。

---

## 1. 写查询的正确思路
- 先用自然语言把问题拆清楚，再翻译成 SQL。
- 查询的**逻辑执行顺序**（便于理解结果）：  
  `FROM` -> `JOIN` -> `WHERE` -> `GROUP BY` -> `HAVING` -> `SELECT` -> `ORDER BY`
- SQL 的**书写顺序**与执行顺序不同，调试时要区分。

---

## 2. SELECT 基本结构
```sql
SELECT ...
FROM ...
[WHERE ...]
[GROUP BY ... HAVING ...]
[ORDER BY ...];
```
- `WHERE` 过滤行，`HAVING` 过滤分组结果。
- `DISTINCT` 去重结果行。

---

## 3. GROUP BY 的核心规则（高频考点）
- `GROUP BY` 后，`SELECT` 里**只能出现**：
  - 分组属性
  - 聚合函数（`COUNT / SUM / AVG / MIN / MAX`）
- 违反规则会报语法错误。

---

## 4. JOIN（连接）
- **INNER JOIN**：两边都匹配才保留。
- **LEFT JOIN**：左表保留全部，右表不匹配为 `NULL`。
- **NATURAL JOIN**：自动用同名属性，**不推荐**（改名会改变语义）。
- 建议使用显式 `JOIN ... ON ...`。

---

## 5. 子查询（Subqueries）
- `IN`：判断值是否在子查询结果中（子查询需返回**一列**）。
- `EXISTS`：判断子查询是否非空，常用于“是否存在某记录”。
- 同表多次使用必须加别名。

---

## 6. 集合运算（Set Operations）
- `UNION`：并集（默认去重），`UNION ALL` 不去重。
- `INTERSECT`：交集。
- `EXCEPT`：差集。
- 要求两侧列数一致、类型顺序兼容。

---

## 7. 数据修改语句（DML）
- `INSERT`：主键不可为 `NULL`，未提供的列默认为 `NULL`。
- `UPDATE`：`WHERE` 决定**哪些行**被更新。
- `DELETE` 只删数据；`DROP TABLE` 删表结构。
- 外键约束常见行为：
  - `ON DELETE NO ACTION`：阻止删除
  - `ON DELETE CASCADE`：级联删除

---

## 8. COUNT 与 NULL 的常见坑
- `COUNT(*)` 统计行数；`COUNT(col)` 会忽略 `NULL`。
- 多表 JOIN 时经常需要 `COUNT(DISTINCT ...)`。

```sql
SELECT COUNT(DISTINCT StudentID)
FROM Enrol;
```

---

## 9. CTE（WITH）
- 用 `WITH` 拆解复杂查询，可读性高，调试更方便。

```sql
WITH Temp AS (...)
SELECT ...
FROM Temp;
```

---

## 一句话总结
Week 3 的核心是：把“问题”翻译成正确的 `SELECT + JOIN + GROUP BY + 子查询`，并通过约束、聚合与集合运算避免逻辑错误。
