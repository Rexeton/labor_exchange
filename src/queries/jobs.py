from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Job
from schemas import JobCreateSchema


async def get_all(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[Job]:
    querie = select(Job).limit(limit).offset(skip)
    jobs_result = await db.execute(querie)
    return jobs_result.scalars().all()


async def get_by_id(db: AsyncSession, job_id: int) -> Optional[Job]:
    querie = select(Job).where(Job.id == job_id)
    job_result = await db.execute(querie)
    return job_result.scalars().first()


async def create(db: AsyncSession, job_schema: JobCreateSchema, curent_user_id) -> Optional[Job]:
    job = Job(
        user_id=curent_user_id,
        title=job_schema.title,
        discription=job_schema.discription,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=job_schema.is_active,
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def update(db: AsyncSession, update_job: Job) -> Optional[Job]:
    db.add(update_job)
    await db.commit()
    await db.refresh(update_job)
    return await get_by_id(db=db, job_id=update_job.id)


async def delete(db: AsyncSession, delete_job: Job) -> Optional[Job]:
    await db.delete(delete_job)
    await db.commit()
    return delete_job
