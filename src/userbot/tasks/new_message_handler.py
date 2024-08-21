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

from sqlalchemy.ext.asyncio import AsyncSession
from telethon.events import NewMessage
from telethon.tl.types import PeerChannel, Message, PeerUser

from database.database import db_session
from database.models.task import TaskState
from database.repositories.task import TaskRepository
from database.repositories.user import UserRepository
from utils import texts
from utils.bot import bot


@db_session
async def new_message(event: NewMessage.Event, session: AsyncSession):
    message = event.message
    message: Message

    if not isinstance(message.peer_id, PeerChannel):
        return

    if not isinstance(message.from_id, PeerUser):
        return

    tg_user_id = message.from_id.user_id
    tg_id = int(f'-100{message.peer_id.channel_id}')

    user_repo = UserRepository(session=session)
    user = await user_repo.get_by(obj_in={'tg_user_id': tg_user_id})
    if not user:
        return

    task_repo = TaskRepository(session=session)
    tasks = await task_repo.get_all_by(
        obj_in={
            'user_id': user.id,
            'state': [TaskState.IN_PROGRESS, TaskState.PENDING_CONFIRMATION]
        },
    )
    if not tasks:
        return

    for task in tasks:
        if not message.fwd_from or message.fwd_from.from_id.user_id != task.ad.bot_tg_id:
            continue

        if task.group.tg_id != tg_id:
            continue

        if task.text:
            if task.text != message.message:
                continue

        # FIXME
        if task.image:
            if not message.media:
                continue

        await task_repo.update(
            id_=task.id,
            obj_in={
                'state': TaskState.COMPLETED,
                'auto_confirmed_datetime': datetime.utcnow(),
            },
        )
        await user_repo.update(
            id_=user.id,
            obj_in={
                'balance': user.balance + task.cost,
            }
        )
        await bot.send_message(
            chat_id=task.user.tg_user_id,
            text=texts.task_completed.format(
                task_id=task.id,
                cost=task.cost,
            ),
        )
        break