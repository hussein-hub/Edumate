from django.http import QueryDict
from django.shortcuts import render
from Edumate_app.models import Teachers

from Student.models import ClassStudents, SubmittedAssignments
from Teacher.models import ClassTeachers, Assignments

# Create your views here.

def stud_home(request, pk):
    # for k in allClasses:
    #     classNames = ClassTeachers.objects.filter(class_code=k.class_code)
    #     if(len(classNames)>0):
    #         teacherName = Teachers.objects.filter(teach_id=classNames[0].teach_id)
    #         for i in classNames:
    #             for j in teacherName:
    #                 if i.teach_id == j.teach_id:
    #                     data.append([i.class_code, i.class_name, j.name])
    
    if(request.method=="POST"):
        class_room=ClassStudents()
        class_room.stud_id=pk
        class_room.class_code=request.POST.get('code')
        class_code_var = request.POST.get('code')
        class_room.save() 
    allClasses = ClassStudents.objects.filter(stud_id=pk)
    data = []
    for i in allClasses:
        classObject=ClassTeachers.objects.filter(class_code=i.class_code)
        teacherObject=Teachers.objects.filter(teach_id=classObject[0].teach_id)
        data.append([i.class_code, classObject[0].class_name, teacherObject[0].name])
    print(data)
    return render(request, 'Student/student_home.html', {"data": data, 'pk': pk})

def classroom(request, pk, pk2):
    assign=Assignments.objects.filter(class_code=pk2)
    return render(request, 'Student/classroom.html', {'assign': assign, 'pk': pk, 'pk2': pk2})

def assignmentsub(request, pk, pk2, pk3):
    assign=Assignments.objects.filter(assignment_id=pk3)
    if(request.method=="POST"):
        assignment=SubmittedAssignments()
        assignment.assign_desc=request.POST.get('description')
        assignment.assignment_id=pk3
        _, file = request.FILES.popitem()
        file = file[0]
        file._name=str(pk)+"_"+str(pk2)+"_"+str(pk3)+".pdf"
        assignment.assign_file = file
        assignment.stud_id=pk
        assignment.save()
    return render(request, 'Student/assignment.html', {'assign': assign, 'pk': pk, 'pk2': pk2})
