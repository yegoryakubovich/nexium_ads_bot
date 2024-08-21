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

from sqlalchemy.ext.asyncio import AsyncSession
from telethon import TelegramClient
from telethon.errors import InviteRequestSentError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputChannel

from database.database import db_session
from database.models.group import GroupState, GroupModel
from database.repositories.group import GroupRepository
from tasks.update_folders import update_folders
from tg_utils.ids import entity_to_tg_id


async def check_group(userbot: TelegramClient, session: AsyncSession):
    group_repo = GroupRepository(session=session)
    groups = await group_repo.get_all_by(obj_in={'state': GroupState.PENDING_CONFIRMATION})
    group_to_check = choice(groups)
    group_to_check: GroupModel

    try:
        group = await userbot.get_entity(entity=group_to_check.username)
    except ValueError:
        await group_repo.update(
            id_=group_to_check.id,
            obj_in={
                'state': GroupState.INACTIVE,
            },
        )
        return

    participants  = await userbot.get_participants(group)
    me = await userbot.get_me()
    if not me in participants:
        try:
            await userbot(
                JoinChannelRequest(
                    channel=InputChannel(
                        channel_id=group.id,
                        access_hash=group.access_hash,
                    ),
                ),
            )
        except InviteRequestSentError:
            return

    subscribers = 0

    tg_id = entity_to_tg_id(entity=group)
    await group_repo.update(
        id_=group_to_check.id,
        obj_in={
            'state': GroupState.ACTIVE,
            'tg_id': tg_id,
            'username': group.username,
            'subscribers': subscribers,
        },
    )
    await update_folders(userbot=userbot, session=session)


@db_session
async def checking_groups(userbot: TelegramClient, session: AsyncSession):
    while True:
        await check_group(userbot=userbot, session=session)
        await sleep(randint(180, 320))

