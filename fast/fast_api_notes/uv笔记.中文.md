# 什么是uv

一句话先给结论

- pip：传统、稳定、人人都会用的 Python 包安装器
- uv：新一代、超快的 Python 包 + 虚拟环境 + 依赖管理工具（pip 的现代替代者）

## pip 是什么？

pip = Python 的包管理器

它只做一件事：

- 把第三方库装进当前 Python 环境

常见用法

```bash
pip install fastapi
pip install requests
pip freeze > requirements.txt
pip install -r requirements.txt
```

pip 的优点

- 官方、默认自带
- 生态成熟，教程多
- 所有 Python 项目都支持

pip 的局限（你迟早会遇到）

- ❌ 不管 Python 版本
- ❌ 不创建虚拟环境
- ❌ 依赖解析慢
- ❌ requirements.txt 容易“漂”

👉 所以真实项目里通常要 pip + venv + 其他工具 搭配使用

## uv 是什么？

uv = Rust 写的下一代 Python 工具链  package manager

它把你平时要用的这些东西👇

- pip
- venv
- pip-tools / poetry 的一部分能力

👉 全部合并成一个工具

## uv 能干什么？

- 📦 安装包（替代 pip）
- 🐍 自动选择 / 下载 Python 版本
- 🧪 创建并管理虚拟环境
- 🔒 锁定依赖（可复现）
- ⚡ 速度极快（比 pip 快很多）

常见用法

```bash
uv init
uv add fastapi
uv add uvicorn
uv run uvicorn main:app --reload
```

你会看到：

- pyproject.toml
- uv.lock

👉 这就是现代 Python 项目的标准形态

## pip vs uv 对比（重点）

| 维度 | pip | uv |
| --- | --- | --- |
| 安装速度 | 慢 | ⚡ 非常快 |
| 虚拟环境 | 不管 | 自动 |
| Python版本 | 不管 | 自动 |
| 依赖锁定 | 手动 | 内置 |
| 新项目体验 | 一堆步骤 | 一条龙 |
| 适合谁 | 初学 | 项目/FastAPI/团队 |

## 为什么现在很多人推荐 uv？

因为以前你要这样👇

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi
pip freeze > requirements.txt
```

现在用 uv 👇

```bash
uv init
uv add fastapi
```

更少坑、更少命令、更不容易搞乱环境

## 在你的场景里怎么选？

✅ 推荐你现在这样用

- 学习概念 / 看教程
  - 👉 看得懂 pip install xxx 就行
- 自己建 FastAPI 项目 / 作业 / GitHub repo
  - 👉 直接用 uv

一个现实建议

会 pip 是基础，用 uv 是进阶

就像：

- 会 javac 是基础
- 用 Gradle / Maven 是工程能力

## 一个超短总结（可以记住）

- pip：装包的“螺丝刀”
- uv：装包 + 环境 + 版本 + 锁定的“工具箱”

# 怎么安装uv

## 一、uv 怎么安装（macOS / Homebrew 场景）

✅ 最推荐方式（不碰现有 Python）

```bash
brew install uv
```

👉 这是最安全、最稳妥的方式

- 不依赖你当前 Python 是不是 Homebrew
- 不污染系统 Python
- 安装完就是一个独立的 uv 可执行文件

验证

```bash
uv --version
which uv
```

正常应看到类似：

```text
/usr/local/bin/uv
uv 0.x.x
```

⚠️ 不推荐但可行的方式（用 pip 装）

```bash
pip install uv
```

❌ 问题在于：

- pip 是装到 某个 Python 环境里的
- 你以后切 Python 版本，uv 可能“消失”
- 新手最容易在这里卡住



## uv 安装后你需要理解的 3 件事（非常重要）

1️⃣ uv ≠ pip
- uv 是 外部工具
- 不属于任何 Python 解释器

2️⃣ uv 会自己管理 Python

你可以：

```bash
uv python list
uv python install 3.12
```


3️⃣ uv 会自动创建 .venv

你不需要：

```bash
python -m venv .venv
source .venv/bin/activate
```

uv 全包了。

## 二、用 uv 创建 FastAPI 项目（标准流程）

1️⃣ 创建项目

```bash
mkdir fastapi-demo
cd fastapi-demo
uv init
```

你会看到：

- pyproject.toml
- uv.lock

2️⃣ 指定 Python 版本（推荐）

```bash
uv python install 3.12
uv python pin 3.12
```

👉 项目里会锁死 Python 版本
👉 以后 clone 到别的机器也一致

3️⃣ 安装 FastAPI 相关依赖

```bash
uv add fastapi
uv add uvicorn
```

这一步等价于：

```bash
pip install fastapi uvicorn
```

但：

- 更快
- 自动进虚拟环境
- 自动写配置

4️⃣ 写一个最小 FastAPI 示例

main.py

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello FastAPI"}
```

