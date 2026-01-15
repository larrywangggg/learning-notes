# Linux Basic Commands Cheat Sheet

## 1. Help Manual

- View brief help:
  ```bash
  <command> --help
  ```

- View the full manual:
  ```bash
  man <command>
  ```

- Examples:
  ```bash
  ls --help
  man ls
  ```

---

## 2. Useful Commands for Navigation

| Command    | Description                           |
| ---------- | ------------------------------------- |
| `pwd`      | Print current working directory (full path) |
| `cd <dir>` | Change to the specified directory     |
| `cd ~`     | Change to the home directory          |
| `cd .`     | Current directory (no change)         |
| `cd ..`    | Change to the parent directory        |
| `cd -`     | Return to the previous directory      |

---

## 3. Listing Files

| Command     | Description                                   |
| ----------- | --------------------------------------------- |
| `ls`        | List contents of the current directory        |
| `ls <dir>`  | List contents of the specified directory      |
| `ls -l`     | Long listing (permissions, size, time, etc.)  |
| `ls -a`     | Show all files (including hidden files)       |
| `ls path/*` | Glob pattern match files (e.g., `labs/l*`)    |

> Hidden files: filenames start with `.` (e.g., `.git`, `.bash_history`).

---

## 4. Useful Commands for Files and Directories

### File viewing

| Command              | Description                       |
| -------------------- | --------------------------------- |
| `touch file.txt`     | Create a new file                 |
| `cat file.txt`       | Show the entire file              |
| `head file.txt`      | Show the first 10 lines           |
| `head -n 3 file.txt` | Show the first 3 lines            |
| `tail file.txt`      | Show the last 10 lines            |
| `tail -n 3 file.txt` | Show the last 3 lines             |
| `file <path>`        | Identify the file type            |

---

### File operations

| Command       | Description                    |
| ------------- | ------------------------------ |
| `cp src dest` | Copy a file                    |
| `mv src dest` | Move or rename a file          |
| `rm file.txt` | Delete a file (use with care)  |
| `mkdir dir`   | Create a directory             |
| `rmdir dir`   | Remove an empty directory      |

> WARNING: `rm` and `rmdir` are irreversible. Always confirm before deleting.

---

### Compression and archiving

| Command                   | Description                               |
| ------------------------- | ----------------------------------------- |
| `tar -cvf file.tar *.txt` | Archive all `.txt` files into a tar file  |

---

## 5. Useful Command Line Shortcuts

| Shortcut            | Description                    |
| ------------------- | ------------------------------ |
| `Tab`               | Autocomplete command or filename |
| `Ctrl + C`          | Interrupt the current command  |
| `Ctrl + R`          | Search command history         |
| `Up / Down`         | Browse command history         |
| `Ctrl + A` / `Home` | Move cursor to line start      |
| `Ctrl + E` / `End`  | Move cursor to line end        |
| `Ctrl + K`          | Delete text after the cursor   |
| `Ctrl + U`          | Clear the entire line          |
| `Ctrl + L`          | Clear the terminal screen      |
| `Shift + PgUp`      | Scroll up                      |
| `Shift + PgDn`      | Scroll down                    |
