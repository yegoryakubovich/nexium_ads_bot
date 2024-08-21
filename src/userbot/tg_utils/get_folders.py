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
from telethon.tl.functions.messages import GetDialogFiltersRequest
from telethon.tl.types import InputPeerChannel
from telethon.tl.types.messages import DialogFilters


async def get_folders(userbot: TelegramClient, only_name: str = None):
    request = await userbot(GetDialogFiltersRequest())
    request: DialogFilters
    dialog_filters = request.filters

    last_id = 1
    folders = []
    for dialog_filter in dialog_filters:
        folder = dialog_filter.to_dict()
        if folder['_'] != 'DialogFilter':
            continue
        if only_name:
            if not dialog_filter.title == only_name:
                continue

        id_ = dialog_filter.id

        if last_id < id_:
            last_id = id_
        folders.append(
            {
                'id': id_,
                'title': dialog_filter.title,
                'include_chats': [
                    chat.channel_id
                    for chat in dialog_filter.include_peers
                    if isinstance(chat, InputPeerChannel)
                ],
                'include_chats_count': len(dialog_filter.include_peers),
                'dialog_filter': dialog_filter,
            }
        )

    return {
        'folders': folders,
        'last_id': last_id,
    }
