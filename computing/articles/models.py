from ckeditor.fields import RichTextField
from django.db import models


class Author(models.Model):
    nickname = models.CharField(max_length=50, verbose_name="Никнейм")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, verbose_name="Фамилия")
    last_name = models.CharField(max_length=50, verbose_name="Отчество")
    photo = models.ImageField(verbose_name="Фото", upload_to="authors_photos")

    def get_articles(self):
        return Article.objects.filter(author=self.nickname)

    def __str__(self):
        return self.nickname

    class Meta:
        pass


class Article(models.Model):
    headline = models.CharField(max_length=100, verbose_name="Заголовок")
    short_description = models.CharField(max_length=300, verbose_name="Краткое описание")
    content = RichTextField(verbose_name="Содержание")
    photo = models.ImageField(verbose_name="Фото", upload_to="article_photos")
    slug = models.SlugField(verbose_name="URL")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор", related_name="author")
    date_create = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, blank=True, null=True, editable=False)

    def __str__(self):
        return self.headline

    class Meta:
        pass
