from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Group

@login_required
def chat_view(request, group_name):
    group, created = Group.objects.get_or_create(name=group_name)
    return render(request, 'chat/chat.html', {'group': group})

# Create your views here.
