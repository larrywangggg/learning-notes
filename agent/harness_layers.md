# Harness 四层结构

四个 harness 层，每层一个 Python Agent 场景的具体例子。

---

## 1. 校验输出格式（Verify）

LLM 让它返回 JSON，它可能给你一坨 markdown 包着的 JSON，或者干脆胡说。

```python
import json

def verify_output(raw: str) -> dict:
    # 剥掉 LLM 经常加的 ```json ... ``` 包裹
    cleaned = raw.strip().removeprefix("```json").removesuffix("```").strip()
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError(f"LLM 返回的不是合法 JSON: {raw[:100]}")

    # 校验必需字段
    required = {"action", "parameters"}
    if missing := required - result.keys():
        raise ValueError(f"缺少字段: {missing}")

    return result
```

没有这层，你的下游代码直接 `result["action"]` 然后炸了，而且报错信息完全看不出是 LLM 输出问题。

---

## 2. 错误重试（Feedback）

第一次输出格式不对？把错误信息喂回去让它改。

```python
def call_with_feedback(prompt: str, max_retries: int = 3) -> dict:
    messages = [{"role": "user", "content": prompt}]

    for attempt in range(max_retries):
        raw = call_llm(messages)
        try:
            return verify_output(raw)
        except ValueError as e:
            # 把错误当 feedback 塞回对话
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": f"格式错误: {e}。请严格返回 JSON。"})

    raise RuntimeError(f"{max_retries} 次重试后仍失败")
```

大部分 agent 框架第一次调用失败就直接抛异常——浪费。LLM 看到自己的错误后修正成功率非常高。

---

## 3. 边界限制（Bound）

LLM 说"删除所有用户数据"你就真删？

```python
ALLOWED_ACTIONS = {"search", "summarize", "draft_email"}
MAX_RESULTS = 20

def enforce_bounds(action: dict) -> dict:
    # 动作白名单
    if action["action"] not in ALLOWED_ACTIONS:
        raise PermissionError(f"禁止执行: {action['action']}")

    # 参数上限
    if action.get("parameters", {}).get("limit", 0) > MAX_RESULTS:
        action["parameters"]["limit"] = MAX_RESULTS  # 强制截断，不是报错

    return action
```

这是最容易被忽略的一层。没有它，你的 agent 就是一个拥有系统权限的随机文本生成器。

---

## 4. 降级方案（Fallback）

API 挂了、模型超时、输出三次都不对——总得有个兜底。

```python
def agent_step(prompt: str) -> str:
    try:
        result = call_with_feedback(prompt)  # 主路径：大模型 + 重试
        result = enforce_bounds(result)
        return execute(result)
    except (RuntimeError, PermissionError):
        # 降级：用规则引擎或小模型处理
        return rule_based_fallback(prompt)
    except Exception:
        # 最终兜底：不要让用户看到 500
        return "抱歉，当前无法处理您的请求，已记录日志，请稍后重试。"
```

没有 fallback 的 agent 在 demo 里很酷，上了生产就是定时炸弹。

---

## 完整 Harness 流程

```
用户输入 → LLM 调用 → verify(校验) → bound(限制) → 执行
                ↑            ↓ 失败
                └── feedback(重试) ──→ fallback(降级)
```

这四层加起来可能就 50 行代码，但它们决定了你的 agent 是玩具还是产品。这就是"小模型 + 强 harness 打赢大模型 + 弱 harness"的底层逻辑。
