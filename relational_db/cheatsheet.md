# Relational Databases Cheat Sheet

Quick recall of key definitions and exam‑level facts.

---

## Core Concepts
- **Database**: collection of related data
- **DBMS**: software to create/manage databases
- **Database system**: DBMS + database (part of an information system)

### Advantages
- reduced redundancy
- integrity and security
- concurrency control
- backup/recovery
- data independence

---

## ANSI/SPARC Three‑Level Architecture
- **External schema**: user/app view (subsets of data)
- **Conceptual schema**: global logical view (entities + relationships)
- **Internal schema**: physical storage view

---

## Integrity Constraints
- **Domain**: values must come from the attribute domain (INT, VARCHAR, NOT NULL)
- **Key**: uniqueness (superkey, candidate key, primary key)
- **Entity integrity**: primary key cannot be NULL
- **Referential integrity**: FK values must match referenced PK values

---

## Keys
- **Superkey**: uniquely determines all attributes
- **Candidate key**: minimal superkey
- **Primary key**: chosen candidate key

---

## ER Model (Week 4)
- **Entity / Attribute / Relationship**
- **Weak entity**: lacks its own key; depends on identifying entity + relationship
- **EER**: adds specialization (ISA) and constraints

---

## Functional Dependencies (Week 5)
- **FD**: X → Y (same X implies same Y)
- **Trivial FD**: Y ⊆ X
- **Closure**: X⁺ is all attributes functionally determined by X
- **Prime attribute**: appears in some candidate key

---

## Normalization (Week 6)
- **Goal**: reduce redundancy and anomalies
- **BCNF**: for any non‑trivial X → A, X is a superkey
- **3NF**: for any non‑trivial X → A, X is a superkey **or** A is prime

### BCNF Properties
- **Lossless join**: no spurious tuples after join
- **Dependency preservation**: FDs can be checked in decomposed schemas
- Both properties may not be achievable together in BCNF

### Minimal Cover (for 3NF)
1. RHS single attribute
2. Remove extraneous attributes from LHS
3. Remove redundant FDs

---

## Relational Algebra (Week 7)
- **RA is procedural**; closure + composability
- **Basic ops**: σ (select), π (project), ρ (rename), ∪, −, ×
- **Selection commutes**: σϕ1(σϕ2(R)) = σϕ2(σϕ1(R)) = σϕ1∧ϕ2(R)
- **Projection not commutative** (can lose columns)

### RA ↔ SQL
- σϕ(R) → `SELECT DISTINCT * FROM R WHERE ϕ`
- πA(R) → `SELECT DISTINCT A FROM R`
- R1 − R2 → `SELECT * FROM R1 EXCEPT SELECT * FROM R2`
- R1 ⋈ϕ R2 → `SELECT DISTINCT * FROM R1 JOIN R2 ON ϕ`

---

## Query Processing & Optimization (Week 8)
### DBMS Pipeline
- **Parser/Translator** → RA
- **Optimizer** → best execution plan
- **Evaluation engine** → run plan

### Optimization Approaches
- **Semantic**: use constraints to simplify
- **Rule‑based**: push‑down selection/projection, reorder joins
- **Cost‑based**: estimate I/O + intermediate sizes

---

## Database Security (Week 9)
- **CIA**: confidentiality, integrity, availability

### Access Control
- **DAC**: owner grants/revokes; flexible but weak leakage control
- **MAC**: centralized; uses clearance/classification
- **RBAC**: roles control privileges

### GRANT / REVOKE
- `WITH GRANT OPTION` allows re‑grant
- `RESTRICT`: block revocation if others depend on it
- `CASCADE`: revoke downstream grants

---

## Transactions (Week 10)
- **ACID**: Atomicity, Consistency, Isolation, Durability
- **WAL**: log before data; commit log on disk before commit
- **2PL**: growing then shrinking phase → serializability

### Anomalies
- Lost update, dirty read, unrepeatable read, phantom read

### Isolation Levels
| Level | Dirty | Unrepeatable | Phantom |
| --- | --- | --- | --- |
| READ UNCOMMITTED | ✔ | ✔ | ✔ |
| READ COMMITTED | ✘ | ✔ | ✔ |
| REPEATABLE READ | ✘ | ✘ | ✔ |
| SERIALIZABLE | ✘ | ✘ | ✘ |

---

## NoSQL (Week 11)
- **Types**: key‑value, column‑family, document, graph
- **BASE**: basically available, soft state, eventual consistency
- **When**: scale, flexible schema, deep relationships

---

## Quick Reminders
- Join = Cartesian product + selection
- SQL tables are bags; RA uses set semantics
- Higher isolation = safer but slower
