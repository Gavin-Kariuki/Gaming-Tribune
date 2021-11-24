from django.db import models
import datetime as dt



# Create your models here.
class Editor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length = 10,blank = True) # when passing blank = true this allows us to add NULL values to our database.

    def __str__(self):
        return self.first_name

    def save_editor(self):
        self.save()

    class Meta:
        ordering = ['first_name']

class tags(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def delete_tags(self): # test for deleting a tags
        self.delete()

    

class Article(models.Model):
    title = models.CharField(max_length=60)
    post = models.TextField()
    editor = models.ForeignKey('Editor', on_delete=models.DO_NOTHING)#from django 2.0 on_delete is required
    tags = models.ManyToManyField(tags)
    pub_date = models.DateTimeField(auto_now=True)
    article_image = models.ImageField(upload_to = 'articles/')# you have to add a null value otherwise django will ask you to so as to make the migration


    @classmethod
    def todays_news(cls):
        today = dt.date.today()
        news = cls.objects.filter(pub_date__date = today)
        return news

    @classmethod
    def days_news(cls,date):
        news = cls.objects.filter(pub_date__date = date)
        return news

    @classmethod
    def search_by_title(cls,search_term):
        news = cls.objects.filter(title__icontains=search_term)
        return news


