from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.authtoken.models import Token

from api.models import Book


def home(request):
    token_key = ""
    user = User.objects.filter(username="admin").first()
    if user:
        token = Token.objects.filter(user=user).first()
        if token:
            token_key = token.key

    return render(request, "api/home.html", {
        "total_books": Book.objects.count(),
        "token_key": token_key,
    })
