# SQLAlchemy 关系整理版

这份笔记梳理外键与 `relationship` 的分工，说明一对多/多对多的正确建模方式，并解释常见误区。

## 1. 一对多关系的本质
外键才是数据库层面的真实连接，`relationship` 只是 ORM 的“导航”。

```python
class User(SQLAlchemyBaseUserTableUUID, Base):
    posts = relationship("Post", back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="posts")
```

要点：
- 数据库只认识 `user_id -> user.id`，不会理解 `relationship`。
- ORM 通过 `relationship` 帮你自动写 SQL，例如访问 `user.posts` 时查询 posts 表。

## 2. relationship 与 back_populates
`relationship` 让你在 Python 层“走关系”，`back_populates` 让双向关系保持同步。

```python
user.posts.append(post)  # 自动填充 post.user_id
post.user = user         # user.posts 同步更新
```

没有 `back_populates` 时数据库还能跑，但 ORM 状态容易不同步。

## 3. 多对多必须有中间表
“一个 post 对多个 user” 本质是多对多，需要关联表。

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

使用方式：
```python
post.users.append(user)
session.commit()
```

## 4. 关系类型速查
| 关系 | 外键在哪 | 是否需要中间表 |
| --- | --- | --- |
| 一对多 | 多的一侧 | 否 |
| 一对一 | 任意一侧（加唯一约束） | 否 |
| 多对多 | 无 | 是 |

## 5. 为什么不能“反向外键”解决多对多
错误思路：
```python
class User(Base):
    post_id = Column(ForeignKey("posts.id"))
```

问题：
- User 只能属于一个 Post
- Post 仍然无法关联多个 User
- 语义和需求不匹配

只要双方都是“多个”，就必须是多对多，必须有中间表。
