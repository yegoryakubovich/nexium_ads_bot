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


from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import db_session
from database.repositories.user import UserRepository
from utils import States, texts
from utils.keyboards import kb_main
from utils.router import Router


router = Router(
    name=__name__,
)


@router.message(Command('start', 'restart'))
@db_session
async def start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    tg_user_id = message.from_user.id

    user_repo = UserRepository(session=session)
    user = await user_repo.get_by(obj_in={'tg_user_id': tg_user_id})
    if not user:
        await user_repo.create(
            obj_in={
                'tg_user_id':tg_user_id,
                'username': message.from_user.username,
            },
        )
        await message.reply(text=texts.register_)

    await state.set_state(state=States.MAIN)
    await message.answer(text=texts.start, reply_markup=kb_main)
