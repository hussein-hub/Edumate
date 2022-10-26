from django.shortcuts import render

from Edumate_app.models import Teachers

# Create your views here.

def teach_home(request, pk):
    teacher_c = Teachers.objects.get(teach_id=pk)
    return render(request, 'Teacher/teacher_home.html', {'teacher_c': teacher_c})