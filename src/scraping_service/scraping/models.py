from enum import unique
from django.db import models
from transliterate import translit
from datetime import datetime

class City(models.Model):
    'Модель города'

    name = models.CharField(max_length=50
                                , verbose_name = 'Название населенного пункта'
                                , unique = True)
    slug = models.CharField(max_length =50
                                , blank = True
                                , verbose_name = 'Код'
                                , unique = True
                                )
    class Meta:
        'Названия модели в единственном и множественном числе'
        verbose_name = 'Название населенного пункта'
        verbose_name_plural = 'Название населенных пунктов'
        db_table = "City"
        ordering  = ('id', )

    def save(self, *args, **kwargs):
        new_name  = self.name.replace(' ', '_')
        if not self.slug:
            self.slug = translit(new_name, 'ru', reversed=True)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class Language(models.Model):
    'Модель языков прогараммирования'

    name = models.CharField(max_length=50
                                , verbose_name = 'Язык программирования'
                                , unique = True)
    slug = models.CharField(max_length =50
                                , blank = True
                                , verbose_name = 'Код'
                                , unique = True
                                )
    class Meta:
        'Названия модели в единственном и множественном числе'
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'
        db_table = "Language"

    def __str__(self) -> str:
        return self.name

class Vacancy(models.Model):
    url = models.URLField(unique = True)
    title = models.CharField(max_length = 250 
                            , verbose_name = 'Вакансия'
                            )
    company = models.CharField(max_length = 250 
                            , verbose_name = 'Компания'
                                )
    description  = models.TextField(verbose_name = 'Описание')
    city = models.ForeignKey('City', on_delete = models.CASCADE)
    language = models.ForeignKey('Language', on_delete = models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        'Названия модели в единственном и множественном числе'
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        db_table = "Vacancy"

    # изменяем дандер str для отображения в всевозможных ссылках на это поле
    def __str__(self) -> str:
        return f"{self.title} в {self.company}"