import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from read_json import get_json


config = get_json('config\\config')
__credentials = get_json('config\\credentials')

id_group = __credentials.get('group').get('id_group')

# Сессия от имени администратора
__login = __credentials.get('user').get('login')
__password = __credentials.get('user').get('password')
vk_sessionUser = vk_api.VkApi(__login, __password)
vk_sessionUser.auth()

# Сессия от имени сообщества
vk_sessionGroup = vk_api.VkApi(token=__credentials.get('group').get('token'))
upload = vk_api.VkUpload(vk_sessionGroup)
# session_api = vk_session.get_api()
longpoll = VkBotLongPoll(vk_sessionGroup, group_id=__credentials.get('group').get('id_group'))
