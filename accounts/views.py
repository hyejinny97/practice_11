from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

# Create your views here.
# 회원 목록 페이지
@login_required
def index(request):
    if request.user.is_superuser:
        users = get_user_model().objects.all()
        context = {
            'users': users,
        }
        return render(request, 'accounts/index.html', context)
    else:
        return render(request, 'accounts/no_access.html')


# 회원 가입 페이지 및 user 데이터 생성
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('accounts:detail', user.pk)
    elif request.method == 'GET':
        form = CustomUserCreationForm()

    context ={
        'form': form,
    }

    return render(request, 'accounts/signup.html', context)

# 회원 정보 상세 페이지(프로필 페이지)
def detail(request, pk):
    if request.user.pk == pk:
        user = get_user_model().objects.get(pk=pk)
        context = {
            'user': user,
        }
        return render(request, 'accounts/detail.html', context)
    else:
        return render(request, 'accounts/no_access.html')


# 회원 기본정보 수정 페이지 및 user 데이터 수정 (비밀번호 제외 기본 정보)
@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:detail', request.user.pk)
    elif request.method == 'GET':
        form = CustomUserChangeForm(instance=request.user)
    
    context = {
        'form': form,
    }

    return render(request, 'accounts/update.html', context)

# 회원 비밀번호 수정 페이지 및 user 데이터 수정 (비밀번호)
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return redirect('accounts:detail', request.user.pk)
    elif request.method == 'GET':
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
    }

    return render(request, 'accounts/password.html', context)

# 회원 탈퇴
@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('home:index')

# 로그인 기능
def login(request):
    if request.user.is_authenticated:
        return redirect('home:index')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect(request.GET.get('next') or 'home:index')
        elif request.method == 'GET':
            form = AuthenticationForm()

        context = {
            'form': form,
        }

        return render(request, 'accounts/login.html', context)

# 로그아웃 기능
def logout(request):
    auth_logout(request)
    return redirect('home:index')
