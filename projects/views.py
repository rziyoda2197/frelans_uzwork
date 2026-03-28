from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Project, Proposal, Category
from .forms import ProjectForm, ProposalForm


def project_list(request):
    """Browse all open projects with filtering."""
    projects = Project.objects.filter(status='open').select_related('client', 'category')
    categories = Category.objects.all()

    # Filters
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    min_budget = request.GET.get('min_budget', '')
    max_budget = request.GET.get('max_budget', '')

    if query:
        projects = projects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    if category_slug:
        projects = projects.filter(category__slug=category_slug)
    if min_budget:
        projects = projects.filter(budget__gte=min_budget)
    if max_budget:
        projects = projects.filter(budget__lte=max_budget)

    context = {
        'projects': projects,
        'categories': categories,
        'query': query,
        'category_slug': category_slug,
        'min_budget': min_budget,
        'max_budget': max_budget,
    }
    return render(request, 'projects/list.html', context)


def project_detail(request, pk):
    """View project details and proposals."""
    project = get_object_or_404(Project.objects.select_related('client', 'assigned_freelancer', 'category'), pk=pk)
    proposals = project.proposals.select_related('freelancer').all()
    user_has_proposed = False
    if request.user.is_authenticated and request.user.is_freelancer:
        user_has_proposed = proposals.filter(freelancer=request.user).exists()

    proposal_form = ProposalForm() if (
        request.user.is_authenticated and
        request.user.is_freelancer and
        not user_has_proposed and
        project.status == 'open'
    ) else None

    context = {
        'project': project,
        'proposals': proposals,
        'user_has_proposed': user_has_proposed,
        'proposal_form': proposal_form,
    }
    return render(request, 'projects/detail.html', context)


@login_required
def project_create(request):
    """Create a new project (clients only)."""
    if not request.user.is_client:
        messages.error(request, "Faqat buyurtmachilar loyiha yaratishi mumkin!")
        return redirect('project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.save()
            messages.success(request, "Loyiha muvaffaqiyatli yaratildi!")
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/create.html', {'form': form})


@login_required
def project_edit(request, pk):
    """Edit a project (owner only)."""
    project = get_object_or_404(Project, pk=pk, client=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Loyiha yangilandi!")
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/create.html', {'form': form, 'editing': True})


@login_required
def project_delete(request, pk):
    """Delete a project (owner only)."""
    project = get_object_or_404(Project, pk=pk, client=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Loyiha o'chirildi!")
        return redirect('project_list')
    return render(request, 'projects/delete_confirm.html', {'project': project})


@login_required
def proposal_create(request, pk):
    """Submit a proposal (freelancers only)."""
    project = get_object_or_404(Project, pk=pk, status='open')
    if not request.user.is_freelancer:
        messages.error(request, "Faqat frilanserlar taklif yuborishi mumkin!")
        return redirect('project_detail', pk=pk)

    if Proposal.objects.filter(project=project, freelancer=request.user).exists():
        messages.warning(request, "Siz allaqachon taklif yuborgansiz!")
        return redirect('project_detail', pk=pk)

    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.project = project
            proposal.freelancer = request.user
            proposal.save()
            messages.success(request, "Taklifingiz muvaffaqiyatli yuborildi!")
            return redirect('project_detail', pk=pk)
    return redirect('project_detail', pk=pk)


@login_required
def proposal_accept(request, pk):
    """Accept a proposal (project owner only)."""
    proposal = get_object_or_404(
        Proposal.objects.select_related('project'),
        pk=pk, project__client=request.user
    )
    proposal.status = 'accepted'
    proposal.save()
    # Update project
    project = proposal.project
    project.status = 'in_progress'
    project.assigned_freelancer = proposal.freelancer
    project.save()
    # Reject other proposals
    project.proposals.exclude(pk=pk).update(status='rejected')
    messages.success(request, f"{proposal.freelancer.get_full_name()} tanlandi!")
    return redirect('project_detail', pk=project.pk)


@login_required
def proposal_reject(request, pk):
    """Reject a proposal."""
    proposal = get_object_or_404(
        Proposal.objects.select_related('project'),
        pk=pk, project__client=request.user
    )
    proposal.status = 'rejected'
    proposal.save()
    messages.success(request, "Taklif rad etildi!")
    return redirect('project_detail', pk=proposal.project.pk)


@login_required
def project_complete(request, pk):
    """Mark project as completed."""
    project = get_object_or_404(Project, pk=pk, client=request.user, status='in_progress')
    project.status = 'completed'
    project.save()
    messages.success(request, "Loyiha yakunlandi!")
    return redirect('project_detail', pk=pk)


@login_required
def my_projects(request):
    """View user's projects (client: created, freelancer: assigned)."""
    if request.user.is_client:
        projects = Project.objects.filter(client=request.user)
    else:
        projects = Project.objects.filter(assigned_freelancer=request.user)
    return render(request, 'projects/my_projects.html', {'projects': projects})
