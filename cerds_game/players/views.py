from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Player
import json
import requests


@csrf_exempt
def create_user(request):
    try:
        user_name = request.POST.get('user_name')
        user_id = request.POST.get('id_user')
        
        # Перевірка на наявність необхідних параметрів
        if not user_name or not user_id:
            return JsonResponse({'error': 'Необхідні параметри user_name та id_user'}, status=400)

        # Перевірка, чи вже існує користувач з таким ID
        if Player.objects.filter(user_id=user_id).exists():
            return JsonResponse({'message': 'Користувач вже існує'}, status=200)

        # Створення нового користувача
        player = Player.objects.create(name=user_name, user_id=user_id, prise=1000)
        return JsonResponse({'message': 'Користувач успішно створений'}, status=201)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def get_user(request):
    if request.method == 'GET':
        user_id = request.GET.get('id_user')
        try:
            user = Player.objects.get(user_id=user_id)
            response_data = {
                'name': user.name,
                'user_id': user.user_id,
                'prise': user.prise
            }
            return JsonResponse(response_data, status=200)
        except Player.DoesNotExist:
            return JsonResponse({'error': 'Користувача не знайдено'}, status=404)

@csrf_exempt
def add_friend_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        friend_id = request.POST.get('friend_id')
        if not user_id or not friend_id:
            return JsonResponse({'error': 'Потрібні user_id і friend_id'}, status=400)

        try:
            user = Player.objects.get(user_id=user_id)
            added = user.add_friend(friend_id)
            if added:
                return JsonResponse({'message': 'Друг доданий'}, status=200)
            return JsonResponse({'message': 'Друг вже є або це той самий користувач'}, status=200)
        except Player.DoesNotExist:
            return JsonResponse({'error': 'Користувача не знайдено'}, status=404)

@csrf_exempt
def get_friends_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('id_user')
            user = Player.objects.get(user_id=user_id)
            friends = user.friends.all().values('name', 'user_id')

            friends_list = list(friends)
            return JsonResponse({'friends': friends_list}, status=200)
        except Player.DoesNotExist:
            return JsonResponse({'error': 'Пользователь не найден'}, status=404)

@csrf_exempt
def remove_friend_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        friend_id = data.get('friend_id')
        
        if not user_id or not friend_id:
            return JsonResponse({'error': 'Потрібні user_id і friend_id'}, status=400)

        try:
            user = Player.objects.get(user_id=user_id)
            removed = user.remove_friend(friend_id)
            
            if removed:
                return JsonResponse({'message': 'Друг видалений'}, status=200)
            return JsonResponse({'message': 'Друг не знайдений у списку друзів або це той самий користувач'}, status=200)
        
        except Player.DoesNotExist:
            return JsonResponse({'error': 'Користувача не знайдено'}, status=404)


TELEGRAM_TOKEN = '7135455707:AAHFXcfiiJaJArustu4kEAnxRwty6h4VM9M'

@csrf_exempt
def send_telegram_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id = 938231668
        players = data.get('numberPlayer')
        room = data.get('roomId')
        bet = data.get('bet')
        game = data.get('game')
        text = 'є таблетка од голови'
        url_link = f'https://65a0-194-39-227-125.ngrok-free.app/{game}/{players}/{room}/{bet}'
        inline_keyboard = {
            "inline_keyboard": [
                [{"text": "Перейти на сайт","web_app": {"url": url_link}}]
            ]
        }

        url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
        payload = {'chat_id': id, 'text': text, 'reply_markup': json.dumps(inline_keyboard)}
        r = requests.post(url, data=payload)

        return JsonResponse({'status': 'ok', 'telegram_response': r.json()})
    return JsonResponse({'error': 'Invalid request'}, status=400)
