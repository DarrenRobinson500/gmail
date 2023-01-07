from django.shortcuts import render
# from .forms import *

def home(request):
    context = {}
    return render(request, 'home.html', context)

# Create your views here.
