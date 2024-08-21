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


from sqlalchemy.ext.asyncio import AsyncSession
from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel

from database.repositories.group import GroupRepository
from tg_utils.add_chat_in_folder import add_entity_in_folder
from tg_utils.create_folder import create_folder
from tg_utils.get_folders import get_folders
from tg_utils.ids import is_supergroup, entity_to_tg_id
from utils.config import LIMIT_CHATS_IN_FOLDER_COUNT, FOLDER_NAME


async def update_folders(userbot: TelegramClient, session: AsyncSession):
    folders_req = await get_folders(userbot=userbot, only_name=FOLDER_NAME)
    folders = folders_req['folders']
    folders_last_id = folders_req['last_id']
    current_folder = 0
    include_chats_ids = []

    for folder in folders:
        include_chats_ids += folder['include_chats']

        if folder['include_chats_count'] < LIMIT_CHATS_IN_FOLDER_COUNT:
            current_folder = folder

    group_repo = GroupRepository(session=session)

    async for dialog in userbot.iter_dialogs(archived=False):
        entity = dialog.entity
        if not is_supergroup(entity=entity):
            continue

        tg_id = entity_to_tg_id(entity=entity)

        group = await group_repo.get_by(obj_in={'tg_id': tg_id})
        if not group:
            continue

        if entity.id in include_chats_ids:
            await userbot.edit_folder(entity=entity, folder=1)
            continue

        input_peer = InputPeerChannel(channel_id=entity.id, access_hash=entity.access_hash)

        async def create_folder_():
            await create_folder(
                userbot=userbot,
                id_=folders_last_id + 1,
                include_peers=[input_peer],
                emoticon='💬',
            )
            await userbot.edit_folder(entity=entity, folder=1)
            await update_folders(userbot=userbot, session=session)

        if current_folder == 0:
            await create_folder_()
            return

        # FIXME userbot.edit_folder
        dialog_filter = await add_entity_in_folder(
            userbot=userbot,
            dialog_filter=current_folder['dialog_filter'],
            entity=entity,
        )
        await userbot.edit_folder(entity=entity, folder=1)

        if len(dialog_filter.include_peers) >= LIMIT_CHATS_IN_FOLDER_COUNT:
            await create_folder_()
            return
