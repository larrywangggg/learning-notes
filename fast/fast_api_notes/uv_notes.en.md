# What is uv

One-line takeaway

- pip: traditional, stable, everyone knows Python package installer
- uv: next-gen, blazing-fast Python package + virtual env + dependency manager (a modern replacement for pip)

## What is pip?

pip = Python's package manager

It only does one thing:

- Install third-party libraries into the current Python environment

Common usage

```bash
pip install fastapi
pip install requests
pip freeze > requirements.txt
pip install -r requirements.txt
```

Pros of pip

- Official, included by default
- Mature ecosystem, plenty of tutorials
- Supported by all Python projects

Limitations of pip (you will hit these sooner or later)

- ❌ Doesn't care about Python versions
- ❌ Doesn't create virtual environments
- ❌ Slow dependency resolution
- ❌ requirements.txt drifts easily

👉 So in real projects you usually need pip + venv + other tools together

## What is uv?

uv = next-gen Python toolchain written in Rust  package manager

It combines the things you usually need👇

- pip
- venv
- part of pip-tools / poetry

👉 All merged into one tool

## What can uv do?

- 📦 Install packages (replace pip)
- 🐍 Auto-select / download Python versions
- 🧪 Create and manage virtual environments
- 🔒 Lock dependencies (reproducible)
- ⚡ Very fast (much faster than pip)

Common usage

```bash
uv init
uv add fastapi
uv add uvicorn
uv run uvicorn main:app --reload
```

You will see:

- pyproject.toml
- uv.lock

👉 This is the modern standard shape for Python projects

## pip vs uv (key comparison)

| Dimension | pip | uv |
| --- | --- | --- |
| Install speed | Slow | ⚡ Very fast |
| Virtual envs | Doesn't manage | Automatic |
| Python version | Doesn't manage | Automatic |
| Dependency lock | Manual | Built-in |
| New project experience | A bunch of steps | All-in-one |
| Best for | Beginners | Projects/FastAPI/teams |

## Why do so many people recommend uv now?

Because before, you had to do this👇

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi
pip freeze > requirements.txt
```

Now with uv 👇

```bash
uv init
uv add fastapi
```

Fewer pitfalls, fewer commands, less chance to mess up environments

## How to choose for your case?

✅ Recommended path

- Learn concepts / follow tutorials
  - 👉 If you can read `pip install xxx`, you're fine
- Build your own FastAPI project / assignment / GitHub repo
  - 👉 Use uv directly

A practical suggestion

Knowing pip is the basics; using uv is the next level

Just like:

- Knowing javac is the basics
- Using Gradle / Maven is engineering skill

## Ultra-short summary (memorize this)

- pip: the "screwdriver" for installing packages
- uv: the "toolbox" for packages + env + versions + locks

# How to install uv

## 1. Install uv (macOS / Homebrew scenario)

✅ Most recommended way (doesn't touch your existing Python)

```bash
brew install uv
```

👉 Safest and most stable approach

- Doesn't depend on whether your Python is from Homebrew
- Doesn't pollute system Python
- Installs a standalone uv executable

Verify

```bash
uv --version
which uv
```

You should see something like:

```text
/usr/local/bin/uv
uv 0.x.x
```

⚠️ Not recommended but possible (install via pip)

```bash
pip install uv
```

❌ The problem is:

- pip installs into a specific Python environment
- if you switch Python versions later, uv may "disappear"
- beginners often get stuck here

## 3 things you must understand after installing uv (very important)

1️⃣ uv ≠ pip
- uv is an external tool
- it doesn't belong to any Python interpreter

2️⃣ uv manages Python for you

You can:

```bash
uv python list
uv python install 3.12
```

3️⃣ uv auto-creates .venv

You don't need:

```bash
python -m venv .venv
source .venv/bin/activate
```

uv handles it all.

## 2. Create a FastAPI project with uv (standard flow)

1️⃣ Create project

```bash
mkdir fastapi-demo
cd fastapi-demo
uv init
```

You will see:

- pyproject.toml
- uv.lock

2️⃣ Pin Python version (recommended)

```bash
uv python install 3.12
uv python pin 3.12
```

👉 Project will lock the Python version
👉 Cloned on another machine, it stays consistent

3️⃣ Install FastAPI dependencies

```bash
uv add fastapi
uv add uvicorn
```

This is equivalent to:

```bash
pip install fastapi uvicorn
```

But:

- Faster
- Automatically uses the venv
- Automatically writes config

4️⃣ Write a minimal FastAPI example

main.py

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello FastAPI"}
```

