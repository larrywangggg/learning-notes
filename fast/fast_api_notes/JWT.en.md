# JWT (JSON Web Token) - Cleaned Version

This note explains JWT from a backend/FastAPI perspective: structure, flow, security, and a common FastAPI Users setup.

![JWT flow](images/JWT.png)

## 1. One-line definition
JWT is a server-signed "pass" string. Clients carry it to prove identity without server-side sessions.

## 2. JWT structure
JWT has three dot-separated parts:
```
header.payload.signature
```
- Header: signing algorithm
- Payload: identity claims (user_id, role, exp)
- Signature: server-side signature to prevent tampering

Key point: **JWT is signed, not encrypted**. Anyone can decode it, but cannot forge it.

## 3. Typical flow (login -> carry -> verify)
1. User logs in, POST `/auth`  
2. Server validates credentials and issues JWT (or returns 401)  
3. Client stores JWT (HttpOnly cookie or Authorization header)  
4. Client calls protected APIs with:  
   `Authorization: Bearer <JWT>`  
5. Server verifies signature and expiration  
6. On success, proceed; on failure, return 401/403  

## 4. Why JWT avoids sessions
Session drawbacks:  
- server-side state  
- shared session storage for multiple servers  
- sticky sessions for scaling  

JWT advantages:  
- stateless  
- easy to scale  
- API-friendly for frontend-backend separation  

## 5. What goes in the payload
Only identity-related fields, no sensitive data.

Example:
```json
{
  "sub": "user_id",
  "email": "eden@example.com",
  "role": "user",
  "exp": 1700000000
}
```

Do not include: passwords, phone numbers, bank cards, private data.

## 6. Security essentials
1. Tamper protection via signature:
```text
HMACSHA256(base64(header) + "." + base64(payload), SECRET_KEY)
```
2. If leaked, a token is valid until expiration, so you need:
   - short expiration
   - refresh tokens
   - HTTPS
3. JWT is authentication, not authorization. Permissions still require logic:
```python
if user.role != "admin":
    raise HTTPException(status_code=403)
```

## 7. Where JWT fits in FastAPI
Typical dependency:
```python
Depends(get_current_user)
```
Flow: read header/cookie -> verify -> decode -> load current_user.

## 8. FastAPI Users setup (user.py perspective)
### 8.1 Key components
- `BearerTransport`: reads token from `Authorization: Bearer`  
- `JWTStrategy`: signing + expiration logic  
- `AuthenticationBackend`: combines transport + strategy  
- `FastAPIUsers`: unified dependency entry point  

### 8.2 SECRET
```python
SECRET = "YOUR-SECRET-KEY"
```
Used for JWT signing and verification tokens. In production, store in `.env`.

### 8.3 UserManager
```python
class UserManager(UUIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
```
Manages user lifecycle logic (register, reset password, verify).

### 8.4 get_user_manager dependency
```python
async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db)
):
    yield UserManager(user_db)
```
`yield` enables proper lifecycle handling.

### 8.5 BearerTransport and JWTStrategy
```python
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)
```

### 8.6 AuthenticationBackend
```python
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
```

### 8.7 FastAPIUsers and current_active_user
```python
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    auth_backend,
)

current_active_user = fastapi_users.current_user(active=True)
```

### 8.8 Route usage
```python
@router.get("/me")
async def me(user: User = Depends(current_active_user)):
    return user
```

## 9. One-line end-to-end flow
Login issues JWT -> client stores -> client sends Bearer -> server verifies -> user loaded -> injected into routes.
