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


from json import loads, JSONDecodeError

from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import db_session
from database.models.group import GroupState
from database.repositories.group import GroupRepository
from utils.config import ADMIN_TG_USER_ID
from utils.router import Router


router = Router(name=__name__)


@router.message(Command('add_groups'))
@db_session
async def add_groups(message: Message, session: AsyncSession) -> None:
    tg_user_id = message.from_user.id
    print(message)
    if tg_user_id != ADMIN_TG_USER_ID:
        return

    try:
        groups_str = message.text.replace('/add_groups ', '')
        print(groups_str)
        groups = loads(groups_str)

        if not isinstance(groups, list) or not all(isinstance(group, str) for group in groups):
            await message.answer(
                text='Неверный формат данных. '
                     'Ожидается список строк, например: /add_groups [\"username1\", \"username2\"]',
            )
            return

        group_repo = GroupRepository(session=session)

        added_groups = []
        for username in groups:
            if await group_repo.get_by(obj_in={'username': username}):
                await message.answer(
                    text=f'Группа @{username} уже добавлена ранее.',
                )
                continue
            await group_repo.create(
                obj_in={
                    'username': username,
                    'state': GroupState.PENDING_CONFIRMATION,
                },
            )
            added_groups.append(username)

        await session.commit()
        await message.answer(f'Группы успешно добавлены: {len(added_groups)} шт.')

    except JSONDecodeError:
        await message.answer(
            text='Ошибка в формате данных. Убедитесь, что вы передали список в формате JSON, например: '
                 '/add_groups [\"username1\", \"username2\"]',
        )
    except Exception as e:
        await session.rollback()
        await message.answer(
            text=f'Произошла ошибка при добавлении групп: {str(e)}',
        )
