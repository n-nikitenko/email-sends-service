from django.shortcuts import render

from blog.services import get_last_three_articles
from email_sends.services import get_mailings_count, get_active_mailings_count, get_clients_count


def home(request):
    """endpoint для главной страницы"""

    return render(request, 'email_sends/index.html', context={
        "articles": get_last_three_articles(),
        "mailings_count": get_mailings_count(),
        "active_mailings_count": get_active_mailings_count(),
        "clients_count": get_clients_count()
    })
