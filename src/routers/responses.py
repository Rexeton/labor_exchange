"""" Model Responses API  """

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_user, get_db
from models import User
from queries import jobs as jobs_queries
from queries import responses as responses_queries
from schemas import (ResponsesCreateSchema, ResponsesSchema,
                     ResponsesUpdateSchema)

router = APIRouter(prefix='/responses', tags=['responses'])


@router.get('/responses_job_id/{job_id}', response_model=list[ResponsesSchema])
async def get_responses_by_job_id(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get responses by job id:
    job_id: job id
    db: datebase connection;
    current_user: current user
    """
    looking_job=await jobs_queries.get_by_id(db=db, id=job_id)
    if not current_user.is_company:
        responses_of_job_id = [await responses_queries.get_response_by_job_id_and_user_id(
        db=db, job_id=job_id, user_id=current_user.id
        )]
    elif looking_job.user_id==current_user.id:
        responses_of_job_id = await responses_queries.get_response_by_job_id(db=db, job_id=job_id)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You can\'t read not yours job responses ')
    if not responses_of_job_id:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='No responses in base by this job id for you')
    return responses_of_job_id


@router.get('/responses_user_id/', response_model=list[ResponsesSchema])
async def get_responses_by_user_id(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get responses by user id:
    user_id: user id
    db: datebase connection;
    current_user: current user
    """
    if not current_user.is_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Only not company user can read there responses',
        )
    responses_of_user = await responses_queries.get_response_by_user_id(db=db, user_id=current_user.id)

    if not responses_of_user:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='No responses in base by this user id')
    return responses_of_user


@router.post('', response_model=ResponsesCreateSchema)
async def create_response(
    response: ResponsesCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create response:
    response: dataset for ResponsesCreateSchema
    db: datebase connection;
    current_user: current user
    """
    if current_user.is_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Companies are prohibited from creating responses ',
        )
    is_double_responce = await responses_queries.get_response_by_job_id_and_user_id(
        db=db, job_id=response.job_id, user_id=current_user.id
    )
    if is_double_responce:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='You alredy have response for thise job'
        )
    is_active_job = await jobs_queries.get_by_id(db=db, id=response.job_id)
    if not is_active_job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='No job ith this id'
        )
    if not is_active_job.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Job is not active'
        )
    new_response = await responses_queries.response_create(
            db=db, response_schema=response, user_id=current_user.id
        )

    return ResponsesCreateSchema.from_orm(new_response)


@router.patch('/patch_response/{job_id}', response_model=ResponsesSchema)
async def patch_response(
    job_id: int,
    response: ResponsesUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Patch response:
    job_id: job id
    response: dataset for ResponsesCreateSchema
    db: datebase connection;
    current_user: current user
    """
    responce_to_patch = await responses_queries.get_response_by_job_id_and_user_id(
        db=db, job_id=job_id, user_id=current_user.id
    )
    if not responce_to_patch:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not responses to update',
        )
    is_active_job = await jobs_queries.get_by_id(db=db, id=response.job_id)
    if not is_active_job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='No job ith this id'
        )
    if not is_active_job.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Job is not active'
        )
    responce_to_patch.massage = (
        response.massage
        if response.massage is not None
        else responce_to_patch.massage
    )
    new_response = await responses_queries.update(db=db, response=responce_to_patch)
    return ResponsesUpdateSchema.from_orm(new_response)


@router.delete('/delete_response/job/{job_id}')
async def delete_response(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    delete responses by job_id:
    job_id: job id
    db: datebase connection;
    current_user: current user
    """
    responce_to_delete = await responses_queries.get_response_by_job_id_and_user_id(
        db=db, job_id=job_id, user_id=current_user.id
    )
    if not responce_to_delete:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail='You dont have responses for this job',
        )
    respose_to_delete = await responses_queries.delete(db=db, response=responce_to_delete)
    return respose_to_delete


@router.delete('/delete_response/{response_id}')
async def delete_response_by_id(
    response_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    delete responses by id:
    id: response id
    db: datebase connection;
    current_user: current user
    """
    responce_to_delete = await responses_queries.get_response_by_id(db=db, response_id=response_id)
    if not responce_to_delete:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail='Response not exist',
        )
    if responce_to_delete.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='It is not your response',
        )
    respose_to_delete = await responses_queries.delete(db=db, response=responce_to_delete)
    return respose_to_delete
