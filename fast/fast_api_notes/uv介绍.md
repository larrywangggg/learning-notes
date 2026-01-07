# 什么是uv
一句话先给结论
    • pip：传统、稳定、人人都会用的 Python 包安装器
    • uv：新一代、超快的 Python 包 + 虚拟环境 + 依赖管理工具（pip 的现代替代者）

pip 是什么？
pip = Python 的包管理器
它只做一件事：
    把第三方库装进当前 Python 环境
常见用法
pip install fastapi
pip install requests
pip freeze > requirements.txt
pip install -r requirements.txt
pip 的优点
    • 官方、默认自带
    • 生态成熟，教程多
    • 所有 Python 项目都支持
pip 的局限（你迟早会遇到）
    • ❌ 不管 Python 版本
    • ❌ 不创建虚拟环境
    • ❌ 依赖解析慢
    • ❌ requirements.txt 容易“漂”
👉 所以真实项目里通常要 pip + venv + 其他工具 搭配使用

uv 是什么？
uv = Rust 写的下一代 Python 工具链  package manager
它把你平时要用的这些东西👇
    • pip
    • venv
    • pip-tools / poetry 的一部分能力
👉 全部合并成一个工具


uv 能干什么？
    • 📦 安装包（替代 pip）
    • 🐍 自动选择 / 下载 Python 版本
    • 🧪 创建并管理虚拟环境
    • 🔒 锁定依赖（可复现）
    • ⚡ 速度极快（比 pip 快很多）
常见用法
uv init
uv add fastapi
uv add uvicorn
uv run uvicorn main:app --reload
你会看到：
    • pyproject.toml
    • uv.lock
👉 这就是现代 Python 项目的标准形态

pip vs uv 对比（重点）
维度	     pip	          uv
安装速度	  慢	           ⚡ 非常快
虚拟环境	  不管	           自动
Python版本	 不管	          自动
依赖锁定	  手动	           内置
新项目体验	  一堆步骤	        一条龙
适合谁	     初学	          项目/FastAPI/团队

为什么现在很多人推荐 uv？
因为以前你要这样👇
python -m venv .venv
source .venv/bin/activate
pip install fastapi
pip freeze > requirements.txt
现在用 uv 👇
uv init
uv add fastapi
更少坑、更少命令、更不容易搞乱环境

在你的场景里怎么选？
✅ 推荐你现在这样用
    • 学习概念 / 看教程
👉 看得懂 pip install xxx 就行
    • 自己建 FastAPI 项目 / 作业 / GitHub repo
👉 直接用 uv
一个现实建议
    会 pip 是基础，用 uv 是进阶
就像：
    • 会 javac 是基础
    • 用 Gradle / Maven 是工程能力

一个超短总结（可以记住）
    • pip：装包的“螺丝刀”
uv：装包 + 环境 + 版本 + 锁定的“工具箱”


# 怎么安装uv
一、uv 怎么安装（macOS / Homebrew 场景）
✅ 最推荐方式（不碰你现有 Python）
brew install uv
👉 这是最安全、最稳妥的方式
    • 不依赖你当前 Python 是不是 Homebrew
    • 不污染系统 Python
    • 安装完就是一个独立的 uv 可执行文件
验证
uv --version
which uv
正常应看到类似：
/usr/local/bin/uv
uv 0.x.x

⚠️ 不推荐但可行的方式（用 pip 装）
pip install uv
❌ 问题在于：
    • pip 是装到 某个 Python 环境里的
    • 你以后切 Python 版本，uv 可能“消失”
    • 新手最容易在这里卡住
👉 结论：你是 macOS + 学 FastAPI，用 brew

uv 安装后你需要理解的 3 件事（非常重要）
1️⃣ uv ≠ pip
    • uv 是 外部工具
    • 不属于任何 Python 解释器
2️⃣ uv 会自己管理 Python
你可以：
uv python list
uv python install 3.12
👉 不再纠结：
    • python 是 brew 的？
    • 是系统的？
    • 是 conda 的？
3️⃣ uv 会自动创建 .venv
你不需要：
python -m venv .venv
source .venv/bin/activate
uv 全包了。

二、用 uv 创建 FastAPI 项目（标准流程）
1️⃣ 创建项目
mkdir fastapi-demo
cd fastapi-demo
uv init
你会看到：
pyproject.toml
uv.lock

2️⃣ 指定 Python 版本（推荐）
uv python install 3.12
uv python pin 3.12
👉 项目里会锁死 Python 版本
👉 以后 clone 到别的机器也一致

3️⃣ 安装 FastAPI 相关依赖
uv add fastapi
uv add uvicorn
这一步等价于：
pip install fastapi uvicorn
但：
    • 更快
    • 自动进虚拟环境
    • 自动写配置

4️⃣ 写一个最小 FastAPI 示例
main.py
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def hello():
    return {"message": "Hello FastAPI"}

三、FastAPI 在 uv 下的常用指令（重点）
🔥 启动开发服务器（最常用）
uv run uvicorn main:app --reload
解释一下：
    • uv run：在 项目虚拟环境里运行命令
    • uvicorn main:app：启动 FastAPI
    • --reload：代码改了自动重启（开发用）
访问：
http://127.0.0.1:8000

📘 自动 API 文档（FastAPI 自带）
    • Swagger UI
👉 http://127.0.0.1:8000/docs
    • ReDoc
👉 http://127.0.0.1:8000/redoc
（这个是 FastAPI 的杀手级特性）

➕ 添加新依赖
uv add sqlalchemy
uv add pydantic-settings
👉 自动：
    • 更新 pyproject.toml
    • 更新 uv.lock

