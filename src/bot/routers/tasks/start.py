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


from datetime import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import db_session
from database.repositories.user import UserRepository
from utils import texts, States
from utils.config import ADMIN_USERNAME
from utils.router import Router


router = Router(name=__name__)


@router.message(F.text == texts.bt_tasks_start, States.MAIN)
@db_session
async def start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    tg_user_id = message.from_user.id

    user_repo = UserRepository(session=session)
    user = await user_repo.get_by(obj_in={'tg_user_id': tg_user_id})

    # Next refill
    now = datetime.utcnow()
    next_refill_h = 24 - now.hour
    next_refill_m = 60 - now.minute

    print(next_refill_h, next_refill_m)

    await state.set_state(States.MAIN)
    await message.answer(
        text=texts.tasks_start_limit.format(
            user_id=str(user.id).zfill(6),
            completed_tasks_today=0,
            daily_tasks_limit=user.daily_tasks_limit,
            completed_today_successful=0,
            next_refill_h=next_refill_h,
            next_refill_m=next_refill_m,
            admin_username=ADMIN_USERNAME,
        ),
    )
