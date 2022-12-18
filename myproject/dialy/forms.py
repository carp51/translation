from django import forms

class TranslationForm(forms.Form):

    sentence = forms.CharField(label='翻訳(日本語)', widget=forms.Textarea(), required=True)


class LoginForm(forms.Form):
    username = forms.CharField(label='ユーザー名', max_length=64)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
