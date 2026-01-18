# FastAPI 数据模型与数据库层整理版

这份笔记把两个核心文件串起来：`schemas.py`（Pydantic 数据模型）和 `db.py`（SQLAlchemy async 数据库层）。目标是把“请求数据 -> 校验 -> ORM -> 数据库”的链路讲清楚。

Pydantic 是一个**数据校验与解析库**，基于类型注解把外部输入转换成安全的 **Python 对象**。
示例（请求体类型不对会报错）：
```python
from pydantic import BaseModel

class User(BaseModel):
    age: int

User(age="18")  # 会被转换成 int，非法值会触发校验错误
```

## 1. schemas.py：Pydantic schema 的职责
- 定义请求/响应数据形状
- 自动做类型校验
- 自动生成 OpenAPI 文档
- 把 JSON 转成 Python 对象

### 示例：PostCreate
```python
from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str
```

请求体应为：
```json
{
  "title": "My Post",
  "content": "Hello FastAPI"
}
```

缺字段或类型不对，FastAPI 会自动返回 422。

## 2. 路由中使用 schema
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/posts")
def create_post(post: PostCreate):
    new_post = {
        "title": post.title,
        "content": post.content,
    }
    return new_post
```

要点：
- `post` 是 Pydantic 对象，不是 dict
- 需要 dict 时：
  - Pydantic v2：`post.model_dump()`
  - Pydantic v1：`post.dict()`

## 3. 为什么 schema 独立放在 schemas.py
- 可复用
- 与数据库模型解耦
- API 层与存储层分离

## 4. db.py 的职责
- 定义 ORM Base 和模型
- 创建 async engine
- 创建 async session 工厂
- 提供 FastAPI 可注入的 session
- 初始化表结构

## 5. Base / DeclarativeBase 的关系
- `DeclarativeBase` 是模板
- `Base` 是项目内的“模型注册中心”
- `Base.metadata` 保存所有表信息，用于建表
- 可以有多套 Base 对应多套 schema

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

## 6. ORM 模型示例（Post）
UUID 是通用唯一标识符，用于生成分布式环境下也安全的主键。
示例：
```python
import uuid
uid = uuid.uuid4()
print(uid)  # e.g. 550e8400-e29b-41d4-a716-446655440000
```

```python
import uuid
import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

说明：
- SQLite 会把 UUID 存成 TEXT，PostgreSQL 用原生 UUID
- `nullable=False` 保证数据完整性
- `created_at` 由数据库层生成，避免信任客户端时间

## 7. 引擎与 Session 工厂
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
```

解释：
- `create_async_engine` 建立异步数据库引擎（连接池 + 驱动 + 配置）。
- `async_sessionmaker` 生成统一配置的 Session 工厂，避免手动创建 Session。
- `DATABASE_URL` 决定数据库类型与驱动，`sqlite+aiosqlite` 表示异步 SQLite。
- `expire_on_commit=False` 可避免 commit 后对象失效导致的额外查询。

## 8. 建表函数
```python
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

解释：
- `engine.begin()` 创建一个异步连接上下文。
- `run_sync` 用同步方式执行 DDL（建表），SQLAlchemy 负责桥接异步。
- `Base.metadata.create_all` 扫描所有 ORM 模型并建表。
- 通常在 FastAPI 启动事件中调用一次。

## 9. Session 依赖注入
```python
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
```

解释：
- `AsyncGenerator[AsyncSession, None]` 告诉类型系统这是一个异步生成器依赖。
- `async with` 确保请求结束后自动关闭 session。
- `yield` 把 session 注入到路由函数，执行完再回到这里做清理。

## 10. 组合使用示例
```python
from fastapi import Depends

@app.post("/posts")
async def create_post(
    payload: PostCreate,
    session: AsyncSession = Depends(get_async_session),
):
    post = Post(title=payload.title, content=payload.content)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return {"id": str(post.id), "title": post.title}
```

解释：
- `Depends(get_async_session)` 注入每个请求独立的 Session。
- `session.add` 把对象加入事务，`commit` 持久化到数据库。
- `refresh` 重新加载数据库生成的字段（如 id、默认值）。
- 返回 dict 作为 JSON 响应。

## 11. 常见误解
- `PostCreate` 不是 dict，不需要 `json.loads()`
- `async` 不是“更快”，而是“不阻塞”
- `yield` 是依赖生命周期钩子，不是普通 return
- `Base` 不能省略，否则无法收集 metadata

## 12. 一句话总结
`schemas.py` 负责“数据长什么样”，`db.py` 负责“数据怎么存取”。
