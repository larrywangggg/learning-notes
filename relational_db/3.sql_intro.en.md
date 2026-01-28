# SQL Basics (Week 3: Query-Centric)

Goal: express questions reliably in SQL and avoid common mistakes.

---

## 1. How to Think When Writing Queries
- Start with the question in plain language, then translate to SQL.
- **Logical execution order** (for reasoning):  
  `FROM` -> `JOIN` -> `WHERE` -> `GROUP BY` -> `HAVING` -> `SELECT` -> `ORDER BY`
- SQL **writing order** differs from execution order.

---

## 2. Basic SELECT Structure
```sql
SELECT ...
FROM ...
[WHERE ...]
[GROUP BY ... HAVING ...]
[ORDER BY ...];
```
- `WHERE` filters rows; `HAVING` filters groups.
- `DISTINCT` removes duplicate result rows.

---

## 3. Core GROUP BY Rule (High-Frequency)
- After `GROUP BY`, the `SELECT` list can include only:
  - grouped attributes
  - aggregate functions (`COUNT / SUM / AVG / MIN / MAX`)
- Violations cause syntax errors.

---

## 4. JOINs
- **INNER JOIN**: keep only matching rows.
- **LEFT JOIN**: keep all left rows; unmatched right values become `NULL`.
- **NATURAL JOIN**: matches same-named columns automatically; **not recommended**.
- Prefer explicit `JOIN ... ON ...`.

---

## 5. Subqueries
- `IN`: checks whether a value is in the subquery result (single column).
- `EXISTS`: checks whether the subquery returns any rows.
- Use table aliases when the same table appears multiple times.

---

## 6. Set Operations
- `UNION`: union (removes duplicates); `UNION ALL` keeps duplicates.
- `INTERSECT`: intersection.
- `EXCEPT`: difference.
- Both sides must have the same number of columns with compatible types.

---

## 7. Data Modification (DML)
- `INSERT`: primary keys cannot be `NULL`; missing columns default to `NULL`.
- `UPDATE`: `WHERE` decides **which rows** to update.
- `DELETE` removes data; `DROP TABLE` removes the schema.
- Common FK actions:
  - `ON DELETE NO ACTION`: reject deletion
  - `ON DELETE CASCADE`: delete dependents

---

## 8. COUNT and NULL Pitfalls
- `COUNT(*)` counts rows; `COUNT(col)` ignores `NULL`.
- After JOINs, `COUNT(DISTINCT ...)` is often necessary.

```sql
SELECT COUNT(DISTINCT StudentID)
FROM Enrol;
```

---

## 9. CTEs (WITH)
- Use `WITH` to split complex queries for readability and debugging.

```sql
WITH Temp AS (...)
SELECT ...
FROM Temp;
```

---

## One-Sentence Summary
Week 3 is about translating questions into correct `SELECT + JOIN + GROUP BY + subquery` logic and using set operations and aggregates without mistakes.
