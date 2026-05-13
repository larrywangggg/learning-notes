# curl 快速参考

## 一句话定义

curl 是命令行 HTTP 客户端——让你在终端直接跟服务器"说话"，不需要打开浏览器。

**心智模型：**

```
浏览器：输入 URL → 发出 HTTP 请求 → 渲染响应
curl：  输入 URL → 发出 HTTP 请求 → 原样打印到终端
```

curl 的价值在于让 HTTP 变得可见、可控——浏览器替你隐藏了所有 HTTP 细节，curl 让你直接看到并控制它们。

---

## 核心概念

| 概念 | 是什么 | 举例 |
|------|--------|------|
| URL | 资源地址 | `https://api.github.com/users/octocat` |
| HTTP 方法 | 你想做什么操作 | GET（取）、POST（发）、PUT（改）、DELETE（删） |
| Header | 请求附带的元信息 | `Content-Type: application/json` |
| Body | 请求携带的数据 | 登录时发的用户名密码 |
| 状态码 | 服务器的回应摘要 | 200（成功）、401（未授权）、404（找不到）、500（服务器报错） |

---

## 常用命令

### GET 请求

```bash
# 最简单的 GET
curl https://api.github.com/users/octocat

# 只看响应头，不要 body
curl -I https://example.com

# 详细模式，显示完整请求/响应（调试必用）
curl -v https://example.com

# 只看头，丢弃 body（-v 的安静版）
curl -v -s -o /dev/null https://api.github.com/users/octocat

# 跟随重定向（默认不跟）
curl -L https://bit.ly/xxxxx

# 格式化 JSON 输出
curl https://api.github.com/users/octocat | jq .
```

### POST / 发送数据

```bash
# 发 JSON 数据
curl -X POST https://api.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"123"}'

# 发表单数据（模拟 HTML 表单提交）
curl -X POST https://example.com/form \
  -d "name=Alice&age=25"

# 上传文件
curl -X POST https://example.com/upload \
  -F "file=@/path/to/photo.jpg"

# 上传文件并附带其他字段
curl -X POST https://example.com/upload \
  -F "file=@photo.jpg" \
  -F "title=My Photo"
```

### 认证

```bash
# Bearer Token
curl https://api.example.com/me \
  -H "Authorization: Bearer YOUR_TOKEN"

# Basic Auth（用户名:密码）
curl -u alice:password123 https://api.example.com/me

# API Key 放在 Header
curl https://api.example.com/data \
  -H "X-API-Key: YOUR_API_KEY"

# Cookie
curl -b "session=abc123" https://example.com/dashboard

# 保存 Cookie 到文件，再带着它请求
curl -c cookies.txt https://example.com/login -d "user=alice&pass=123"
curl -b cookies.txt https://example.com/dashboard
```

### 下载文件

```bash
# 下载并保存为指定文件名
curl -o filename.zip https://example.com/file.zip

# 下载并保留原始文件名（-O 大写）
curl -O https://example.com/file.tar.gz

# 断点续传（网络中断后继续下载）
curl -C - -O https://example.com/large-file.zip

# 批量下载（1 到 100）
curl -O https://example.com/img[1-100].jpg
```

### PUT / PATCH / DELETE

```bash
# PUT 更新资源
curl -X PUT https://api.example.com/users/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"name":"Bob"}'

# PATCH 部分更新
curl -X PATCH https://api.example.com/users/1 \
  -H "Content-Type: application/json" \
  -d '{"email":"new@example.com"}'

# DELETE
curl -X DELETE https://api.example.com/users/1 \
  -H "Authorization: Bearer TOKEN"
```

### 网络排查

```bash
# 查看请求各阶段耗时（DNS/TCP/TLS/TTFB）
curl -w "\nDNS:   %{time_namelookup}s\nTCP:   %{time_connect}s\nTLS:   %{time_appconnect}s\nTTFB:  %{time_starttransfer}s\nTotal: %{time_total}s\n" \
  -s -o /dev/null https://example.com

# 测试特定 IP，绕过 DNS（验证新服务器前）
curl --resolve api.example.com:443:1.2.3.4 https://api.example.com

# 检查重定向链（跳了几次、跳去哪）
curl -v -L https://short.url/xxxxx 2>&1 | grep -E "^[<>*] (HTTP|Location)"

# 指定 HTTP 版本
curl --http1.1 https://example.com
curl --http2 https://example.com

# 忽略 TLS 证书错误（只用于测试，不可用于生产）
curl -k https://self-signed.example.com
```

### Shell 脚本常用

