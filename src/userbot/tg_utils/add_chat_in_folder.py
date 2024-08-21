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


from telethon import TelegramClient
from telethon.tl.functions.messages import UpdateDialogFilterRequest
from telethon.tl.types import InputPeerChannel, Chat, User, Channel, DialogFilter, InputPeerUser, InputPeerChat


async def add_entity_in_folder(
        userbot: TelegramClient,
        dialog_filter: DialogFilter,
        entity: Chat | User | Channel,
):
    dialog_entity = await userbot.get_entity(entity)

    input_peer = None
    if isinstance(entity, Channel):
        input_peer = InputPeerChannel(dialog_entity.id, dialog_entity.access_hash)
    elif isinstance(entity, User):
        input_peer = InputPeerUser(dialog_entity.id, dialog_entity.access_hash)
    elif isinstance(entity, Chat):
        input_peer = InputPeerChat(dialog_entity.id)

    dialog_filter.include_peers.append(input_peer)
    await userbot(UpdateDialogFilterRequest(dialog_filter.id, dialog_filter))
    return dialog_filter