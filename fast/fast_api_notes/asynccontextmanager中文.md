# FastAPI asynccontextmanager 与 lifespan 整理版

这份笔记整理 app.py 中的 import 与 `@asynccontextmanager` + `lifespan` 的用法，核心是理解 FastAPI 的启动/关闭生命周期。

## 1. import 区的作用
- `from app.images import imagekit`  
  复用在 `images.py` 中初始化好的 ImageKit 客户端（配置一次，全局复用）。

- `UploadFileRequestOptions`  
  ImageKit SDK 的上传参数对象，用来设置重命名、标签、目录等。

- `shutil`  
  常用 `shutil.copyfileobj(src, dst)`，把上传的文件流写入临时文件。

- `os`  
  路径与文件删除，如 `os.path.exists(path)`、`os.unlink(path)`。

- `uuid`  
  `uuid.uuid4()` 生成全局唯一 ID，用于主键或临时文件名。

- `tempfile`  
  `tempfile.NamedTemporaryFile(...)` 安全创建临时文件，避免冲突且跨平台。

## 2. lifespan 的基本写法
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
```

## 3. lifespan 是什么
`lifespan` 是 FastAPI 的启动/关闭钩子：  
- `yield` 之前：启动阶段（startup）  
- `yield` 之后：关闭阶段（shutdown）  

等价于旧写法：
```python
@app.on_event("startup")
async def startup():
    ...

@app.on_event("shutdown")
async def shutdown():
    ...
```

## 4. yield 在这里的含义
`lifespan` 是一个 **异步上下文管理器**。执行顺序：
```
启动 -> 运行初始化代码 -> yield -> 正式服务请求 -> 退出时执行收尾
```
所以 `yield` 等价于：“初始化完成，可以开始接请求了”。

如果需要清理资源，可以把逻辑写在 `yield` 之后：
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    await close_resources()
```

## 5. asynccontextmanager 的作用与用法
`@asynccontextmanager` 把一个 `async def` + `yield` 变成“可被 `async with` 使用”的上下文管理器。
它的核心作用是：**把“资源的获取/释放”包装成一个清晰的生命周期**。

### 5.1 最小示例
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_resource():
    resource = await open_resource()
    try:
        yield resource
    finally:
        await close_resource(resource)

async with get_resource() as r:
    ...
```
上面的结构等价于：
```
进入 async with -> 执行 yield 之前 -> yield 之后继续 -> finally 关闭
```

### 5.2 与 async with 的关系
`async with` 负责调用“进入/退出”逻辑：  
- 进入时执行 `yield` 之前的代码  
- 退出时执行 `yield` 之后的代码  

因此你可以在 `yield` 前做初始化，在 `yield` 后做清理，形成稳定的资源生命周期。

### 5.3 与 FastAPI lifespan 的关系
FastAPI 需要一个“启动/关闭”钩子，`@asynccontextmanager` 正好提供这种结构：
- 启动阶段：创建数据库连接、初始化缓存、准备外部服务  
- 运行阶段：处理所有请求  
- 关闭阶段：释放连接、清理资源  

这比旧的 `@app.on_event("startup")` / `@app.on_event("shutdown")` 更集中、更清晰。

## 5. 为什么建表放在这里
`create_db_and_tables()` 适合放在生命周期中，因为它必须：
- 只执行一次
- 发生在任何请求之前
- 支持 async 数据库操作

放在路由里会导致重复建表、并发风险和性能问题。

## 6. 挂到 FastAPI 应用上
```python
app = FastAPI(lifespan=lifespan)
```
这行代码把你定义的生命周期逻辑接到应用上。

## 7. 记住这三点就够了
1. `lifespan` = FastAPI 的启动/关闭钩子  
2. `yield` = 初始化完成，进入服务阶段  
3. `imagekit` 是一次性配置好的外部服务客户端  
