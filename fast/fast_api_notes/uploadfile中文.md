# FastAPI UploadFile 整理版

这份笔记整理了 FastAPI 上传文件的完整链路：请求解析 -> 临时文件 -> 第三方上传 -> 写数据库 -> 资源清理。

## 1. 路由签名做了什么
```python
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session),
):
    ...
```

关键点：
- `file: UploadFile = File(...)`  
  来自 `multipart/form-data` 的文件字段，FastAPI 会把它包装成 `UploadFile`。
- `caption: str = Form("")`  
  这是表单字段，不是 JSON body。
- `session: AsyncSession = Depends(...)`  
  每个请求自动注入一个 session，用完自动关闭。

注意：`UploadFile.file` 是文件流，不是磁盘路径。

## 2. 临时文件的必要性
第三方 SDK 通常需要 **真实文件或 bytes**，而上传文件是流，所以要写成临时文件。

```python
temp_file_path = None
with tempfile.NamedTemporaryFile(
    delete=False,
    suffix=os.path.splitext(file.filename)[1],
) as temp_file:
    shutil.copyfileobj(file.file, temp_file)
    temp_file_path = temp_file.name
```

解释：
- `NamedTemporaryFile` 安全创建临时文件，跨平台且避免冲突。
- `suffix` 保留原始扩展名，便于后端识别文件类型。
- `temp_file_path = None` 用于异常情况下的安全清理。

## 3. 上传到 ImageKit
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

要点：
- ImageKit 不接受 `UploadFile`，需要文件对象/bytes/base64。
- `use_unique_file_name=True` 防止重名覆盖。

## 4. 先确认成功再写数据库
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

解释：
- 上传失败不写库，避免脏数据。
- `refresh` 让生成字段（id、created_at）回到 Python 对象。

## 5. 必须的资源清理
```python
finally:
    if temp_file_path and os.path.exists(temp_file_path):
        os.unlink(temp_file_path)
    file.file.close()
```

无论成功或失败都要：
- 删除临时文件
- 关闭文件流

## 6. 全流程一句话
接收 multipart 文件 -> 写临时文件 -> 调用 ImageKit -> 成功则写库 -> 清理资源。
