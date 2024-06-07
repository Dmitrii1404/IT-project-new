# import uuid
# import base64
# import json
# import requests
#
#
# def get_token(auth_token, scope='GIGACHAT_API_PERS'):
#     rq_uid = str(uuid.uuid4())
#
#     url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
#
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'Accept': 'application/json',
#         'RqUID': rq_uid,
#         'Authorization': f'Basic {auth_token}'
#     }
#
#     payload = {
#         'scope': scope
#     }
#
#     try:
#         response = requests.post(url, headers=headers, data=payload, verify=False)
#         return response
#     except requests.RequestException as e:
#         print(f"Ошибка: {str(e)}")
#         return -1
#
#
# def get_chat_completion(auth_token, user_message):
#     url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
#
#     payload = json.dumps({
#         "model": "GigaChat",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": user_message
#             }
#         ],
#         "temperature": 1,  # Температура генерации
#         "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов
#         "n": 1,  # Количество возвращаемых ответов
#         "stream": False,  # Потоковая ли передача ответов
#         "max_tokens": 512,  # Максимальное количество токенов в ответе
#         "repetition_penalty": 1,
#         "update_interval": 0
#     })
#
#     # Заголовки запроса
#     headers = {
#         'Content-Type': 'application/json',  # Тип содержимого - JSON
#         'Accept': 'application/json',  # Принимаем ответ в формате JSON
#         'Authorization': f'Bearer {auth_token}'  # Токен авторизации
#     }
#
#     # Выполнение POST-запроса и возвращение ответа
#     try:
#         response = requests.request("POST", url, headers=headers, data=payload, verify=False)
#         return response
#     except requests.RequestException as e:
#         # Обработка исключения в случае ошибки запроса
#         print(f"Произошла ошибка: {str(e)}")
#         return -1
#
#
# def send_request(message: str):
#     auth = 'OWIwODRlYzAtMzMzNS00YmE0LTg0M2ItMzgzMmMxMDY3NDY0OjM5NmZlZTNhLThmY2EtNDE2Yy1iNjM0LWNiYjY0OWFiNGU0Ng=='
#     client_id = '9b084ec0-3335-4ba4-843b-3832c1067464'
#     scope = 'GIGACHAT_API_PERS'
#     secret = '396fee3a-8fca-416c-b634-cbb649ab4e46'
#     credentials = f"{client_id}:{secret}"
#     encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
#     response = get_token(encoded_credentials)
#     if response != 1:
#         giga_token = response.json()['access_token']
#         answer = get_chat_completion(giga_token, message)
#         answer.json()
#         return answer.json()['choices'][0]['message']['content']
#     return None
