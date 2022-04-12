from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """Функция-фильтр полей формы."""
    return field.as_widget(attrs={'class': css})
