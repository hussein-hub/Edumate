from django.http import QueryDict
from django.shortcuts import render, redirect
from Edumate_app.models import Students, Teachers
import json, os
from Student.models import ClassStudents, Quiz_marks, SubmittedAssignments,  Progress
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
import re
import cv2
from django.http import JsonResponse
from datetime import datetime, timedelta

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
    classroomName = ClassTeachers.objects.get(class_code=pk2).class_name
    assign=Assignments.objects.filter(class_code=pk2).order_by('-duedate')
    submitted_assign = SubmittedAssignments.objects.filter(stud_id=pk, assignment_id__class_code=pk2)
    data = []

    for i in assign:
        temp = [i]
        check = SubmittedAssignments.objects.filter(stud_id=pk, assignment_id=i.assignment_id)
        if len(check):
            temp.append(True)
            if check[0].sub_date > i.duedate:
                temp.append(True)
            else:
                temp.append(False)
        else:
            temp.append(False)
            temp.append(False)
        data.append(temp)
        
    print(data)

    # print(submitted_assign)
    # status = [False for i in range(len(assign))]
    # late_submit_status = [False for i in range(len(assign))]
    # k = 0
    # for i in assign:
    #     for j in submitted_assign:
    #         if i.assignment_id==j.assignment_id.assignment_id:
    #             print(i.assignment_name, j.sub_date, i.duedate)
    #             status[k]=True
    #             if j.sub_date > i.duedate:
    #                 late_submit_status[k]=True
    #     k += 1
    # data = []
    # for i in range(len(assign)):
    #     data.append([assign[i], status[i], late_submit_status[i]])

    return render(request, 'Student/classroom.html', {'assign': data, 'pk': pk, 'pk2': pk2,'classroomName': classroomName})

def assignmentsub(request, pk, pk2, pk3):
    assign=Assignments.objects.filter(assignment_id=pk3)
    pflag=assign[0].peer_grade
    submi=SubmittedAssignments.objects.filter(stud_id=pk, assignment_id=pk3)
    submidone={}
    assigned=[]
    pe_assigned=[]
    marks=0
    marksflag=True
    pe=None
    feeds=None
    if pflag:
        pet=Peergrade.objects.get(class_code=pk2, assignment_id=pk3)
        pe=PeerAssigns.objects.filter(peergrade_id=pet.peergrade_id, stud_id=pk)
        assigned=pe
        feeds=PeerAssigns.objects.filter(peergrade_id=pet.peergrade_id, assigned_stud_id=pk)
        for i in feeds:
            if i.feedb:
                pe_assigned.append(i.feedb)
            else:
                pe_assigned.append(None)
    if submi:
        submidone['desc']=submi[0].assign_desc
        submidone['file']=submi[0].assign_file
    else:
        submidone['desc']=""
        submidone['file']=""
    if submi and feeds:
        if submi[0].marks:
            marks=marks+4*submi[0].marks
            for i in feeds:
                if i.marks:
                    marks=marks+i.marks
                else:
                    marks=0
                    marksflag=False
                    break
        else:
            marks=0
            marksflag=False
    else:
        if submi:
            if submi[0].marks:
                marks=submi[0].marks
                marksflag=True
            else:
                marks=0
                marksflag=False
        else:
            marks=0
            marksflag=False
    if marksflag and feeds:
        marks=marks/(len(feeds)+4)
    if(request.method=="POST"):
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
    return render(request, 'Student/assignment.html', {'assign': assign, 'pk': pk, 'pk2': pk2, 'pk3': pk3, 'submi': submidone, 'pflag': pflag, 'assigned': assigned, 'pe': pe_assigned, 'marks': marks, 'marksflag': marksflag})

