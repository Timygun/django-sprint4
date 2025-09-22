from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    template_name = 'pages/about.html'


class Rules(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """Кастомная 404."""
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """Кастомная 500."""
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=''):
    """Кастомная 403 CSRF."""
    return render(request, 'pages/403_csrf.html', status=403)
