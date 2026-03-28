from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    """Project category."""
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


class Project(models.Model):
    """Project posted by a client."""
    STATUS_CHOICES = (
        ('open', 'Ochiq'),
        ('in_progress', 'Jarayonda'),
        ('completed', 'Yakunlangan'),
        ('cancelled', 'Bekor qilingan'),
    )

    title = models.CharField(max_length=200, verbose_name="Loyiha nomi")
    description = models.TextField(verbose_name="Tavsif")
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='client_projects', verbose_name="Buyurtmachi"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='projects', verbose_name="Kategoriya"
    )
    budget = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Byudjet (so'm)")
    deadline = models.DateField(verbose_name="Muddat")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name="Holat")
    assigned_freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assigned_projects',
        verbose_name="Tanlangan frilanser"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    class Meta:
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def proposals_count(self):
        return self.proposals.count()

    @property
    def is_overdue(self):
        return self.deadline < timezone.now().date() and self.status == 'open'

    @property
    def days_left(self):
        delta = self.deadline - timezone.now().date()
        return max(delta.days, 0)


class Proposal(models.Model):
    """Freelancer proposal for a project."""
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('accepted', 'Qabul qilindi'),
        ('rejected', 'Rad etildi'),
    )

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,
        related_name='proposals', verbose_name="Loyiha"
    )
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='proposals', verbose_name="Frilanser"
    )
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Taklif narxi (so'm)")
    message = models.TextField(verbose_name="Xabar")
    delivery_days = models.PositiveIntegerField(default=7, verbose_name="Bajarish muddati (kun)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan sana")

    class Meta:
        verbose_name = "Taklif"
        verbose_name_plural = "Takliflar"
        ordering = ['-created_at']
        unique_together = ['project', 'freelancer']

    def __str__(self):
        return f"{self.freelancer.username} → {self.project.title}"