def grad(request, pk, pk2, pk3, pk4):
    pet=Peergrade.objects.get(class_code=pk2, assignment_id=pk3)
    pe=PeerAssigns.objects.get(peergrade_id=pet.peergrade_id, stud_id=pk, assigned_stud_id=pk4)
    questions=pet.questions.split("*")
    final_options=[]
    final_options.append(pet.opt1.split("*"))
    final_options.append(pet.opt2.split("*"))
    final_options.append(pet.opt3.split("*"))
    submitted=SubmittedAssignments.objects.get(assignment_id=pk3, stud_id=pk4)
    assignment=Assignments.objects.get(assignment_id=pk3)
    pe_assigned=[]
    if request.method=="POST":
        pe.feedb=request.POST.get('feedback')
        pe.options_selec=request.POST.get('1')+"*"+request.POST.get('2')+"*"+request.POST.get('3')
        total_marks=0
        if request.POST.get('1')=='1':
            total_marks=total_marks+assignment.max_marks*0.50
        elif request.POST.get('1')=='2':
            total_marks=total_marks+assignment.max_marks*0.75
        elif request.POST.get('1')=='3':
            total_marks=total_marks+assignment.max_marks
        if request.POST.get('2')=='1':
            total_marks=total_marks+assignment.max_marks*0.50
        elif request.POST.get('2')=='2':
            total_marks=total_marks+assignment.max_marks*0.75
        elif request.POST.get('2')=='3':
            total_marks=total_marks+assignment.max_marks
        if request.POST.get('3')=='1':
            total_marks=total_marks+assignment.max_marks*0.50
        elif request.POST.get('3')=='2':
            total_marks=total_marks+assignment.max_marks*0.75
        elif request.POST.get('3')=='3':
            total_marks=total_marks+assignment.max_marks
        total_marks=total_marks/3
        pe.marks=total_marks
        pe.save()
        return redirect('assignment', pk=pk, pk2=pk2, pk3=pk3)
    return render(request, 'Student/grad.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'pk4': pk4, 'ques_and_ans': zip(questions, final_options), 'submitted': submitted, 'assignment': assignment, 'pe': pe_assigned})

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
    allImages = []#[folderName[1:]+"/"+i if os.path.isFile(i) else continue for i in os.listdir(folderName)]
    for i in os.listdir(folderName):
        if os.path.isfile(folderName+"/"+i):
            allImages.append(folderName[1:]+"/"+i)

    allImages = sorted(allImages, key = lambda x: (int(re.sub('\D','',x)),x))
    allImages = {allImages[j]:j for j in range(len(allImages))}
    for i, j in allImages.items():
        if j in marked_img_numbers.keys():
            final_list_list.append([i, marked_img_numbers[j].stud_id.name])
        else:
            final_list_list.append([i, ""])
    imagePath[-1] = "a" + imagePath[-1]
    imagePath = '/'.join(imagePath)
    
    att_check = AttStud.objects.filter(att_id=att_obj.att_id, stud_id=pk)

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
        att.is_approved = True
        att.save()
        return redirect('markatt', pk=pk, pk2=pk2, pk3=pk3)
    return render(request, 'Student/markatt.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'imagePath': imagePath, 'folderName': folderName, 'final_list_list': final_list_list, 'all_marked_images': all_marked_images , 'att_crop_check': len(att_check)})

def testing(request,pk, pk2, pk3):
    if request.method == "POST":
        x = float(request.POST.get('x'))
        y = float(request.POST.get('y'))
        w = float(request.POST.get('w'))
        h = float(request.POST.get('h'))
        num = int(request.POST.get('num'))

        att_obj = Attendance.objects.get(code=pk3)
        mainAttObj = Attendance_images.objects.filter(att_id=att_obj.att_id)

        cropped_folder_name = "./"+mainAttObj[0].att_image.url.split('/')[0] + '/' + mainAttObj[0].att_image.url.split('/')[1] + '/' + mainAttObj[0].att_image.url.split('/')[2].split(".")[0] + '/' + mainAttObj[num-1].att_image.url.split('/')[2].split(".")[0] + '/'
        image_folder_path = mainAttObj[num-1].att_image.url.split('/')[0] + '/' + mainAttObj[num-1].att_image.url.split('/')[1] + '/' + 'a' + mainAttObj[num-1].att_image.url.split('/')[2]
        img = cv2.imread("./"+image_folder_path)
        copy_img = cv2.imread("./"+image_folder_path)

        print("Creating directory")
        # try:
        #     for i in mainAttObj:
        #         os.mkdir(i.att_image.url.split('/')[2].split(".")[0])
        #     os.mkdir(cropped_folder_name)
        # except:
        #     print("Dir already present")

        cropped_img = copy_img[int(round(y,0)):int(round(y+h,0)),int(round(x,0)):int(round(x+w,0))]
        count = 0
        for root_dir, cur_dir, files in os.walk("./"+mainAttObj[0].att_image.url.split('/')[0] + '/' + mainAttObj[0].att_image.url.split('/')[1] + '/' + mainAttObj[0].att_image.url.split('/')[2].split(".")[0] + '/'):
            count += len(files)

        new_cropped_image_number = count
        cv2.imwrite(cropped_folder_name+str(new_cropped_image_number)+".jpg",cropped_img)

        img = cv2.rectangle(img, (int(round(x,0)),int(round(y,0))), (int(round(x+w,0)),int(round(y+h,0))), (255,0,0), 2)
        img = cv2.putText(img, "crop"+str(new_cropped_image_number), (int(round(x,0)), int(round(y,0))-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
        cv2.imwrite("./"+image_folder_path,img)

        student_att = AttStud()
        student_att.att_id = att_obj
        student_att.stud_id = Students.objects.get(stud_id=pk)
        student_att.att_time = datetime.now()
        student_att.img_number = new_cropped_image_number
        student_att.is_approved = False
        student_att.is_cropped = True
        student_att.save()
        
        return JsonResponse(data={"url":reverse('submitatt', kwargs={'pk':pk,'pk2':pk2})})

def attcropimg(request, pk, pk2, pk3):
    final_list_list=[]
    att_obj = Attendance.objects.get(code=pk3)
    mainAttObj = Attendance_images.objects.filter(att_id=att_obj.att_id)
    all_marked_images = []
    for j in mainAttObj:
        all_marked_images.append(j.att_image.url.split('/')[0] + '/' + j.att_image.url.split('/')[1] + '/' + 'a' + j.att_image.url.split('/')[2])
    # imagePath = mainAttObj[0].att_image.url.split('/')
    # print(all_marked_images)
    # try:
    #     folderName = "."+"/".join(imagePath[:-1]) + "/" + imagePath[-1].split('.')[0]
    # except:
    #     print()
    # att_objects = AttStud.objects.filter(att_id=att_obj.att_id)
    # marked_img_numbers = att_objects.values_list('img_number', flat=True)
    # names = att_objects
    # marked_img_numbers = list(marked_img_numbers)
    # marked_img_numbers= {marked_img_numbers[j]:names[j] for j in range(len(marked_img_numbers))}
    # allImages = [folderName[1:]+"/"+i for i in os.listdir(folderName)]
    # allImages = sorted(allImages, key = lambda x: (int(re.sub('\D','',x)),x))
    # allImages = {allImages[j]:j for j in range(len(allImages))}
    # for i, j in allImages.items():
    #     if j in marked_img_numbers.keys():
    #         final_list_list.append([i, marked_img_numbers[j].stud_id.name])
    #     else:
    #         final_list_list.append([i, ""])
    # imagePath[-1] = "a" + imagePath[-1]
    # imagePath = '/'.join(imagePath)
    return render(request, 'Student/crop_img_attendance.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'all_marked_images': all_marked_images})

def enterattcode(request, pk, pk2):
    if request.method=="POST":
        att_obj = Attendance.objects.filter(code=request.POST.get('code'))
        if(len(att_obj)==0):
            messages.error(request, "Please enter correct code")
            return redirect('submitatt', pk=pk, pk2=pk2)
        else:
            return redirect('markatt', pk=pk, pk2=pk2, pk3=request.POST.get('code'))
    return render(request, 'Student/entercode.html', {'pk': pk, 'pk2': pk2})

def projecttrack(request, pk, pk2):
    projects = Project.objects.filter(class_code=pk2)
    return render(request, 'Student/projecttrack.html', {'pk': pk, 'pk2': pk2, 'projects': projects})

def single_project(request, pk, pk2, pk3):
    project=Project.objects.get(pro_id=pk3)
    checks=project.prog_check.split("\r")
    group=Groups.objects.filter(pro_id=pk3)
    final_group=None
    members=None
    prog_value=None
    for i in group:
        member=Members.objects.filter(group_id=i.group_id, stud_id=pk)
        if member:
            final_group=i
            members=Members.objects.filter(group_id=i.group_id)
            temp=Progress.objects.filter(group_id=i.group_id)
            if temp:
                prog_value=temp[0].prog
            else:
                t=""
                for j in checks:
                    if j:
                        t=t+"b"
                prog_value=t
            break
    if request.method == "POST":
        res=""
        for i in range(1, len(checks)+1):
            if request.POST.get(f'checks_{i}') == "on":
                res=res+'a'
            else:
                res=res+'b'
        che=Progress.objects.filter(group_id=final_group.group_id)
        if che:
            che[0].prog=res
            che[0].save()
            messages.error(request, "Progress saved!")
            return redirect('single_project', pk=pk, pk2=pk2, pk3=pk3)
        resp=Progress()
        resp.group_id=final_group
        resp.prog=res
        resp.save()
        messages.error(request, "Progress saved!")
        return redirect('single_project', pk=pk, pk2=pk2, pk3=pk3)
    return render(request, 'Student/single_project.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'project': project, 'group': final_group, 'members': members, 'check': zip(checks, list(prog_value))})

def stud_group(request, pk, pk2):
    groups=Grouppeers.objects.filter(class_code=pk2).order_by('-created_date')
    temp=[]
    for i in groups:
        peers=PeerGroups.objects.filter(gro_id=i.gro_id)
        for j in peers:
            peer_members=Peermembers.objects.filter(pgro_id=j.group_id, stud_id=pk)
            if peer_members:
                if j.submit_file:
                    temp.append("T")
                else:
                    temp.append("F")
                break
    return render(request, 'Student/stud_group.html', {'pk': pk, 'pk2': pk2, 'groups': zip(groups, temp)})

def single_stud_group(request, pk, pk2, pk3):
    group=Grouppeers.objects.get(gro_id=pk3)
    all_group=PeerGroups.objects.filter(gro_id=group.gro_id)
    single_group=None
    members=None
    assigned=None
    total_marks="X"
    for i in all_group:
        mems=Peermembers.objects.filter(stud_id=pk, pgro_id=i.group_id)
        if mems:
            single_group=i
            members=Peermembers.objects.filter(pgro_id=i.group_id)
            break
    submi=None
    if single_group.submit_desc:
        submi=single_group.submit_file.url
    peerreviews=[]
    p_groups=PeergradeGroups.objects.filter(class_code=pk2, assignment_id=pk3)
    if p_groups:
        p_groups=p_groups[0]
        p_reviews=PeerAssignsGroups.objects.filter(peergrade_id=p_groups.peergrade_id, assigned_stud_id=pk)
        peer_marks=[]
        if single_group and single_group.marksbyteacher:
            peer_marks.append(single_group.marksbyteacher*4)
        for i in p_reviews:
            if i.feedb:
                peerreviews.append(i.feedb)
                peer_marks.append(i.marks)
            else:
                peerreviews.append("X")
        if len(peer_marks) == group.num_studs + 1:
            total_marks=sum(peer_marks)/(group.num_studs + 4)
        assigned=PeerAssignsGroups.objects.filter(peergrade_id=p_groups.peergrade_id, stud_id=pk)
    if request.method=="POST":
        single_group.submit_desc=request.POST.get('description')
        _, file = request.FILES.popitem()
        file = file[0]
        file._name="Group"+str(pk)+"_"+str(pk2)+"_"+str(pk3)+"_"+file._name
        single_group.submit_file = file
        single_group.submit_by=Students.objects.get(stud_id=pk)
        if(timezone.now()>group.gpeer_due):
            messages.error(request, "Assignment submitted late")
        else:
            messages.error(request, "Assignment submitted!!")
        single_group.submit_date=timezone.now()
        single_group.save()
        return redirect('single_stud_group', pk=pk, pk2=pk2, pk3=pk3)
    return render(request, 'Student/single_stud_group.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'group': group, 'single_group': single_group, 'members': members, 'submi': submi, 'pe': peerreviews, 'assigned': assigned, 'total_marks': total_marks})

def gradesingle(request, pk, pk2, pk3, pk4):
    pet=PeergradeGroups.objects.get(class_code=pk2, assignment_id=pk3)
    pe=PeerAssignsGroups.objects.get(peergrade_id=pet.peergrade_id, stud_id=pk, assigned_stud_id=pk4)
    questions=pet.questions.split("*")
    final_options=[]
    final_options.append(pet.opt1.split("*"))
    final_options.append(pet.opt2.split("*"))
    final_options.append(pet.opt3.split("*"))
    submitted=[]
    members=[]
    assignment=Grouppeers.objects.get(gro_id=pk3)
    all_groups=PeerGroups.objects.filter(gro_id=pk3)
    for i in all_groups:
        membs=Peermembers.objects.filter(stud_id=pk4, pgro_id=i.group_id)
        if membs:
            submitted=i
            members=Peermembers.objects.filter(pgro_id=i.group_id)
    pe_assigned=[]
    if request.method=="POST":
        pe.feedb=request.POST.get('feedback')
        pe.options_selec=request.POST.get('1')+"*"+request.POST.get('2')+"*"+request.POST.get('3')
        total_marks=0
        if request.POST.get('1')=='1':
            total_marks=total_marks+assignment.marks*0.50
        elif request.POST.get('1')=='2':
            total_marks=total_marks+assignment.marks*0.75
        elif request.POST.get('1')=='3':
            total_marks=total_marks+assignment.marks
        if request.POST.get('2')=='1':
            total_marks=total_marks+assignment.marks*0.50
        elif request.POST.get('2')=='2':
            total_marks=total_marks+assignment.marks*0.75
        elif request.POST.get('2')=='3':
            total_marks=total_marks+assignment.marks
        if request.POST.get('3')=='1':
            total_marks=total_marks+assignment.marks*0.50
        elif request.POST.get('3')=='2':
            total_marks=total_marks+assignment.marks*0.75
        elif request.POST.get('3')=='3':
            total_marks=total_marks+assignment.marks
        total_marks=total_marks/3
        pe.marks=total_marks
        pe.save()
        return redirect('single_stud_group', pk=pk, pk2=pk2, pk3=pk3)
    return render(request, 'Student/gradesingle.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'pk4': pk4, 'ques_and_ans': zip(questions, final_options), 'submitted': submitted, 'assignment': assignment, 'pe': pe_assigned, 'members': members})

def analytics(request, pk, pk2):
    class_info=ClassTeachers.objects.get(class_code=pk2)
    today = datetime.today()
    week1 = today + timedelta(days=-7)
    week1_data = Attendance.objects.filter(class_id=pk2, start_time__gte=week1)
    week2 = today + timedelta(days=-14)
    week2_data = Attendance.objects.filter(class_id=pk2, start_time__gte=week2, start_time__lte=week1)
    week3 = today + timedelta(days=-21)
    week3_data = Attendance.objects.filter(class_id=pk2, start_time__gte=week3, start_time__lte=week2)
    week4 = today + timedelta(days=-28)
    week4_data = Attendance.objects.filter(class_id=pk2, start_time__gte=week4, start_time__lte=week3)
    total_lecs=len(week1_data)+len(week2_data)+len(week3_data)+len(week4_data)
    final_data=[]
    count=0
    for i in week1_data:
        check=AttStud.objects.filter(att_id=i.att_id, stud_id=pk)
        if check:
            count=count+1
    final_data.append(count)
    count=0
    for i in week2_data:
        check=AttStud.objects.filter(att_id=i.att_id, stud_id=pk)
        if check:
            count=count+1
    final_data.append(count)
    count=0
    for i in week3_data:
        check=AttStud.objects.filter(att_id=i.att_id, stud_id=pk)
        if check:
            count=count+1
    final_data.append(count)
    count=0
    for i in week4_data:
        check=AttStud.objects.filter(att_id=i.att_id, stud_id=pk)
        if check:
            count=count+1
    final_data.append(count)
    perct=0
    if total_lecs!=0:
        perct=float(sum(final_data)/total_lecs)*100
    assignments=Assignments.objects.filter(class_code=pk2)
    academics=[]
    pending_assignments=[]
    for i in assignments:
        sub=SubmittedAssignments.objects.filter(assignment_id=i.assignment_id, stud_id=pk)
        temp_list=[]
        if len(sub):
            if sub[0].sub_date > i.duedate:
                temp_list=[i.assignment_name, sub[0].marks, i.max_marks, 'L']
            else:
                temp_list=[i.assignment_name, sub[0].marks, i.max_marks, 'O']
            if i.peer_grade:
                temp_list.append("P")
                per_g=Peergrade.objects.get(assignment_id=i.assignment_id)
                per_m=PeerAssigns.objects.filter(peergrade_id=per_g.peergrade_id, assigned_stud_id=pk)
                marks_list=[]
                for j in per_m:
                    if j.marks:
                        marks_list.append(j.marks)
                    else:
                        marks_list=[]
                        break
                if marks_list and sub[0].marks:
                    marks_list.append(4*sub[0].marks)
                    temp_list[1]=sum(marks_list)/(len(marks_list)+3)
                else:
                    temp_list[1]=""
            else:
                temp_list.append("NP")
            academics.append(temp_list)
        else:
            pending_assignments.append([i.assignment_name, i.duedate])
    quizzes=Quiz_marks.objects.filter(class_id=pk2, student=pk)
    marks_quiz=[]
    for i in quizzes:
        if i.total_marks:
            marks_quiz.append([i.quiz.quiz_name, i.total_marks])
    all_class_quizzes=Quiz.objects.filter(class_code=pk2)
    pending_quiz=[]
    for i in all_class_quizzes:
        temp=Quiz_marks.objects.filter(class_id=pk2, student=pk, quiz=i.id)
        if temp:
            continue
        else:
            pending_quiz.append([i.quiz_name, i.quiz_date])
    all_peers=Grouppeers.objects.filter(class_code=pk2)
    group_peer_grading=[]
    group_peer_marks=[]
    for i in all_peers:
        all_gs=PeerGroups.objects.filter(gro_id=i.gro_id)
        for j in all_gs:
            peer_m=Peermembers.objects.filter(pgro_id=j.group_id)
            if peer_m:
                created_peer=PeergradeGroups.objects.filter(assignment_id=i.gro_id)
                if created_peer:
                    created_peer=created_peer[0]
                    peer_assign=PeerAssignsGroups.objects.filter(peergrade_id=created_peer.peergrade_id, assigned_stud_id=pk)
                    all_marks=[]
                    for k in peer_assign:
                        if k.marks:
                            all_marks.append(k.marks)
                        else:
                            all_marks=[]
                            break
                    if all_marks and j.marksbyteacher:
                        print(all_marks, " . ", j.marksbyteacher)
                        group_peer_marks.append([i.gpeer_name, (sum(all_marks)+j.marksbyteacher*4)/(len(all_marks)+4)])
                    else:
                        group_peer_marks.append([i.gpeer_name, ""])
                if not j.submit_file:
                    group_peer_grading.append([i.gpeer_name, i.gpeer_due])
                break
    return render(request, 'Student/analytics.html', {'pk': pk, 'pk2': pk2, 'class_info': class_info, 'final_data': final_data, 'total_lecs': total_lecs, 'attended': sum(final_data), 'perct': perct, 'assign': academics, 'quiz': marks_quiz, 'pending_assignments': pending_assignments, 'pending_quiz': pending_quiz, 'group_peer_grading': group_peer_grading, 'group_peer_marks': group_peer_marks})