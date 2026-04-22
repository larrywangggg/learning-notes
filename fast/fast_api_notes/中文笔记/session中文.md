# SQLAlchemy Session 整理版

Session 是你和数据库之间的一次**对话窗口 / 工作台**。它不是数据库、不是连接、不是表，而是你进行一段业务操作时的统一上下文。

## 1. 一句话理解
Session = 一次事务内所有数据库操作的“统一上下文”。

## 2. Session 在管理什么
### 2.1 事务（commit / rollback）
```python
session.add(post)
await session.commit()
```
- commit 前数据库还没变
- commit 后才真正落库

### 2.2 对象状态（对象 ↔ 数据库）
```python
post = Post(url="x", file_type="y")
session.add(post)
```
对象状态会在以下几种之间切换：
- transient：纯 Python 对象
- pending：已加入 session
- persistent：已落库且在 session 中
- detached：脱离 session

### 2.3 缓存（Identity Map）
```python
post1 = await session.get(Post, id)
post2 = await session.get(Post, id)
```
同一个 session 内不会重复查库，避免对象不一致。

### 2.4 连接（但不是连接本身）
Session 需要连接来工作，但它是“管理层”，不是连接本体。

## 3. AsyncSession 是什么
AsyncSession 只是在等待数据库时不阻塞事件循环，核心职责不变：
- 管事务
- 管对象状态
- 管缓存
- 管 flush / commit / rollback

## 4. 为什么 FastAPI 要“每个请求一个 Session”
正确生命周期：
```
请求开始 -> 创建 session -> 业务逻辑 -> commit/rollback -> 关闭 session -> 请求结束
```
如果共用 Session，会带来：
- 数据串读
- 脏状态
- 并发问题
- 难以排查

## 5. FastAPI 依赖注入写法
```python
async def get_async_session():
    async with async_session_maker() as session:
        yield session
```
含义是：
“每个请求给一张新桌子，用完自动收走。”

## 6. 常见误区
- Session = 数据库连接（错）
- Session = ORM 对象（错）
- 一个项目只需要一个 Session（错）

## 7. 记忆钩子
Session ≈ Git 的 working tree：
- 你做了很多变更（add / update）
- commit 前数据库不变
- commit 后一次性生效

## 8. 超短总结
Session 是 ORM 的核心：管事务、对象状态和一致性；每个请求一个，用完就关。
