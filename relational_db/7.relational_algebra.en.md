# Relational Algebra Notes

Goal: understand the logical steps behind SQL queries and the essence of joins.

---

## 1. Core Assumptions
- **Input/output are relations**
- **Set semantics**: no duplicate tuples
- **Unordered**: no row/column order

Implications:
- Projection removes duplicates automatically
- You cannot rely on row order

---

## 2. Unary Operations
- **Selection σ**: filter rows (WHERE)
- **Projection π**: choose columns (SELECT), **deduplicates**
- **Rename ρ**: rename for self-joins or division

---

## 3. Binary Operations (Key Section)

### 3.1 Set Operations
- **Union ∪**: requires compatible schemas
- **Intersection ∩**
- **Difference −**

SQL: `UNION`, `INTERSECT`, `EXCEPT`

---

### 3.2 Cartesian Product × (Join Foundation)
Definition:  
R × S pairs every tuple in R with every tuple in S.

Properties:
- If R has m rows and S has n rows, result has **m × n rows**
- Rarely used alone; mainly a step inside joins

Key identity:  
**Join = Cartesian Product + Selection**

---

### 3.3 Joins (Most Important)

#### 3.3.1 θ-Join (General Form)
Definition:
```
R ⋈θ S = σθ (R × S)
```
θ can be any condition (=, ≠, <, >, ≤, ≥, or combined predicates).

#### 3.3.2 Equi-Join (Common)
- Special case of θ-join with only equality conditions
- **Both join columns are kept** (no automatic deduplication)

SQL:
```sql
FROM R JOIN S ON R.a = S.b
```

#### 3.3.3 Natural Join (Concise but Risky)
- Automatically matches **same-named attributes**
- Performs equi-join and **merges duplicate columns**
- Renaming a column changes the query’s meaning

SQL:
```sql
NATURAL JOIN
```

---

### 3.4 Join Result Shape (Exam Favorite)
| Join Type | Same-name attributes | Deduplicate |
| --- | --- | --- |
| θ-join | kept | no |
| equi-join | kept | no |
| natural join | merged | yes |

---

## 4. Why This Matters for Optimisation
Relational algebra justifies valid rewrites:
- join order can change
- selections can be pushed down
- projections can be pushed down
- avoid Cartesian products until necessary

These principles power query optimizers.

---

## One-Sentence Summary
Relational algebra formalizes query logic with set operations, shows that **Join = × + σ**, and provides the theory behind SQL semantics and query optimization.

---

## Why Learn It
It helps you translate SQL into precise logical steps, prove query equivalence, and reason about safe optimizations. It also explains how query optimizers think, which is essential for writing efficient, correct queries.
