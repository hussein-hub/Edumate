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
    if(request.method=="POST"):
        claso=ClassTeachers.objects.filter(class_code=request.POST.get('code'))
        check=ClassStudents.objects.filter(stud_id=pk, class_code=request.POST.get('code'))
        if check:
            messages.error(request, "Classroom already joined")
            return redirect('student_home', pk=pk)
        if claso:
            class_room=ClassStudents()
            class_room.stud_id=Students.objects.get(stud_id=pk)
            class_room.class_code=claso[0]
            class_room.save()
            return redirect('student_home', pk=pk)
        else:
            messages.error(request, "Please enter correct code")
            return redirect('student_home', pk=pk) 
    allClasses = ClassStudents.objects.filter(stud_id=pk)
    data = []
    # assignmentsNotSubmitted = []
    for i in allClasses:
        totalAssignmentsInOneClass = Assignments.objects.filter(class_code=i.class_code.class_code)
        temp = []
        for j in totalAssignmentsInOneClass:
            check = SubmittedAssignments.objects.filter(stud_id=pk, assignment_id=j.assignment_id)
            if not check:
                # print(timezone.localtime(timezone.now()))
                if timezone.localtime(timezone.now()) < j.duedate:
                    temp.append([j.assignment_id, j.assignment_name, j.class_code.class_name, j.duedate, False])
                else:
                    temp.append([j.assignment_id, j.assignment_name, j.class_code.class_name, j.duedate, True])
        # assignmentsNotSubmitted.append(temp)
        temp.sort(key=lambda x: x[3])
        data.append([i.class_code.class_code, i.class_code.class_name, i.class_code.teach_id.name, temp])
    # print(assignmentsNotSubmitted)

    return render(request, 'Student/student_home.html', {"data": data, 'pk': pk})

def classroom(request, pk, pk2):
    assign=Assignments.objects.filter(class_code=pk2).order_by('-duedate')
    submitted_assign = SubmittedAssignments.objects.filter(stud_id=pk, assignment_id__class_code=pk2)
    # print(submitted_assign)
    status = [False for i in range(len(assign))]
    late_submit_status = [False for i in range(len(assign))]
    k = 0
    for i in assign:
        for j in submitted_assign:
            if i.assignment_id==j.assignment_id.assignment_id:
                status[k]=True
        # print(timezone.localtime(timezone.now()), i.duedate)
        if timezone.localtime(timezone.now()) > i.duedate:
            late_submit_status[k]=True
        k += 1
    # print(status)
    data = []
    for i in range(len(assign)):
        data.append([assign[i], status[i], late_submit_status[i]])
    
    return render(request, 'Student/classroom.html', {'assign': data, 'pk': pk, 'pk2': pk2, 'status': status})

