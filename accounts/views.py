from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

# Create your views here.
# 회원 목록 페이지
def index(request):
    users = get_user_model().objects.all()

    context = {
        'users': users,
    }

    return render(request, 'accounts/index.html', context)

# 회원 가입 페이지 및 user 데이터 생성
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('accounts:detail', user.pk)
    elif request.method == 'GET':
        form = CustomUserCreationForm()

    context ={
        'form': form,
    }

    return render(request, 'accounts/signup.html', context)

# 회원 정보 상세 페이지(프로필 페이지)
def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)

    context = {
        'user': user,
    }

    return render(request, 'accounts/detail.html', context)