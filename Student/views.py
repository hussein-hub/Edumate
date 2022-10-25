from django.shortcuts import render

# Create your views here.

def stud_home(request, pk):
    return render(request, 'Student/student_home.html')