```bash
# 只取状态码（脚本判断用）
curl -s -o /dev/null -w "%{http_code}" https://myapp.com

# 健康检查示例
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://myapp.com/health)
if [ "$STATUS" != "200" ]; then
  echo "服务异常！状态码：$STATUS"
fi

# 发 Slack Webhook 通知
curl -X POST "$SLACK_WEBHOOK" \
  -H "Content-Type: application/json" \
  -d '{"text":"部署完成"}'

# 触发 GitHub Actions 工作流
curl -X POST https://api.github.com/repos/ORG/REPO/dispatches \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"event_type":"deploy"}'
```

---

## 常用 Flag 速查

| Flag | 作用 |
|------|------|
| `-v` | verbose，显示完整请求/响应细节，调试必用 |
| `-s` | silent，不显示进度条（脚本中用） |
| `-I` | 只取响应头（HEAD 方法） |
| `-L` | 跟随 30x 重定向 |
| `-o <file>` | 输出到指定文件 |
| `-O` | 输出到文件（保留原始文件名） |
| `-C -` | 断点续传 |
| `-H "Key: Val"` | 添加请求头 |
| `-d "data"` | 请求 body（字符串） |
| `-F "field=val"` | multipart 表单数据 |
| `-X METHOD` | 指定 HTTP 方法 |
| `-u user:pass` | HTTP Basic Auth |
| `-b "k=v"` | 发送 Cookie |
| `-c <file>` | 保存 Cookie 到文件 |
| `-k` | 忽略 TLS 证书错误 |
| `-A "UA"` | 指定 User-Agent |
| `--compressed` | 接受压缩响应（gzip） |
| `-w "format"` | 自定义输出格式（含时间、状态码等变量） |
| `--resolve host:port:ip` | 绕过 DNS，指定 IP |
| `--http1.1 / --http2` | 强制指定 HTTP 版本 |
| `-x host:port` | 使用代理 |

---

## 读懂 curl -v 输出

`-v` 输出有 4 种前缀，对应 4 类信息：

| 前缀 | 含义 |
|------|------|
| `*` | curl 自身状态（DNS、TCP、TLS 过程） |
| `>` | 你发出去的请求头 |
| `<` | 服务器返回的响应头 |
| 无前缀 | 响应 body |

**阅读顺序（从下往上）：**

1. 无前缀 — body 内容对不对？
2. `<` 里的状态码 — 200 / 401 / 500？
3. `<` 里的响应头 — `content-type`、`x-ratelimit-remaining` 等
4. `>` — 只在"服务器说请求格式不对"时才需要看
5. `*` — 只在连接失败时才需要看（DNS 失败、TLS 报错等）

**一次完整 HTTPS 请求的生命周期：**

```
* DNS 解析 → IP
* TCP 连接建立（:443）
* TLS 握手（Client hello → Server hello → 证书 → Finished）
* 证书验证（subject、subjectAltName、issuer、verify ok）
* HTTP/2 流建立
> 发出请求头（方法、路径、Host、User-Agent）
> 空行（请求头结束）
< 响应状态行（HTTP/2 200）
< 响应头（content-type、cache-control、x-ratelimit-* 等）
< 空行（响应头结束）
  body 数据
* Connection left intact（连接可复用）
```

---

## 使用场景

### 1. 调试和测试 API

```bash
# 测试接口通不通
curl https://api.example.com/health

# 模拟登录
curl -X POST https://api.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"email":"a@b.com","password":"123"}'

# 带 token 调鉴权接口
curl https://api.example.com/me \
  -H "Authorization: Bearer eyJhbGci..."
```

### 2. 轻量爬虫（无 JS 渲染）

```bash
# 取网页源码
curl -s https://example.com

# 模拟浏览器 User-Agent（有些网站会拦截无 UA 的请求）
curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" https://example.com
```

### 3. 场景选型

| 场景 | 推荐工具 |
|------|---------|
| 临时测一个 API | curl，最快 |
| 需要保存/复用请求 | Postman / Insomnia |
| 脚本里调接口 | curl，几乎所有环境都有 |
| 需要 JS 渲染的页面 | Playwright / Puppeteer |
| 复杂的批量下载 | wget（支持递归）或 aria2 |
| 生产代码里的 HTTP 请求 | 各语言 HTTP 库（requests、axios 等） |

curl 最大的优势是**到处都有，不需要安装**——服务器、Docker 容器、CI 环境里几乎不用考虑依赖问题。

---

## 参考资源

- [官方教程](https://curl.se/docs/tutorial.html)
- [everything curl](https://everything.curl.dev/)（官方完整书，免费）
- [HTTP 脚本化专项](https://curl.se/docs/httpscripting.html)
- [在线练习环境](https://reqbin.com/curl)
