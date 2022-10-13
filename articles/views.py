from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from .models import Article

# Create your views here.
# 글 목록 페이지
def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'articles/index.html', context)

# 글 작성 페이지 및 글 데이터 생성
@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.writer = request.user
            article.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()

    context = {
        'form': form,
    }

    return render(request, 'articles/create.html', context)

# 글 상세 페이지
def detail(request, pk):
    article = Article.objects.get(pk=pk)

    context = {
        'article': article,
    }

    return render(request, 'articles/detail.html', context)

# 글 수정 페이지 및 글 데이터 수정
@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.writer:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
        context = {
            'form': form,
        }
        return render(request, 'articles/update.html', context)
    else:
        return render(request, 'accounts/no_access.html')

# 글 삭제
@login_required
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.writer:
        article.delete()
        return redirect('articles:index')
    else:
        return render(request, 'accounts/no_access.html')