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


from asyncio import run, create_task, gather

from telethon import events

from tasks.checking_groups import checking_groups
from tasks.new_message_handler import new_message
from tasks.task_1 import task_1
from utils.userbot import userbot


TASKS = [
    task_1,
    checking_groups,
]


async def main():
    userbot.add_event_handler(callback=new_message, event=events.NewMessage)

    await userbot.start()

    tasks = [create_task(task(userbot=userbot)) for task in TASKS]
    await gather(*tasks)

    await userbot.run_until_disconnected()


run(main())
