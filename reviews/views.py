from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from projects.models import Project


@login_required
def create_review(request, project_pk):
    """Create a review for a freelancer after project completion."""
    project = get_object_or_404(
        Project, pk=project_pk, client=request.user, status='completed'
    )
    if not project.assigned_freelancer:
        messages.error(request, "Bu loyihada frilanser yo'q!")
        return redirect('project_detail', pk=project_pk)

    if Review.objects.filter(reviewer=request.user, project=project).exists():
        messages.warning(request, "Siz allaqachon sharh qoldirgansiz!")
        return redirect('project_detail', pk=project_pk)

    if request.method == 'POST':
        rating = request.POST.get('rating', 5)
        comment = request.POST.get('comment', '')
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                rating = 5
        except (ValueError, TypeError):
            rating = 5

        Review.objects.create(
            reviewer=request.user,
            freelancer=project.assigned_freelancer,
            project=project,
            rating=rating,
            comment=comment
        )
        messages.success(request, "Sharh muvaffaqiyatli qo'shildi!")
        return redirect('profile', username=project.assigned_freelancer.username)

    return render(request, 'reviews/create.html', {'project': project})
