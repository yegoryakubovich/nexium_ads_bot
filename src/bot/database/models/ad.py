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


from sqlalchemy import Column, Integer, String

from database.models.base import BaseModel


class AdModel(BaseModel):
    __tablename__ = 'ads'
    id = Column(Integer, primary_key=True, index=True)
    text_1 = Column(String(1024))
    text_2 = Column(String(1024))
    text_3 = Column(String(1024))
    image_1 = Column(String(16))
    image_2 = Column(String(16))
    image_3 = Column(String(16))
    button_1_text = Column(String(32))
    button_1_url = Column(String(32))
    button_2_text = Column(String(32))
    button_2_url = Column(String(32))
    button_3_text = Column(String(32))
    button_3_url = Column(String(32))
