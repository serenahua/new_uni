from datetime import datetime

from django.template.defaultfilters import register

@register.filter(name='times')
def times(number) -> list:
    try:
        return range(number)
    except:
        return []

@register.filter
def date_with_day(date) -> str:
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    if type(date) == datetime:
        _d = date
    elif type(date) == str:
        _d = datetime.strptime(date, '%Y-%m-%d')
    else:
        return ''

    _w = _d.weekday()
    date_string = _d.strftime('%Y-%m-%d')
    result = "%s %s" % (date_string, weekdays[_w])

    return result