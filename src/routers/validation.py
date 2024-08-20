from typing import Any, Union

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from queries import jobs as jobs_queries
from queries import responses as responses_queries
from schemas import ResponsesCreateSchema


class Real_Validation:
    @staticmethod
    def element_not_found(flag: Any) -> None:
        if not flag:
            raise HTTPException(
                status_code=204,
            )

    @staticmethod
    def is_company_for_job(flag: bool) -> None:
        if not flag:
            raise HTTPException(status_code=403, detail={"message": "User is not company"})

    @staticmethod
    def is_company_for_response(flag: bool) -> None:
        if flag:
            raise HTTPException(
                status_code=403,
                content={
                    "message": "Only not company user can read/create/update/delete there responses"
                },
            )

    @staticmethod
    def element_not_current_user_for(
        user_1: Union[int], user_2: Union[int], router_name: str, action_name: str
    ) -> None:
        if user_1 != user_2:
            raise HTTPException(
                status_code=403,
                detail={
                    "message": "it is not your {router} to {action}".format(
                        router=router_name, action=action_name
                    )
                },
            )

    @staticmethod
    async def post_responses_validation(db: AsyncSession, current_user: User, job_id: int) -> None:
        is_double_response = await responses_queries.get_response_by_job_id_and_user_id(
            db=db, job_id=job_id, user_id=current_user.id
        )
        if is_double_response:
            raise HTTPException(
                status_code=498,
                detail={"message": "You alredy have response for thise job"},
            )
        is_active_job = await jobs_queries.get_by_id(db=db, job_id=job_id)
        if not is_active_job:
            raise HTTPException(
                status_code=204,
            )
        if not is_active_job.is_active:
            raise HTTPException(status_code=499, detail={"message": "Job is not active"})

    @staticmethod
    async def patch_responses_validation(
        db: AsyncSession, response_to_patch: Union[ResponsesCreateSchema, None]
    ) -> None:
        if not response_to_patch:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "it is not your {router} to {action}".format(
                        router="Respose", action="update"
                    )
                },
            )

        is_active_job = await jobs_queries.get_by_id(db=db, job_id=response_to_patch.job_id)
        if not is_active_job.is_active:
            raise HTTPException(status_code=499, detail={"message": "Job is not active"})
