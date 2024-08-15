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


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton as Kb

from utils import texts


class Rkm(ReplyKeyboardMarkup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, resize_keyboard=True)


main = Rkm(
    keyboard=[
        [Kb(text=texts.bt_tasks_start)],
        [Kb(text=texts.bt_balance)],
    ],
)
