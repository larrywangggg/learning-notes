# Gopher 协议

## 是什么

Gopher 是 1991 年由明尼苏达大学 Mark McCahill 团队发明的互联网信息检索协议（RFC 1436），比 HTTP/HTML 早成熟，一度是"互联网图书馆"的实际标准。

---

## 核心机制

Gopher 是应用层协议，运行在 TCP 之上（端口 70），就像 HTTP 跑在 80 一样。

```
应用层  →  Gopher（定义 selector 格式、菜单格式）
传输层  →  TCP（可靠传输、分包、重组）
网络层  →  IP
```

交互流程极简：

```
客户端  →  TCP 连接端口 70
        →  发送 selector（一行文本，可为空，回车换行结尾）
服务端  →  返回文本块，末尾以单独一行 "." 结束
        →  关闭连接
```

没有 header，没有状态码，没有 cookie。

**具体例子**：访问一个 Gopher 服务器根菜单

```
# 客户端发送（空 selector，表示请求根目录）
\r\n

# 服务端返回（菜单格式：类型 + 显示名 + selector + 主机 + 端口）
1University of Minnesota    /                gopher.tc.umn.edu  70
1Computer Science Dept      /cs              gopher.tc.umn.edu  70
0README                     /README.txt      gopher.tc.umn.edu  70
.
```

行首字符是类型码：`1` = 目录，`0` = 文本文件，`7` = 搜索，`9` = 二进制文件。

---

## 心智模型：文件系统 vs 超文本

| | Gopher | HTTP/HTML |
|---|---|---|
| 信息结构 | 严格树状菜单，像文件系统 | 任意超链接图 |
| 链接位置 | 链接存在菜单文件里，与内容分离 | 链接嵌入文档内 |
| 内容类型 | 纯文本、文件、搜索 | 任意（图片、脚本、多媒体…） |
| 导航方式 | 逐级选菜单项 | 随意跳转 |
| 协议复杂度 | 极低（selector + 文本块） | 高（方法、header、状态码…） |

**关键洞察**：Gopher 的层级由服务器定义，用户只能在服务器规定的树里走。HTML 把链接权交给了内容创作者，Gopher 没有。

---

## 为什么消亡

1. **1993 年 2 月**：明尼苏达大学宣布对 Gopher 服务器收费
2. **1993 年 4 月**：CERN 将 WWW（HTTP + HTML）放入公共领域，免费
3. 商业化叫停 Gopher 扩张，开发者涌向 Web

> 端口号方面：Gopher 用 70，HTTP 用 80。70 < 80 正好对应 Gopher 比 HTTP 更早的历史事实，方便记忆。

---

## 今天的意义

**Gopherspace 仍然存活**：有小众爱好者社群维护 Gopher 服务器，可用 Lagrange、Kristall 等客户端访问。

**安全研究 — SSRF 利用**：`gopher://` URL scheme 在服务端请求伪造（SSRF）攻击中仍被利用。因为 Gopher 可以构造任意 TCP 字节流，攻击者能借此绕过 HTTP 限制，直接向内网服务发送原始请求。

```
# 攻击者构造的恶意 URL，让服务器去请求内网 Redis
gopher://127.0.0.1:6379/_%2A1%0D%0A%248%0D%0Aflushall%0D%0A
# 解码后实际发送给 Redis 的内容：
# *1\r\n$8\r\nflushall\r\n
```

**协议设计教材**：它是"极简协议"的典型范例，与 HTTP 的对比常出现在网络课程里。

---

## Sources

- https://datatracker.ietf.org/doc/html/rfc1436
- https://en.wikipedia.org/wiki/Gopher_(protocol)
- https://boston.conman.org/2019/01/12.2
- https://www.ils.unc.edu/callee/gopherpaper.htm
- https://dev.to/dotcomboom/the-gopher-protocol-in-brief-1d88
