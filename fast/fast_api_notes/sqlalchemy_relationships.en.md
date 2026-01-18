# SQLAlchemy Relationships (Cleaned Version)

This note explains how foreign keys and `relationship` work together, when to use many-to-many tables, and common pitfalls.

## 1. One-to-many basics
The foreign key is the real database link; `relationship` is ORM navigation.

```python
class User(SQLAlchemyBaseUserTableUUID, Base):
    posts = relationship("Post", back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="posts")
```

Key points:
- The DB only knows `user_id -> user.id`.
- The ORM uses `relationship` to generate SQL when you access `user.posts`.

## 2. relationship and back_populates
`relationship` lets you traverse relations in Python; `back_populates` keeps both sides in sync.

```python
user.posts.append(post)  # fills post.user_id
post.user = user         # updates user.posts
```

Without `back_populates`, the DB still works, but ORM state can drift.

## 3. Many-to-many requires an association table
"One post for multiple users" is many-to-many and needs a join table.

```python
user_posts = Table(
    "user_posts",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True),
    Column("post_id", UUID(as_uuid=True), ForeignKey("posts.id"), primary_key=True),
)
```

```python
class User(SQLAlchemyBaseUserTableUUID, Base):
    posts = relationship("Post", secondary=user_posts, back_populates="users")

class Post(Base):
    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    users = relationship("User", secondary=user_posts, back_populates="posts")
```

Usage:
```python
post.users.append(user)
session.commit()
```

## 4. Relationship quick reference
| Relationship | Foreign key location | Join table needed |
| --- | --- | --- |
| one-to-many | on the "many" side | no |
| one-to-one | either side (unique constraint) | no |
| many-to-many | none | yes |

## 5. Why "reverse foreign key" is wrong for many-to-many
Wrong approach:
```python
class User(Base):
    post_id = Column(ForeignKey("posts.id"))
```

Issues:
- User can only belong to one Post
- Post still cannot map to many Users
- The semantics are incorrect

If both sides are "many", you must use a join table.
