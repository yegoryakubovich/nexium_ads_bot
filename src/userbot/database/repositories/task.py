#
# (c) 2024, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from datetime import datetime, timedelta
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import UserModel
from database.models.task import TaskModel, TaskState
from database.repositories.base import BaseRepository


class TaskRepository(BaseRepository[TaskModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(TaskModel, session)

    async def get_today(self, user_id: int) -> List[TaskModel]:
        now = datetime.utcnow()
        return await self.get_all_by(
            obj_in={
                'user_id': user_id,
                'datetime >=': now.replace(hour=0, minute=0, second=0, microsecond=0),
                'datetime <=': (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0),
            },
        )

    async def get_current(self, user: UserModel):
        return await self.get_all_by(
            obj_in={
                'user_id': user.id,
                'state': TaskState.IN_PROGRESS,
            },
        )

    async def get_count_today(self, user_id: int) -> int:
        return len(await self.get_today(user_id=user_id))
