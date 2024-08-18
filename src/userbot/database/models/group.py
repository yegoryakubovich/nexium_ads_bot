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


from enum import Enum

from sqlalchemy import Column, Integer, String, BigInteger, Boolean, DateTime

from database.models.base import BaseModel


class GroupStateEnum(Enum):
    PENDING_CONFIRMATION = 'WAITING_FOR_CHECK'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE' # ЕСЛИ НЕ ПОДПИСАН НА НЕЕ9


class GroupModel(BaseModel):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String(64), default=GroupStateEnum.PENDING_CONFIRMATION)

    chat_id = Column(BigInteger, unique=True)
    username = Column(String(256))
    subscribers = Column(Integer, default=0)
    have_capcha = Column(Boolean, default=False)
    last_check = Column(DateTime, default=None, nullable=True)
