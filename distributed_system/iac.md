# Infrastructure as Code (IaC)

## 一、什么是 IaC

用代码来定义和管理基础设施，而不是手动点云平台控制台或 SSH 进去手工配置。

**解决了什么问题？**

传统手工运维的痛点：
- 配置只存在某人脑子里，换个人就不会了
- staging 和 production 环境配置不一致，导致"staging 没问题，production 出问题"
- 无法知道某台机器上周被谁改了什么配置
- 扩容时需要人工一台一台操作，容易出错

IaC 的核心价值：
- **可重复**：同一份代码部署出完全相同的环境
- **可审查**：infra 变更通过 PR review，就像业务代码一样
- **可版本控制**：git history 记录所有变更，可以 rollback
- **自动化**：集成到 CI/CD pipeline，减少人工干预

---

## 二、IaC 的两种主要类型

### 声明式（Declarative）
描述"我想要什么状态"，工具自动计算需要做哪些操作来达到目标状态。

```hcl
# Terraform 例子：声明我想要 3 台 EC2
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  count         = 3
}
```

工具会对比当前状态和目标状态，只做必要的变更（idempotent）。

**代表工具**：Terraform、CloudFormation、Pulumi

### 命令式（Imperative）
描述"我想执行哪些步骤"，按顺序执行指令。

```yaml
# Ansible 例子：命令式安装 nginx
- name: Install nginx
  apt:
    name: nginx
    state: present
- name: Start nginx
  service:
    name: nginx
    state: started
```

**代表工具**：Ansible、Chef、Puppet（部分支持声明式）

---

## 三、Terraform 深入

### 核心概念

**Provider**：对接各种云平台的插件（AWS、GCP、Azure、Cloudflare 等）。

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}
```

**Resource**：要创建的具体云资源。

```hcl
# 创建一个 S3 bucket
resource "aws_s3_bucket" "logs" {
  bucket = "my-app-logs-bucket"
}

