from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13)
    publisher = models.CharField(max_length=255)  
    cover_page_url = models.URLField(blank=True, null=True)  
    language = models.CharField(max_length=50, blank=True, null=True) 
    
    def __str__(self):
        return self.title

