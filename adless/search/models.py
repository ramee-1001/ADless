from django.db import models

# Create your models here.
class Keyword(models.Model):
    word = models.CharField(max_length=50,primary_key= True)

class blogList(models.Model):
    title = models.CharField(max_length=50,primary_key= True)
    blogurl = models.URLField("site URL")#여기까지 수정함
    text = models.TextField(null=True)

    def __str__(self):
        return self.title