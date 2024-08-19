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


from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import db_session
from database.models.task import TaskState
from database.repositories.task import TaskRepository
from database.repositories.user import UserRepository
from routers.tasks.create_task import create_task
from utils import texts, States
from utils.keyboards import kb_main
from utils.router import Router


router = Router(name=__name__)


@router.message(F.text == texts.bt_task_skip, States.TASKS)
@db_session
async def mark_as_complete(message: Message, state: FSMContext, session: AsyncSession) -> None:
    user_repo = UserRepository(session=session)
    task_repo = TaskRepository(session=session)

    user = await user_repo.get_by(obj_in={'tg_user_id': message.from_user.id})
    tasks = await task_repo.get_current(user=user)

    if tasks:
        for t in tasks:
            await task_repo.update(
                id_=t.id,
                obj_in={
                    'state': TaskState.SKIPPED,
                },
            )
        await message.answer(text=texts.task_skipped)
        await create_task(message=message, state=state, session=session)
    else:
        await state.set_state(States.MAIN)
        await message.answer(text=texts.task_skipped_error, reply_markup=kb_main)