from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class trans_data(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField(max_length=15)
    date = models.DateTimeField(default=timezone.now)
    des1 = models.CharField(max_length=100)
    des2 = models.CharField(max_length=150)
    tr_amount = models.FloatField(max_length=15)
    in_out = models.CharField(max_length=10)

    def __str__(self):
        return str(self.owner)

class balance_data(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_amount = models.FloatField(max_length=15, default=0)

    def __str__(self):
        return str(self.user)

class key_pair1(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    public_key = models.IntegerField(default=0)
    private_key = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

class key_pair2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    public_key = models.IntegerField(default=0)
    private_key = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

class notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    subject = models.CharField(max_length=150)
    description = models.TextField()
    amount = models.FloatField(max_length=15, default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)