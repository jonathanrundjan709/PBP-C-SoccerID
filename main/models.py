import uuid
from django.db import models
from django.core.validators import MinValueValidator


class News(models.Model):
    CATEGORY_CHOICES = [
        ('transfer', 'Transfer'),
        ('update', 'Update'),
        ('exclusive', 'Exclusive'),
        ('match', 'Match'),
        ('rumor', 'Rumor'),
        ('analysis', 'Analysis'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    thumbnail = models.URLField(blank=True, null=True)
    news_views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    @property
    def is_news_hot(self):
        return self.news_views > 20
        
    def increment_views(self):
        self.news_views += 1
        self.save()

class Product(models.Model):
    name = models.CharField(max_length=255) 
    price = models.IntegerField(validators=[MinValueValidator(0)])  
    description = models.TextField()  
    thumbnail = models.URLField()  
    category = models.CharField(max_length=100)  
    is_featured = models.BooleanField(default=False)  

    def __str__(self):
        return self.name
