from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User


class Author1(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
       return self.name.title()



class Category(models.Model):                            # Категория, к которой будет привязываться новость
    name = models.CharField(max_length=100, unique=True) # названия категорий тоже не должны повторяться
    subscribers =  models.ManyToManyField(User, related_name ='categories')

    def __str__(self):
        return self.name.title()


class New(models.Model):         # Новости для нашей витрины
    ARTICLE = 'AR'
    NEWS = 'NE'
    TYPE = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    post_type = models.CharField(
        max_length=2,
        choices=TYPE,
        default=NEWS,
    )
    name = models.CharField(
        max_length=64,
        unique=True,              # названия новостей не должны повторяться
    )
    time_in = models.DateTimeField(auto_now_add=True)
    textPost = models.TextField()

    author = models.ForeignKey(Author1, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='NewCategory')

    def __str__(self):
        return f'"{self.name.title()}" - {self.textPost}'

    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.id)])

    def preview(self):
        text = self.textPost[:124] + "..."
        return text


class NewCategory(models.Model):
    new = models.ForeignKey(New, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
