# 一、最常见的 8 个「必须用 nano」的真实例子

## 1. 改环境变量 / shell 配置（新手 & 老手都会用）

### 场景

- 装了 Java / Node / Python
- 想加 PATH、alias、环境变量
- **服务器 / Linux / WSL / Docker 里没有 GUI**

### 典型文件

```bash
nano ~/.bashrc
nano ~/.zshrc
```

### 你会改什么

```bash
export JAVA_HOME=/usr/lib/jvm/java-17
export PATH=$JAVA_HOME/bin:$PATH

alias ll='ls -alh'
```

👉 **这是 nano 的“第一使用场景”**

---

## 2. 编辑 `.env`（后端 / Docker / 项目配置）

### 场景

- FastAPI / Django / Node 项目
- Docker Compose
- 数据库密码、端口、key

### 命令

```bash
nano .env
```

### 内容例子

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=admin
DB_PASSWORD=secret
```

👉 `.env` **100% 是纯文本**，nano 完美适配

---

## 3. 服务器上改配置文件（最典型）

### 场景

- SSH 登录服务器
- 远程 VPS / 云服务器
- 没法用 VS Code

### 常见文件

```bash
nano /etc/nginx/nginx.conf
nano /etc/ssh/sshd_config
nano /etc/hosts
```

### 举例：改端口

```text
Port 2222
```

👉 这种情况 **99% 的人用 nano 或 vim**

---

## 4. 临时改一个 YAML / JSON / txt 文件

### 场景

- CI 配置
- docker-compose
- 一次性修改

```bash
nano docker-compose.yml
```

```yaml
services:
  web:
    ports:
      - "8000:8000"
```

👉 不值得开 IDE，用 nano **最快**

---

## 5. 改 crontab（定时任务）

### 场景

- 定时跑脚本
- 定时备份

```bash
crontab -e
```

👉 很多系统默认**直接打开 nano**

```cron
0 2 * * * /home/user/backup.sh
```

---

## 6. 写 / 改脚本（小规模）

### 场景

- Bash 脚本
- 自动化小工具

```bash
nano deploy.sh
```

```bash
#!/bin/bash
echo "Deploying..."
docker compose up -d
```

👉 脚本 < 50 行，nano 非常舒服

---

## 7. 改 SSH 配置

```bash
nano ~/.ssh/config
```

```text
Host github
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
```

👉 **这是 nano 的经典用途**

---

## 8. 考试 / 实验机 / 学校服务器

### 场景

- 学校 Linux 实验环境
- 权限受限
- 只给你终端

👉 **nano = 唯一安全选择**

---

# 二、为什么这些场景「不用 VS Code / IDE」？

| 原因    | 解释          |
| ----- | ----------- |
| 没 GUI | 服务器 / SSH   |
| 文件太小  | 不值得开 IDE    |
| 权限受限  | sudo + nano |
| 临时修改  | 30 秒完成      |
| 考试    | vim 容易翻车    |

---

# 三、你可以这样理解 nano

> **nano 就是：Linux 终端里的“临时文本修改工具”，不是写代码的，是“改配置的”。**

# 四、nano 的使用方法

## Nano 常用快捷键速查表

### 一、文件操作（最重要）

| 功能 | 快捷键 | 说明 |
| --- | --- | --- |
| 保存文件（Write Out） | `Ctrl + O` | 将内容写入文件 |
| 确认文件名 | `Enter` | 保存时确认 |
| 退出 nano | `Ctrl + X` | 未保存会提示 |
| 读取文件 | `Ctrl + R` | 将其他文件插入当前文件 |

---

### 二、编辑操作

| 功能 | 快捷键 | 说明 |
| --- | --- | --- |
| 剪切当前行 | `Ctrl + K` | 删除并放入剪贴缓冲 |
| 粘贴 | `Ctrl + U` | 粘贴剪切/复制内容 |
| 设置选区起点 | `Ctrl + 6` | 开始选择文本 |
| 复制选中文本 | `Alt + 6` | 复制（不删除） |
| 删除到文件结尾 | `Alt + T` | 从光标删到 EOF |

---

### 三、撤销 / 重做

| 功能 | 快捷键 | 说明 |
| --- | --- | --- |
| 撤销 | `Alt + U` | Undo |
| 重做 | `Alt + E` | Redo |

---

### 四、搜索与替换

| 功能 | 快捷键 | 说明 |
| --- | --- | --- |
| 搜索 | `Ctrl + W` | 查找文本 |
| 查找下一个 | `Ctrl + W` → `Enter` | 跳转下一个 |
| 替换 | `Ctrl + \` | 查找并替换 |
| 区分大小写 | `Alt + C` | 搜索/替换时启用 |

---

### 五、光标与导航

| 功能 | 快捷键 | 说明 |
| --- | --- | --- |
| 跳转到行号 | `Ctrl + C` | 显示当前行列 |
| 跳转到指定行 | `Ctrl + _` | Go To Line |
| 文件开头 | `Alt + \` | 移动到第一行 |
| 文件结尾 | `Alt + /` | 移动到最后一行 |

---

### 六、帮助与其他

| 功能 | 快捷键 | 说明 |
| --- | --- | --- |
| 打开帮助 | `Ctrl + G` | 查看全部快捷键 |
| 执行命令 | `Ctrl + T` | 调用外部命令 |
| 对齐文本 | `Ctrl + J` | Justify（少用） |

---

### 七、终端相关（非 Nano 本身）

| 功能 | 快捷键 | 说明 |
| --- | --- | --- |
| 从系统粘贴 | `Ctrl + Shift + V` | 终端粘贴 |

# 五、最常用指令

- `Ctrl + O` 保存
- `Ctrl + X` 退出
- `Ctrl + W` 搜索
- `Ctrl + K` 剪切行
- `Ctrl + U` 粘贴
- `Ctrl + G` 帮助

- `nano` 里的 `^` 表示 `Ctrl`
- `nano` 里的 `M-` 表示 `Alt`
- Mac 上 `Alt` = `Option`
