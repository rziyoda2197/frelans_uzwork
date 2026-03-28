from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from projects.models import Project, Category
from accounts.models import User


def home_view(request):
    """Landing page."""
    featured_projects = Project.objects.filter(status='open').select_related('client', 'category')[:6]
    categories = Category.objects.all()
    freelancers_count = User.objects.filter(role='freelancer').count()
    clients_count = User.objects.filter(role='client').count()
    projects_count = Project.objects.count()
    completed_count = Project.objects.filter(status='completed').count()
    top_freelancers = User.objects.filter(role='freelancer')[:4]

    context = {
        'featured_projects': featured_projects,
        'categories': categories,
        'freelancers_count': freelancers_count,
        'clients_count': clients_count,
        'projects_count': projects_count,
        'completed_count': completed_count,
        'top_freelancers': top_freelancers,
    }
    return render(request, 'home.html', context)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('projects/', include('projects.urls')),
    path('messages/', include('messaging.urls')),
    path('reviews/', include('reviews.urls')),
    path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
