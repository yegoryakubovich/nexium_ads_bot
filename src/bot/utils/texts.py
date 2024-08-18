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


from json import load

from pydantic import BaseModel, Field


class Texts(BaseModel):
    register_: str = Field(alias='register')
    start: str

    bt_back: str
    back: str

    bt_tasks_start: str
    bt_balance: str
    bt_referral: str
    bt_bug: str

    bt_task_mark_as_complete: str
    task_mark_as_complete: str
    task_mark_as_complete_error: str
    bt_task_skip: str
    task_skipped: str
    task_skipped_error: str
    bt_task_have_problems: str
    task_have_problems: str
    tasks_start_limit: str
    task_1: str
    task_2: str
    bt_task_group: str
    bt_task_message: str

    balance: str
    bt_balance_withdrawal: str
    balance_withdrawal: str

    referral: str

    bug: str


with open('texts.json', 'r', encoding='utf-8') as file:
    data = load(file)


texts = Texts(**data)
