
# Linux Basic Commands Cheat Sheet

## 1. Help Manual（命令帮助）

- 查看简要帮助：
  ```bash
  <command> --help
  ```

- 查看完整手册（manual）：
  ```bash
  man <command>
  ```

- 示例：
  ```bash
  ls --help
  man ls
  ```

---

## 2. Useful Commands for Navigation（目录导航）

| Command    | Description    |
| ---------- | -------------- |
| `pwd`      | 显示当前工作目录（绝对路径） |
| `cd <dir>` | 切换到指定目录        |
| `cd ~`     | 切换到用户主目录       |
| `cd .`     | 当前目录（不发生变化）    |
| `cd ..`    | 切换到父目录         |
| `cd -`     | 返回上一个目录        |

---

## 3. Listing Files（查看文件）

| Command     | Description          |
| ----------- | -------------------- |
| `ls`        | 列出当前目录内容             |
| `ls <dir>`  | 列出指定目录内容             |
| `ls -l`     | 详细列表（权限、大小、时间等）      |
| `ls -a`     | 显示所有文件（包括隐藏文件）       |
| `ls path/*` | 通配符匹配文件（如 `labs/l*`） |

> 隐藏文件：文件名以 `.` 开头（如 `.git`、`.bash_history`）

---

## 4. Useful Commands for Files and Directories（文件与目录）

### 文件查看

| Command              | Description |
| -------------------- | ----------- |
| `touch file.txt`     | 创建新文件       |
| `cat file.txt`       | 显示文件全部内容    |
| `head file.txt`      | 显示前 10 行    |
| `head -n 3 file.txt` | 显示前 3 行     |
| `tail file.txt`      | 显示后 10 行    |
| `tail -n 3 file.txt` | 显示后 3 行     |
| `file <path>`        | 判断文件类型      |

---

### 文件操作

| Command       | Description |
| ------------- | ----------- |
| `cp src dest` | 复制文件        |
| `mv src dest` | 移动或重命名文件    |
| `rm file.txt` | 删除文件 ⚠️     |
| `mkdir dir`   | 创建目录        |
| `rmdir dir`   | 删除空目录 ⚠️    |

> ⚠️ `rm` 和 `rmdir` **不可恢复，删除前务必确认**

---

### 压缩与打包

| Command                   | Description             |
| ------------------------- | ----------------------- |
| `tar -cvf file.tar *.txt` | 将所有 `.txt` 文件打包为 tar 文件 |

---

## 5. Useful Command Line Shortcuts（命令行快捷键）

| Shortcut            | Description |
| ------------------- | ----------- |
| `Tab`               | 自动补全命令或文件名  |
| `Ctrl + C`          | 中断当前命令      |
| `Ctrl + R`          | 搜索历史命令      |
| `↑ / ↓`             | 浏览历史命令      |
| `Ctrl + A` / `Home` | 光标移到行首      |
| `Ctrl + E` / `End`  | 光标移到行尾      |
| `Ctrl + K`          | 删除光标后内容     |
| `Ctrl + U`          | 清空整行        |
| `Ctrl + L`          | 清空终端窗口      |
| `Shift + PgUp`      | 向上滚屏        |
| `Shift + PgDn`      | 向下滚屏        |

