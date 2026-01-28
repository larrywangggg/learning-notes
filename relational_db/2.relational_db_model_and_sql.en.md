# Week 2: Relational Data Model and SQL DDL

> Goal: define tables precisely with set theory and enforce correctness via SQL DDL.

---

## 1. Mathematical Foundations: Sets, Tuples, Cartesian Product, Relations
- **Set**: unordered, no duplicates, has cardinality (size).
- **Tuple**: ordered sequence of elements; values may repeat.
- **Cartesian product**: all possible pairs from two sets.

![Cartesian product example](images/Caetesian%20product.png)

- **Relation**: **a subset of a Cartesian product**, i.e., a set of tuples.

![Relation as subset example](images/Relations%20examples.png)

Key points:
- A relation is a set, so **no duplicate tuples**.
- Tuple order does not matter; attribute names define meaning.

---

## 2. Relation vs Table (Terminology)
- Table -> **Relation**
- Column -> **Attribute**
- Row -> **Tuple**
- Data type -> **Domain**
- Table definition -> **Relation schema**

Note:
- Math relations have **set semantics**, while SQL tables allow duplicates by default (bag semantics), so constraints are needed for uniqueness.

---

## 3. Schema and State
- **Relation schema**: structural definition (attributes + domains).
- **Relational database schema**: a set of relation schemas + integrity constraints.
- **Relational database state**: the actual data at a point in time; **one relation per schema**, must satisfy constraints.

![Relational database schema example](images/schema.png)

---

## 4. Keys
- **Superkey**: any attribute set that uniquely identifies a tuple.
- **Candidate key**: a minimal superkey.
- **Primary key**: one chosen candidate key.
- A relation can have multiple candidate keys but **only one primary key**.
- Composite keys are common, e.g., `{StudentID, CourseNo, Semester}`.

---

## 5. Integrity Constraints
1. **Domain constraints**: values must come from the domain (type, NOT NULL, CHECK).
2. **Key constraints**: uniqueness (UNIQUE / PRIMARY KEY).
3. **Entity integrity**: primary key **cannot be NULL**.
4. **Referential integrity (foreign keys)**: child values must exist in parent; composite FKs must match **as a whole**.

---

## 6. SQL DDL (Structure Definition)
Common commands: **CREATE / ALTER / DROP TABLE**.

Example (schema + constraints):

```sql
CREATE TABLE Student (
  StudentID CHAR(8) PRIMARY KEY,
  Name TEXT NOT NULL,
  DoB DATE,
  Email TEXT UNIQUE
);

CREATE TABLE Course (
  No TEXT PRIMARY KEY,
  Cname TEXT NOT NULL,
  Unit INTEGER CHECK (Unit > 0)
);

CREATE TABLE Enrol (
  StudentID CHAR(8),
  CourseNo TEXT,
  Semester TEXT,
  Status TEXT CHECK (Status IN ('enrolled', 'withdrawn')),
  EnrolDate DATE,
  PRIMARY KEY (StudentID, CourseNo, Semester),
  FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
  FOREIGN KEY (CourseNo) REFERENCES Course(No)
);
```

Notes:
- Create referenced tables before tables with foreign keys.
- PostgreSQL is case-insensitive by default unless identifiers are quoted.

---

## 7. Indexes (FYI)
- **CREATE INDEX** is for performance (B-tree, Hash, etc.).
- This week focuses on models and constraints, not tuning.

---

## One-Sentence Summary
Week 2 formalizes tables with sets and relations, uses keys and integrity constraints to ensure correctness, and applies the rules through SQL DDL.
