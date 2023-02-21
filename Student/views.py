from django.http import QueryDict
from django.shortcuts import render, redirect
from Edumate_app.models import Students, Teachers
import json, os
from Student.models import ClassStudents, Quiz_marks, SubmittedAssignments, PeerStudents
from Student.utils import Calendar
from Teacher.models import *
import calendar
from datetime import date
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.safestring import mark_safe
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
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
    # print(data)
    return render(request, 'Student/student_home.html', {"data": data, 'pk': pk})

def classroom(request, pk, pk2):
    assign=Assignments.objects.filter(class_code=pk2)
    return render(request, 'Student/classroom.html', {'assign': assign, 'pk': pk, 'pk2': pk2})

def assignmentsub(request, pk, pk2, pk3):
    assign=Assignments.objects.filter(assignment_id=pk3)
    pflag=assign[0].peer_grade
    peer_1=[]
    peer_2=[]
    temp=False
    if assign[0].peer_grade:
        assigned=PeerGrade.objects.filter(stud_id=pk, assign_id=pk3)
        if(assigned):
            peer_1=SubmittedAssignments.objects.filter(assign_id=assigned[0].peer_1)
            peer_2=SubmittedAssignments.objects.filter(assign_id=assigned[0].peer_2)
    if(request.method=="POST" and request.POST.get('caller')=="call"):
        peer_marks=PeerStudents()
        peer_marks.stud_id=pk
        peer_marks.assign_id=pk3
        peer_marks.as_peer_1=peer_1[0].stud_id
        peer_marks.as_1_marks=request.POST.get('peer1')
        peer_marks.as_peer_2=peer_2[0].stud_id
        peer_marks.as_2_marks=request.POST.get('peer2')
        peer_marks.save()
        temp=True
    if(request.method=="POST" and temp==False):
        assignment=SubmittedAssignments()
        assignment.assign_desc=request.POST.get('description')
        assignment.assignment_id=pk3
        _, file = request.FILES.popitem()
        file = file[0]
        file._name=str(pk)+"_"+str(pk2)+"_"+str(pk3)+".pdf"
        assignment.assign_file = file
        assignment.stud_id=pk
        assignment.save()
    if(len(peer_1) and len(peer_2)):
        return render(request, 'Student/assignment.html', {'assign': assign, 'pk': pk, 'pk2': pk2, 'desc1': peer_1[0], 'desc2': peer_2[0], 'pflag': pflag})
    else:
        return render(request, 'Student/assignment.html', {'assign': assign, 'pk': pk, 'pk2': pk2, 'desc1': "X", 'desc2': "X", 'pflag': pflag})
    # return render(request, 'Student/assignment.html', {'assign': assign, 'pk': pk, 'pk2': pk2, 'desc1': peer_1[0].assign_desc, 'desc2': peer_2[0].assign_desc})
    return render(request, 'Student/assignment.html', {'pk': pk, 'pk2': pk2, })

def announcement_stud(request, pk, pk2):
    announcements = Announcements.objects.filter(class_code = pk2)
    # print(pk, pk2)
    return render(request, 'Student/announcement_student.html', {'pk': pk, 'pk2': pk2, 'announcements': announcements})

class schedule(generic.ListView):
    model = Schedule
    template_name = 'Student/schedule.html'
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

def quiz(request, pk, pk2):
    quiz = Quiz.objects.filter(class_code = pk2)
    stud = Students.objects.get(stud_id=pk)
    answered=Quiz_marks.objects.filter(student=stud).values_list('student','quiz')
    quiz_list = []
    for i in quiz:
        a=(pk,i.id)
        answer = False
        if a in answered:
            answer = True
        quiz_list.append([i,answer])
    today = timezone.now()
    # print(quiz[1].quiz_date)
    # print(today)
    # print(quiz[1].quiz_date > today)
    # print(quiz_list)
    # print(quiz)
    # print(answered)
    
    return render(request, 'Student/quiz_student.html', {'pk': pk, 'pk2': pk2, 'quiz': quiz_list,'today':today})

def ansquiz(request,pk,pk2,pk3):
    quiz = Quiz.objects.get(id = pk3)
    questions = Question.objects.filter(quiz=quiz)
    q_time = quiz.time_limit
    ops=[]
    correct_ans=[]
    for i in questions:
        options = Options.objects.filter(question=i)
        img = QuestionImage.objects.filter(question=i)
        correct_count=0
        c_ops=[]
        for j in options:
            if j.correct == True:
                c_ops.append(j.option_name)
                correct_count += 1
        ops.append([options,correct_count,img])
        multi = i.marks / correct_count
        correct_ans.append([c_ops,multi])
    total_questions = len(ops)
    stud_responses =[]
    if request.method=='POST':
        cheat_check = request.POST.get('cheat')
        if str(cheat_check) == 'cheated':
            teacher_email = Teachers.objects.get(teach_id = quiz.teach_id).email
            student_name = Students.objects.get(stud_id=pk).name
            subject = 'Cheating detecting in quiz'
            message = 'Cheating detected in quiz ' + str(quiz.quiz_name) + ' of class ' + str(quiz.class_code) + ' by student ' + str(student_name)
            send_mail(subject, message, settings.EMAIL_HOST_USER, [teacher_email], fail_silently = False)

        for i in range(total_questions):
            op = request.POST.getlist('op_'+str(i+1))
            stud_responses.append(op)
        mks = 0
        ind_mks = []
        for i in range(len(stud_responses)):
            mk=0
            for j in stud_responses[i]:
                if len(correct_ans[i][0])>1:
                    if j in correct_ans[i][0]:
                        mk += correct_ans[i][1]
                    else :
                        mk -= correct_ans[i][1]
                    
                else:
                    if j in correct_ans[i][0]:
                        mk += correct_ans[i][1]

            if mk<0:
                mk=0
            ind_mks.append(mk)
            mks += mk


        stud = Students.objects.get(stud_id = pk)
        quiz_mks = Quiz_marks(quiz=quiz,student=stud,class_id=pk2,student_responses=json.dumps(stud_responses),correct_responses=json.dumps(correct_ans),total_marks=mks,marks_breakup=json.dumps(ind_mks))
        quiz_mks.save()
        return redirect('quiz_stud',pk=pk,pk2=pk2)
        
    return render(request, 'Student/ansquiz.html', {'pk': pk, 'pk2': pk2,'pk3':pk3, 'quiz': ops,'q_time':q_time})

