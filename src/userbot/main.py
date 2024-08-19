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


import asyncio

from pyrogram import Client
from pyrogram.handlers import MessageHandler

from tasks.new_message_handler import new_message
from utils.config import USER_ID, USER_HASH


TASKS = []
HANDLERS = [MessageHandler(new_message)]


async def task1(app):
    async for dialog in app.get_dialogs():
        await asyncio.sleep(2)


async def main():
    async with Client(
        name='userbot',
        api_id=USER_ID,
        api_hash=USER_HASH,
        device_model='Nexium Ads User Bot',
        app_version='v 1.0',
    ) as app:
        task_1 = asyncio.create_task(task1(app))

        app.add_handler(MessageHandler(new_message))

        await asyncio.gather(task_1)


asyncio.run(main())