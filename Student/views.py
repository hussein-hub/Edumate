from django.http import QueryDict
from django.shortcuts import render
from Edumate_app.models import Teachers

from Student.models import ClassStudents
from Teacher.models import ClassTeachers

# Create your views here.

def stud_home(request, pk):
    allClasses = ClassStudents.objects.filter(stud_id=pk)
    data = []
    for k in allClasses:
        classNames = ClassTeachers.objects.filter(class_code=k.class_code)
        teacherName = Teachers.objects.filter(teach_id=classNames[0].teach_id)
        for i in classNames:
            for j in teacherName:
                if i.teach_id == j.teach_id:
                    data.append([i.class_code, i.class_name, j.name])
    
    if(request.method=="POST"):
        class_room=ClassStudents()
        class_room.stud_id=pk
        class_room.class_code=request.POST.get('code')
        class_code_var = request.POST.get('code')
        class_room.save() 
        return render(request, 'Student/student_home.html', {'data': data})
    
    print(data)
    return render(request, 'Student/student_home.html', {"data": data})
