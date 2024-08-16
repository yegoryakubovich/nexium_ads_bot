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
from database.repositories.ad import AdRepository
from database.repositories.task import TaskRepository
from database.repositories.user import UserRepository
from utils import texts, States
from utils.config import ADMIN_USERNAME
from utils.keyboards import create_ad_kb
from utils.router import Router


router = Router(name=__name__)


@router.message(F.text.in_({texts.bt_tasks_start, }))
@db_session
async def start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if await state.get_state() not in [States.MAIN, States.TASKS]:
        return
    tg_user_id = message.from_user.id

    user_repo = UserRepository(session=session)
    user = await user_repo.get_by(obj_in={'tg_user_id': tg_user_id})

    # Next refill
    now = datetime.utcnow()
    next_refill_h = 24 - now.hour
    next_refill_m = 60 - now.minute

    task_repo = TaskRepository(session=session)
    tasks_today = await task_repo.get_count_today(user_id=user.id)

    if tasks_today >= user.daily_tasks_limit:
        await message.answer(
            text=texts.tasks_start_limit.format(
                user_id=str(user.id).zfill(6),
                tasks_today=tasks_today,
                daily_tasks_limit=user.daily_tasks_limit,
                completed_today_successful=0,
                next_refill_h=next_refill_h,
                next_refill_m=next_refill_m,
                admin_username=ADMIN_USERNAME,
            ),
        )
        return

    ad_repo = AdRepository(session=session)
    ad = await ad_repo.get_by_id(id_=1)
    ad_texts = [ad.text_1, ad.text_2, ad.text_3]
    ad_images = [ad.image_1, ad.image_2, ad.image_3]
    ad_keyboard = create_ad_kb(
        buttons={
            ad.button_1_text: ad.button_1_url,
            ad.button_2_text: ad.button_2_url,
            ad.button_3_text: ad.button_3_url,
        }
    )

    await state.set_state(States.TASKS)
