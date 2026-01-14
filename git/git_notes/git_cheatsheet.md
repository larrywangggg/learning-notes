# ✅ Git Common Commands Cheatsheet

| Category | Command | Description |
|--------|--------|-------------|
| Install | git --version | Check whether Git is installed |
| Install | brew install git | Install Git on macOS via Homebrew |
| Init | git init | Initialise a Git repository in the current directory |
| Status | git status | Show the current repository status (most used) |
| Clone | git clone <repo_url> | Clone a remote repository from GitHub |
| Config | git config --global user.name "Name" | Set global Git username |
| Config | git config --global user.email "email" | Set global Git email |
| Stage | git add . | Stage all modified files |
| Stage | git add <file> | Stage a specific file |
| Commit | git commit -m "message" | Commit staged changes |
| Commit | git commit --amend | Edit the most recent commit |
| Push | git push | Push local commits to the remote repository |
| Push | git push -u origin main | First push and set upstream branch |
| Pull | git pull | Fetch and merge changes from remote |
| Branch | git branch | List local branches |
| Branch | git branch <name> | Create a new branch |
| Branch | git checkout <name> | Switch to an existing branch |
| Branch | git checkout -b <name> | Create and switch to a new branch |
| Merge | git merge <branch> | Merge a branch into the current branch |
| Remote | git remote -v | Show remote repository URLs |
| Remote | git remote add origin <url> | Add a remote repository |
| History | git log | View full commit history |
| History | git log --oneline | View concise commit history |
| Restore | git restore file | Restore the working directory file from the latest commit (HEAD) |
| Restore | git restore --source=staging file | Restore the working directory file from the staging area |
| Restore | git restore --source=<commit> file | Restore the working directory file from a specific commit |
| Undo | git restore --staged file | Unstage a file (reset staging area back to HEAD) |
| Rollback | git reset --soft HEAD~1 | Roll back the last commit, keep changes in staging area |
| Rollback | git reset --mixed HEAD~1 | Roll back the last commit, keep changes in working directory (default) |
| Rollback | git reset --hard HEAD~1 | Roll back the last commit and discard all changes (DANGEROUS) |
| Discard | git checkout -- file | Discard working directory changes (legacy syntax) |
| Discard | git checkout <commit> -- file | Restore file from a specific commit (legacy syntax) |
| Reset | git reset --hard HEAD~1 | Reset to the previous commit (use with caution) |
| Discard | git checkout . | Discard all unstaged local changes |
| Ignore | .gitignore | Specify files to be ignored by Git |
| Help | git help | Show Git help information |
