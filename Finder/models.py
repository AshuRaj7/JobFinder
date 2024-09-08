from django.db import models

# Create your models here.

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    responsibilities = models.TextField()
    requirements = models.TextField()
    qualification = models.TextField()
    benefits = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)
    applylink = models.URLField()
    
    def __str__(self):
        return self.title
