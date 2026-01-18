# SQLAlchemy Session (Cleaned Version)

Session is your "workbench" for talking to the database. It is not the database, not a connection, and not a table. It is the unified context for a unit of work.

## 1. One-line definition
Session = the unified context for all database operations within a single transaction.

## 2. What Session manages
### 2.1 Transactions (commit / rollback)
```python
session.add(post)
await session.commit()
```
- Before commit, the database is unchanged
- After commit, changes are persisted

### 2.2 Object states (object ↔ database)
```python
post = Post(url="x", file_type="y")
session.add(post)
```
Common states:
- transient: pure Python object
- pending: added to the session
- persistent: stored in the DB and tracked
- detached: removed from the session

### 2.3 Identity map (cache)
```python
post1 = await session.get(Post, id)
post2 = await session.get(Post, id)
```
Within the same session, the object is loaded once, avoiding duplicate queries.

### 2.4 Connections (but not the connection itself)
Session needs a connection to work, but it is a management layer, not the connection.

## 3. What AsyncSession means
AsyncSession does not change the responsibilities. It only avoids blocking the event loop while waiting for I/O:
- transactions
- object states
- identity map
- flush / commit / rollback

## 4. Why FastAPI uses "one session per request"
Correct lifecycle:
```
request start -> create session -> business logic -> commit/rollback -> close session -> request end
```
Sharing a session leads to:
- cross-request data leaks
- dirty state
- concurrency issues
- hard debugging

## 5. FastAPI dependency pattern
```python
async def get_async_session():
    async with async_session_maker() as session:
        yield session
```
Meaning:
"Each request gets a new workbench, and it is cleaned up automatically."

## 6. Common misconceptions
- Session = database connection (wrong)
- Session = ORM object (wrong)
- One global session is enough (wrong)

## 7. Memory hook
Session ≈ Git working tree:
- you make many changes (add / update)
- before commit, the database is unchanged
- commit applies everything at once

## 8. Ultra-short summary
Session is the ORM core: it manages transactions, object state, and consistency; use one per request and close it.
