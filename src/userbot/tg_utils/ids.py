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


from telethon.tl.types import Chat, Channel, User


def entity_to_tg_id(entity: Chat | User | Channel):
    id_ = entity.id

    if isinstance(entity, Chat):
        return int(f'-{id_}')
    elif isinstance(entity, Channel):
        return int(f'-100{id_}')
    else: # User
        return id_


def is_supergroup(entity: Chat | User | Channel):
    if isinstance(entity, Channel):
        return entity.broadcast or entity.megagroup
    else:
        return False