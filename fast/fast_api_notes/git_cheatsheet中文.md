# ✅ Git 常用指令 Cheatsheet

| 分类 | 常用指令 | 作用说明 |
|----|----|----|
| 安装 | git --version | 检查是否已安装 Git |
| 安装 | brew install git | 在 macOS 上通过 Homebrew 安装 Git |
| 初始化 | git init | 初始化当前目录为 Git 仓库 |
| 状态 | git status | 查看当前仓库状态（最常用） |
| 克隆 | git clone <repo_url> | 从 GitHub 克隆远程仓库 |
| 配置 | git config --global user.name "Name" | 设置全局用户名 |
| 配置 | git config --global user.email "email" | 设置全局邮箱 |
| 暂存 | git add . | 将所有改动加入暂存区 |
| 暂存 | git add <file> | 暂存指定文件 |
| 提交 | git commit -m "message" | 提交一次版本记录 |
| 提交 | git commit --amend | 修改最近一次提交 |
| 推送 | git push | 推送本地提交到远程仓库 |
| 推送 | git push -u origin main | 首次推送并绑定远程分支 |
| 拉取 | git pull | 拉取远程最新代码并合并 |
| 分支 | git branch | 查看本地分支 |
| 分支 | git branch <name> | 新建分支 |
| 分支 | git checkout <name> | 切换分支 |
| 分支 | git checkout -b <name> | 新建并切换分支 |
| 合并 | git merge <branch> | 合并指定分支到当前分支 |
| 远程 | git remote -v | 查看远程仓库地址 |
| 远程 | git remote add origin <url> | 添加远程仓库 |
| 历史 | git log | 查看完整提交历史 |
| 历史 | git log --oneline | 查看简洁提交历史 |
| 回退 | git reset --hard HEAD~1 | 回退到上一个提交（慎用） |
| 放弃 | git checkout . | 放弃所有未暂存的修改 |
| 忽略 | .gitignore | 指定不被 Git 跟踪的文件 |
| 帮助 | git help | 查看 Git 帮助 |
