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
from random import choice, random

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.group import GroupState
from database.repositories.ad import AdRepository
from database.repositories.group import GroupRepository
from database.repositories.task import TaskRepository
from database.repositories.user import UserRepository
from utils import texts, States
from utils.config import ADMIN_USERNAME, COST
from utils.keyboards import create_ad_kb, create_task_kb, kb_task


async def create_task(message: Message, state: FSMContext, session: AsyncSession) -> None:
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

    await state.set_state(States.TASKS)

    ad_repo = AdRepository(session=session)
    group_repo = GroupRepository(session=session)

    ad = await ad_repo.get_by_id(id_=1)
    ad_text = choice([ad.text_1, ad.text_2, ad.text_3])
    ad_image = choice([ad.image_1, ad.image_2, ad.image_3, None])
    ad_text = (ad_text if random() < 0.7 else None) if ad_image else ad_text
    ad_keyboard = create_ad_kb(
        buttons={
            ad.button_1_text: ad.button_1_url,
            ad.button_2_text: ad.button_2_url,
            ad.button_3_text: ad.button_3_url,
        }
    ) if random() < 0.6 else None

    groups = await group_repo.get_all_by(obj_in={'state': GroupState.ACTIVE})
    group = choice(groups) # await group_repo.get_by_id(id_=122)

    async with Bot(
        token=ad.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    ) as ad_bot:
        if ad_image:
            ad_message = await ad_bot.send_photo(
                chat_id=ad.group_id,
                photo=FSInputFile(path=f'static/images/{ad_image}'),
                caption=ad_text,
                reply_markup=ad_keyboard,
            )
        else:
            ad_message = await ad_bot.send_message(
                chat_id=ad.group_id,
                text=ad_text,
                reply_markup=ad_keyboard,
            )

    ad_message_url = f'https://t.me/{ad.group_username}/{ad_message.message_id}'
    datetime_ = datetime.utcnow()
    expiration_datetime = datetime_+timedelta(hours=1)
    task = await task_repo.create(
        obj_in={
            'ad_id': ad.id,
            'user_id': user.id,
            'group_id': group.id,
            'cost': COST,
            'text': ad_text,
            'image': ad_image,
            'have_keyboard': False if ad_keyboard is None else True,
            'message_url': ad_message_url,
            'datetime': datetime_,
            'expiration_datetime': expiration_datetime,
        }
    )
    await message.answer(
        text=texts.task_1.format(
            task_id=str(task.id).zfill(8),
            task_cost=task.cost,
            group_username=group.username,
            url=task.message_url,
        ),
        reply_markup=create_task_kb(
            group_url=f'https://t.me/{group.username}',
            message_url=task.message_url,
        ),
    )
    await message.answer(
        text=texts.task_2,
        reply_markup=kb_task,
    )