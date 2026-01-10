from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.schemas import PostCreate, PostResponse, UserCreate, UserRead, UserUpdate
from app.db import Post, create_db_and_tables, get_async_session, User
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import uuid
import tempfile
from pathlib import Path
from app.users import auth_backend, current_active_user, fastapi_users

@asynccontextmanager
async def lifespan(app : FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", include_in_schema=False)
async def index():
    return FileResponse(STATIC_DIR / "index.html")

app.include_router(fastapi_users.get_auth_router(auth_backend),prefix="/auth/jwt", tags=["auth"]) # JWT authentication routes
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate),prefix="/auth", tags=["auth"]) # User registration routes
app.include_router(fastapi_users.get_reset_password_router(),prefix="/auth", tags=["auth"]) # Password reset routes
app.include_router(fastapi_users.get_verify_router(UserRead),prefix="/auth", tags=["auth"]) # Email verification routes
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate),prefix="/users", tags=["users"]) # User management routes



@app.post("/upload")
async def upload_file(file: UploadFile = File(...),
                      caption: str = Form(""),
                      user: User = Depends(current_active_user), # don't allow unauthenticated users
                      session: AsyncSession = Depends(get_async_session)
                      ):
    
    temp_file_path = None
    
    try: 
        with tempfile.NamedTemporaryFile(delete=False,suffix = os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file) # Save uploaded file to a temporary location
            
        upload_result = imagekit.upload_file(
            file = open(temp_file_path, "rb"),
            file_name = file.filename,
            options = UploadFileRequestOptions(
                use_unique_file_name = True,
                tags = ["backend_upload"]
            )
        )
        
        print(
            "upload status:", upload_result.response_metadata.status_code,
            "error:", upload_result.response_metadata.error,
        )
        
        if upload_result.response_metadata.http_status_code == 200:
            post = Post(
                user_id = user.id,  # Associate the post with the authenticated user's ID
                caption = caption,
                url = upload_result.url,
                file_type = "video" if file.content_type.startswith("video/") else "image",
                file_name = upload_result.name
            )
            session.add(post)
            await session.commit() # Save the new post to the database, which will generate the ID and created_at fields
            await session.refresh(post)
            return post
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close() # Close the uploaded file
    
    
@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
    ):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.fetchall()] # Extract Post objects from the result
    
    result = await session.execute(select(User))
    users = [row[0] for row in result.fetchall()]
    user_dict = {u.id: u.email for u in users}
    
    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "user_id": str(post.user_id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(), # Convert datetime to ISO format string
                "is_owner": post.user_id == user.id,
                "email": user_dict.get(post.user_id, "Unknown") 
            }
                          )
    return {"posts": posts_data}



@app.delete("/post/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    try:
        post_uuid = uuid.UUID(post_id) # Convert string to UUID object
        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()
        
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this post")
        
        await session.delete(post)
        await session.commit()
        return{"success":True, "message":"Post deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
