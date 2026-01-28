# Functional Dependencies（函数依赖）整理

本节聚焦：**为何会出现冗余/异常、什么是 FD、如何用 FD 找 key、如何指导拆表**。

---

## 1. 为什么要学 FD
一个“看起来没问题”的大表（如 ENROLMENT）经常出现：
- **数据冗余**：同一学生信息重复存储
- **数据不一致**：同一 StudentID 出现不同 DoB
- **更新异常**：更新/插入/删除会连带影响不该变的数据

FD 的价值：**解释这些问题为什么必然发生**，并提供“拆表”的依据。

---

## 2. 什么是 FD（核心定义）
**X → Y** 表示：在关系中，若两行在 X 上相同，则在 Y 上也必须相同。  
X 是 **determinant**，Y 是 **dependent**。

判断 FD 是否成立的方法：
- 看是否存在两行 **X 相同但 Y 不同**。
- 有则违背，无则成立（在该关系中）。

---

## 3. FD 的来源
1. **语义/业务规则（最可靠）**  
   例：`StudentID → Name, DoB`
2. **样本数据（仅提示，不能保证）**  
   “在样本中成立 ≠ 在现实中成立”

---

## 4. FD 与 Key 的关系（必会）
- **X⁺（closure）包含所有属性** ⇒ X 是 superkey  
- **最小 superkey** ⇒ candidate key

![Key 与 FD 的关系示例](images/keys.png)

---

## 5. Armstrong 推理规则（推导 FD）
常用三条基础规则：
- **反身性**：若 Y ⊆ X，则 X → Y  
- **增广性**：若 X → Y，则 XZ → YZ  
- **传递性**：若 X → Y 且 Y → Z，则 X → Z

![Armstrong 推理规则](images/armstrong%20inference%20rules.png)

补充常用推导（由基础规则组合得到）：
- **合并（Union）**：X → Y 且 X → Z ⇒ X → YZ
- **分解（Decomposition）**：X → YZ ⇒ X → Y 且 X → Z
- **伪传递（Pseudotransitivity）**：X → Y 且 WY → Z ⇒ WX → Z

![其他常用规则](images/other%20rules.png)

---

## 6. FD 如何导致冗余与异常（直觉）
如果**非主属性依赖于非 key**：
-> 数据冗余不可避免  
-> 更新异常不可避免  
这就是后续 **规范化（Normalisation）** 要解决的根因。

---

## 7. 用 FD 指导拆表（示例直觉）
原表：
```
ENROLMENT(StudentID, Name, DoB, CourseNo, Unit, Semester)
```
常见 FD：
- `StudentID → Name, DoB`
- `CourseNo → Unit`

拆分为：
- `STUDENT(StudentID, Name, DoB)`
- `COURSE(CourseNo, Unit)`
- `ENROL(StudentID, CourseNo, Semester)`

拆表依据不是“感觉”，而是 **FD 约束**。

---

## 一句话总结
FD 用形式化方式说明“哪些属性决定哪些属性”，帮助识别 key、解释冗余与异常，并为规范化拆表提供严格依据。