def revquiz(request,pk,pk2,pk3):
    quiz = Quiz.objects.get(id = pk3)
    questions = Question.objects.filter(quiz=quiz)
    ops=[]
    answer = Quiz_marks.objects.get(quiz=quiz,student_id = pk)
    k=0
    for i in questions:
        options = Options.objects.filter(question=i)
        jsonDec = json.decoder.JSONDecoder()
        stud_res = jsonDec.decode(answer.student_responses)
        stud_res = stud_res[k]
        cor_res = jsonDec.decode(answer.correct_responses)
        cor_res = cor_res[k]
        num_cor = len(cor_res[0])
        indmarks = jsonDec.decode(answer.marks_breakup)
        indmarks = indmarks[k]
        ops.append([options,stud_res,cor_res,indmarks,num_cor])
        k+=1
    return render(request, 'Student/revquiz.html', {'pk': pk, 'pk2': pk2, 'quiz': ops,'total_marks':answer.total_marks})

def submitatt(request, pk, pk2):
    imagePath = None
    if(request.method=="POST"):
        att_obj=Attendance.objects.filter(code=request.POST.get('code'))
        if(len(att_obj)!=0):
            if(att_obj[0].class_id!=pk2):
                messages.error(request, 'Please enter the code in the correct classroom')
                return redirect('submitatt', pk=pk, pk2=pk2)
            obj=AttStud.objects.filter(att_id=att_obj[0].att_id,stud_id=pk)
            if(len(obj)>0):
                messages.error(request, 'Attendance already marked')
                return redirect('submitatt', pk=pk, pk2=pk2)
            curr=datetime.now()
            if(curr.timestamp()<datetime(int(att_obj[0].start_time[0:4]), int(att_obj[0].start_time[5:7]), int(att_obj[0].start_time[8:10]), int(att_obj[0].start_time[11:13]), int(att_obj[0].start_time[14:16])).timestamp()):
                messages.error(request, 'Attendance marking not started yet')
                return redirect('submitatt', pk=pk, pk2=pk2)
            if(curr.timestamp()>datetime(int(att_obj[0].end_time[0:4]), int(att_obj[0].end_time[5:7]), int(att_obj[0].end_time[8:10]), int(att_obj[0].end_time[11:13]), int(att_obj[0].end_time[14:16])).timestamp()):
                messages.error(request, 'Attendance marking finished please contact teacher')
                return redirect('submitatt', pk=pk, pk2=pk2)
            # print(datetime(int(att_obj[0].start_time[0:4]), int(att_obj[0].start_time[5:7]), int(att_obj[0].start_time[8:10]), int(att_obj[0].start_time[11:13]), int(att_obj[0].start_time[14:16])).timestamp())
            # print(datetime(int(att_obj[0].end_time[0:4]), int(att_obj[0].end_time[5:7]), int(att_obj[0].end_time[8:10]), int(att_obj[0].end_time[11:13]), int(att_obj[0].end_time[14:16])).timestamp())
            att=AttStud()
            att.att_id=att_obj[0].att_id
            att.stud_id=pk
            att.att_time=curr
            att.save()
            # messages.success(request, 'Attendance Marked')
            mainAttObj = Attendance_images.objects.get(att_id=att_obj[0].att_id)
            imagePath = mainAttObj.att_image.url.split('/')
            folderName = "."+"/".join(imagePath[:-1]) + "/" + imagePath[-1].split('.')[0]
            # os.listdir(f'{folderName}')
            allImages = [folderName[1:]+"/"+i for i in os.listdir(folderName)]
            imagePath[-1] = "a" + imagePath[-1]
            imagePath = '/'.join(imagePath)
            print(imagePath)

            return render(request, 'Student/markatt.html', {'pk': pk, 'pk2': pk2, 'imagePath': imagePath, 'folderName': folderName, 'allImages': allImages})
        else:
            messages.error(request, 'Incorrect code')
            return redirect('submitatt', pk=pk, pk2=pk2, imagePath=imagePath)
    return render(request, 'Student/markatt.html', {'pk': pk, 'pk2': pk2, 'imagePath': imagePath})