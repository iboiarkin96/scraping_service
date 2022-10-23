from django.contrib import admin
from .models import *

@admin.register(City)
class City(admin.ModelAdmin):
    list_display = ("id", "name", 'slug')
    
@admin.register(Language)
class Language(admin.ModelAdmin):
    list_display = ("id", "name", 'slug')

@admin.register(Vacancy)
class Vacancy(admin.ModelAdmin):
    list_display = ('id', "url", "title", 'company', 'get_description', 'get_city_name', 'get_lang_name', )
    list_filter = ("city",)

    # выводим в поле language название города, а не его id
    def get_city_name(self, obj):
        return obj.city.name
    get_city_name.short_description = "city"

    # выводим в поле language название языка, а не его id
    def get_lang_name(self, obj):
        return obj.language.name
    get_lang_name.short_description = "language"

    # усекаем отображение в админке 
    def get_description(self, obj):
       return obj.description[:20]
    get_description.short_description = "description"


@admin.register(STG_HH_Vacancy)
class STG_HH_Vacancy(admin.ModelAdmin):
    pass


@admin.register(URL)
class URL(admin.ModelAdmin):
    list_display = ('city', 'language', 'url_data')