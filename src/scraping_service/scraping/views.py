from .forms import FindForm
from django.shortcuts import render
from .models import Vacancy

def home_view(request):
    #  данныепараметры пришли из формы на сайте 
    city = request.GET.get('city')
    language = request.GET.get('language')
    
    qs = []
    _filter = {}
    form = FindForm()

    if city or language:
        if city:
            _filter['city__name'] = city
        if language:
            _filter['language__name'] = language
        qs = Vacancy.objects.filter(**_filter)
    _context = dict(object_list = qs, form = form)
    return render(request, 'scraping/home.html', context = _context)