## 三、FastAPI 在 uv 下的常用指令（重点）

🔥 启动开发服务器（最常用）

```bash
uv run uvicorn main:app --reload
```

解释一下：

- uv run：在 项目虚拟环境里运行命令
- uvicorn main:app：启动 FastAPI
- --reload：代码改了自动重启（开发用）

访问：

- http://127.0.0.1:8000

📘 自动 API 文档（FastAPI 自带）

- Swagger UI
  - 👉 http://127.0.0.1:8000/docs
- ReDoc
  - 👉 http://127.0.0.1:8000/redoc
- （这个是 FastAPI 的杀手级特性）

➕ 添加新依赖

```bash
uv add sqlalchemy
uv add pydantic-settings
```

👉 自动：

- 更新 `pyproject.toml`
- 更新 `uv.lock`

➖ 删除依赖

```bash
uv remove sqlalchemy
```

📦 查看依赖

```bash
uv pip list
```

（uv 内部兼容 pip 命令）

🧪 运行测试（以后一定会用）

```bash
uv run pytest
```

🐍 进入项目 Python REPL

```bash
uv run python
```

👉 这是正确的方式
❌ 不要直接敲 python

# 四、uv add 常见依赖示例

先记住一句：**uv add = 把依赖加进项目 + 自动更新配置 + 锁版本 + 可复现**

## 1) python-dotenv

```bash
uv add python-dotenv
```


python-dotenv 是什么？

python-dotenv = 让 Python 自动读取 .env 文件里的环境变量

典型 .env 文件长这样：

```dotenv
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=super-secret
DEBUG=true
```

有了 python-dotenv，你就可以在代码里这样用：

```python
import os

os.getenv("DATABASE_URL")
```

👉 而不用把密码、密钥写死在代码里

为什么 FastAPI 项目几乎一定会用到它？

FastAPI 项目通常需要：

- 数据库地址
- JWT / Session Secret
- 第三方 API Key
- Debug / Prod 环境区分

这些都应该：

- ❌ 不写进代码
- ❌ 不提交到 Git
- ✅ 放在 .env

在 FastAPI 里怎么用 python-dotenv？

1️⃣ 创建 .env

```dotenv
APP_NAME=FastAPI Demo
DEBUG=true
```

2️⃣ 在项目启动时加载

```python
from dotenv import load_dotenv

load_dotenv()
```

通常放在：

- main.py
- 或 app/core/config.py

3️⃣ 读取变量

```python
import os

app_name = os.getenv("APP_NAME")
debug = os.getenv("DEBUG") == "true"
```



FastAPI 官方推荐搭配 Pydantic Settings：

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

👉 这是生产级写法


新手最常见误解（帮你避坑）

❌ 误解 1：uv 自带 dotenv？
不带，必须显式 uv add python-dotenv

❌ 误解 2：.env 会自动生效？
不会，必须：

- 用 **`load_dotenv()`**
- 或用 Pydantic Settings

❌ 误解 3：.env 可以提交到 Git？
不可以，记得加到 .gitignore

用一句话把整个链路串起来

> uv add python-dotenv
> = 把“环境变量支持”作为项目的正式依赖加进 FastAPI 项目

## 2) imagekitio


```bash
uv add imagekitio
```

👉 把 imagekitio（ImageKit 官方 Python SDK）加入你当前 uv 项目的依赖


