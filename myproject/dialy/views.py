from django.shortcuts import render
import requests

def translate(request):
    form_text, down_arrow = '', ''

    # Deepl APIを使用する
    api_key = "66676f39-4ab7-4e17-be92-cd5c1aa2babd:fx"
    endpoint = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

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

    context = {
        'base_text': form_text,
        'down_arrow': down_arrow,
        'translated_text': translated_text,
    }

    # 翻訳されたテキストを表示するためにテンプレートを使用してHTMLを生成する
    return render(request, 'dialy/translate.html', context)