import uuid
import base64
import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from giga_token import auth, client_id, secret


def get_token(auth_token, scope="GIGACHAT_API_PERS"):
    rq_uid = str(uuid.uuid4())

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": rq_uid,
        "Authorization": f"Basic {auth_token}",
    }

    payload = {"scope": scope}

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1


def get_chat_completion(auth_token, user_message):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps(
        {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": user_message}],
            "temperature": 1,
            "top_p": 0.1,
            "n": 1,
            "stream": False,
            "max_tokens": 512,
            "repetition_penalty": 1,
            "update_interval": 0,
        }
    )

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {auth_token}",
    }

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Произошла ошибка: {str(e)}")
        return -1


def send_request(message: str):
    scope = "GIGACHAT_API_PERS"
    credentials = f"{client_id}:{secret}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    response = get_token(encoded_credentials)
    if response != 1:
        giga_token = response.json()["access_token"]
        answer = get_chat_completion(giga_token, message)
        return answer.json()["choices"][0]["message"]["content"]
    return None


def chat(request):
    return render(request, "chat/chat.html")


def get_response(request):
    if request.method == "POST":
        message = request.POST.get("message")
        response = send_request(message)
        return JsonResponse({"response": response})
    return JsonResponse({"response": "Invalid request method"})