ImageKit 是一个 图片 / 视频 CDN + 实时处理平台，常用于：

- 📸 图片上传
- 🧠 自动压缩、裁剪、格式转换
- 🌍 全球 CDN 加速
- 🔐 安全私有存储

👉 在 Web / FastAPI 项目中，非常常见

你在 FastAPI 里通常用 ImageKit 干什么？

典型场景：

- 用户头像上传
- 商品图片
- 内容管理系统（CMS）
- Notta / SaaS 产品里的媒体资源（你这个背景很熟）

imagekitio 在 FastAPI 中的“标准用法”

1️⃣ 配置环境变量

.env

```dotenv
IMAGEKIT_PUBLIC_KEY=xxx
IMAGEKIT_PRIVATE_KEY=yyy
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_id
```

👉 这几个KEY在imagekitio的个人账号的 `developer options` > `API Keys`里。
👉 不要写死在代码里。

2️⃣ 初始化 ImageKit 客户端

```python
from imagekitio import ImageKit
import os

imagekit = ImageKit(
    public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
    url_endpoint=os.getenv("IMAGEKIT_URL_ENDPOINT"),
)
```

3️⃣ 上传图片（最常用）

```python
result = imagekit.upload_file(
    file=open("avatar.png", "rb"),
    file_name="avatar.png",
)
print(result["url"])
```

👉 返回的是 已经走 CDN + 可变换的 URL

4️⃣ 在 FastAPI API 里用（常见写法）

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

ImageKit URL 的“真正威力”

ImageKit 支持 URL 参数即处理：

https://ik.imagekit.io/xxx/avatar.png?tr=w-300,h-300,fo-auto

- 不重新上传
- 不重新存储
- 通过改变的URL里的参数实现即时裁剪 / 压缩 

👉 对性能和存储成本极其友好

常见坑（很重要）

❌ 1. 忘了装 python-dotenv
如果你用 .env，通常要：

```bash
uv add python-dotenv
```

否则环境变量可能读不到。

❌ 2. 把 private key 写进 Git
一定要：

.env

❌ 3. 直接把文件传给 ImageKit 而不校验
生产环境至少要：

- 校验文件类型
- 校验大小
- 防止任意文件上传

imagekitio vs 其他方案（快速对比）

| 方案 | 适合场景 |
| --- | --- |
| imagekitio | 图片为主、前端展示多、CDN 优先 |
| S3 + CloudFront | 通用存储、偏后端 |
| Cloudinary | 类似 ImageKit，价格偏高 |
| 本地存储 | ❌ 不适合生产 |

一句话总结

> uv add imagekitio
> = 给 FastAPI 项目加上“专业级图片上传 + CDN + 实时处理”的能力

## 3) uvicorn[standard]

一句话结论

```bash
uv add uvicorn[standard]
```

👉 给 FastAPI 项目安装“完整版”的 uvicorn 服务器（uvicorn + 官方推荐的一整套增强组件）

拆开看这条命令

1️⃣ uv add

- 往当前项目里添加依赖
- 自动更新：
  - pyproject.toml
  - uv.lock
- 安装到 uv 管理的虚拟环境

2️⃣ uvicorn

- FastAPI 最常用的 ASGI 服务器
- 负责接收请求、交给 FastAPI、返回响应
- 没有 uvicorn，FastAPI 跑不起来

3️⃣ [standard]

- Python 的可选依赖（extras）语法
- 表示安装 uvicorn + 官方推荐的一整套增强组件

uvicorn[standard] 通常包含

| 组件 | 作用 |
| --- | --- |
| uvloop | 🚀 更快的事件循环（Linux / macOS） |
| httptools | ⚡ 更快的 HTTP 解析 |
| watchfiles | 🔁 --reload 热重载 |
| python-dotenv | 🌱 支持 .env 文件 |
| websockets | 🔌 WebSocket 支持 |

和 uv add uvicorn 的区别

| 命令 | 适合谁 |
| --- | --- |
| uv add uvicorn | 最小安装（能跑但简陋） |
| uv add uvicorn[standard] | ✅ 推荐：开发 / 项目 / 部署 |

