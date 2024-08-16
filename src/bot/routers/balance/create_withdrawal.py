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


from aiogram import F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import db_session
from database.repositories.user import UserRepository
from utils import texts, States
from utils.config import ADMIN_USERNAME
from utils.router import Router


router = Router(name=__name__)


@router.message(F.text == texts.bt_balance_withdrawal, States.BALANCE)
@db_session
async def create_withdrawal(message: Message, session: AsyncSession) -> None:
    tg_user_id = message.from_user.id

    user_repo = UserRepository(session=session)
    user = await user_repo.get_by(obj_in={'tg_user_id': tg_user_id})

    await message.answer(
        text=texts.balance_withdrawal.format(
            user_id=str(user.id).zfill(6),
            balance=user.balance,
            admin_username=ADMIN_USERNAME,
        ),
    )
