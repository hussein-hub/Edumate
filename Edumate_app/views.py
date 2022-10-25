from django.shortcuts import render, redirect
from .models import Students, Teachers
import string, random
from Student import views as stud_views
from Teacher import views as teach_views
# Create your views here.


def home(request):
    return render(request, 'Edumate_app/index.html')

def register(request):
    if(request.method=="POST"):
        if(request.POST.get('email')=="admin@gmail.com" and request.POST.get('password')=="admin@123"):
            return redirect('final_register')
    return render(request, 'Edumate_app/register.html')

def final_reg(request):
    if(request.method=="POST"):
        if(request.POST.get('type')=="student"):
            student=Students()
            student.name=request.POST.get('name')
            student.email=request.POST.get('email')
            student.password=str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 8)))  
            student.save()
        else:
            teacher=Teachers()
            teacher.name=request.POST.get('name')
            teacher.email=request.POST.get('email')
            teacher.password=str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 8)))
            teacher.save()
    return render(request, 'Edumate_app/final_reg.html')

def login_student(request):
    if(request.method=="POST"):
        student=None
        try:
            student=Students.objects.get(email=request.POST.get('email'))
        except:
            return render(request, 'Edumate_app/login.html')
        if(student!=None and student.password==request.POST.get('password')):
             return redirect(stud_views.stud_home, pk=student.stud_id)
    return render(request, 'Edumate_app/login.html')

def login_teacher(request):
    if(request.method=="POST"):
        teacher=None
        try:
            teacher=Teachers.objects.get(email=request.POST.get('email'))
        except:
            return render(request, 'Edumate_app/login_teacher.html')
        if(teacher!=None and teacher.password==request.POST.get('password')):
            return redirect(teach_views.teach_home, pk=teacher.teach_id)
    return render(request, 'Edumate_app/login_teacher.html')