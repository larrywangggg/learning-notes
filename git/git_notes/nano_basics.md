# 1. Eight Common Real-World Cases Where You Must Use nano

## 1. Edit environment variables / shell configs (beginners and pros)

### Scenarios

- Installed Java / Node / Python
- Need to add PATH, aliases, environment variables
- **No GUI in server / Linux / WSL / Docker**

### Typical files

```bash
nano ~/.bashrc
nano ~/.zshrc
```

### What you would edit

```bash
export JAVA_HOME=/usr/lib/jvm/java-17
export PATH=$JAVA_HOME/bin:$PATH

alias ll='ls -alh'
```

Note: This is nano's number one use case.

---

## 2. Edit `.env` (backend / Docker / project config)

### Scenarios

- FastAPI / Django / Node projects
- Docker Compose
- Database passwords, ports, keys

### Command

```bash
nano .env
```

### Example content

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=admin
DB_PASSWORD=secret
```

Note: `.env` files are plain text, and nano is a perfect fit.

---

## 3. Edit config files on servers (the most common case)

### Scenarios

- SSH into a server
- Remote VPS / cloud server
- No VS Code available

### Common files

```bash
nano /etc/nginx/nginx.conf
nano /etc/ssh/sshd_config
nano /etc/hosts
```

### Example: change the port

```text
Port 2222
```

Note: In this situation, 99% of people use nano or vim.

---

## 4. Quickly edit a YAML / JSON / txt file

### Scenarios

- CI config
- docker-compose
- One-off changes

```bash
nano docker-compose.yml
```

```yaml
services:
  web:
    ports:
      - "8000:8000"
```

Note: Not worth opening an IDE, nano is fastest.

---

## 5. Edit crontab (scheduled tasks)

### Scenarios

- Scheduled scripts
- Scheduled backups

```bash
crontab -e
```

Note: Many systems open nano by default.

```cron
0 2 * * * /home/user/backup.sh
```

---

## 6. Write / edit scripts (small scale)

### Scenarios

- Bash scripts
- Small automation tools

```bash
nano deploy.sh
```

```bash
#!/bin/bash
echo "Deploying..."
docker compose up -d
```

Note: For scripts under 50 lines, nano feels great.

---

## 7. Edit SSH config

```bash
nano ~/.ssh/config
```

```text
Host github
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
```

Note: This is a classic nano use case.

---

## 8. Exams / lab machines / school servers

### Scenarios

- School Linux lab environment
- Restricted permissions
- Terminal only

Note: nano is the only safe choice.

---

# 2. Why these cases do not use VS Code / IDE

| Reason              | Explanation              |
| ------------------- | ------------------------ |
| No GUI              | Server / SSH             |
| Files are too small | Not worth opening an IDE |
| Restricted access   | sudo + nano              |
| Quick edits         | Done in 30 seconds       |
| Exams               | Easy to mess up in vim   |

---

# 3. How to think about nano

> **nano is a temporary text editing tool in the Linux terminal. It is not for coding, but for editing configs.**

# 4. How to use nano

## Common nano shortcuts cheat sheet

### 1. File operations (most important)

| Action                 | Shortcut    | Description                     |
| ---------------------- | ----------- | ------------------------------- |
| Save file (Write Out)  | `Ctrl + O`  | Write content to file           |
| Confirm filename       | `Enter`     | Confirm on save                 |
| Exit nano              | `Ctrl + X`  | Prompts if not saved            |
| Read file              | `Ctrl + R`  | Insert another file into buffer |

---

### 2. Editing

| Action                 | Shortcut   | Description                     |
| ---------------------- | ---------- | ------------------------------- |
| Cut current line       | `Ctrl + K` | Delete and store in cut buffer  |
| Paste                  | `Ctrl + U` | Paste cut/copied content        |
| Set selection start    | `Ctrl + 6` | Start selecting text            |
| Copy selection         | `Alt + 6`  | Copy (no delete)                |
| Delete to end of file  | `Alt + T`  | Delete from cursor to EOF       |

---

### 3. Undo / Redo

| Action | Shortcut  | Description |
| ------ | --------- | ----------- |
| Undo   | `Alt + U` | Undo        |
| Redo   | `Alt + E` | Redo        |

---

### 4. Search and replace

| Action           | Shortcut             | Description                         |
| ---------------- | -------------------- | ----------------------------------- |
| Search           | `Ctrl + W`           | Find text                           |
| Find next        | `Ctrl + W` then `Enter` | Jump to the next match            |
| Replace          | `Ctrl + \`           | Find and replace                    |
| Case sensitive   | `Alt + C`            | Enable case sensitivity in search   |

---

### 5. Cursor and navigation

| Action            | Shortcut  | Description                 |
| ----------------- | --------- | --------------------------- |
| Show line/column  | `Ctrl + C` | Display current line/column |
| Go to line        | `Ctrl + _` | Go to line                  |
| Start of file     | `Alt + \` | Move to the first line      |
| End of file       | `Alt + /` | Move to the last line       |

---

### 6. Help and other

| Action        | Shortcut  | Description               |
| ------------- | --------- | ------------------------- |
| Open help       | `Ctrl + G` | View all shortcuts        |
| Execute command | `Ctrl + T` | Run external command      |
| Justify text    | `Ctrl + J` | Justify (rarely used)     |

---

### 7. Terminal related (not nano itself)

| Action             | Shortcut            | Description     |
| ------------------ | ------------------- | --------------- |
| Paste from system  | `Ctrl + Shift + V`  | Terminal paste  |

# 5. Most common commands

- `Ctrl + O` Save
- `Ctrl + X` Exit
- `Ctrl + W` Search
- `Ctrl + K` Cut line
- `Ctrl + U` Paste
- `Ctrl + G` Help

Notes:

- In `nano`, `^` means `Ctrl`
- In `nano`, `M-` means `Alt`
- On Mac, `Alt` = `Option`
