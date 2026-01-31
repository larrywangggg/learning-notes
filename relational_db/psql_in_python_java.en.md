# Using PostgreSQL in Python and Java (Including ORM)

Goal: show common ways to connect to PostgreSQL in Python/Java and use ORMs.  
Key terms kept in English.

---

## 1. General Setup
- Install PostgreSQL and ensure `psql` works
- Create Database / User / Password
- Connection string example:
  - `postgresql://user:password@host:5432/dbname`

---

## 2. Python

### 2.1 Driver (psycopg)
```python
import psycopg

conn = psycopg.connect("postgresql://user:password@host:5432/dbname")
with conn.cursor() as cur:
    cur.execute("SELECT id, email FROM users WHERE email = %s", ("a@ex.com",))
    rows = cur.fetchall()
conn.close()
```
Explanation:
- `psycopg.connect(...)` opens a DB connection
- `conn.cursor()` creates a cursor to execute SQL
- `execute(..., params)` uses parameterized queries to prevent SQL injection
- `fetchall()` retrieves results
- `conn.close()` releases the connection

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
Explanation:
- `create_engine(...)` creates the SQLAlchemy engine (entry to the pool)
- `DeclarativeBase` defines the ORM base class
- `User` maps to the `users` table
- `mapped_column(...)` defines columns and constraints
- `create_all(...)` creates tables from models
- `Session(...)` opens a session
- `add(...)` stages data; `commit()` writes it

---

### 2.3 FastAPI + SQLAlchemy (Typical Layout)
- `database.py`: engine/session
- `models.py`: ORM models
- `crud.py`: query logic
- `routers/`: API endpoints

Explanation: layered structure improves maintainability and testing.

---

## 3. Java

### 3.1 JDBC (Direct)
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
Explanation:
- `DriverManager.getConnection(...)` opens a connection
- `PreparedStatement` precompiles SQL and binds parameters
- `setString(1, ...)` sets the first placeholder
- `executeQuery()` runs the query
- `ResultSet` iterates rows
- try‑with‑resources auto‑closes resources

---

### 3.2 JPA / Hibernate ORM
`application.properties` (Spring Boot):
```properties
spring.datasource.url=jdbc:postgresql://host:5432/dbname
spring.datasource.username=user
spring.datasource.password=password
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
```

Entity:
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
Explanation:
- `@Entity` marks a persistent entity
- `@Table` sets the table name
- `@Id` defines the primary key
- `@GeneratedValue` sets key generation strategy
- `@Column(unique = true)` adds a uniqueness constraint
- `ddl-auto` should be used only in dev

---

## 4. ORM Selection
| Scenario | Recommendation |
| --- | --- |
| Small scripts/tools | Driver only |
| Medium/large apps | ORM |
| Max performance | Driver + hand‑written SQL |

---

## 4.1 Java vs Python Ecosystem Map
| Java | Python | Note |
| --- | --- | --- |
| **JDBC** | **DB‑API / psycopg** | Low‑level driver API |
| **JPA** | **SQLAlchemy ORM** | ORM spec/abstraction |
| **Hibernate** | **SQLAlchemy ORM** | Common ORM implementation |

---

## 5. Practical Tips
- Centralize connection strings (env/config)
- Use connection pools (`SQLAlchemy pool`, `HikariCP`)
- Use `EXPLAIN ANALYZE` for critical queries
- Keep transaction boundaries clear (`BEGIN/COMMIT`)

---

## One‑Sentence Summary
Python commonly uses `psycopg + SQLAlchemy`, Java uses `JDBC + JPA/Hibernate`; ORM fits larger apps, while raw SQL fits performance‑critical paths.
