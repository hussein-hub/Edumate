from django.shortcuts import render, redirect
from .models import Students, Teachers
import string, random
from Student import views as stud_views
from Teacher import views as teach_views
from django.contrib import messages
import re
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
        messages.error(request, 'Registration successful')
        return redirect('final_register')
    return render(request, 'Edumate_app/final_reg.html')

def login_student(request):
    if(request.method=="POST"):
        student=None
        try:
            student=Students.objects.get(email=request.POST.get('email'))
        except:
            messages.error(request, 'Invalid credentials')
            return redirect('login_student')
        if(student!=None and student.password==request.POST.get('password')):
            request.session['sname']=student.name
            if(student.is_change==0):
                return redirect('change_pass', pk=student.stud_id, pk2="S")    
            return redirect(stud_views.stud_home, pk=student.stud_id)
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login_student')
    return render(request, 'Edumate_app/login.html')

def login_teacher(request):
    if(request.method=="POST"):
        teacher=None
        try:
            teacher=Teachers.objects.get(email=request.POST.get('email'))
        except:
            messages.error(request, 'Invalid credentials')
            return render(request, 'Edumate_app/login_teacher.html')
        if(teacher!=None and teacher.password==request.POST.get('password')):
            request.session['tname']=teacher.name
            if(teacher.is_change==0):
                return redirect('change_pass', pk=teacher.teach_id, pk2="T")    
            return redirect(teach_views.teach_home, pk=teacher.teach_id)
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login_teacher')
    return render(request, 'Edumate_app/login_teacher.html')


def change_pass(request, pk, pk2):
    if request.method=="POST":
        if request.POST.get('password')!=request.POST.get('conpassword'):
            messages.error(request, 'Both passwords should match')
            return redirect('change_pass', pk=pk, pk2=pk2)
        if not re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', request.POST['password']):
            messages.error(request, "Please enter a valid password")
            return redirect('change_pass', pk=pk, pk2=pk2)
        user=None
        if pk2=="S":
            user=Students.objects.get(stud_id=pk)
        elif pk2=="T":
            user=Teachers.objects.get(teach_id=pk)
        user.password=request.POST.get('password')
        user.is_change=1
        user.save()
        if(pk2=="S"):
            return redirect(stud_views.stud_home, pk=pk)
        return redirect(teach_views.teach_home, pk=pk)
    return render(request, 'Edumate_app/change_password.html', {'pk': pk, 'pk2': pk2})

