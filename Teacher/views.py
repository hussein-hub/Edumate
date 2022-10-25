from django.shortcuts import render

# Create your views here.

def teach_home(request, pk):
    return render(request, 'Teacher/teacher_home.html')