from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # Use the 'reverse' function to dynamically find the URL for viewing this recipe's details
        return reverse('recipe-detail', kwargs={'recipe_id': self.id})