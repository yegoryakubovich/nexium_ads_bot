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


from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from database.models.base import BaseModel


class TaskModel(BaseModel):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)

    ad_id = Column(Integer, ForeignKey('ads.id'))
    ad = relationship(argument='AdModel', lazy='selectin')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(argument='UserModel', lazy='selectin')
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship(argument='GroupModel', lazy='selectin')

    text = Column(Integer)
    image = Column(Integer)
    button = Column(Boolean)

    datetime = Column(DateTime)
    datetime_user_confirmed = Column(DateTime, nullable=True, default=None)
    datetime_auto_confirmed = Column(DateTime, nullable=True, default=None)
    datetime_auto_confirmed_10m = Column(DateTime, nullable=True, default=None)
    datetime_auto_confirmed_30m = Column(DateTime, nullable=True, default=None)
    datetime_auto_confirmed_1h = Column(DateTime, nullable=True, default=None)
