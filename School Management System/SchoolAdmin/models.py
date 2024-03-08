from django.db import models

# Create your models here.
class users(models.Model):
    user_role = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100)
    user_name = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)
    user_image = models.FileField(upload_to="profile/",default="default_img.jpg")
    user_status = models.IntegerField(default=1)

class branch(models.Model):
    user_id = models.ForeignKey(users,on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=100)
    branch_address = models.CharField(max_length=100)

