from django import forms
from .models import Project, Proposal


class ProjectForm(forms.ModelForm):
    """Form for creating/editing projects."""
    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'budget', 'deadline']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Loyiha nomi'})
        self.fields['description'].widget.attrs.update({
            'class': 'form-textarea', 'rows': 6, 'placeholder': "Loyiha haqida batafsil ma'lumot..."
        })
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['budget'].widget.attrs.update({'class': 'form-input', 'placeholder': "Byudjet (so'mda)"})
        self.fields['deadline'].widget = forms.DateInput(
            attrs={'class': 'form-input', 'type': 'date'},
            format='%Y-%m-%d'
        )


class ProposalForm(forms.ModelForm):
    """Form for submitting a proposal."""
    class Meta:
        model = Proposal
        fields = ['price', 'message', 'delivery_days']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].widget.attrs.update({'class': 'form-input', 'placeholder': "Narx (so'mda)"})
        self.fields['message'].widget.attrs.update({
            'class': 'form-textarea', 'rows': 5,
            'placeholder': "Nima uchun siz bu loyiha uchun eng yaxchi tanlovsiz..."
        })
        self.fields['delivery_days'].widget.attrs.update({
            'class': 'form-input', 'placeholder': 'Bajarish muddati (kun)'
        })
