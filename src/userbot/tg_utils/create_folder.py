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


from typing import Optional

from telethon import TelegramClient
from telethon.tl.functions.messages import UpdateDialogFilterRequest
from telethon.tl.types import DialogFilter


async def create_folder(userbot: TelegramClient, id_: int, include_peers: list, emoticon: Optional[str] = None):
    await userbot(
        UpdateDialogFilterRequest(
            id=id_,
            filter=DialogFilter(
                id=id_,
                title='GROUPS',
                include_peers=include_peers,
                exclude_peers=[],
                pinned_peers=[],
                emoticon=emoticon,
            ),
        ),
    )
