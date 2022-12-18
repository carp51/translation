from django.shortcuts import render, redirect
import requests
from dialy.models import dialylog
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


def translate(request):
    form_text, down_arrow = '', ''

    # Deepl APIを使用する
    api_key = "66676f39-4ab7-4e17-be92-cd5c1aa2babd:fx"
    endpoint = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    user_data = dialylog.objects.all()

    data = {
                "auth_key": api_key,
                "text": form_text,
                "source_lang": 'EN',
                "target_lang": 'JA',  
            }

    if request.method == "POST":
        # フォームから送信された文を取得する
        form_text = request.POST['text']
        #dataのtextをアップデートする
        data["text"] = form_text

        #押されたボタンで翻訳する言語を変更する
        if "E_to_J" in request.POST:
            data["source_lang"] = 'EN'
            data["target_lang"] = 'JA'
        elif "J_to_E"  in request.POST:
            data["source_lang"] = 'JA'
            data["target_lang"] = 'EN'

        down_arrow = "↓"
    
    
    response = requests.post(endpoint, headers=headers, data=data)
    result = response.json()

    # 翻訳されたテキストを取得する
    translated_text = result['translations'][0]['text']

    user = request.user

    if user.is_authenticated:
        if form_text != '':
            dialylog.objects.create(author=user, source_text=form_text, tranlated_text=translated_text)
        #モデルのデータを取得
        user_data = dialylog.objects.filter(author=user).order_by('-id')

    context = {
        'base_text': form_text,
        'down_arrow': down_arrow,
        'translated_text': translated_text,
        'user_data': user_data,
    }

    # 翻訳されたテキストを表示するためにテンプレートを使用してHTMLを生成する
    return render(request, 'dialy/translate.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('translate')
        else:
            context = {'error_message': 'ログインに失敗しました'}
            return render(request, 'registration/login.html', context)
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('translate')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('registration/login')
    else:
        form = UserCreationForm()
    return render(request, 'dialy/signup.html', {'form': form})


def save_value(request):
    if request.method == 'POST':
        value = request.POST['value']
        user = request.user
        dialylog.objects.create(user=user, value=value)
        return render(request, 'success.html')
    else:
        return render(request, 'form.html')