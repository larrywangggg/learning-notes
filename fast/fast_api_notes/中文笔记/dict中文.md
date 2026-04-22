# Python Dictionary（dict）整理版

dict 是基于哈希表的 key -> value 映射结构，是后端/FastAPI 中最常见的数据承载形式之一。下面按基础 -> 进阶 -> 易踩坑整理。

## 1. 本质与特性
- key 唯一
- 平均查找 O(1)
- 可变对象（mutable）

```python
user = {"name": "Eden", "age": 23}
```

## 2. 创建方式
1. 字面量
```python
d = {"a": 1, "b": 2}
```

2. dict 构造器（key 需是合法变量名）
```python
d = dict(a=1, b=2)
```

3. fromkeys（了解即可）
```python
keys = ["a", "b", "c"]
d = dict.fromkeys(keys, 0)
```

4. 字典推导式
```python
d = {x: x * 2 for x in range(3)}
d_even = {x: x for x in range(10) if x % 2 == 0}
```

## 3. key / value 规则
- key 必须可 hash 且不可变
- value 可以是任何对象

合法 key：
```python
valid = {"str": 1, 1: "one", 3.14: "pi", (1, 2): "tuple"}
```

非法 key：
```python
invalid = {[]: 1, {}: 2, set(): 3}  # 会报错
```

## 4. 取值与存在性
```python
user["email"]          # KeyError
user.get("email")      # None
user.get("email", "N/A")
"email" in user
```

## 5. 增、改、删（CRUD）
```python
user["age"] = 24
user["email"] = "eden@test.com"

del user["email"]          # KeyError 风险
user.pop("email", None)    # 安全删除
user.popitem()             # 删除并返回最后一项
```

## 6. 遍历方式
```python
for k in user:
    ...

for v in user.values():
    ...

for k, v in user.items():
    ...
```

## 7. 常用方法速查
| 方法 | 作用 |
| --- | --- |
| get | 安全取值 |
| keys | 所有 key |
| values | 所有 value |
| items | key-value 对 |
| update | 合并 dict |
| pop | 删除指定 key |
| clear | 清空 |

`update` 常见用法：
```python
a = {"x": 1}
b = {"y": 2}
a.update(b)  # {'x': 1, 'y': 2}
```

## 8. 拷贝与可变性
浅拷贝只复制第一层：
```python
a = {"x": [1, 2]}
b = a.copy()
b["x"].append(3)
print(a)  # 被影响
```

深拷贝复制所有层级：
```python
import copy
b = copy.deepcopy(a)
```

函数内修改会影响原对象：
```python
def change(d):
    d["x"] = 100

data = {}
change(data)
print(data)  # {'x': 100}
```

## 9. 嵌套 dict 与安全取值
```python
user = {
    "id": 1,
    "profile": {"email": "eden@test.com", "address": {"city": "Canberra"}},
}
user["profile"]["address"]["city"]
user.get("profile", {}).get("address", {}).get("city")
```

## 10. dict 与函数参数
```python
data = {"name": "Eden", "age": 23}

def create_user(name, age):
    ...

create_user(**data)

def func(**kwargs):
    print(kwargs)
```

## 11. dict、list、set、JSON 的关系
| 结构 | 典型用途 |
| --- | --- |
| list | 有序集合 |
| dict | 结构化键值数据 |
| set | 去重集合 |

JSON 与 dict 的关系：
```python
# JSON:
# {"name": "Eden", "age": 23}

data = {"name": "Eden", "age": 23}
```

## 12. FastAPI 与 Pydantic
数据流：
```
JSON -> dict -> Pydantic model -> 业务逻辑
```

对比：
| 能力 | dict | Pydantic |
| --- | --- | --- |
| 类型安全 | 否 | 是 |
| 校验 | 否 | 是 |
| IDE 提示 | 弱 | 强 |
| API 文档 | 否 | 是 |

## 13. FastAPI / Pydantic 示例
### 示例 1：请求校验 + 响应模型
```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class UserIn(BaseModel):
    name: str
    age: int = Field(ge=0)

class UserOut(BaseModel):
    id: int
    name: str
    age: int

@app.post("/users", response_model=UserOut)
def create_user(payload: UserIn):
    data = payload.model_dump()  # Pydantic v1: payload.dict()
    data["id"] = 1
    return data
```

### 示例 2：直接接收 dict 的风险
```python
from fastapi import Body

@app.post("/raw")
def raw(payload: dict = Body(...)):
    age = payload.get("age")
    return {"age_next": age + 1}  # age 是字符串或 None 就会出错
```

### 示例 3：PATCH 局部更新
```python
from typing import Optional
from fastapi import HTTPException

class UserPatch(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

fake_db = {1: {"id": 1, "name": "Eden", "age": 23}}

@app.patch("/users/{user_id}")
def update_user(user_id: int, patch: UserPatch):
    user = fake_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updates = patch.model_dump(exclude_unset=True)  # v1: patch.dict(exclude_unset=True)
    user.update(updates)
    return user
```

## 14. 常见坑
- 不确定的 key 直接用 `[]`
- 忘记 dict 是可变对象
- 误用浅拷贝导致共享引用
- 把 dict 当对象用（`user.name`）
- 直接信任外部 dict 的类型

## 15. 一句话总结
dict 是 Python 世界的 "原始 JSON"，灵活强大，但不安全；进入业务逻辑前应尽量做校验和约束。
