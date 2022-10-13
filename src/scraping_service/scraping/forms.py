from django import forms
from .models import Language, City

class FindForm(forms.Form):
    """Основная форма поиска на сайте
    """
    city = forms.ModelChoiceField(queryset= City.objects.all(),
                                    empty_label='Введите город', 
                                    to_field_name='name', 
                                    required=False,
                                    widget = forms.Select(attrs = {'class' : 'form-control'}), 
                                    label='Город'
                                   
                                    )

    Language = forms.ModelChoiceField(queryset= Language.objects.all()
                                        , empty_label='Введите специальность'
                                        , to_field_name='name'
                                        , required=False
                                        , widget = forms.Select(attrs = {'class' : 'form-control'}),
                                        label='Специальность'
                                     )