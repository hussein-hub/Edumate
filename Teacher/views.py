from django.shortcuts import render
import string, random

from Edumate_app.models import Teachers
from Student.models import ClassStudents
from .models import ClassTeachers

# Create your views here.

def teach_home(request, pk):
    teacher_c = Teachers.objects.get(teach_id=pk)
    class_data = ClassTeachers.objects.filter(teach_id=pk)
    if(request.method=="POST"):
        class_room=ClassTeachers()
        class_room.teach_id=pk
        class_room.class_name=request.POST.get('name')
        class_room.class_code=str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 6)))
        class_room.save() 
        return render(request, 'Teacher/teacher_home.html', {'class_data': class_data})
    return render(request, 'Teacher/teacher_home.html', {'class_data': class_data})