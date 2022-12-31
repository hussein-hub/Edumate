import calendar
from datetime import date
from datetime import datetime, timedelta
from django.shortcuts import render
import string, random
from django.http import FileResponse, Http404

from Edumate_app.models import Students, Teachers
from Student.models import ClassStudents, SubmittedAssignments, PeerStudents
from .models import ClassTeachers, Assignments, PeerGrade, Announcements, Schedule
import random
import copy
from django.shortcuts import redirect, render

from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar

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
        if request.POST.get('peer')=="on":
            assignment.peer_grade=True
        else:
            assignment.peer_grade=False
        print(request.POST.get('peer'))
        assignment.save()
    assign=Assignments.objects.filter(class_code=pk2)
    return render(request, 'Teacher/classroom.html', {'assign': assign, 'pk': pk, 'pk2': pk2})

def assignmentsub(request, pk, pk2, pk3):
    submitted=SubmittedAssignments.objects.filter(assignment_id=pk3)
    peerassign=PeerStudents.objects.filter(assign_id=pk3)
    assign_grade=Assignments.objects.filter(assignment_id =pk3)
    assign_flag=assign_grade[0].peer_grade
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
    return render(request, 'Teacher/show_assignments.html', {'submit': submitted, 'pk': pk, 'pk2': pk2 ,'pk3': pk3, "peer": peerassign, "shr": sorterval, 'peerf': assign_flag})

def assignmentgrade(request, pk, pk2, pk3,pk4):
    submitted=SubmittedAssignments.objects.get(assignment_id=pk3,stud_id = pk4)
    stud = Students.objects.get(stud_id = pk4)
    print(submitted.assign_file.url)
    file_url = "http://127.0.0.1:8000"+submitted.assign_file.url
    return render(request, 'Teacher/grade_assignments.html', {'student_name':stud.name,'file':file_url,'submit': submitted, 'pk': pk, 'pk2': pk2})

def announcement(request, pk, pk2):
    if (request.method == 'POST'):
        announcement = Announcements()
        announcement.announce_data = request.POST.get('announce_data')
        announcement.teach_id = pk
        announcement.class_code = pk2
        # print(announcement.announce_data, announcement.teach_id, announcement.class_code)
        announcement.save()
    announcement_data = Announcements.objects.filter(class_code = pk2).order_by('-date')
    return render(request, 'Teacher/announcement_teach.html', {'pk': pk, 'pk2': pk2, 'announcement_data': announcement_data})


def delete(request, pk, pk2, id):
    delAnnouncement = Announcements.objects.get(id=id)
    delAnnouncement.delete()
    return redirect('announcementteach', pk, pk2)


class schedule(generic.ListView):
    model = Schedule
    template_name = 'Teacher/schedule.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        d = get_date(self.request.GET.get('month', None))
        pk1 = self.kwargs['pk']
        classcode = self.kwargs['pk2']
        cal = Calendar(d.year, d.month, classcode)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['pk2'] = classcode
        context['pk1'] = pk1
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
