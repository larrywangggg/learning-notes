# Normal Forms Notes

Focus: definitions and intuition for 1NF/3NF/BCNF, the two key decomposition properties, and the common algorithms.

---

## 1. The Normalisation Framework
Normalisation answers three questions:
- **What is a good design?** (Normal Forms)
- **How to decompose?** (Normalisation algorithms)
- **Why decompose this way?** (Functional Dependencies)

![Normal form hierarchy](images/nomarl%20forms.png)

Key points:
- **BCNF ⊂ 3NF ⊂ 2NF ⊂ 1NF**
- 1NF is not FD-based; 2NF/3NF/BCNF are FD-based
- In practice, 3NF or BCNF are most common

---

## 2. 1NF (Atomicity)
Definition: **each attribute value is atomic**, not a set/list.

Common mistakes:
- Splitting into `Course1, Course2` (many NULLs)
- Repeating rows (redundancy)

Conclusion: **1NF is the minimum requirement, not a good design by itself**.

---

## 3. Two Critical Decomposition Properties
1. **Lossless Join**  
   Joining the decomposed tables gives **exactly** the original data.
2. **Dependency Preservation**  
   Original FDs can still be enforced within the sub-relations.

Intuition:
- **Lossless**: shared attributes form a superkey of some sub-relation
- **Dependency preservation**: closures of the projected FDs imply the original FDs

---

## 4. BCNF (Cleaner but Stricter)
Definition: for every non-trivial FD **X → A**, **X must be a superkey**.

Intuition:
- Removes all FD-based redundancy
- May **break dependency preservation**

BCNF decomposition (high level):
1. Find an FD that violates BCNF
2. Decompose along that FD
3. Repeat until BCNF holds

![BCNF decomposition](images/BCNFnomalisation.png)

---

## 5. 3NF (Most Common in Practice)
Definition: for FD **X → A**, either:
- X is a superkey, **or**
- A is a **prime attribute** (part of some candidate key)

3NF eliminates:
- **partial dependencies**
- **transitive dependencies**

![3NF definition](images/3NF.png)

### 5.1 Minimal Cover (Key Tool for 3NF)
Steps:
1. Single-attribute RHS
2. Remove redundant attributes from LHS
3. Remove redundant FDs
4. Merge FDs with the same LHS

![Minimal cover](images/minimal%20cover.png)

### 5.2 3NF Decomposition (Short Version)
1. Compute a minimal cover
2. Create a relation for each LHS group
3. Remove subsumed relations
4. If no relation contains a candidate key, add a key relation

![3NF decomposition](images/3NFnomalisation.png)

---

## 6. BCNF vs 3NF (Exam Favorite)
| Aspect | BCNF | 3NF |
| --- | --- | --- |
| Redundancy | Less | Possible |
| Dependency preservation | May fail | Preserved |
| Usage | Theoretically cleanest | Most practical |

---

## One-Sentence Summary
Normalisation formalises redundancy via FDs and decomposes relations into 3NF/BCNF under lossless-join and dependency-preservation constraints.
