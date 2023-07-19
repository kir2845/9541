from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .filters import NewFilter, CategoryFilter
from .forms import NewForm
from .models import New, Category, NewCategory
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail






class NewsList(ListView):

    model = New                      # Указываем модель, объекты которой мы будем выводить
    ordering = '-time_in'            # Поле, которое будет использоваться для сортировки объектов
    template_name = 'news.html'      # Указываем имя шаблона, в котором будут все инструкции о том,
                                     # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'news'     # Это имя списка, в котором будут лежать все объекты.
                                     # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    paginate_by = 10                  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        return context

class NewsCategoryList(ListView):

    model = New                      # Указываем модель, объекты которой мы будем выводить
#    ordering = '-time_in'            # Поле, которое будет использоваться для сортировки объектов
    template_name = 'news_category.html'      # Указываем имя шаблона, в котором будут все инструкции о том,
                                     # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'news_category'     # Это имя списка, в котором будут лежать все объекты.
                                     # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    paginate_by = 7                  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = New.objects.filter(category = self.category).order_by('-time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Поздравляем! Вы успешно подписались на рассылку новостей категории  '
    return render(request, 'subscribe.html', {'category': category, 'message': message})



class NewsSearchList(ListView):

    model = New                      # Указываем модель, объекты которой мы будем выводить
    ordering = '-time_in'            # Поле, которое будет использоваться для сортировки объектов
    template_name = 'news_search.html'      # Указываем имя шаблона, в котором будут все инструкции о том,
                                     # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'news_search'     # Это имя списка, в котором будут лежать все объекты.
                                     # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    paginate_by = 5                  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context



class NewDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = New
    # Используем другой шаблон — product.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'new'



class NewCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    permission_required = ('News_from_Ozersk.add_new')
    form_class = NewForm
    # модель товаров
    model = New
    # и новый шаблон, в котором используется форма.
    template_name = 'new_create.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = New.objects.filter(category = self.category).order_by('-time_in')
        return queryset

    def form_valid(self, form):
        self.object = form.save(commit = False)
        if 'news' in self.request.path:
            post_type = 'NE'
        elif 'articles' in self.request.path:
            post_type = 'AR'
        self.object.post_type = post_type
        return super().form_valid(form)



class NewEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('News_from_Ozersk.change_new')
    form_class = NewForm
    model = New
    template_name = 'new_edit.html'


# Представление удаляющее товар.
class NewDelete(DeleteView):
    model = New
    template_name = 'new_delete.html'
    success_url = reverse_lazy('new_list')

class ArtCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News_from_Ozersk.add_new')
    # Указываем нашу разработанную форму
    form_class = NewForm
    # модель товаров
    model = New
    # и новый шаблон, в котором используется форма.
    template_name = 'art_create.html'

    def form_valid(self, form):
        self.object = form.save(commit = False)
        if 'news' in self.request.path:
            post_type = 'NE'
        elif 'articles' in self.request.path:
            post_type = 'AR'
        self.object.post_type = post_type
        return super().form_valid(form)

class ArtEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('News_from_Ozersk.change_new')
    form_class = NewForm
    model = New
    template_name = 'art_edit.html'

# Представление удаляющее товар.
class ArtDelete(DeleteView):
    model = New
    template_name = 'art_delete.html'
    success_url = reverse_lazy('new_list')