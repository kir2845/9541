import django_filters
from django_filters import FilterSet, ChoiceFilter
from .models import New
from django.forms import SelectDateWidget
import datetime


class NewFilter(django_filters.FilterSet):

   class Meta:                    # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
       model = New
       fields = {
#           'category': ['exact'],# В fields мы описываем по каким полям модели будет производиться фильтрация.
           'name': ['icontains'],  # поиск по названию
           'time_in': ['date__gte'],
           'author': ['exact'],
           }


class CategoryFilter(django_filters.FilterSet):

   class Meta:                    # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
       model = New
       fields = {
           'category': ['exact'],# В fields мы описываем по каким полям модели будет производиться фильтрация.
           }

