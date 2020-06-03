**Проект API Yatube**  :mortar_board:

API oснован на [DJANGO REST framework](https://www.django-rest-framework.org/)


Получения поста, списка постов.

В API Yatube используется модель Post, которая наследует от *Model* из *django.db* со следующими полями:
```
from django.db import models


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
```
Никто не ограничивает Вас в использовании полей, Вы можете добавлять любые, не забывайте делать миграции.

В Serializers мы должны указать каждое поле, которое будет выводиться.
```
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post
 ```
 Пример вывода:
 ```
 [

    {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2020-06-03T11:48:57Z"
    }

]
``` 
Во views класс PostViewSet наследуется от модуля viewsets.ModelViewSet, что значительно облегчает написание кода.
В данном классе необходимо переопределить метод *def get_queryset()*
```
    def get_queryset(self):
        queryset = Post.objects.all()
```
В котором мы получаем парамтр запроса *'group'* для дальнейшей фильтрации queryset
```
        group = self.request.query_params.get('group')
        if group is not None:
            queryset = queryset.filter(group_id=group)
        return queryset
```
Так как мы указывали поле автора только для чтения, мы обязаны при создании или частичном изменении поста сохранять имя автора. Для этого переопределяем метод *perfom_create()*:
```
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

