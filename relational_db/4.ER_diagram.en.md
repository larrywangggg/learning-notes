# ER Diagram (Entity-Relationship) Notes

This file summarizes the core ER/EER concepts, notation, and modeling tips, with the related images for reference.

---

## 1. Basic ER Notation (Peter Chen, 1976)
- **Entity**: rectangle
- **Attribute**: oval
- **Key attribute**: underlined
- **Relationship**: diamond

![ER notation](images/ER%20diagram.png)

---

## 2. Entities, Attributes, and Attribute Types
- **Entity set**: a collection of similar real‑world objects (e.g., Student, Course).
- **Attribute**: describes an entity’s properties (e.g., name, id).
- Common attribute types:
  - **Simple / composite** (e.g., Address can be split into City/Street)
  - **Single-valued / multi-valued** (e.g., phone can be multi-valued)
  - **Derived** (e.g., age derived from dob)

Modeling tips:
- Key attributes must uniquely identify each entity.
- Composite and multi-valued attributes usually require decomposition in the relational model.

---

## 3. Relationships
- **Binary relationships** are the most common (e.g., Student–Enrol–Course).
- Relationships can also have attributes (e.g., EnrolDate, Grade).

### 3.1 Cardinality
- **1:1**: one-to-one
- **1:N**: one-to-many
- **M:N**: many-to-many (typically needs a bridge table)

### 3.2 Participation Constraints
- **Total participation**: every entity must participate (double line)
- **Partial participation**: participation is optional (single line)

---

## 4. Weak Entities
- A **weak entity** depends on a strong entity and cannot be uniquely identified by its own attributes.
- It uses an **identifying relationship** plus the strong entity’s key.

---

## 5. EER (Extended ER) and Inheritance
- **ISA (superclass/subclass)**: subclasses inherit attributes and relationships.
- Useful for modeling specializations (e.g., Student vs Staff).

![EER example](images/EER%20example.png)

---

## 6. Mapping ER to the Relational Model (Intuition)
- Entity -> table
- 1:N relationship -> foreign key on the N side
- M:N relationship -> separate relation with two FKs + relationship attributes
- Weak entity -> primary key includes the strong entity’s key

---

## One-Sentence Summary
ER diagrams abstract the real world using entities, relationships, attributes, and constraints, and serve as the starting point for relational database design.
