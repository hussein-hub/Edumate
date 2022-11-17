from django.shortcuts import render
import string, random
from django.http import FileResponse, Http404

from Edumate_app.models import Students, Teachers
from Student.models import ClassStudents, SubmittedAssignments, PeerStudents
from .models import ClassTeachers, Assignments, PeerGrade
import random
import copy

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
    peerassign=PeerStudents.objects.filter(assign_id=pk3)
    sorterval=[]
    for i in submitted:
        received1=PeerStudents.objects.filter(assign_id=pk3, as_peer_1=i.stud_id)
        received2=PeerStudents.objects.filter(assign_id=pk3, as_peer_2=i.stud_id)
        temp=[i.stud_id]
        for j in received1:
            temp.append(j.stud_id)
            temp.append(j.as_1_marks)
        for j in received2:
            temp.append(j.stud_id)
            temp.append(j.as_2_marks)
        sorterval.append(temp)
    if(request.method=="POST"):
        sub_stud=SubmittedAssignments.objects.filter(assignment_id=pk3)
        studs=ClassStudents.objects.filter(class_code=pk2)
        if(len(sub_stud)!=len(studs)):
            print("Some students are still left to submit their assignments")
        else:
            a=[]
            stud_sub=[]
            for i in sub_stud:
                a.append(i.assign_id)
                stud_sub.append(i.stud_id)
            b=copy.deepcopy(a)
            random.shuffle(a)
            a=a+a
            ans=[]
            j=0
            for i in range(0, len(b)):
                while(a[j]==b[i] or a[j]=="X"):
                    j=(j+1)%len(a)
                ans.append([a[j]])
                a[j]="X"
                while(a[j]==b[i] or ans[i][0]==a[j] or a[j]=="X"):
                    j=(j+1)%len(a)
                ans[i].append(a[j])
                a[j]="X"
            for i in range(0,len(stud_sub)):
                peer=PeerGrade()
                peer.stud_id=stud_sub[i]
                peer.assign_id=pk3
                peer.peer_1=ans[i][0]
                peer.peer_2=ans[i][1]
                peer.save()
    return render(request, 'Teacher/show_assignments.html', {'submit': submitted, 'pk': pk, 'pk2': pk2 ,'pk3': pk3, "peer": peerassign, "shr": sorterval})

def assignmentgrade(request, pk, pk2, pk3,pk4):
    submitted=SubmittedAssignments.objects.get(assignment_id=pk3,stud_id = pk4)
    stud = Students.objects.get(stud_id = pk4)
    print(submitted.assign_file.url)
    file_url = "http://127.0.0.1:8000"+submitted.assign_file.url
    return render(request, 'Teacher/grade_assignments.html', {'student_name':stud.name,'file':file_url,'submit': submitted, 'pk': pk, 'pk2': pk2})
