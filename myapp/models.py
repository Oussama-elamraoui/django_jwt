from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()  # e.g., 30 days

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = (
        ('beta_player', 'Beta Player'),
        ('company_user', 'Company User'),
        ('growth_plan_subscriber', 'Growth Plan Subscriber'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='beta_player')
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Custom related name to avoid clashes
        blank=True,
        help_text=('The groups this user blgs  A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  
        blank=True,
        help_text='Specific permissions for this user',
        verbose_name='user permissions',
    )

# Image model
class Image(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_file = models.ImageField(upload_to='images/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