def assignmentsub(request, pk, pk2, pk3):
    assign=Assignments.objects.filter(assignment_id=pk3)
    pflag=assign[0].peer_grade
    peer_1=[]
    peer_2=[]
    marks_1=""
    marks_2=""
    temp=False
    submi=SubmittedAssignments.objects.filter(stud_id=pk, assignment_id=pk3)
    submidone={}
    marks_given=0
    if submi:
        submidone['desc']=submi[0].assign_desc
        submidone['file']=submi[0].assign_file
        if assign[0].peer_grade:
            peer1=PeerStudents.objects.filter(assign_id=pk3, as_peer_1=pk)
            peer2=PeerStudents.objects.filter(assign_id=pk3, as_peer_2=pk)
            flag1=False
            flag2=False
            flag3=False
            for i in peer1:
                if i.as_1_marks:
                    marks_given=marks_given+i.as_1_marks
                    flag1=True
            for i in peer2:
                if i.as_2_marks:
                    marks_given=marks_given+i.as_2_marks
                    flag2=True
            if submi[0].marks:
                marks_given=marks_given+4*submi[0].marks
                flag3=True
            if flag1 and flag2 and flag3:
                marks_given=marks_given/6
            else:
                marks_given=""
        else:
            if submi[0].marks:
                marks_given=submi[0].marks
            else:
                marks_given=""
    else:
        submidone['desc']=""
        submidone['file']=""
    if assign[0].peer_grade:
        assigned=PeerGrade.objects.filter(stud_id=pk, assign_id=pk3)
        temp_marks=PeerStudents.objects.filter(stud_id=pk, assign_id=pk3)
        if temp_marks:
            if temp_marks[0].as_1_marks:
                marks_1=temp_marks[0].as_1_marks
            if temp_marks[0].as_2_marks:
                marks_2=temp_marks[0].as_2_marks
        if(assigned):
            peer_1=SubmittedAssignments.objects.filter(assign_id=assigned[0].peer_1.assign_id)
            peer_2=SubmittedAssignments.objects.filter(assign_id=assigned[0].peer_2.assign_id)
    if(request.method=="POST" and request.POST.get('caller')=="call"):
        if float(request.POST.get('peer1'))>float(assign[0].max_marks) or float(request.POST.get('peer2'))>float(assign[0].max_marks):
            messages.error(request, 'Marks cannot be greater than maximum marks')
            return redirect('assignment', pk=pk, pk2=pk2, pk3=pk3)
        peer_marks=PeerStudents()
        peer_marks.stud_id=Students.objects.get(stud_id=pk)
        peer_marks.assign_id=Assignments.objects.get(assignment_id=pk3)
        peer_marks.as_peer_1=peer_1[0].stud_id
        peer_marks.as_1_marks=request.POST.get('peer1')
        peer_marks.as_peer_2=peer_2[0].stud_id
        peer_marks.as_2_marks=request.POST.get('peer2')
        peer_marks.save()
        temp=True
        return redirect('assignment', pk=pk, pk2=pk2, pk3=pk3)
    if(request.method=="POST" and temp==False):
        if(submi):
            submi[0].assign_desc=request.POST.get('description')
            if request.FILES:
                _, file = request.FILES.popitem()
                file = file[0]
                file._name=str(pk)+"_"+str(pk2)+"_"+str(pk3)+"_"+file._name
                submi[0].assign_file = file
            if(timezone.now()>assign[0].duedate):
                messages.error(request, "Assignment submitted late")
            submi[0].sub_date=timezone.now()
            submi[0].save()
            messages.error(request, "Assignment resubmited successfully")
            return redirect('assignment', pk=pk, pk2=pk2, pk3=pk3)
        assignment=SubmittedAssignments()
        assignment.assign_desc=request.POST.get('description')
        assignment.assignment_id=Assignments.objects.get(assignment_id=pk3)
        _, file = request.FILES.popitem()
        file = file[0]
        file._name=str(pk)+"_"+str(pk2)+"_"+str(pk3)+"_"+file._name
        assignment.assign_file = file
        assignment.stud_id=Students.objects.get(stud_id=pk)
        if(timezone.now()>assign[0].duedate):
            messages.error(request, "Assignment submitted late")
        else:
            messages.error(request, "Assignment submitted!!")
        assignment.sub_date=timezone.now()
        assignment.save()
        return redirect('assignment', pk=pk, pk2=pk2, pk3=pk3)
    if(len(peer_1) and len(peer_2)):
        return render(request, 'Student/assignment.html', {'assign': assign, 'pk': pk, 'pk2': pk2, 'desc1': peer_1[0], 'desc2': peer_2[0], 'pflag': pflag, 'submi': submidone, 'marks': marks_given, 'marks_1': marks_1, 'marks_2': marks_2})
    else:
        return render(request, 'Student/assignment.html', {'assign': assign, 'pk': pk, 'pk2': pk2, 'desc1': "X", 'desc2': "X", 'pflag': pflag, 'submi': submidone, 'marks': marks_given, 'marks_1': marks_1, 'marks_2': marks_2})
    # return render(request, 'Student/assignment.html', {'assign': assign, 'pk': pk, 'pk2': pk2, 'desc1': peer_1[0].assign_desc, 'desc2': peer_2[0].assign_desc})
    # return render(request, 'Student/assignment.html', {'pk': pk, 'pk2': pk2, })

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
        # print(i.quiz_date)
        a=(pk,i.id)
        answer = False
        if a in answered:
            answer = True
        quiz_list.append([i,answer])
    today = timezone.localtime(timezone.now())
    # print(str(today) + "-----")
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
    remark = "None"
    if request.method=='POST':
        cheat_check = request.POST.get('cheat')
        if str(cheat_check) == 'cheated':
            remark = "Cheating detected"
            teacher_email = Teachers.objects.get(teach_id = quiz.teach_id.teach_id).email
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
        cla = ClassTeachers.objects.get(class_code = pk2)
         
        quiz_mks = Quiz_marks(quiz=quiz,student=stud,class_id=cla,student_responses=json.dumps(stud_responses),correct_responses=json.dumps(correct_ans),total_marks=mks,marks_breakup=json.dumps(ind_mks),remarks=remark)
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
        typeCastedOptions = []
        for j in range(len(options)):
            typeCastedOptions.append([options[j], str(options[j].option_name)])
        jsonDec = json.decoder.JSONDecoder()
        stud_res = jsonDec.decode(answer.student_responses)
        stud_res = stud_res[k]
        cor_res = jsonDec.decode(answer.correct_responses)
        cor_res = cor_res[k]
        # print(type(cor_res[0]))
        num_cor = len(cor_res[0])
        indmarks = jsonDec.decode(answer.marks_breakup)
        indmarks = indmarks[k]
        ops.append([typeCastedOptions,stud_res,cor_res,(int(indmarks) if indmarks == int(indmarks) else indmarks),num_cor])
        k+=1
    return render(request, 'Student/revquiz.html', {'pk': pk, 'pk2': pk2, 'quiz': ops,'total_marks':answer.total_marks})

