from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import User
from reviews.models import Review


def register_view(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri!")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """User logout."""
    logout(request)
    messages.success(request, "Tizimdan chiqdingiz!")
    return redirect('home')


@login_required
def profile_view(request, username):
    """View user profile."""
    user = get_object_or_404(User, username=username)
    reviews = Review.objects.filter(freelancer=user).select_related('reviewer', 'project')[:10]
    context = {
        'profile_user': user,
        'reviews': reviews,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    """Edit own profile."""
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi!")
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})


def freelancers_list(request):
    """Browse freelancers."""
    freelancers = User.objects.filter(role='freelancer')
    query = request.GET.get('q', '')
    skill = request.GET.get('skill', '')
    if query:
        freelancers = freelancers.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(skills__icontains=query)
        )
    if skill:
        freelancers = freelancers.filter(skills__icontains=skill)
    return render(request, 'accounts/freelancers.html', {
        'freelancers': freelancers,
        'query': query,
        'skill': skill,
    })
