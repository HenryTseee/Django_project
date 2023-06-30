from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.timezone import now

class LogMessage(models.Model):
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"
    
    
 ##below is for forum   

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)    
    image = models.ImageField(upload_to="images",default="default/user.png")
       
class Post(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post_id = models.AutoField
    post_content = models.CharField(max_length=5000)
    timestamp= models.DateTimeField(default=now)
    image = models.ImageField(upload_to="images",default="")
    
class Replie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    reply_id = models.AutoField
    reply_content = models.CharField(max_length=5000) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default='')
    timestamp= models.DateTimeField(default=now)
    image = models.ImageField(upload_to="images",default="")
