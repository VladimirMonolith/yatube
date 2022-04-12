import datetime as dt


def year(request):
    """Функция для отображения текущего года."""
    year = dt.datetime.now().year
    return {'year': year}
