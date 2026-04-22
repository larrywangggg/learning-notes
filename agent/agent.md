# Agent

## 本质：一个循环

所有 Agent 框架拆到底就是这个结构：

```
while 任务未完成:
    1. 把当前状态 + 历史 组装成 prompt
    2. 调 LLM，拿到它的"决策"
    3. 解析决策 → 确定要调哪个 tool
    4. 执行 tool，拿到结果
    5. 把结果塞回历史，回到 1
```

LangChain 几万行代码干的事情，核心就是这个循环。

---

## 架构分层

```
┌─────────────────────────────────────┐
│           用户输入                   │
├─────────────────────────────────────┤
│         Agent Core Loop             │
│  ┌───────────┐  ┌────────────────┐  │
│  │  Planner  │→│  Tool Router   │  │
│  │ (LLM调用) │  │ (解析+分发)     │  │
│  └───────────┘  └────────────────┘  │
├─────────────────────────────────────┤
│            Harness 层               │
│  verify │ bound │ feedback │ fallback│
├─────────────────────────────────────┤
│            Tools 层                 │
│  搜索 │ 计算 │ 文件读写 │ API调用    │
└─────────────────────────────────────┘
```

- **Planner**：LLM，负责"想"下一步做什么
- **Tool Router**：解析 LLM 输出并调用对应工具
- **Harness**：四层保护（verify / bound / feedback / fallback）
- **Tools**：agent 能操作的具体能力

---

## 最小可运行实现

用本地模型（Ollama）写一个完整 agent，不依赖任何框架：

```python
"""
最小 Agent 实现 - 依赖: pip install ollama
启动前确保 ollama 在跑: ollama serve
拉个模型: ollama pull qwen2.5:7b
"""
import json
import ollama
import math

# ===== 1. 定义 Tools =====
TOOLS = {
    "calculator": {
        "description": "计算数学表达式，参数: expression (str)",
        "func": lambda params: str(eval(params["expression"], {"__builtins__": {}}, {"math": math}))
    },
    "get_length": {
        "description": "返回字符串长度，参数: text (str)",
        "func": lambda params: str(len(params["text"]))
    },
    "finish": {
        "description": "任务完成，参数: answer (str)",
        "func": lambda params: params["answer"]
    },
}

# ===== 2. System Prompt =====
SYSTEM = f"""你是一个 Agent。根据用户问题，决定调用哪个工具。

可用工具:
{json.dumps({k: v['description'] for k, v in TOOLS.items()}, ensure_ascii=False, indent=2)}

严格返回 JSON，格式:
{{"tool": "工具名", "parameters": {{...}}}}

完成任务时调用 finish 工具。每次只调一个工具。"""

# ===== 3. Harness: Verify =====
def parse_action(raw: str) -> dict:
    for prefix in ["```json", "```"]:
        raw = raw.strip().removeprefix(prefix)
    raw = raw.removesuffix("```").strip()

    action = json.loads(raw)
    if action["tool"] not in TOOLS:
        raise ValueError(f"未知工具: {action['tool']}")
    return action

# ===== 4. Harness: Bound =====
def check_bounds(action: dict) -> dict:
    if action["tool"] == "calculator":
        expr = action["parameters"].get("expression", "")
        forbidden = ["import", "open", "exec", "eval", "__"]
        if any(f in expr for f in forbidden):
            raise PermissionError(f"危险表达式: {expr}")
    return action

# ===== 5. Agent Core Loop =====
def run_agent(user_input: str, max_steps: int = 10):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_input},
    ]

    for step in range(max_steps):
        response = ollama.chat(model="qwen2.5:7b", messages=messages)
        raw = response["message"]["content"]
        print(f"\n--- Step {step + 1} ---")
        print(f"LLM 输出: {raw}")

        # Verify + Feedback
        try:
            action = parse_action(raw)
            action = check_bounds(action)
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": f"格式错误: {e}。请严格返回 JSON。"})
            continue
        except PermissionError as e:
            print(f"安全拦截: {e}")
            return "操作被安全策略拒绝。"

        # 执行 Tool
        if action["tool"] == "finish":
            print(f"\n最终答案: {action['parameters']['answer']}")
            return action["parameters"]["answer"]

        result = TOOLS[action["tool"]]["func"](action["parameters"])
        print(f"工具 [{action['tool']}] 返回: {result}")

        messages.append({"role": "assistant", "content": raw})
        messages.append({"role": "user", "content": f"工具返回: {result}\n根据结果继续。"})

    return "超过最大步数，任务失败。"  # Fallback

# ===== 运行 =====
if __name__ == "__main__":
    run_agent("'hello world' 有多少个字符？把字符数乘以 3 是多少？")
```

---

## 这 80 行覆盖了什么

4 层 harness 全在里面：

| 函数 / 行为 | 对应 harness 层 |
|-------------|----------------|
| `parse_action` | verify |
| `check_bounds` | bound |
| 格式错误重试 | feedback |
| 超步数兜底 | fallback |

**下一步可以扩展的方向：**

- 更多 tools：文件读写、网页搜索、数据库查询
- 更好的 prompt：few-shot examples、CoT
- 持久化记忆：对话历史存数据库
- 异步执行：多 tool 并行调用

骨架永远是这个循环。先把这个跑通，再考虑框架。
