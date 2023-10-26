import requests
import json
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('MORALIS_API_KEY')

def request_message(request):
    data = json.loads(request.body)

    REQUEST_URL = 'https://authapi.moralis.io/challenge/request/evm'
    request_object = {
      "domain": "127.0.0.1:8000",
      "chainId": 1,
      "address": data['address'],
      "statement": "Please confirm",
      "uri": "http://127.0.0.1:8000/",
      "expirationTime": "2024-01-01T00:00:00.000Z",
      "notBefore": "2020-01-01T00:00:00.000Z",
      "timeout": 100
    }

    x = requests.post(
        REQUEST_URL,
        json=request_object,
        headers={'X-API-KEY': API_KEY})

    return JsonResponse(json.loads(x.text))


def verify_message(request):
    data = json.loads(request.body)

    REQUEST_URL = 'https://authapi.moralis.io/challenge/verify/evm'
    x = requests.post(
        REQUEST_URL,
        json=data,
        headers={'X-API-KEY': API_KEY})
    print(json.loads(x.text))
    print(x.status_code)
    if x.status_code == 201:
        # user can authenticate
        eth_address=json.loads(x.text).get('address')
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            user = User(username=eth_address)
            user.is_staff = False
            user.is_superuser = False
            user.save()
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['auth_info'] = data
                request.session['verified_data'] = json.loads(x.text)
                return JsonResponse({'user': user.username})
            else:
                return JsonResponse({'error': 'account disabled'})
    else:
        return JsonResponse(json.loads(x.text))


# Create your views here.
def index(request):
    context = {
        "title": "Homepage"
    }
    return render(request, 'users/base.html', context)


def connect(request):
    context = {
        "title" : "Login"
    }

    return render(request, 'users/login.html', context)
