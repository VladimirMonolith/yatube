from http import HTTPStatus

from django.shortcuts import render


def page_not_found(request, exception):
    """Настройка шаблона для страницы с ошибкой 404."""
    return render(request, 'core/404.html', {'path': request.path},
                  status=HTTPStatus.NOT_FOUND)


def server_error(request):
    """Настройка шаблона для страницы с ошибкой 500."""
    return render(request, 'core/500.html',
                  status=HTTPStatus.INTERNAL_SERVER_ERROR)


def permission_denied(request, exception):
    """Настройка шаблона для страницы с ошибкой 403."""
    return render(request, 'core/403.html', status=HTTPStatus.FORBIDDEN)


def csrf_failure(request, reason=''):
    """Настройка шаблона для страницы с ошибкой проверки CSRF,
    запрос отклонён"""
    return render(request, 'core/403csrf.html')
