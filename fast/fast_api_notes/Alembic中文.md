# Alembic 速记（中文）

目标：理解 Alembic 在 FastAPI/SQLAlchemy 项目里的作用、工作流与关键文件。

---

## 1. Alembic 是什么
一句话：**Alembic 是 SQLAlchemy 官方的数据库 schema 版本管理工具**。  
它把每次表结构变化记录成 migration 脚本，像“数据库的 Git commit”。

---

## 2. 为什么一定要用 Alembic
不使用会出现：
- 本地/测试/生产 schema 不一致
- 无法追溯“表是怎么变成这样的”
- 手动改表不可回滚

示例（不用 Alembic 的混乱场景）：
- A 同学在本地手动加了 `users.nickname`
- B 同学在测试库加了 `users.age`
- 生产库还停留在旧结构
结果：
- 同一段代码在不同环境报错
- 不知道该先加哪个字段、加了会不会冲突
- 出问题时无法回滚到“上一版结构”

使用 Alembic 的收益：
- **版本可追踪**（有 revision 与 down_revision）
- **多环境一致**（统一 upgrade）
- **可回滚**（downgrade）

---

## 3. 三个核心角色
1. **SQLAlchemy Models**：理想结构（你写的 ORM 模型）
2. **Database**：真实结构（PostgreSQL 里的实际表）
3. **Migration Scripts**：把“现实”变成“理想”的桥梁

示例（模型改动）：
```python
class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String, unique=True, nullable=False)
    is_active = mapped_column(Boolean, default=True)  # 新增字段
```

---

## 4. 关键目录与文件
```
alembic/
├─ env.py
├─ script.py.mako
└─ versions/
   ├─ xxxx_init.py
   └─ yyyy_create_jobs_and_results.py
```

- `alembic/versions/*.py`：迁移脚本，包含 `upgrade()` / `downgrade()`
- `alembic/env.py`：读取 `DATABASE_URL`，加载 `Base.metadata`
- `alembic_version` 表：记录当前数据库版本

示例（migration 脚本片段）：
```python
def upgrade():
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=True))

def downgrade():
    op.drop_column("users", "is_active")
```

示例（env.py 关键配置片段）：
```python
from app.db import Base
target_metadata = Base.metadata
```

---

## 5. 标准工作流（最常用）
1. **改模型**（SQLAlchemy Models）
2. **生成迁移**  
   `alembic revision --autogenerate -m "add xxx"`
3. **执行迁移**  
   `alembic upgrade head`

回滚：
`alembic downgrade -1`

示例（实际命令）：
```bash
alembic revision --autogenerate -m "add users.is_active"
alembic upgrade head
```

统一流程的“脑内模型”：
```
models.py
↓
alembic revision（生成脚本）
↓
alembic upgrade（执行脚本）
↓
数据库 schema 改变
↓
alembic_version 记录当前版本
```

---

## 6. Autogenerate 在做什么
`--autogenerate` 会：
- 读取 `Base.metadata`
- 对比当前数据库结构
- 生成差异 migration 文件  
说明：**只生成文件，不改数据库**。

示例（输出提示）：
```
INFO  [alembic.autogenerate.compare] Detected added column 'users.is_active'
```

---

## 7. 常见注意点
- 修改模型后一定要生成并执行 migration
- migration 里要检查自动生成的内容是否正确
- 线上环境只执行 `upgrade`，不要手工改表
- `alembic_version` 表只有一行，表示当前版本号

---

## 一句话总结
Alembic 把数据库结构变化流程化、可追踪、可回滚，是后端项目“可长期维护”的基础设施。