# 创建一个安全组
resource "aws_security_group" "web" {
  name = "web-sg"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

**Variable**：参数化配置，避免硬编码。

```hcl
variable "instance_count" {
  type    = number
  default = 3
}

resource "aws_instance" "web" {
  count         = var.instance_count
  instance_type = "t3.micro"
}
```

**Output**：导出资源的属性，供其他模块或人工查看。

```hcl
output "web_public_ips" {
  value = aws_instance.web[*].public_ip
}
```

**State**：Terraform 记录当前基础设施实际状态的文件（`terraform.tfstate`）。

- 本地 state：适合个人项目，团队协作容易冲突
- 远程 state：存在 S3 + DynamoDB（加锁），团队共享

---

### Terraform 工作流

```
terraform init      # 下载 provider 插件
terraform plan      # 预览会做哪些变更（dry run）
terraform apply     # 执行变更
terraform destroy   # 销毁所有资源
```

**`terraform plan` 的输出示例**：
```
# aws_instance.web will be created
+ resource "aws_instance" "web" {
    + ami           = "ami-0c55b159cbfafe1f0"
    + instance_type = "t3.micro"
  }

Plan: 1 to add, 0 to change, 0 to destroy.
```

`+` 表示新建，`~` 表示修改，`-` 表示删除。

---

### Module（模块化）

将可复用的资源组合封装成模块。

```
modules/
  vpc/
    main.tf
    variables.tf
    outputs.tf
  rds/
    main.tf
    variables.tf
    outputs.tf
```

调用模块：
```hcl
module "database" {
  source        = "./modules/rds"
  instance_type = "db.t3.medium"
  db_name       = "myapp"
}
```

**好处**：不同环境（staging/production）复用同一套模块，只改参数。

---

### Workspace（工作空间）

用同一套代码管理多套环境（dev/staging/production）。

```bash
terraform workspace new staging
terraform workspace select production
terraform apply  # 使用不同 state 文件，互不干扰
```

---

## 四、Ansible 深入

### 核心概念

**Inventory**：定义要管理哪些机器。

```ini
# inventory.ini
[web_servers]
web1.example.com
web2.example.com

[db_servers]
db1.example.com ansible_user=admin
```

**Playbook**：定义要在哪些机器上执行哪些任务。

```yaml
# deploy.yml
- name: Deploy web application
  hosts: web_servers
  become: true  # sudo 权限

  tasks:
    - name: Install required packages
      apt:
        name:
          - nginx
          - python3
        state: present
        update_cache: true

    - name: Copy app config
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: Restart nginx  # 配置变更后触发 handler

    - name: Ensure nginx is running
      service:
        name: nginx
        state: started
        enabled: true

  handlers:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted
```

**Role**：结构化的 Playbook 组件，按功能封装（类似 Terraform module）。

```
roles/
  nginx/
    tasks/main.yml
    templates/nginx.conf.j2
    defaults/main.yml
    handlers/main.yml
```

**Idempotency**：Ansible 大多数 module 是幂等的——多次执行同一个 playbook，只有需要变更时才会变更，不会重复执行。

---

### 常用 Module

| Module | 用途 | 例子 |
|--------|------|------|
| `apt` / `yum` | 安装包 | 安装 Java、nginx |
| `copy` / `template` | 下发文件/配置 | 发配置文件（支持 Jinja2 模板） |
| `service` | 管理服务 | 启动/停止/重启 systemd 服务 |
| `user` | 管理用户 | 创建运维账号 |
| `command` / `shell` | 执行命令 | 跑初始化脚本 |
| `file` | 管理文件/目录 | 创建目录、设置权限 |
| `git` | 拉代码 | 从 repo 拉指定 branch |

---

## 五、Terraform vs Ansible

| | Terraform | Ansible |
|---|---|---|
| **主要用途** | 创建和管理基础设施资源 | 配置机器和部署应用 |
| **风格** | 声明式 | 命令式为主 |
| **State 管理** | 维护 state 文件，追踪资源状态 | 无 state，每次重新检测当前状态 |
| **适合场景** | 云资源生命周期管理 | 批量配置机器、应用部署 |
| **执行方式** | 从本地/CI 执行，直连云 API | 通过 SSH 连接目标机器 |
| **学习曲线** | HCL 语法，state 管理需要理解 | YAML 语法，上手相对容易 |

**典型分工**：
1. Terraform 创建 VM、VPC、数据库、负载均衡等云资源
2. Ansible 进入机器，安装软件、配置服务、部署代码

---

## 六、其他 IaC 工具

### CloudFormation
AWS 原生 IaC，用 JSON/YAML 描述 AWS 资源。深度集成 AWS 服务，但只能用于 AWS。

### Pulumi
用真正的编程语言（TypeScript、Python、Go）来写 IaC，而非 DSL。对开发者更友好，可以使用 for 循环、函数等语言特性。

```typescript
// Pulumi 例子（TypeScript）
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("my-bucket", {
  acl: "private",
});

export const bucketName = bucket.id;
```

### Helm（Kubernetes）
Kubernetes 的包管理器，用于管理 K8s 应用的部署配置（类似 apt/brew，但管的是 K8s 资源）。

---

## 七、IaC 最佳实践

### 1. 不要手动改云资源
通过 Terraform 管理的资源，不要直接在控制台手动修改，否则 state 会和实际状态不一致（称为 **drift**）。定期用 `terraform plan` 检测 drift。

### 2. 远程 State + 锁
团队协作时必须用远程 state（如 S3 + DynamoDB）：
- S3 存储 state 文件
- DynamoDB 提供锁，防止两个人同时 apply 导致冲突

### 3. 环境隔离
不同环境用不同的 state 和不同的云账号（或至少不同的 VPC），避免误操作影响生产。

```
environments/
  dev/
    main.tf        # 调用共用 modules，传入 dev 参数
    terraform.tfvars
  staging/
    main.tf
    terraform.tfvars
  production/
    main.tf
    terraform.tfvars
```

### 4. Plan 前必须 Review
`terraform apply` 前先跑 `terraform plan`，仔细看会有哪些 destroy/replace 操作，避免意外删除资源。

> `~` 修改通常安全，`-/+` replace 和 `-` destroy 要特别小心。

### 5. 敏感信息不进代码库
密码、密钥等不能写在 `.tf` 文件里。使用：
- 环境变量传入
- AWS Secrets Manager / HashiCorp Vault 在运行时读取
- `.tfvars` 文件加入 `.gitignore`

---

## 八、IaC 在 CI/CD 中的位置

```
开发者提 PR 修改 .tf 文件
  → CI 自动跑 terraform validate（语法检查）
  → CI 自动跑 terraform plan，输出变更预览，贴到 PR 评论
  → 人工 Review PR 和 plan 输出
  → merge 后，CI/CD 自动跑 terraform apply
  → 变更生效，state 更新
```

这样 infra 变更和业务代码变更走同一套 review 流程，可审查、可追溯。
