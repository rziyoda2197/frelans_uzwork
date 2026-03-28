from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg


class User(AbstractUser):
    """Custom user model with role support."""
    ROLE_CHOICES = (
        ('client', 'Buyurtmachi'),
        ('freelancer', 'Frilanser'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client', verbose_name="Rol")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon raqam")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Profil rasmi")
    bio = models.TextField(blank=True, verbose_name="O'zi haqida")
    skills = models.CharField(max_length=500, blank=True, verbose_name="Ko'nikmalar",
                              help_text="Vergul bilan ajrating: masalan, Python, Django, JavaScript")
    location = models.CharField(max_length=100, blank=True, verbose_name="Joylashuv")
    portfolio_url = models.URLField(blank=True, verbose_name="Portfolio havolasi")
    date_joined_display = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatdan o'tgan sana")

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def average_rating(self):
        """Get average rating from reviews."""
        from reviews.models import Review
        avg = Review.objects.filter(freelancer=self).aggregate(avg=Avg('rating'))['avg']
        return round(avg, 1) if avg else 0

    @property
    def skills_list(self):
        """Return skills as a list."""
        if self.skills:
            return [s.strip() for s in self.skills.split(',') if s.strip()]
        return []

    @property
    def completed_projects_count(self):
        """Count completed projects."""
        if self.role == 'freelancer':
            return self.assigned_projects.filter(status='completed').count()
        return self.client_projects.filter(status='completed').count()

    @property
    def is_freelancer(self):
        return self.role == 'freelancer'

    @property
    def is_client(self):
        return self.role == 'client'

    @property
    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser
