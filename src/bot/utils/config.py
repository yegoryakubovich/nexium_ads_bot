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


from dotenv import load_dotenv
from os import getenv


load_dotenv()


DATABASE_URL = getenv('DATABASE_URL')
REDIS_URL = getenv('REDIS_URL')
BOT_TOKEN = getenv('BOT_TOKEN')
BOT_USERNAME = getenv('BOT_USERNAME')
ADMIN_USERNAME = getenv('ADMIN_USERNAME')
ADMIN_TG_USER_ID = getenv('ADMIN_TG_USER_ID')
USER_ID = getenv('USER_ID')
USER_HASH = getenv('USER_HASH')
DEFAULT_DAILY_TASKS_LIMIT = getenv('DEFAULT_DAILY_TASKS_LIMIT')
COST = getenv('COST')
LIMIT_CHATS_IN_FOLDER_COUNT = int(getenv('LIMIT_CHATS_IN_FOLDER_COUNT'))
FOLDER_NAME = getenv('FOLDER_NAME')
