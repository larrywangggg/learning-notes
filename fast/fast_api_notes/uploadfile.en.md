# FastAPI UploadFile (Cleaned Version)

This note summarizes the full upload flow in FastAPI: request parsing -> temp file -> third-party upload -> database write -> cleanup.

## 1. What the route signature does
```python
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session),
):
    ...
```

Key points:
- `file: UploadFile = File(...)`  
  File field from `multipart/form-data`, wrapped as `UploadFile`.
- `caption: str = Form("")`  
  A form field, not JSON body.
- `session: AsyncSession = Depends(...)`  
  Injects a per-request session and closes it automatically.

Note: `UploadFile.file` is a stream, not a file path.

## 2. Why a temp file is needed
Most SDKs expect a **real file or bytes**, while uploads are streams, so you need to write a temp file.

```python
temp_file_path = None
with tempfile.NamedTemporaryFile(
    delete=False,
    suffix=os.path.splitext(file.filename)[1],
) as temp_file:
    shutil.copyfileobj(file.file, temp_file)
    temp_file_path = temp_file.name
```

Explanation:
- `NamedTemporaryFile` creates a safe, cross-platform temp file.
- `suffix` preserves the original extension for type detection.
- `temp_file_path = None` enables safe cleanup on errors.

## 3. Upload to ImageKit
```python
upload_result = imagekit.upload_file(
    file=open(temp_file_path, "rb"),
    file_name=file.filename,
    options=UploadFileRequestOptions(
        use_unique_file_name=True,
        tags=["backend_upload"],
    ),
)
```

Key points:
- ImageKit does not accept `UploadFile`; it needs a file object/bytes/base64.
- `use_unique_file_name=True` prevents name collisions.

## 4. Write to DB only on success
```python
if upload_result.response_metadata.http_status_code == 200:
    post = Post(
        caption=caption,
        url=upload_result.url,
        file_type="video" if file.content_type.startswith("video/") else "image",
        file_name=upload_result.name,
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
```

Explanation:
- If upload fails, do not write to the DB.
- `refresh` pulls generated fields (id, created_at) back into the object.

## 5. Always clean up
```python
finally:
    if temp_file_path and os.path.exists(temp_file_path):
        os.unlink(temp_file_path)
    file.file.close()
```

Clean up on success or failure:
- delete temp file
- close file stream

## 6. One-line flow
Receive multipart file -> write temp file -> upload to ImageKit -> write DB on success -> clean up.
