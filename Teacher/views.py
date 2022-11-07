from django.shortcuts import render
import string, random
from django.http import FileResponse, Http404

from Edumate_app.models import Students, Teachers
from Student.models import ClassStudents, SubmittedAssignments
from .models import ClassTeachers, Assignments

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
        return render(request, 'Teacher/teacher_home.html', {'class_data': class_data, 'teacher': teacher_c})
    return render(request, 'Teacher/teacher_home.html', {'class_data': class_data, 'teacher': teacher_c})

def classroom(request, pk, pk2):
    context={'pk': pk, 'pk2': pk}
    if(request.method=="POST"):
        assignment=Assignments()
        assignment.assignment_name=request.POST.get('name')
        assignment.assignment_description=request.POST.get('description')
        assignment.class_code=pk2
        assignment.max_marks=request.POST.get('marks')
        assignment.save()
    assign=Assignments.objects.filter(class_code=pk2)
    return render(request, 'Teacher/classroom.html', {'assign': assign, 'pk': pk, 'pk2': pk2})

def assignmentsub(request, pk, pk2, pk3):
    submitted=SubmittedAssignments.objects.filter(assignment_id=pk3)
    for i in submitted:
        print(i.assign_file.url.split('/'))
    return render(request, 'Teacher/show_assignments.html', {'submit': submitted, 'pk': pk, 'pk2': pk2 ,'pk3': pk3})

def assignmentgrade(request, pk, pk2, pk3,pk4):
    submitted=SubmittedAssignments.objects.get(assignment_id=pk3,stud_id = pk4)
    stud = Students.objects.get(stud_id = pk4)
    print(submitted.assign_file.url)
    file_url = "http://127.0.0.1:8000"+submitted.assign_file.url
    
    return render(request, 'Teacher/grade_assignments.html', {'student_name':stud.name,'file':file_url,'submit': submitted, 'pk': pk, 'pk2': pk2})
