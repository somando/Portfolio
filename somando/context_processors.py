import datetime

def year(request):
    return {
        'year': datetime.date.today().year
    }

def root_url(request):
    return {
        'url': 'https://somando.jp'
    }
