# Python Dictionary (dict) - Cleaned Version

dict is a hash-table based key -> value mapping and one of the most common data containers in backend/FastAPI work. The notes below are organized from basics to pitfalls.

## 1. Essence and traits
- Unique keys
- Average lookup O(1)
- Mutable object

```python
user = {"name": "Eden", "age": 23}
```

## 2. Creation methods
1. Literal
```python
d = {"a": 1, "b": 2}
```

2. dict constructor (keys must be valid identifiers)
```python
d = dict(a=1, b=2)
```

3. fromkeys (optional knowledge)
```python
keys = ["a", "b", "c"]
d = dict.fromkeys(keys, 0)
```

4. Dict comprehension
```python
d = {x: x * 2 for x in range(3)}
d_even = {x: x for x in range(10) if x % 2 == 0}
```

## 3. Key / value rules
- Keys must be hashable and immutable
- Values can be any Python object

Valid keys:
```python
valid = {"str": 1, 1: "one", 3.14: "pi", (1, 2): "tuple"}
```

Invalid keys:
```python
invalid = {[]: 1, {}: 2, set(): 3}  # will raise
```

## 4. Access and existence
```python
user["email"]          # KeyError
user.get("email")      # None
user.get("email", "N/A")
"email" in user
```

## 5. Create, update, delete (CRUD)
```python
user["age"] = 24
user["email"] = "eden@test.com"

del user["email"]          # KeyError risk
user.pop("email", None)    # safe delete
user.popitem()             # remove and return last item
```

## 6. Iteration
```python
for k in user:
    ...

for v in user.values():
    ...

for k, v in user.items():
    ...
```

## 7. Common methods cheat sheet
| Method | Purpose |
| --- | --- |
| get | safe access |
| keys | all keys |
| values | all values |
| items | key-value pairs |
| update | merge dict |
| pop | delete by key |
| clear | clear all |

Common `update` usage:
```python
a = {"x": 1}
b = {"y": 2}
a.update(b)  # {'x': 1, 'y': 2}
```

## 8. Copying and mutability
Shallow copy only copies the first level:
```python
a = {"x": [1, 2]}
b = a.copy()
b["x"].append(3)
print(a)  # affected
```

Deep copy copies all nested levels:
```python
import copy
b = copy.deepcopy(a)
```

Mutations inside functions affect the original:
```python
def change(d):
    d["x"] = 100

data = {}
change(data)
print(data)  # {'x': 100}
```

## 9. Nested dict and safe access
```python
user = {
    "id": 1,
    "profile": {"email": "eden@test.com", "address": {"city": "Canberra"}},
}
user["profile"]["address"]["city"]
user.get("profile", {}).get("address", {}).get("city")
```

## 10. dict and function parameters
```python
data = {"name": "Eden", "age": 23}

def create_user(name, age):
    ...

create_user(**data)

def func(**kwargs):
    print(kwargs)
```

## 11. dict, list, set, and JSON
| Structure | Typical usage |
| --- | --- |
| list | ordered collection |
| dict | structured key-value data |
| set | unique collection |

JSON vs dict:
```python
# JSON:
# {"name": "Eden", "age": 23}

data = {"name": "Eden", "age": 23}
```

## 12. FastAPI and Pydantic
Data flow:
```
JSON -> dict -> Pydantic model -> business logic
```

Comparison:
| Capability | dict | Pydantic |
| --- | --- | --- |
| Type safety | no | yes |
| Validation | no | yes |
| IDE hints | weak | strong |
| API docs | no | yes |

## 13. FastAPI / Pydantic examples
### Example 1: request validation + response model
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

### Example 2: risk of accepting raw dict
```python
from fastapi import Body

@app.post("/raw")
def raw(payload: dict = Body(...)):
    age = payload.get("age")
    return {"age_next": age + 1}  # breaks if age is str or None
```

### Example 3: PATCH partial update
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

## 14. Common pitfalls
- Using `[]` for uncertain keys
- Forgetting dict is mutable
- Misusing shallow copy and sharing references
- Treating dict as object attributes (`user.name`)
- Trusting external dict types without validation

## 15. One-line summary
dict is Python's "raw JSON": flexible and powerful, but unsafe without validation before business logic.
