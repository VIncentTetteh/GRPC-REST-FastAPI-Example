from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Todo

async def create_todo(db: AsyncSession, title: str, description: str, user_id: int):
    todo = Todo(title=title, description=description, user_id=user_id)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo

async def get_todo(db: AsyncSession, todo_id: int):
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    return result.scalar_one_or_none()