➖ 删除依赖
uv remove sqlalchemy

📦 查看依赖
uv pip list
（uv 内部兼容 pip 命令）

🧪 运行测试（以后一定会用）
uv run pytest

🐍 进入项目 Python REPL
uv run python
👉 这是正确的方式
❌ 不要直接敲 python

四、uv add 常见依赖示例（保留关键内容）
先记住一句：uv add = 把依赖加进项目 + 自动更新配置 + 锁版本 + 可复现

## 1) python-dotenv
一句话结论
uv add python-dotenv
👉 把 python-dotenv 加进当前 uv 项目的依赖
等价于：
pip install python-dotenv
但 uv 会多做很多事。

python-dotenv 是什么？
python-dotenv = 让 Python 自动读取 .env 文件里的环境变量
典型 .env 文件长这样：
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=super-secret
DEBUG=true
有了 python-dotenv，你就可以在代码里这样用：
import os
os.getenv("DATABASE_URL")
👉 而不用把密码、密钥写死在代码里

为什么 FastAPI 项目几乎一定会用到它？
FastAPI 项目通常需要：
	• 数据库地址
	• JWT / Session Secret
	• 第三方 API Key
	• Debug / Prod 环境区分
这些都应该：
	• ❌ 不写进代码
	• ❌ 不提交到 Git
	• ✅ 放在 .env

在 FastAPI 里怎么用 python-dotenv？
1️⃣ 创建 .env
APP_NAME=FastAPI Demo
DEBUG=true
2️⃣ 在项目启动时加载
from dotenv import load_dotenv
load_dotenv()
通常放在：
	• main.py
	• 或 app/core/config.py
3️⃣ 读取变量
import os
app_name = os.getenv("APP_NAME")
debug = os.getenv("DEBUG") == "true"

FastAPI 更“正统”的用法（你以后会学到）
FastAPI 官方推荐搭配 Pydantic Settings：
uv add pydantic-settings python-dotenv
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_name: str
    debug: bool = False
class Config:
        env_file = ".env"
settings = Settings()
👉 这是生产级写法

新手最常见误解（帮你避坑）
❌ 误解 1：uv 自带 dotenv？
不带，必须显式 uv add python-dotenv
❌ 误解 2：.env 会自动生效？
不会，必须：
	• 用 load_dotenv()
	• 或用 Pydantic Settings
❌ 误解 3：.env 可以提交到 Git？
不可以，记得加到 .gitignore

用一句话把整个链路串起来
	uv add python-dotenv
	= 把“环境变量支持”作为项目的正式依赖加进 FastAPI 项目

## 2) imagekitio
一句话结论
uv add imagekitio
👉 把 imagekitio（ImageKit 官方 Python SDK）加入你当前 uv 项目的依赖
等价于旧写法：
pip install imagekitio
但 uv 会自动写配置 + 锁版本 + 管环境。

imagekitio 是什么？
imagekitio = ImageKit 的 Python SDK
ImageKit 是一个 图片 / 视频 CDN + 实时处理平台，常用于：
	• 📸 图片上传
	• 🧠 自动压缩、裁剪、格式转换
	• 🌍 全球 CDN 加速
	• 🔐 安全私有存储
👉 在 Web / FastAPI 项目中，非常常见

你在 FastAPI 里通常用 ImageKit 干什么？
典型场景：
	• 用户头像上传
	• 商品图片
	• 内容管理系统（CMS）
	• Notta / SaaS 产品里的媒体资源（你这个背景很熟）

imagekitio 在 FastAPI 中的“标准用法”
1️⃣ 配置环境变量（强烈推荐）
.env
IMAGEKIT_PUBLIC_KEY=xxx
IMAGEKIT_PRIVATE_KEY=yyy
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_id
👉 不要写死在代码里

2️⃣ 初始化 ImageKit 客户端
from imagekitio import ImageKit
import os
imagekit = ImageKit(
    public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
    url_endpoint=os.getenv("IMAGEKIT_URL_ENDPOINT"),
)

3️⃣ 上传图片（最常用）
result = imagekit.upload_file(
    file=open("avatar.png", "rb"),
    file_name="avatar.png",
)
print(result["url"])
👉 返回的是 已经走 CDN + 可变换的 URL

4️⃣ 在 FastAPI API 里用（常见写法）
from fastapi import FastAPI, UploadFile, File
app = FastAPI()
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    result = imagekit.upload_file(
        file=file.file,
        file_name=file.filename,
    )
    return {"url": result["url"]}

ImageKit URL 的“真正威力”（你以后一定会用）
ImageKit 支持 URL 参数即处理：
https://ik.imagekit.io/xxx/avatar.png?tr=w-300,h-300,fo-auto
	• 不重新上传
	• 不重新存储
	• 即时裁剪 / 压缩
👉 对性能和存储成本极其友好

常见坑（很重要）
❌ 1. 忘了装 python-dotenv
如果你用 .env，通常要：
uv add python-dotenv
否则环境变量可能读不到。

❌ 2. 把 private key 写进 Git
一定要：
.env

❌ 3. 直接把文件传给 ImageKit 而不校验
生产环境至少要：
	• 校验文件类型
	• 校验大小
	• 防止任意文件上传

imagekitio vs 其他方案（快速对比）
方案	适合场景
imagekitio	图片为主、前端展示多、CDN 优先
S3 + CloudFront	通用存储、偏后端
Cloudinary	类似 ImageKit，价格偏高
本地存储	❌ 不适合生产

一句话总结
	uv add imagekitio
	= 给 FastAPI 项目加上“专业级图片上传 + CDN + 实时处理”的能力
