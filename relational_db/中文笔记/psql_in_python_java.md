# 在 Python 与 Java 工程中使用 PostgreSQL（含 ORM）

在 Python / Java 工程中连接 PostgreSQL（psql 服务器）的常见方式与 ORM 实践。  

---

## 1. 通用准备
- 安装 PostgreSQL 并确保 `psql` 可用
- 建好 Database / User / Password
- 连接串示例：
  - `postgresql://user:password@host:5432/dbname`

---

## 2. Python 工程

### 2.1 直接使用 Driver（psycopg）
```python
import psycopg

conn = psycopg.connect("postgresql://user:password@host:5432/dbname")
with conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE email = %s", ("a@ex.com",))
    rows = cur.fetchall()
conn.close()
```
说明：
- `psycopg.connect(...)` 创建数据库连接
- `conn.cursor()` 创建游标执行 SQL
- `execute(..., params)` 使用参数化查询（`%s`），防 SQL injection
- `fetchall()` 取回查询结果
- `conn.close()` 关闭连接释放资源

---

### 2.2 SQLAlchemy ORM
```python
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

engine = create_engine("postgresql+psycopg://user:password@host:5432/dbname")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)

Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add(User(email="a@ex.com"))
    session.commit()
```
说明：
- `create_engine(...)` 创建 SQLAlchemy 引擎（连接池入口）
- `DeclarativeBase` 定义 ORM 基类
- `User` 类映射到 `users` 表
- `mapped_column(...)` 定义列属性与约束
- `create_all(...)` 按模型创建表
- `Session(...)` 打开会话
- `add(...)` 添加对象，`commit()` 提交事务

---

### 2.3 FastAPI + SQLAlchemy（典型项目结构）
- `database.py`：engine / session
- `models.py`：ORM model
- `crud.py`：查询逻辑
- `routers/`：API 入口

说明：分层结构便于维护与测试。

---

## 3. Java 工程

### 3.1 JDBC 直连
```java
import java.sql.*;

String url = "jdbc:postgresql://host:5432/dbname";
String user = "user";
String password = "password";

try (Connection conn = DriverManager.getConnection(url, user, password)) {
    String sql = "SELECT id, email FROM users WHERE email = ?";
    try (PreparedStatement ps = conn.prepareStatement(sql)) {
        ps.setString(1, "a@ex.com");
        ResultSet rs = ps.executeQuery();
        while (rs.next()) {
            System.out.println(rs.getInt("id") + " " + rs.getString("email"));
        }
    }
}
```
说明：
- `DriverManager.getConnection(...)` 获取数据库连接
- `PreparedStatement` 预编译 SQL，占位符 `?` 绑定参数
- `setString(1, ...)` 设置第一个参数
- `executeQuery()` 执行查询
- `ResultSet` 逐行读取结果
- `try-with-resources` 自动关闭连接/语句/结果集

---

### 3.2 JPA / Hibernate ORM
`application.properties` 示例（Spring Boot）：
```properties
spring.datasource.url=jdbc:postgresql://host:5432/dbname
spring.datasource.username=user
spring.datasource.password=password
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
```

Entity 示例：
```java
import jakarta.persistence.*;

@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true)
    private String email;
}
```
说明：
- `@Entity` 标记为持久化实体
- `@Table` 指定表名
- `@Id` 声明主键
- `@GeneratedValue` 主键生成策略
- `@Column(unique = true)` 列唯一约束

---

## 4. ORM 选型建议
| 场景 | 建议 |
| --- | --- |
| 简单脚本 / 工具 | Driver 直连 |
| 中大型项目 | ORM |
| 性能极致 | Driver + 手写 SQL |

---

## 4.1 Java vs Python 生态对照
| Java 生态 | Python 生态 | 说明 |
| --- | --- | --- |
| **JDBC** | **DB-API / psycopg** | 低层数据库访问接口 |
| **JPA** | **SQLAlchemy ORM** | ORM 规范/抽象 |
| **Hibernate** | **SQLAlchemy ORM** | ORM 常用实现 |

---

## 5. 常见实践建议
- 统一配置连接串（环境变量/配置文件）
- 使用连接池（`SQLAlchemy pool`, `HikariCP`）
- 对关键查询加 `EXPLAIN ANALYZE`
- 事务边界清晰（`BEGIN/COMMIT`）

---

## 一句话总结
Python 通常用 `psycopg + SQLAlchemy`，Java 常用 `JDBC + JPA/Hibernate`；中大型项目优先 ORM，性能敏感场景保留原生 SQL。
