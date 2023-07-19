from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewDetail, NewCreate, NewEdit, NewDelete, NewsSearchList, ArtCreate, ArtEdit, ArtDelete
from .views import NewsCategoryList, subscribe



urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('news/', NewsList.as_view(), name='new_list'),
   path('news/search/', NewsSearchList.as_view(), name='new_search'),
   path('news/<int:pk>', NewDetail.as_view(), name='new_detail'),
   path('news/create/', NewCreate.as_view(), name='new_create'),
   path('news/<int:pk>/edit/', NewEdit.as_view(), name='new_edit'),
   path('news/<int:pk>/delete/', NewDelete.as_view(), name='new_delete'),
   path('articles/create/', ArtCreate.as_view(), name='art_create'),
   path('articles/<int:pk>/edit/', ArtEdit.as_view(), name='art_edit'),
   path('articles/<int:pk>/delete/', ArtDelete.as_view(), name='art_delete'),
#   path('news/category/', NewsCategoryList.as_view(), name='new_category'),
   path('news/categories/<int:pk>', NewsCategoryList.as_view(), name='new_category'),
#   path('news/category/<int:pk>', NewsCategoryList.as_view(), name='new_category'),
   path('news/categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]