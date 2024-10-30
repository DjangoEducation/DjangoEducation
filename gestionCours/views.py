from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CourseForm,ChapitreForm
from .models import Course,Chapitre

@login_required(login_url='signin')
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            print(f"Utilisateur assigné : {course.user}")
            course.save()
            print("Cours sauvegardé avec succès")
            return redirect('courses_list')
    else:
        form = CourseForm()
    return render(request, 'cours/add_course.html', {'form': form})


@login_required(login_url='signin')
def courses_list(request):
    #courses = Course.objects.all()
    courses = Course.objects.filter(user=request.user)
    return render(request, 'cours/courses_list.html', {'courses': courses})

# views.py
@login_required(login_url='signin')
def update_course(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'cours/update_course.html', {'form': form, 'course': course})


@login_required(login_url='signin')
def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('courses_list')
    return render(request, 'cours/delete_course.html', {'course': course})


@login_required(login_url='signin')
def courses_selectionner(request, course_id):
    cours_id = get_object_or_404(Course, id=course_id, user=request.user)  # Retrieve course for logged-in user
    chapters = Chapitre.objects.filter(cours_id=cours_id)  # Filter chapters by the selected course
    return render(request, 'chapitre/chapitre_list.html', {'course': cours_id, 'chapters': chapters})


    
@login_required(login_url='signin')
def add_chapitre(request, course_id):
    print(f"enetred     : {course_id}")
    course = get_object_or_404(Course, id=course_id, user=request.user)
    print(f"course  : {course}")
    if request.method == 'POST':
        form = ChapitreForm(request.POST, request.FILES)
        if form.is_valid():
            print(f"valid  :")
            chapitre = form.save(commit=False)  # Do not save to the database yet
            chapitre.cours = course  # Set the course for this chapter
            chapitre.save()  # Save the chapter with the course set
            return redirect('courses_selectionner', course_id=course.id)  # Redirect to the course's chapter list
    else:
        form = ChapitreForm()

    return render(request, 'chapitre/add_chapitre.html', {'form': form, 'course': course})