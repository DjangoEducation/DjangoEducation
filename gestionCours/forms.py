from django import forms
from .models import Course,Chapitre

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'specialites', 'niveau', 'image', 'pdf']


class ChapitreForm(forms.ModelForm):
    class Meta:
        model = Chapitre
        fields = ['title', 'description', 'categorie', 'document', 'viewChapitre']
