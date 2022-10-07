
from django.shortcuts import render
import datetime

def home(request):
    'Функция с подстановкой'
    date = datetime.datetime.now().date
    name = 'Dave'
    _context = {'date' : date, 'name' : name}
    return render(request, 'home.html', _context)