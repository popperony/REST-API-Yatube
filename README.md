**Проект API Yatube**  :mortar_board:

API oснован на [DJANGO REST framework](https://www.django-rest-framework.org/)

________________________________________________________________________________________________________________________________

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
 Пример запроса:
 ```
 {

    "text": "string"

}
 ```
 
 
 Пример ответа:
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

________________________________________________________________________________________________________________________________

Комментарии к постам.

В данном проекте через API с помощью дополнительной библиотеки *drf-nested-routers* к каждому посту можно оставлять комментарии.
Пример urls.py:
```
router = DefaultRouter()
router.register('posts', PostsViewSet, basename='posts')
comments_router = routers.NestedSimpleRouter(router, r'posts', lookup='posts')
comments_router.register(r'comments', CommentViewSet, basename='comments')
```
Создаем serializers используя *ModelSerializer* с нужными нам полями комментария:
```
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment
```
где автор будет только для чтения.
Не забываем, что каждый сериалайзер работает от модели:
```
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)
```
Для получения списка комментариев под постом:
```
GET /posts/{post_id}/comments/
```

Ответ:
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

Для корректной работы Comments от ModelViewSet необходимо переопределить методы 
Чтобы получать комментарии от определенных постов:
```
    def get_queryset(self):
        queryset = Comment.objects.all()
        posts_pk = self.kwargs['posts_pk']
        if posts_pk is not None:
            queryset = queryset.filter(post_id=posts_pk)
        return queryset
```
Сохраняем автора комментария:
```
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

Создаем комментарий:
```
POST /posts/{post_id}/comments/
```
```
{
        "text": "string",

    }
```
Ответ:
```
{

    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2020-06-03T14:38:46Z"

}
```

________________________________________________________________________________________________________________________________
