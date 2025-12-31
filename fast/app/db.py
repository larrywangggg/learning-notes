from collections.abc import AsyncGenerator
import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclaritiveBase, relationship
import datetime

DATABASE_URL = "sqlite+aiosqlite:///./test.db" #change later to something like postgresql if needed

class Post(DeclaritiveBase):
    __tableame__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # Generate a unique identifier for each post, as a primary key
    column = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn: # conn is short for connection
        await conn.run_sync(DeclaritiveBase.metadata.create_all) # find all classes that inherit from DeclaritiveBase and create tables for them
        
        

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session