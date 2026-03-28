from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Avg, Q
from accounts.models import User
from projects.models import Project, Proposal
from reviews.models import Review
from messaging.models import Message


def admin_required(view_func):
    """Decorator: only allow admin users."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin_user:
            messages.error(request, "Sizda admin huquqlari yo'q!")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def admin_dashboard(request):
    """Admin dashboard with platform statistics."""
    stats = {
        'total_users': User.objects.count(),
        'total_clients': User.objects.filter(role='client').count(),
        'total_freelancers': User.objects.filter(role='freelancer').count(),
        'total_projects': Project.objects.count(),
        'open_projects': Project.objects.filter(status='open').count(),
        'in_progress_projects': Project.objects.filter(status='in_progress').count(),
        'completed_projects': Project.objects.filter(status='completed').count(),
        'total_proposals': Proposal.objects.count(),
        'total_reviews': Review.objects.count(),
        'total_messages': Message.objects.count(),
        'avg_rating': Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0,
        'total_budget': Project.objects.aggregate(total=Sum('budget'))['total'] or 0,
    }
    recent_projects = Project.objects.select_related('client').order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]

    return render(request, 'dashboard/admin_dashboard.html', {
        'stats': stats,
        'recent_projects': recent_projects,
        'recent_users': recent_users,
    })


@login_required
@admin_required
def manage_users(request):
    """Manage all users."""
    users = User.objects.all().order_by('-date_joined')
    role_filter = request.GET.get('role', '')
    query = request.GET.get('q', '')
    if role_filter:
        users = users.filter(role=role_filter)
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    return render(request, 'dashboard/manage_users.html', {
        'users': users,
        'role_filter': role_filter,
        'query': query,
    })


@login_required
@admin_required
def delete_user(request, pk):
    """Delete a user."""
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if user == request.user:
            messages.error(request, "O'zingizni o'chira olmaysiz!")
        else:
            user.delete()
            messages.success(request, "Foydalanuvchi o'chirildi!")
    return redirect('manage_users')


@login_required
@admin_required
def manage_projects(request):
    """Manage all projects."""
    projects = Project.objects.select_related('client', 'category').all().order_by('-created_at')
    status_filter = request.GET.get('status', '')
    query = request.GET.get('q', '')
    if status_filter:
        projects = projects.filter(status=status_filter)
    if query:
        projects = projects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'dashboard/manage_projects.html', {
        'projects': projects,
        'status_filter': status_filter,
        'query': query,
    })


@login_required
@admin_required
def delete_project(request, pk):
    """Delete a project."""
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Loyiha o'chirildi!")
    return redirect('manage_projects')


@login_required
@admin_required
def toggle_user_active(request, pk):
    """Activate/deactivate a user."""
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if user == request.user:
            messages.error(request, "O'zingizni o'chira olmaysiz!")
        else:
            user.is_active = not user.is_active
            user.save()
            status = "faollashtirildi" if user.is_active else "o'chirildi"
            messages.success(request, f"Foydalanuvchi {status}!")
    return redirect('manage_users')
