from django.db import models

# Create your models here.
class User(models.Model):
    iduser = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    age = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'user'