import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model

User = get_user_model()
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# ── Pages ────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('resumes:dashboard')

    error = None
    if request.method == 'POST':
        email    = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('resumes:dashboard')
        error = 'E-mail ou senha inválidos.'

    return render(request, 'login.html', {'error': error})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('resumes:dashboard')

    error = None
    if request.method == 'POST':
        name     = request.POST.get('name', '').strip()
        email    = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm  = request.POST.get('confirm', '')

        if not name or not email or not password:
            error = 'Preencha todos os campos.'
        elif len(password) < 6:
            error = 'A senha deve ter pelo menos 6 caracteres.'
        elif password != confirm:
            error = 'As senhas não coincidem.'
        elif User.objects.filter(email=email).exists():
            error = 'Este e-mail já está cadastrado.'
        else:
            username = email.split('@')[0]
            base, counter = username, 1
            while User.objects.filter(username=username).exists():
                username = f'{base}{counter}'; counter += 1

            first_name, *rest = name.split(' ', 1)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=rest[0] if rest else '',
            )
            login(request, user)
            return redirect('resumes:dashboard')

    return render(request, 'register.html', {'error': error})


@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('resumes:index')


# ── API ──────────────────────────────────────────────────────────────────────

@require_POST
def api_login(request):
    body = json.loads(request.body)
    email = body.get('email', '').strip().lower()
    password = body.get('password', '')

    user = authenticate(request, email=email, password=password)
    if user is None:
        return JsonResponse({'error': 'Credenciais inválidas.'}, status=401)

    login(request, user)
    return JsonResponse({'id': user.id, 'name': user.get_full_name() or user.username, 'email': user.email})


@require_POST
def api_register(request):
    body = json.loads(request.body)
    name = body.get('name', '').strip()
    email = body.get('email', '').strip().lower()
    password = body.get('password', '')

    if not name or not email or not password:
        return JsonResponse({'error': 'Preencha todos os campos.'}, status=400)

    if len(password) < 6:
        return JsonResponse({'error': 'A senha deve ter pelo menos 6 caracteres.'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Este e-mail já está cadastrado.'}, status=400)

    username = email.split('@')[0]
    base = username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f'{base}{counter}'
        counter += 1

    first_name, *rest = name.split(' ', 1)
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=rest[0] if rest else '',
    )
    login(request, user)
    return JsonResponse({'id': user.id, 'name': user.get_full_name(), 'email': user.email}, status=201)


@require_POST
def api_logout(request):
    logout(request)
    return JsonResponse({'ok': True})


def api_me(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Não autenticado.'}, status=401)
    u = request.user
    return JsonResponse({'id': u.id, 'name': u.get_full_name() or u.username, 'email': u.email})
