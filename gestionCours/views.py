from io import BytesIO
import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CourseForm,ChapitreForm
from .models import Course,Chapitre ,Summarize
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile


import google.generativeai as genai
import PyPDF2
from fpdf import FPDF

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
    user = request.user
    if user.role == 'Enseignant' :
        courses = Course.objects.filter(user=request.user)
    else:
        courses = Course.objects.all()
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
    user = request.user
    if user.role == 'Enseignant' :
        cours_id = get_object_or_404(Course, id=course_id, user=request.user)
        chapters = Chapitre.objects.filter(cours_id=cours_id)  
    else:
        cours_id = get_object_or_404(Course, id=course_id)
        chapters = Chapitre.objects.filter(cours_id=cours_id,viewChapitre=1) 
    return render(request, 'chapitre/chapitre_list.html', {'course': cours_id, 'chapters': chapters, 'user': user})


    
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


@csrf_exempt  # Consider using decorators to ensure security
def toggle_view_chapitre(request):
    if request.method == "POST":
        chapter_id = request.POST.get('chapter_id')
        viewed = request.POST.get('viewed') == 'true'  # Convert to boolean
        
        # Assuming you have a Chapter model
        chapter = Chapitre.objects.get(id=chapter_id)
        chapter.viewChapitre = viewed
        chapter.save()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)




os.environ["GEMINI_API_KEY"] = "AIzaSyCrf5J9HRqb5D5hJMU1Yz7Z5JvvgjTZ38U"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def summarize_pdf(request, chapter_id):
    chapter = Chapitre.objects.get(id=chapter_id)
    pdf_path = chapter.document.path

    # Open the PDF and extract text
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        full_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page_text = pdf_reader.pages[page_num].extract_text()
            full_text += page_text + "\n\n"

    # Generate the summary
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(f"Resumer cela en précissant les informations importantes: {full_text}")
    pdf_summary = response.text

    # Create a new PDF for the summary
    # Define the storage path
    storage_path = "storage"
    os.makedirs(storage_path, exist_ok=True)  # Create storage folder if it doesn't exist

    # Define the PDF file path
    sanitized_title = "".join([c if c.isalnum() else "_" for c in chapter.title])
    pdf_buffer = f"{storage_path}/{sanitized_title}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, pdf_summary)
    pdf.output(pdf_buffer)  # Save PDF content to buffer


    modelDesc = genai.GenerativeModel(model_name="gemini-1.5-flash")
    description = modelDesc.generate_content(f"fait une court description pour cette texte :\n {full_text}").text
    # Create a Summarize object
    summary = Summarize(
        title=f"Summary of {chapter.title}",
        description=description,
        cours=chapter.cours,
        categorie=chapter.categorie
    )
    # Save PDF file in Summarize instance
    summary.pdf.save(f"{chapter.title}_summary.pdf", ContentFile(pdf_buffer))
    summary.save()

    organized_summary = "<p>" + pdf_summary.replace("\n", "</p><p>") + "</p>"
    return JsonResponse({"summary": organized_summary})
