from .models import Article
from django import forms

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('writer', )