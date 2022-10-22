from django.db import models
import jsonfield
from transliterate import translit
from django.utils import timezone

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


class STG_HH_Vacancy(models.Model):
    # vacancy_id = models.IntegerField()
    # premium = models.BooleanField()
    # name = models.TextField()
    # has_test = models.BooleanField()
    # response_letter_required = models.BooleanField()
    # published_at = models.DateTimeField()
    # created_at = models.DateTimeField()
    # archived = models.BooleanField()
    # alternate_url = models.URLField()
    # area_id = models.IntegerField()
    # area_name = models.TextField()
    # salary_from = models.FloatField()
    # salary_to = models.FloatField()
    # salary_currency = models.TextField()
    # salary_gross = models.BooleanField()
    # type_id = models.IntegerField()
    # type_name = models.TextField()
    # employer_id = models.IntegerField()
    # employer_name = models.TextField()
    # employer_alternate_url = models.URLField()
    # employer_logo_urls_original = models.URLField()
    # employer_vacancies_url = models.URLField()
    # employer_trusted = models.BooleanField()
    # snippet_requirement = models.TextField()
    # snippet_responsibility = models.TextField()
    # schedule_id = models.IntegerField()
    # schedule_name = models.TextField()
    # address_city = models.TextField()
    # address_street = models.TextField()
    # address_building = models.TextField()
    # address_lat = models.TextField()
    # address_lng = models.FloatField()
    # address_raw = models.FloatField()
    # address_metro_station_name = models.TextField()
    # address_metro_line_name = models.TextField()
    # address_metro_lat = models.FloatField()
    # address_metro_lng = models.FloatField()
    vacancy_id = models.TextField(null=True)
    premium = models.TextField(null=True)
    name = models.TextField(null=True)
    has_test = models.TextField()
    response_letter_required = models.TextField(null=True)
    published_at = models.TextField(null=True)
    created_at = models.TextField(null=True)
    archived = models.TextField(null=True)
    alternate_url = models.TextField(null=True)
    area_id = models.TextField(null=True)
    area_name = models.TextField(null=True)
    salary_from = models.TextField(null=True)
    salary_to = models.TextField(null=True)
    salary_currency = models.TextField(null=True)
    salary_gross = models.TextField(null=True)
    type_id = models.TextField(null=True)
    type_name = models.TextField(null=True)
    employer_id = models.TextField(null=True)
    employer_name = models.TextField(null=True)
    employer_alternate_url = models.TextField(null=True)
    employer_logo_urls_original = models.TextField(null=True)
    employer_vacancies_url = models.TextField(null=True)
    employer_trusted = models.TextField(null=True)
    snippet_requirement = models.TextField(null=True)
    snippet_responsibility = models.TextField(null=True)
    schedule_id = models.TextField(null=True)
    schedule_name = models.TextField(null=True)
    address_city = models.TextField(null=True)
    address_street = models.TextField(null=True)
    address_building = models.TextField(null=True)
    address_lat = models.TextField(null=True)
    address_lng = models.TextField(null=True)
    address_raw = models.TextField(null=True)
    address_metro_station_name = models.TextField(null=True)
    address_metro_line_name = models.TextField(null=True)
    address_metro_lat = models.TextField(null=True)
    address_metro_lng = models.TextField(null=True)
    created     = models.DateTimeField(editable=False, default=timezone.now)
    modified    = models.DateTimeField(default=timezone.now)

    class Meta:
        'Названия модели в единственном и множественном числе'
        verbose_name = 'Вакансии с сайта hh.ru'
        verbose_name_plural = 'Вакансии с сайта hh.ru'
        db_table = "STG_Vacancy_hh_ru"
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(STG_HH_Vacancy, self).save(*args, **kwargs)
    
    # изменяем дандер str для отображения в всевозможных ссылках на это поле
    def __str__(self) -> str:
        return f"{self.name} ({self.vacancy_id}) c hh.ru"


class Error(models.Model):
    """Model definition for MODELNAME."""

    date = models.DateField(default=timezone.now)
    error = jsonfield.JSONField()

    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = 'Ошибка'
        verbose_name_plural = 'Ошибки'

    def __str__(self):
        pass