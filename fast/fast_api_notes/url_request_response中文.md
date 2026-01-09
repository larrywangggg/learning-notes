# URL 结构 & Request/Response

先理解 URL/Endpoint，再理解 Request/Response。因为“请求路径 + 参数”就是 Request 的核心输入，所以放同一篇更连贯。

![URL 结构示意图](images/urlexample.png)

## 一、URL 的三大组成部分

以这个为例：

```
https://training.devlaunch.us/tim?video=123
```

### 1️⃣ Domain（域名）

```
https://training.devlaunch.us
```

- 作用：告诉浏览器 / 客户端，去找哪一台服务器
- 类似：一栋楼的地址
- 后端角度：由 DNS + 服务器处理，和 FastAPI / 后端代码本身关系不大

### 2️⃣ Path / Endpoint（路径 / 接口）

```
/tim
```

- 这是后端最关心的部分
- 在 FastAPI 里通常对应一个函数，比如：

```python
@app.get("/tim")
def get_tim():
    ...
```

👉 所以：Q

- Endpoint ≈ Path
- Path 决定「你访问的是哪个功能」

### 3️⃣ Query Parameters（查询参数）

```
?video=123
```

- video 是参数名
- 123 是参数值
- 用来给同一个 endpoint 传不同条件 / 数据

FastAPI 里会写成：

```python
@app.get("/tim")
def get_tim(video: int):
    return {"video": video}
```

## 二、第二个例子（多个参数）

```
https://techwithtim.net/courses/python?utm_source=youtube&page=2
```

拆开来看：

- Domain
  - https://techwithtim.net
- Path / Endpoint
  - /courses/python
- Query Parameters
  - utm_source=youtube
  - page=2

👉 多个参数用 `&` 分隔
👉 参数顺序通常不重要

## 三、一个非常关键的理解

❌ 错误理解

- endpoint = 整个 URL

✅ 正确理解

- Endpoint = Path
- Query parameters 是给 endpoint 的输入

也就是说：

```
/tim?video=123
/tim?video=456
```

👉 是同一个 endpoint
👉 只是参数不同

## 四、放到 FastAPI / API 学习里怎么用？

你之后会经常看到这种设计：

```
GET /users
GET /users?id=5
GET /users?page=2
GET /users/5
```

它们的区别就在于：

- Path：功能入口
- Query params：筛选、分页、搜索条件

---

![Request/Response 示意图](images/requestresponse.png)

## 五、整张图一句话总结

用户 → 前端（Client）→ 发 Request → 后端（API）→ 回 Response → 前端 → 用户

这是 HTTP Request / Response 的完整生命周期。

## 六、左边：Request（请求）是什么？

前端（浏览器 / App / 前端代码）发给后端的东西。

图里列了 Request Components：

### 1️⃣ Type / Method（请求方法）

常见的：

- GET：获取数据
- POST：创建数据
- PUT / PATCH：更新数据
- DELETE：删除数据

👉 告诉后端：我要干什么

### 2️⃣ Path（路径 / Endpoint）

例如：

```
/users
/users/123
/posts?page=2
```

👉 告诉后端：我要操作哪个资源 / 哪个功能

### 3️⃣ Body（请求体）

- 不是所有请求都有
- 常见于 POST / PUT / PATCH

例如（JSON）：

```json
{
  "username": "eden",
  "password": "123456"
}
```

👉 用来传大量或结构化数据

### 4️⃣ Headers（请求头）

一些“元信息”，比如：

- Content-Type: application/json
- Authorization: Bearer xxx
- Accept: application/json

👉 用来说明：

- 数据格式
- 身份认证
- 客户端信息

## 七、右边：Response（响应）是什么？

后端处理完请求后，回给前端的结果。

### 1️⃣ Status Code（状态码）

非常重要，前端第一眼看的东西：

- 200 OK：成功
- 201 Created：创建成功
- 400 Bad Request：参数有问题
- 401 Unauthorized：没登录 / token 不对
- 404 Not Found：路径或资源不存在
- 500 Internal Server Error：后端炸了 💥

👉 前端经常根据 status code 决定 UI 行为

### 2️⃣ Body（响应体）

后端真正返回的数据：

```json
{
  "id": 1,
  "name": "Eden"
}
```

或者：

```json
{
  "error": "User not found"
}
```

### 3️⃣ Headers（响应头）

例如：

- Content-Type: application/json
- Set-Cookie
- Cache-Control

👉 告诉前端：怎么处理这份数据

## 八、图中最重要的箭头（理解前后端边界）

🔁 Request Sent（请求发出）

Frontend → Backend

- 前端只能发 request
- 前端不能直接访问数据库

🔁 Response Received（响应返回）

Backend → Frontend

- 后端只能回 response
- 后端不能控制页面长什么样

👉 这是前后端解耦的核心

## 九、把这张图翻译成 FastAPI + 前端代码

前端（比如 JS）

```javascript
fetch("/users/1")
  .then(res => res.json())
  .then(data => console.log(data))
```

后端（FastAPI）

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": "Eden"}
```

---

![Request/Response 示例图](images/Untitled picture.png)

## 十、一个非常容易混的点

❌ 前端 = 页面

❌ 后端 = 数据库

正确是：

| 角色 | 职责 |
| --- | --- |
| User | 点击、输入 |
| Frontend / Client | 发请求、渲染页面 |
| Backend / API | 处理逻辑、校验、访问数据库 |
| Database | 存数据 |