👉 99% 的 FastAPI 项目都应该用 [standard]


```bash
uv add uvicorn[standard]
```

你会得到：

- pyproject.toml 里记录的是：
  ```toml
  uvicorn = { extras = ["standard"], version = "*" }
  ```
- uv.lock 锁定精确版本
- 别人 clone 项目后：
  ```bash
  uv sync
  ```
  → 环境完全一致

新手常见误解

❌ “standard 是必须的吗？” 不是必须，但强烈推荐

❌ “standard 会不会太重？” 不会，都是 FastAPI 常用组件

❌ “生产环境要不要？” 要，通常还会加 gunicorn 或 --workers

推荐组合（记住这行）

```bash
uv add fastapi uvicorn[standard]
```

一句话记忆法

uvicorn[standard] = “能跑 + 跑得快 + 少踩坑”

## 4) aiosqlite

一句话结论

```bash
uv add aiosqlite
```

👉 给 uv 项目添加“异步 SQLite 数据库支持”

aiosqlite 是什么？

aiosqlite = SQLite 的异步封装库

- SQLite：轻量级、文件型数据库
- aiosqlite：用 async/await 包一层 SQLite

👉 适合：学习 / 作业 / 原型 / 小项目 / FastAPI

为什么 FastAPI 要用 aiosqlite，而不是 sqlite3？

sqlite3 是同步的，会阻塞事件循环；
aiosqlite 解决的正是这一点。

uv add aiosqlite 背后发生了什么？

- 1️⃣ 安装到项目虚拟环境

- 2️⃣ 写入 pyproject.toml

- 3️⃣ 锁定到 uv.lock

- 4️⃣ uv sync 可复现


FastAPI + aiosqlite 的最小示例

1️⃣ 初始化数据库

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

2️⃣ 路由中使用

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

常见的“标准封装方式”（推荐）

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

aiosqlite 的优点 & 局限

✅ 优点

- 零配置
- 一个文件就是数据库
- 适合学习 / 小项目 / 单机

⚠️ 局限（很重要）

- 并发写能力弱
- 不适合高并发生产
- 不支持复杂用户权限

👉 以后会升级到：

- PostgreSQL + asyncpg
- MySQL + aiomysql

新手常见坑

❌ 1. 用 sqlite3 + async def（这是假异步）

❌ 2. 忘了 commit（写操作一定要 await db.commit()）

❌ 3. 多请求同时写（SQLite 写锁容易冲突）

一句话总结

> uv add aiosqlite
> = 让 FastAPI 用“正确的异步方式”访问 SQLite

# 五、uv 常用指令

| 分类 | 常用指令 | 作用说明 |
| --- | --- | --- |
| 安装 | brew install uv | 在 macOS 上安装 uv（推荐方式） |
| 版本 | uv --version | 查看 uv 版本 |
| 初始化 | uv init | 初始化项目（生成 pyproject.toml） |
| Python | uv python list | 查看可用 / 已安装的 Python 版本 |
| Python | uv python install 3.12 | 下载并安装指定 Python 版本 |
| Python | uv python pin 3.12 | 固定项目使用的 Python 版本 |
| 依赖 | uv add fastapi | 添加依赖（等价于 pip install） |
| 依赖 | uv add uvicorn sqlalchemy | 一次添加多个依赖 |
| 依赖 | uv remove sqlalchemy | 移除依赖 |
| 依赖 | uv pip list | 查看当前环境已安装的包 |
| 锁定 | uv lock | 重新生成 uv.lock |
| 运行 | uv run python | 在项目虚拟环境中启动 Python |
| 运行 | uv run uvicorn main:app --reload | 启动 FastAPI 开发服务器 |
| 运行 | uv run pytest | 运行测试 |
| 运行 | uv run <cmd> | 在 uv 管理的环境中运行任意命令 |
| 同步 | uv sync | 按 pyproject.toml + uv.lock 安装依赖 |
| 清理 | uv cache clean | 清理 uv 缓存 |
| 帮助 | uv help | 查看 uv 帮助信息 |
