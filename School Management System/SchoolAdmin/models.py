from django.db import models
import os

# Create your models here.
class users(models.Model):
    user_role = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100)
    user_name = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)
    user_image = models.FileField(upload_to="profile/",default="user_default.jpg")
    user_status = models.IntegerField(default=1)

    def delete(self, *args, **kwargs):
        # Delete the image file from the file system
        if self.user_image:
            if os.path.isfile(self.user_image.path):
                os.remove(self.user_image.path)
        super().delete(*args, **kwargs)

    def delete_old_image(self):
        if self.pk:
            old_instance = users.objects.get(pk=self.pk)
            if old_instance.user_image:
                if os.path.isfile(old_instance.user_image.path):
                    os.remove(old_instance.user_image.path)

    def save(self, *args, **kwargs):
        self.delete_old_image()  # Delete old image before saving new one
        super().save(*args, **kwargs)

    def save1(self, *args, **kwargs):
        super().save(*args, **kwargs)



class branch(models.Model):
    user_id = models.ForeignKey(users,on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=100)
    branch_address = models.CharField(max_length=100)

