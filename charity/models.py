from django.db import models
from django.urls import reverse
from django.conf import settings


class Article(models.Model):
    img = models.ImageField()
    tags = models.ManyToManyField('Tag')
    categories = models.ManyToManyField('Category', related_name='articles_amount')
    title = models.CharField(max_length=40)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('article', kwargs={"article_slug": self.slug})

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={"tag_slug": self.slug})


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def post_count(self):
        return self.articles_amount.count()

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_slug": self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Volunteer(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=30)
    cv = models.FileField(upload_to='media/cv', blank=True)
    comment = models.TextField(blank=True, max_length=1000)

