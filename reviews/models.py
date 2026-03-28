from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """Review left by client for freelancer after project completion."""
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='given_reviews', verbose_name="Baholovchi"
    )
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='received_reviews', verbose_name="Frilanser"
    )
    project = models.ForeignKey(
        'projects.Project', on_delete=models.CASCADE,
        related_name='reviews', verbose_name="Loyiha"
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Baho"
    )
    comment = models.TextField(verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sana")

    class Meta:
        verbose_name = "Sharh"
        verbose_name_plural = "Sharhlar"
        unique_together = ['reviewer', 'project']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer.username} → {self.freelancer.username}: {self.rating}★"
