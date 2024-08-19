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

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String
from sqlalchemy.orm import relationship

from database.models.base import BaseModel


class TaskState(Enum):
    IN_PROGRESS = 'IN_PROGRESS'
    PENDING_CONFIRMATION = 'PENDING_CONFIRMATION'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    SKIPPED = 'SKIPPED'


class TaskModel(BaseModel):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String(64), default=TaskState.IN_PROGRESS)

    ad_id = Column(Integer, ForeignKey('ads.id'))
    ad = relationship(argument='AdModel', lazy='selectin')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(argument='UserModel', lazy='selectin')
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship(argument='GroupModel', lazy='selectin')
    cost = Column(Integer)

    text = Column(String(1024))
    image = Column(String(16))
    have_keyboard = Column(Boolean)
    message_url = Column(String(128))

    datetime = Column(DateTime)
    expiration_datetime = Column(DateTime)
    user_confirmed_datetime = Column(DateTime, nullable=True, default=None)
    auto_confirmed_datetime = Column(DateTime, nullable=True, default=None)
    auto_confirmed_10m_datetime = Column(DateTime, nullable=True, default=None)
    auto_confirmed_30m_datetime = Column(DateTime, nullable=True, default=None)
    auto_confirmed_1h_datetime = Column(DateTime, nullable=True, default=None)
