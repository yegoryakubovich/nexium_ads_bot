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


from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils import texts, States
from utils.go_back import go_back
from utils.keyboards import kb_main
from utils.router import Router


router = Router(name=__name__)


@router.message(States.BALANCE)
async def back(message: Message, state: FSMContext) -> None:
    await go_back(message=message, state=state, state_to_set=States.MAIN, text=texts.back, reply_markup=kb_main)
