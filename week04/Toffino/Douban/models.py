from django.db import models

# Create your models here.


class Review(models.Model):
    author = models.CharField(max_length=50, blank=True, null=True)
    content = models.TextField()
    rate = models.FloatField(blank=True, null=True)
    created_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review'