def submitatt(request, pk, pk2, pk3):
    final_list_list=[]
    att_obj = Attendance.objects.get(code=pk3)
    mainAttObj = Attendance_images.objects.filter(att_id=att_obj.att_id)
    all_marked_images = []
    for j in mainAttObj:
        all_marked_images.append(j.att_image.url.split('/')[0] + '/' + j.att_image.url.split('/')[1] + '/' + 'a' + j.att_image.url.split('/')[2])
    imagePath = mainAttObj[0].att_image.url.split('/')
    # print(all_marked_images)
    try:
        folderName = "."+"/".join(imagePath[:-1]) + "/" + imagePath[-1].split('.')[0]
    except:
        print()
    att_objects = AttStud.objects.filter(att_id=att_obj.att_id)
    marked_img_numbers = att_objects.values_list('img_number', flat=True)
    names = att_objects
    marked_img_numbers = list(marked_img_numbers)
    marked_img_numbers= {marked_img_numbers[j]:names[j] for j in range(len(marked_img_numbers))}
    allImages = [folderName[1:]+"/"+i for i in os.listdir(folderName)]
    allImages = {allImages[j]:j for j in range(len(allImages))}
    for i, j in allImages.items():
        if j in marked_img_numbers.keys():
            final_list_list.append([i, marked_img_numbers[j].stud_id.name])
        else:
            final_list_list.append([i, ""])
    imagePath[-1] = "a" + imagePath[-1]
    imagePath = '/'.join(imagePath)
    if(request.method=="POST"):
        att = AttStud()
        obj=AttStud.objects.filter(att_id=att_obj.att_id,stud_id=pk)
        if(len(obj)>0):
            messages.error(request, 'Attendance already marked')
            return redirect('markatt', pk=pk, pk2=pk2, pk3=pk3)
        curr=datetime.now()
        if(curr.timestamp()<datetime(int(att_obj.start_time[0:4]), int(att_obj.start_time[5:7]), int(att_obj.start_time[8:10]), int(att_obj.start_time[11:13]), int(att_obj.start_time[14:16])).timestamp()):
            messages.error(request, 'Attendance marking not started yet')
            return redirect('markatt', pk=pk, pk2=pk2, pk3=pk3)
        if(curr.timestamp()>datetime(int(att_obj.end_time[0:4]), int(att_obj.end_time[5:7]), int(att_obj.end_time[8:10]), int(att_obj.end_time[11:13]), int(att_obj.end_time[14:16])).timestamp()):
            messages.error(request, 'Attendance marking finished please contact teacher')
            return redirect('markatt', pk=pk, pk2=pk2, pk3=pk3)
        img_obj = AttStud.objects.filter(att_id=att_obj.att_id,img_number=request.POST.get('img_id'))
        if(len(img_obj)>0):
            messages.error(request, 'Attendance already marked for image')
            return redirect('markatt', pk=pk, pk2=pk2, pk3=pk3)
        att.img_number = request.POST.get('img_id')
        att.att_id=att_obj
        att.stud_id=Students.objects.get(stud_id=pk)
        att.att_time=curr
        att.save()
        return redirect('markatt', pk=pk, pk2=pk2, pk3=pk3)
    return render(request, 'Student/markatt.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'imagePath': imagePath, 'folderName': folderName, 'final_list_list': final_list_list, 'all_marked_images': all_marked_images })


def enterattcode(request, pk, pk2):
    if request.method=="POST":
        att_obj = Attendance.objects.filter(code=request.POST.get('code'))
        if(len(att_obj)==0):
            messages.error(request, "Please enter correct code")
            return redirect('submitatt', pk=pk, pk2=pk2)
        else:
            return redirect('markatt', pk=pk, pk2=pk2, pk3=request.POST.get('code'))
    return render(request, 'Student/entercode.html', {'pk': pk, 'pk2': pk2})