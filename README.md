# 장고 실습 11 - Django Auth를 활용한 회원 정보 수정 및 탈퇴 서비스 개발

## 과정

- [목표](#목표)
- [준비 사항](#준비-사항)
- [요구 사항](#요구-사항)
- [실습 결과 완성본](#실습-결과-완성본)

## 목표

- Django Auth를 활용한 회원관리(회원가입 / 회원 조회 / 회원 정보 수정 / 회원 탈퇴 / 로그인 / 로그아웃)가 가능한 서비스를 개발합니다.

## 준비 사항
### 1) 개발 관련 준비 사항

> 가상 환경 생성 및 실행

```bash
$ python -m venv venv
```

```bash
$ source venv/Scripts/activate
```

> 패키지 설치
1. Django 
  
   ```bash
   $ pip install django==3.2.13
   ```

2. Code Formatter black 
  
   ```bash
   $ pip install black
   ```

3. django-bootstrap5
  
   ```bash
   $ pip install django-bootstrap5
   ```

   - 패키지 설치 후, settings.py의 INSTALLED_APPS에 `'django_bootstrap5',` 추가

> 설치된 패키지 목록 기록

```bash
$ pip freeze > requirements.txt
```

> 장고 프로젝트 생성 & 앱 생성 및 앱 등록

```bash
$ django-admin startproject pjt .
```

```bash
$ python manage.py startapp accounts
```

> SECRET KEY 분리 설정

- secrets.json
  
  ```json
  {
      "SECRET_KEY": "new secret key"
  }
  ```

- settings.py 수정
  
  ```python
  import os, json
  from django.core.exceptions import ImproperlyConfigured
  
  secret_file = os.path.join(BASE_DIR, 'secrets.json') # secrets.json 파일 위치를 명시
  
  with open(secret_file) as f:
      secrets = json.loads(f.read())
  
  def get_secret(setting, secrets=secrets):
      try:
          return secrets[setting]
      except KeyError:
          error_msg = "Set the {} environment variable".format(setting)
          raise ImproperlyConfigured(error_msg)
  
  SECRET_KEY = get_secret("SECRET_KEY")
  ```

- .gitignore에 추가
  
  ```
  secrets.json
  ```

> .gitignore 설정

```
.venv
```

### 2) 협업 관련 준비 사항
- [GitHub Flow](https://ujuc.github.io/2015/12/16/git-flow-github-flow-gitlab-flow/)에 따라 다른 사람들과 협업하여 개발하는 연습 필요
- VScode에 [`Git Graph`](https://jhyeok.com/vscode-git-graph/) extension 설치

> git 생성

```bash
$ git init
```

> GigHub 원격 저장소 생성, (collaborator 설정), 로컬 저장소를 원격 저장소와 연결

```bash
$  git remote add origin {원격저장소URL}
```

> master 브랜치에서 새 브랜치 생성

```bash
$ git branch home
```

> master 브랜치에서 방금 생성한 새 브랜치로 이동

```bash
$ git switch home
```

> 개발 작업 진행

```bash
$ git add .
```

```bash
$ git commit -m '커밋메시지'
```

```bash
$ git push origin home
```

> GitHub에서 새 브런치를 Pull Request

> 관리자가 GitHub에서 PR된 브런치를 Merge

> 로컬 저장소에서 master 브랜치로 이동

```bash
$ git switch master
```

> master 브랜치에서 pull 당기기

```bash
$ git pull origin master
```

> 로컬 저장소에서 이미 병합한 브런치 삭제

```bash
$ git branch -d home
```

> 다시 새로운 브랜치 만들어서 이동 후 작업 반복

```bash
$ git branch accounts
```

## 요구 사항

> 모델 Model - `M`

- 모델 이름 : User
- Django `AbstractUser 모델` 상속

> 폼 Form

**회원가입**

- Django 내장 회원가입 폼 `UserCreationForm`을 상속받아서 `CustomUserCreationForm` 작성 & 활용
- 해당 폼은 아래 필드만 출력합니다.
  - username
  - email
  - password1
  - password2

**회원 정보 수정**

1. 비밀번호 제외한 기본 정보 수정
  
   - Django 내장 폼 `UserChangeForm`을 상속 받아서 `CustomUserChangeForm` 작성 & 활용
   - 해당 폼은 아래 필드만 출력합니다.
     - first_name
     - last_name
     - email

2. 비밀번호 수정

   - Django 내장 비밀번호 변경 폼 `PasswordChangeForm` 활용

**로그인**

- Django 내장 로그인 폼 `AuthenticationForm` 활용

> 기능 View - `V`

**회원가입**

1. 회원가입 Create
  
   - `POST` `http://127.0.0.1:8000/accounts/signup/`
   - `CustomUserCreationForm`을 활용해서 회원가입 구현

2. 회원 목록 조회 Read(index)

   - `GET` `http://127.0.0.1:8000/accounts/`

3. 회원 정보 조회 Read(detail)

   - `GET` `http://127.0.0.1:8000/accounts/<int:user_pk>/`

4. 회원 정보(비밀번호를 제외한 기본 정보) 수정 Update(update)

   - `POST` `http://127.0.0.1:8000/accounts/update/`
   - `CustomUserChangeForm`를 활용해서 회원 정보 수정 구현

5. 회원 정보(비밀번호) 수정 Update(change_password)
   
   - `POST` `http://127.0.0.1:8000/accounts/password/`
   - `PasswordChangeForm`를 활용해서 회원 정보 수정 구현

6. 회원 탈퇴 Delete

   - `POST` `http://127.0.0.1:8000/accounts/delete/`

**로그인**

1. 로그인

   - `POST` `http://127.0.0.1:8000/accounts/login/`
   - `AuthenticationForm`를 활용해서 로그인 구현

2. 로그아웃

   - `POST` `http://127.0.0.1:8000/accounts/logout/`

> 화면 Template - `T`

1. 네비게이션바, Bootstrap `<nav>`

   - 로그인 상태에 따라 다른 화면 출력
  
   1. 로그인 상태인 경우
      - 로그인한 사용자의 username 출력
      - username 클릭 시 해당 회원 조회 페이지(프로필 페이지)로 이동
      - 로그아웃 버튼
   2. 비 로그인 상태인 경우
      - 로그인 페이지 이동 버튼
      - 회원가입 페이지 이동 버튼
   
2. 회원가입 페이지

   - `GET` `http://127.0.0.1:8000/accounts/signup/`
   - 회원가입 폼

3. 로그인 페이지
   
   - `GET` `http://127.0.0.1:8000/accounts/login/`
   - 로그인 폼
   - 회원가입 페이지 이동 버튼
  
4. 회원 목록 페이지

   - `GET` `http://127.0.0.1:8000/accounts/`
   - 회원 목록 테이블
   - 회원 아이디를 클릭하면 해당 회원 조회 페이지(프로필 페이지)로 이동

5. 회원 조회 페이지(프로필 페이지)
   
   - `GET` `http://127.0.0.1:8000/accounts/<user_pk>/`
   - 회원 정보 출력
  
6. 회원 정보 수정 페이지
   
   - `GET` `http://127.0.0.1:8000/accounts/update/`


## 실습 결과 완성본

> 회원관리 서비스

![]()