# psql 语法 Cheatsheet（中文）

面向日常使用与进阶操作的速查表，关键术语保留英文。

---

## 1. 连接与基础信息
```bash
psql -U user -d dbname
psql "postgresql://user:password@host:5432/dbname"
```

常用元命令：
```sql
\l          -- 列出 databases
\c dbname   -- 切换 database
\dn         -- 列出 schemas
\dt         -- 列出 tables
\dv         -- 列出 views
\df         -- 列出 functions
\d table    -- 查看表结构
\x          -- 切换扩展显示
\?          -- 帮助
\q          -- 退出
```

---

## 2. 数据导入导出
```sql
\copy table_name FROM 'file.csv' CSV HEADER;
\copy table_name TO 'out.csv' CSV HEADER;
```

与 `COPY` 区别：
- `\copy` 在 **客户端** 读写文件
- `COPY` 在 **服务器** 读写文件

---

## 3. 常用 SQL 片段（进阶）

### CTE（WITH）
```sql
WITH recent AS (
  SELECT * FROM users ORDER BY created_at DESC LIMIT 10
)
SELECT * FROM recent;
```
说明：将复杂查询拆分成可读的临时结果集，方便复用与调试。

### Window Function
```sql
SELECT
  user_id,
  amount,
  SUM(amount) OVER (PARTITION BY user_id ORDER BY created_at) AS running_total
FROM orders;
```
说明：在不分组折叠行的情况下做聚合（如累计和、排名），保留明细行。

### LATERAL
```sql
SELECT u.id, o.*
FROM users u
JOIN LATERAL (
  SELECT * FROM orders o WHERE o.user_id = u.id ORDER BY created_at DESC LIMIT 1
) o ON true;
```
说明：子查询可以引用外层表的列，用来做“每个用户取一条最新订单”之类的场景。

### UPSERT（ON CONFLICT）
```sql
INSERT INTO users (email, name)
VALUES ('a@ex.com', 'Ann')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;
```
说明：冲突时更新，避免先查后插的竞态条件。

### RETURNING
```sql
INSERT INTO users (email) VALUES ('b@ex.com') RETURNING id;
```
说明：在插入/更新后直接返回生成的值（如自增 id）。

### JSONB 常用
```sql
SELECT data->>'name' AS name FROM profiles;
SELECT data->'tags' FROM profiles;
```
说明：`->>` 取文本值，`->` 取 JSON 值，适合半结构化字段查询。

---

## 4. 查询调试与性能
```sql
EXPLAIN SELECT * FROM users WHERE email = 'a@ex.com';
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'a@ex.com';
```
说明：`EXPLAIN` 查看执行计划，`EXPLAIN ANALYZE` 真实执行并给出耗时与行数，用于定位慢查询原因。

---

## 5. 事务与隔离级别
```sql
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- SQL ...
COMMIT;
```
说明：显式事务保证多条语句的原子性，隔离级别决定并发一致性与性能的取舍。

---

## 6. 用户与权限
```sql
CREATE ROLE analyst LOGIN PASSWORD 'pwd';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst;
REVOKE SELECT ON users FROM analyst;
```
说明：通过角色统一管理权限，适合多人协作与生产环境最小权限控制。

---

## 7. 小技巧
- `\timing`：显示每条 SQL 的执行时间
- `\set ON_ERROR_STOP on`：遇错即停
- `\pset pager off`：关闭分页显示
- `\watch 2`：每 2 秒重复执行上一条查询

---

## 一句话总结
掌握 `psql` 元命令、`COPY/\copy`、`EXPLAIN` 与常用进阶 SQL（CTE/Window/UPSERT），能覆盖大多数实际开发和调试需求。
