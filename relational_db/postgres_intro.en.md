# PostgreSQL Intro (Quick Notes)

Goal: get started with PostgreSQL (Postgres) and master common concepts, SQL, and daily workflows.

---

## 1. Core Concepts
- **Database**: logical data collection inside a PostgreSQL instance
- **Schema**: namespace (default `public`)
- **Table / Row / Column**
- **Constraint**: `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`
- **Index**: speeds up reads

---

## 2. Common Tools
- **psql**: official CLI
- **pg_dump / pg_restore**: backup and restore
- **pgAdmin**: GUI management

---

## 3. Connect and Basic Commands (psql)
```sql
\l          -- list databases
\c your_db  -- connect
\dn         -- list schemas
\dt         -- list tables
\d table    -- describe table
```

---

## 4. DDL (Schema)
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

## 5. DML (Data)
```sql
INSERT INTO users (email, name) VALUES ('a@ex.com', 'Ann');
SELECT id, email FROM users WHERE email LIKE '%@ex.com';
UPDATE users SET name = 'Anna' WHERE id = 1;
DELETE FROM users WHERE id = 1;
```

---

## 6. Constraints
```sql
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  amount NUMERIC CHECK (amount > 0)
);
```
Common constraints:
- `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`, `CHECK`

---

## 7. Index
```sql
CREATE INDEX idx_users_email ON users(email);
```
Notes:
- Indexes speed reads but slow writes
- Best for `WHERE` / `JOIN` columns

---

## 8. Transaction
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

---

## 9. Common Data Types
- **INT**, **BIGINT**
- **TEXT**, **VARCHAR**
- **BOOLEAN**
- **DATE**, **TIMESTAMP**
- **NUMERIC**
- **UUID**
- **JSON / JSONB**

---

## 10. Practical Query Tips
```sql
SELECT user_id, COUNT(*) FROM orders GROUP BY user_id;
SELECT * FROM users ORDER BY created_at DESC LIMIT 10 OFFSET 0;

WITH recent_users AS (
  SELECT * FROM users ORDER BY created_at DESC LIMIT 5
)
SELECT * FROM recent_users;
```

---

## 11. Backup and Restore
```bash
pg_dump -U user -d dbname > backup.sql
psql -U user -d dbname < backup.sql
```

---

## One‑Sentence Summary
PostgreSQL is a full‑featured relational database; mastering `psql`, DDL/DML, constraints, indexes, and transactions covers most day‑to‑day work.
