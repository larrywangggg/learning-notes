# FastAPI Data Models and Database Layer (Cleaned Version)

This note connects two core files: `schemas.py` (Pydantic data models) and `db.py` (SQLAlchemy async database layer). The goal is to explain the full path from request data to validation, ORM, and storage.

Pydantic is a data validation and parsing library. It uses type annotations to convert external input into safe Python objects.
Example (invalid input triggers validation errors):
```python
from pydantic import BaseModel

class User(BaseModel):
    age: int

User(age="18")  # converted to int; invalid values raise validation errors
```

## 1. schemas.py: what Pydantic schemas do
- Define request/response shapes
- Validate types automatically
- Generate OpenAPI docs
- Convert JSON into Python objects

### Example: PostCreate
```python
from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str
```

Expected request body:
```json
{
  "title": "My Post",
  "content": "Hello FastAPI"
}
```

Missing fields or wrong types will return 422 automatically.

## 2. Using schemas in routes
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

Key points:
- `post` is a Pydantic object, not a dict
- When you need a dict:
  - Pydantic v2: `post.model_dump()`
  - Pydantic v1: `post.dict()`

## 3. Why schemas live in schemas.py
- Reusable
- Decoupled from database models
- Clear separation between API and storage

## 4. db.py responsibilities
- Define ORM Base and models
- Create async engine
- Create async session factory
- Provide FastAPI-injectable sessions
- Initialize tables

## 5. Base / DeclarativeBase relationship
- `DeclarativeBase` is the template
- `Base` is the project's model registry
- `Base.metadata` stores all table info for migrations/creation
- You can have multiple Base classes for multiple schemas

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

## 6. ORM model example (Post)
UUID is a universally unique identifier, useful for safe primary keys in distributed systems.
Example:
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

Notes:
- SQLite stores UUID as TEXT, PostgreSQL uses native UUID
- `nullable=False` enforces data integrity
- `created_at` is generated at the database layer

## 7. Engine and session factory
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
```

Explanation:
- `create_async_engine` builds the async engine (pool + driver + config).
- `async_sessionmaker` provides a consistent Session factory.
- `DATABASE_URL` selects database type and driver; `sqlite+aiosqlite` is async SQLite.
- `expire_on_commit=False` avoids extra queries after commit.

## 8. Table creation
```python
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

Explanation:
- `engine.begin()` opens an async connection context.
- `run_sync` runs DDL (table creation) in a sync bridge.
- `Base.metadata.create_all` scans all ORM models and creates tables.
- Usually called once on app startup.

## 9. Session dependency
```python
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
```

Explanation:
- `AsyncGenerator[AsyncSession, None]` indicates an async generator dependency.
- `async with` ensures the session is closed after the request.
- `yield` injects the session, then resumes for cleanup.

## 10. Combined usage example
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

Explanation:
- `Depends(get_async_session)` injects a per-request Session.
- `session.add` registers the object, `commit` persists it.
- `refresh` reloads database-generated fields (id, defaults).
- Returning a dict produces a JSON response.

## 11. Common misunderstandings
- `PostCreate` is not a dict; no need for `json.loads()`
- `async` is not "faster", it is "non-blocking"
- `yield` is a lifecycle hook, not a normal return
- You must keep `Base` to collect metadata

## 12. One-line summary
`schemas.py` defines data shape; `db.py` defines how data is stored and retrieved.
