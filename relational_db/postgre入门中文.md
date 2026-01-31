# PostgreSQL 入门（中文速记）

目标：快速上手 PostgreSQL（简称 Postgres），掌握基本概念、SQL 操作与实用技巧。**关键术语保留英文**。

---

## 1. 基本概念
- **Database**：数据库实例中的逻辑数据集
- **Schema**：命名空间（默认 `public`）
- **Table**：数据表
- **Row**：数据行
- **Column**：列
- **Constraint**：约束（如 `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`）
- **Index**：索引（加速查询）

---

## 2. 常用工具
- **psql**：PostgreSQL 官方 CLI
- **pg_dump / pg_restore**：备份与恢复
- **pgAdmin**：图形化管理工具

---

## 3. 连接与基础命令（psql）
```sql
-- 列出数据库
\l

-- 切换数据库
\c your_db

-- 列出 schema / 表
\dn
\dt

-- 查看表结构
\d table_name
```

---

## 4. 创建与修改结构（DDL）
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

ALTER TABLE users ADD COLUMN name TEXT;
DROP TABLE users;
```

---

## 5. 数据操作（DML）
```sql
-- INSERT
INSERT INTO users (email, name) VALUES ('a@ex.com', 'Ann');

-- SELECT
SELECT id, email FROM users WHERE email LIKE '%@ex.com';

-- UPDATE
UPDATE users SET name = 'Anna' WHERE id = 1;

-- DELETE
DELETE FROM users WHERE id = 1;
```

---

## 6. 约束（Constraints）
```sql
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  amount NUMERIC CHECK (amount > 0)
);
```

常见约束：
- `PRIMARY KEY`
- `FOREIGN KEY`
- `UNIQUE`
- `NOT NULL`
- `CHECK`

---

## 7. Index（索引）
```sql
CREATE INDEX idx_users_email ON users(email);
```
说明：
- `INDEX` 提升查询速度，但会增加写入成本。
- 常用于 `WHERE`、`JOIN` 条件列。

---

## 8. Transaction（事务）
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

常用：
- `BEGIN` / `COMMIT` / `ROLLBACK`
- 避免部分更新导致不一致

---

## 9. 常见数据类型
- **INT**, **BIGINT**
- **TEXT**, **VARCHAR**
- **BOOLEAN**
- **DATE**, **TIMESTAMP**
- **NUMERIC**
- **UUID**
- **JSON / JSONB**

---

## 10. 实用查询技巧
```sql
-- 分组与聚合
SELECT user_id, COUNT(*) FROM orders GROUP BY user_id;

-- 排序与分页
SELECT * FROM users ORDER BY created_at DESC LIMIT 10 OFFSET 0;

-- 使用 CTE
WITH recent_users AS (
  SELECT * FROM users ORDER BY created_at DESC LIMIT 5
)
SELECT * FROM recent_users;
```

---

## 11. 备份与恢复
```bash
# 备份
pg_dump -U user -d dbname > backup.sql

# 恢复
psql -U user -d dbname < backup.sql
```

---

## 一句话总结
PostgreSQL 是功能完整、标准兼容的关系型数据库，掌握 **psql**、**DDL/DML**、**Constraints**、**Index** 与 **Transaction** 就能完成大多数日常开发任务。