## 3. Common uv commands in FastAPI (key)

🔥 Start the dev server (most common)

```bash
uv run uvicorn main:app --reload
```

Explanation:

- uv run: run a command inside the project venv
- uvicorn main:app: start FastAPI
- --reload: auto-restart on code changes (dev only)

Visit:

- http://127.0.0.1:8000

📘 Auto API docs (built into FastAPI)

- Swagger UI
  - 👉 http://127.0.0.1:8000/docs
- ReDoc
  - 👉 http://127.0.0.1:8000/redoc
- (This is FastAPI's killer feature)

➕ Add new dependencies

```bash
uv add sqlalchemy
uv add pydantic-settings
```

👉 Automatically:

- updates `pyproject.toml`
- updates `uv.lock`

➖ Remove a dependency

```bash
uv remove sqlalchemy
```

📦 List installed packages

```bash
uv pip list
```

(uv is compatible with pip commands internally)

🧪 Run tests (you will use this later)

```bash
uv run pytest
```

🐍 Enter Python REPL for the project

```bash
uv run python
```

👉 This is the correct way
❌ Don't run `python` directly

# 4. Common dependencies added with uv

Remember this: **uv add = add dependency + auto update config + lock versions + reproducible**

## 1) python-dotenv

```bash
uv add python-dotenv
```

What is python-dotenv?

python-dotenv = let Python automatically read environment variables from .env

A typical .env looks like this:

```dotenv
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=super-secret
DEBUG=true
```

With python-dotenv, you can do this in code:

```python
import os

os.getenv("DATABASE_URL")
```

👉 Instead of hardcoding secrets in code

Why almost every FastAPI project uses it

FastAPI projects usually need:

- Database URL
- JWT / Session Secret
- Third-party API keys
- Debug / Prod environment split

These should be:

- ❌ Not in code
- ❌ Not committed to Git
- ✅ Stored in .env

How to use python-dotenv in FastAPI

1️⃣ Create .env

```dotenv
APP_NAME=FastAPI Demo
DEBUG=true
```

2️⃣ Load at startup

```python
from dotenv import load_dotenv

load_dotenv()
```

Common location:

- main.py
- or app/core/config.py

3️⃣ Read variables

```python
import os

app_name = os.getenv("APP_NAME")
debug = os.getenv("DEBUG") == "true"
```

FastAPI officially recommends Pydantic Settings:

```bash
uv add pydantic-settings python-dotenv
```

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    debug: bool = False

class Config:
        env_file = ".env"

settings = Settings()
```

👉 This is production-grade

Common beginner misunderstandings (avoid them)

❌ Misconception 1: uv includes dotenv by default?
No, you must explicitly `uv add python-dotenv`

❌ Misconception 2: .env works automatically?
No, you must:

- use **`load_dotenv()`**
- or use Pydantic Settings

❌ Misconception 3: Can I commit .env to Git?
No, add it to .gitignore

One-line chain summary

> uv add python-dotenv
> = Add "environment variable support" as a formal dependency to your FastAPI project

## 2) imagekitio

```bash
uv add imagekitio
```

👉 Add imagekitio (ImageKit official Python SDK) to your uv project

ImageKit is an image/video CDN + real-time processing platform, commonly used for:

- 📸 Image upload
- 🧠 Auto compression, crop, format conversion
- 🌍 Global CDN acceleration
- 🔐 Secure private storage

👉 Very common in Web / FastAPI projects

What do you usually do with ImageKit in FastAPI?

Typical scenarios:

- User avatar upload
- Product images
- Content management system (CMS)
- Media assets for Notta / SaaS products (this matches your background)

"Standard usage" of imagekitio in FastAPI

1️⃣ Configure environment variables

.env

```dotenv
IMAGEKIT_PUBLIC_KEY=xxx
IMAGEKIT_PRIVATE_KEY=yyy
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_id
```

👉 These keys are in ImageKit account `developer options` > `API Keys`.
👉 Don't hardcode them in code.

2️⃣ Initialize ImageKit client

```python
from imagekitio import ImageKit
import os

imagekit = ImageKit(
    public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
    url_endpoint=os.getenv("IMAGEKIT_URL_ENDPOINT"),
)
```

3️⃣ Upload an image (most common)

```python
result = imagekit.upload_file(
    file=open("avatar.png", "rb"),
    file_name="avatar.png",
)
print(result["url"])
```

👉 Returns a CDN-backed, transformable URL

4️⃣ Use in a FastAPI API route (common pattern)

```python
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    result = imagekit.upload_file(
        file=file.file,
        file_name=file.filename,
    )
    return {"url": result["url"]}
```

ImageKit URL's real power

ImageKit supports URL-param transforms:

https://ik.imagekit.io/xxx/avatar.png?tr=w-300,h-300,fo-auto

- No re-upload
- No re-storage
- Instant crop/compression via URL params

👉 Great for performance and storage cost

Common pitfalls (important)

❌ 1. Forgot to install python-dotenv
If you use .env, usually you need:

```bash
uv add python-dotenv
```

Otherwise env vars may not load.

❌ 2. Committing private key into Git
Must be:

.env

❌ 3. Sending files to ImageKit without validation
In production, at least:

- validate file type
- validate file size
- prevent arbitrary file upload

imagekitio vs other options (quick comparison)

| Option | Best for |
| --- | --- |
| imagekitio | Image-heavy, front-end display, CDN-first |
| S3 + CloudFront | General storage, backend-leaning |
| Cloudinary | Similar to ImageKit, pricier |
| Local storage | ❌ Not for production |

One-line summary

> uv add imagekitio
> = Add "pro-level image upload + CDN + real-time processing" to your FastAPI project

## 3) uvicorn[standard]

One-line takeaway

```bash
uv add uvicorn[standard]
```

👉 Install the "full" uvicorn server for FastAPI (uvicorn + a recommended set of performance extras)

Break down the command

1️⃣ uv add

- Add dependency to the current project
- Auto update:
  - pyproject.toml
  - uv.lock
- Install into uv-managed venv

2️⃣ uvicorn

- The most common ASGI server for FastAPI
- Receives HTTP requests, passes to FastAPI, returns response
- Without uvicorn, FastAPI won't run

3️⃣ [standard]

- Python extras syntax
- Means install uvicorn + the official recommended extra components

uvicorn[standard] usually includes

| Component | Purpose |
| --- | --- |
| uvloop | 🚀 Faster event loop (Linux / macOS) |
| httptools | ⚡ Faster HTTP parsing |
| watchfiles | 🔁 --reload hot reload |
| python-dotenv | 🌱 .env support |
| websockets | 🔌 WebSocket support |

Difference vs uv add uvicorn

| Command | Best for |
| --- | --- |
| uv add uvicorn | Minimal install (runs but bare) |
| uv add uvicorn[standard] | ✅ Recommended: dev / project / deployment |

👉 99% of FastAPI projects should use [standard]

```bash
uv add uvicorn[standard]
```

You will get:

- pyproject.toml records:
  ```toml
  uvicorn = { extras = ["standard"], version = "*" }
  ```
- uv.lock pinned versions
- After clone, others can run:
  ```bash
  uv sync
  ```
  → identical environment

Common beginner misunderstandings

❌ "Is standard required?" Not required, but strongly recommended

❌ "Is standard too heavy?" No, it's all common FastAPI components

❌ "Do I need it in production?" Yes, and you typically add gunicorn or --workers

Recommended combo (remember this)

```bash
uv add fastapi uvicorn[standard]
```

One-line memory hook

uvicorn[standard] = "runs + runs fast + fewer pitfalls"

## 4) aiosqlite

One-line takeaway

```bash
uv add aiosqlite
```

👉 Add "async SQLite support" to your uv project

What is aiosqlite?

aiosqlite = async wrapper for SQLite

- SQLite: lightweight, file-based database
- aiosqlite: wraps SQLite with async/await

👉 Good for: learning / assignments / prototypes / small projects / FastAPI

Why FastAPI should use aiosqlite instead of sqlite3

sqlite3 is synchronous and blocks the event loop;
aiosqlite solves exactly this.

What happens behind `uv add aiosqlite`?

- 1️⃣ Install into project venv
- 2️⃣ Write into pyproject.toml
- 3️⃣ Lock in uv.lock
- 4️⃣ uv sync reproducible

FastAPI + aiosqlite minimal example

1️⃣ Initialize DB

```python
import aiosqlite
import asyncio

async def init_db():
    async with aiosqlite.connect("test.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
        """)
        await db.commit()

asyncio.run(init_db())
```

2️⃣ Use in route

```python
from fastapi import FastAPI
import aiosqlite

app = FastAPI()

@app.get("/users")
async def get_users():
    async with aiosqlite.connect("test.db") as db:
        async with db.execute("SELECT id, name FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows
```

Common "standard wrapper" (recommended)

```python
# db.py
import aiosqlite

async def get_db():
    async with aiosqlite.connect("app.db") as db:
        yield db

# main.py
from fastapi import Depends
from db import get_db

@app.get("/users")
async def users(db=Depends(get_db)):
    async with db.execute("SELECT * FROM users") as cur:
        return await cur.fetchall()
```

Pros & limits of aiosqlite

✅ Pros

- Zero config
- Single file database
- Great for learning / small / single-machine

⚠️ Limits (important)

- Weak concurrent writes
- Not for high-concurrency production
- No complex user permissions

👉 Later you'll upgrade to:

- PostgreSQL + asyncpg
- MySQL + aiomysql

Common pitfalls

❌ 1. sqlite3 + async def (fake async)

❌ 2. Forget commit (writes must `await db.commit()`)

❌ 3. Many concurrent writes (SQLite write locks conflict easily)

One-line summary

> uv add aiosqlite
> = Let FastAPI access SQLite the "correct async way"

# 5. Common uv commands

| Category | Command | Description |
| --- | --- | --- |
| Install | brew install uv | Install uv on macOS (recommended) |
| Version | uv --version | Check uv version |
| Init | uv init | Initialize project (generate pyproject.toml) |
| Python | uv python list | List available / installed Python versions |
| Python | uv python install 3.12 | Download and install a specific Python version |
| Python | uv python pin 3.12 | Pin Python version for the project |
| Dependencies | uv add fastapi | Add dependency (equivalent to pip install) |
| Dependencies | uv add uvicorn sqlalchemy | Add multiple dependencies at once |
| Dependencies | uv remove sqlalchemy | Remove dependency |
| Dependencies | uv pip list | List installed packages in current env |
| Lock | uv lock | Regenerate uv.lock |
| Run | uv run python | Start Python in project venv |
| Run | uv run uvicorn main:app --reload | Start FastAPI dev server |
| Run | uv run pytest | Run tests |
| Run | uv run <cmd> | Run any command inside uv-managed env |
| Sync | uv sync | Install deps based on pyproject.toml + uv.lock |
| Clean | uv cache clean | Clean uv cache |
| Help | uv help | Show uv help |
