import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Resume


# ── Pages ────────────────────────────────────────────────────────────────────

def index_view(request):
    return render(request, 'index.html')


@login_required
def dashboard_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip() or 'Sem título'
        resume = Resume.objects.create(user=request.user, name=name)
        return redirect('resumes:builder_edit', pk=resume.pk)

    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'resumes': resumes})


@login_required
@require_http_methods(['POST'])
def delete_resume_view(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    resume.delete()
    return redirect('resumes:dashboard')


@login_required
def builder_view(request, pk=None):
    context = {}
    if pk:
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        context['resume'] = resume
    return render(request, 'builder.html', context)


@login_required
def preview_view(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    tpl = request.GET.get('template', resume.template)
    if tpl not in ('executive', 'minimal'):
        tpl = 'executive'
    return render(request, 'preview.html', {'resume': resume, 'active_template': tpl})


# ── API ──────────────────────────────────────────────────────────────────────

@login_required
@require_http_methods(['GET', 'POST'])
def api_resume_list(request):
    if request.method == 'GET':
        resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')
        data = [r.to_dict() for r in resumes]
        return JsonResponse(data, safe=False)

    body = json.loads(request.body)
    resume = Resume.objects.create(
        user=request.user,
        name=body.get('name', 'Sem título'),
        template=body.get('template', 'executive'),
        data=body.get('data', {}),
    )
    return JsonResponse(resume.to_dict(), status=201)


@login_required
@require_http_methods(['GET', 'PUT', 'DELETE'])
def api_resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)

    if request.method == 'GET':
        return JsonResponse(resume.to_dict())

    if request.method == 'PUT':
        body = json.loads(request.body)
        resume.name = body.get('name', resume.name)
        resume.template = body.get('template', resume.template)
        if 'data' in body:
            resume.data = body['data']
        resume.save()
        return JsonResponse(resume.to_dict())

    resume.delete()
    return JsonResponse({'ok': True})
