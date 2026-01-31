# Query Optimization Notes

Goal: keep results the same while transforming SQL into a faster execution plan.

---

## 1. How SQL Is Processed in a DBMS
1. **Parser & Translator**  
   Validate syntax/permissions, translate SQL into relational algebra and a **logical query tree**.
2. **Query Optimizer**  
   Choose the **lowest-cost** plan among equivalent trees.
3. **Evaluation Engine**  
   Execute the chosen plan and return results.

![Query processing flow](images/query%20processing.png)

---

## 2. Query Trees: The Optimization Target
- **Logical query tree**: describes *what* to compute
- **Physical query tree**: describes *how* to compute (operators/algorithms)

![Query tree example](images/query%20processing%20example.png)

---

## 3. Why “Equivalent” Does Not Mean “Fast”
Equivalent queries can perform very differently due to:
- different intermediate result sizes
- different join orders
- early vs late filtering/projection
- unnecessary Cartesian products

---

## 4. Three Optimization Approaches

### 4.1 Semantic Optimization
Use constraints (PK/FK/business rules) to remove redundant operations.  
Very powerful, but depends on complete semantic info.

---

### 4.2 Rule-Based Optimization (Exam Focus)
Core idea: **shrink data as early as possible**.

Key rules:
- **Push down selection** (`σ`)
- **Push down projection** (`π`) while keeping join attributes
- **Avoid needless ×**: `σ(R × S) -> R ⋈ S`
- **Reorder joins** to join smaller results first

![Rule-based optimization overview](images/query%20optimization%20rules.png)

Examples:

![Selection pushdown example](images/pushdown%20selection%20example.png)
![Projection pushdown example](images/pushdown%20projection%20example.png)

---

### 4.3 Cost-Based Optimization
Use a cost model instead of rules alone.

Typical cost sources:
- I/O reads and writes
- materializing intermediate results
- sorting and duplicate elimination

![Optimizer overview](images/query%20optimizer.png)

---

## 5. Execution Plan Choices
The optimizer decides:
- join algorithm: nested loop / hash / sort-merge
- **pipelined** (streaming) vs **materialized** (write to disk)

---

## 6. Link to Relational Algebra
Valid rewrites come from algebraic equivalences:
- selection pushdown
- projection pushdown (keep join attributes)
- join commutativity/associativity

---

## One-Sentence Summary
Query optimization rewrites equivalent query trees using rules and cost models to produce a lower-cost execution plan without changing results.
