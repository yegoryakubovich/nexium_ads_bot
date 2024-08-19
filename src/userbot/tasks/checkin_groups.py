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
from asyncio import sleep
from random import choice, randint

from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.errors import UsernameNotOccupied
from pyrogram.raw.functions.folders import EditPeerFolders
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import db_session
from database.models.group import GroupState, GroupModel
from database.repositories.group import GroupRepository


async def check_group(client: Client, session: AsyncSession):
    group_repo = GroupRepository(session=session)
    groups = await group_repo.get_all_by(obj_in={'state': GroupState.PENDING_CONFIRMATION})
    group_to_check = choice(groups)
    group_to_check: GroupModel

    try:
        chat = await client.get_chat(chat_id=group_to_check.username)
    except UsernameNotOccupied:
        await group_repo.update(
            id_=group_to_check.id,
            obj_in={
                'state': GroupState.INACTIVE,
            },
        )
        return

    if not chat:
        return
    if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return
    if not chat.username:
        return

    await client.join_chat(chat_id=chat.username)

    await group_repo.update(
        id_=group_to_check.id,
        obj_in={
            'state': GroupState.ACTIVE,
            'tg_group_id': chat.id,
            'username': chat.username,
            'subscribers': chat.members_count,
        },
    )


@db_session
async def checking_groups(app: Client, session: AsyncSession):
    while True:
        await check_group(client=app, session=session)
        await sleep(randint(180, 1200))

