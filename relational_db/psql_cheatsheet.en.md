# psql Cheatsheet (English)

Quick reference for daily use and advanced tips. Key terms kept in English.

---

## 1. Connect and Basic Info
```bash
psql -U user -d dbname
psql "postgresql://user:password@host:5432/dbname"
```

Common meta-commands:
```sql
\l          -- list databases
\c dbname   -- connect to database
\dn         -- list schemas
\dt         -- list tables
\dv         -- list views
\df         -- list functions
\d table    -- describe table
\x          -- expanded display
\?          -- help
\q          -- quit
```

---

## 2. Import and Export
```sql
\copy table_name FROM 'file.csv' CSV HEADER;
\copy table_name TO 'out.csv' CSV HEADER;
```

Difference from `COPY`:
- `\copy` reads/writes files on the **client**
- `COPY` reads/writes files on the **server**

---

## 3. Common SQL Snippets (Advanced)

### CTE (WITH)
```sql
WITH recent AS (
  SELECT * FROM users ORDER BY created_at DESC LIMIT 10
)
SELECT * FROM recent;
```
Explanation: split complex queries into readable temporary result sets.

### Window Function
```sql
SELECT
  user_id,
  amount,
  SUM(amount) OVER (PARTITION BY user_id ORDER BY created_at) AS running_total
FROM orders;
```
Explanation: aggregate without collapsing rows (running totals, ranks).

### LATERAL
```sql
SELECT u.id, o.*
FROM users u
JOIN LATERAL (
  SELECT * FROM orders o WHERE o.user_id = u.id ORDER BY created_at DESC LIMIT 1
) o ON true;
```
Explanation: subquery can reference outer columns; useful for “latest row per user”.

### UPSERT (ON CONFLICT)
```sql
INSERT INTO users (email, name)
VALUES ('a@ex.com', 'Ann')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;
```
Explanation: update on conflict, avoids race conditions.

### RETURNING
```sql
INSERT INTO users (email) VALUES ('b@ex.com') RETURNING id;
```
Explanation: return generated values (e.g., identity id).

### JSONB
```sql
SELECT data->>'name' AS name FROM profiles;
SELECT data->'tags' FROM profiles;
```
Explanation: `->>` gets text, `->` gets JSON.

---

## 4. Debugging and Performance
```sql
EXPLAIN SELECT * FROM users WHERE email = 'a@ex.com';
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'a@ex.com';
```
Explanation: `EXPLAIN` shows the plan; `EXPLAIN ANALYZE` runs and reports actual timing/rows.

---

## 5. Transactions and Isolation
```sql
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- SQL ...
COMMIT;
```
Explanation: explicit transactions ensure atomicity; isolation level trades consistency for performance.

---

## 6. Users and Privileges
```sql
CREATE ROLE analyst LOGIN PASSWORD 'pwd';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst;
REVOKE SELECT ON users FROM analyst;
```
Explanation: manage access with roles and least privilege.

---

## 7. Handy Tips
- `\timing`: show execution time
- `\set ON_ERROR_STOP on`: stop on error
- `\pset pager off`: disable pager
- `\watch 2`: re-run last query every 2 seconds

---

## One‑Sentence Summary
Mastering `psql` meta-commands, `\copy`, `EXPLAIN`, and advanced SQL (CTE/Window/LATERAL/UPSERT) covers most daily usage and debugging needs.
