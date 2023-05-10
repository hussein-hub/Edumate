import calendar
from datetime import date
from datetime import datetime, timedelta
import time
import cv2
from django.shortcuts import get_object_or_404, render
import string, random
from django.http import FileResponse, Http404, HttpResponseRedirect, StreamingHttpResponse
from django.urls import reverse

from Edumate_app.models import Students, Teachers
from Student.models import ClassStudents, SubmittedAssignments,  Quiz_marks, Progress
from Teacher.forms import EventForm
from .models import *
import random
import copy
from django.shortcuts import redirect, render

from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar, gen_bounding_boxes
import requests
from django.contrib import messages

from PyPDF2 import PdfReader
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer
import numpy as np
from huggingface_hub import from_pretrained_keras
from keras.models import load_model
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from json import dumps

import os
from pathlib import Path
# from decouple import config

from dotenv import load_dotenv
load_dotenv()

import json
import hashlib
import hmac
from collections import OrderedDict


def get_viewer_url_signature(account_id, auth_token, identifier, valid_until_timestamp):
    policy = (str(account_id), str(identifier), int(valid_until_timestamp))
    
    # Alternatively, policy as an ordered object.
    policy = OrderedDict((
        ('account_id', str(account_id)),
        ('identifier', str(identifier)),
        ('valid_until', int(valid_until_timestamp)),
    ))
    json_policy = json.dumps(policy, separators=(',', ':'))
    return hmac.new(key=auth_token.encode('utf-8'), msg=json_policy.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()


capture = 0
frame = None

# Create your views here.
#similarity_sentence_transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
model = load_model(os.path.join('./Teacher/static/Teacher',"model.h5"))

def teach_home(request, pk):
    teacher_c = Teachers.objects.get(teach_id=pk)
    class_data = ClassTeachers.objects.filter(teach_id=pk)
    studs=[]
    for i in class_data:
        studs.append(len(ClassStudents.objects.filter(class_code=i.class_code)))
    if(request.method=="POST"):
        class_room=ClassTeachers()
        class_room.teach_id=Teachers.objects.get(teach_id=pk)
        class_room.class_name=request.POST.get('name')
        class_room.class_code=str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 6)))
        class_room.save()
        return redirect('teacher_home', pk=pk)
    return render(request, 'Teacher/teacher_home.html', {'class_data': zip(class_data, studs), 'teacher': teacher_c, 'pk': pk})

def deleteclass(request, pk):
    if request.method == "POST":
        ClassTeachers.objects.get(class_code=request.POST['class_code']).delete()
        return JsonResponse({'info': 'succ'})

def all_students(request, pk, pk2):
    all_studs=ClassStudents.objects.filter(class_code=pk2)
    if request.method=="POST":
        ClassStudents.objects.get(stud_id=request.POST.get('stud_id'), class_code=pk2).delete()
        return redirect('all_students', pk=pk, pk2=pk2)
    return render(request, 'Teacher/all_students.html', {'pk': pk, 'pk2': pk2, 'all_studs': all_studs})

def classroom(request, pk, pk2):

    classroomName = ClassTeachers.objects.get(class_code=pk2).class_name
    if(request.method=="POST"):
        assignment=Assignments()
        assignment.assignment_name=request.POST.get('name')
        assignment.assignment_description=request.POST.get('description')
        assignment.class_code=ClassTeachers.objects.get(class_code=pk2)
        assignment.max_marks=request.POST.get('marks')
        assignment.duedate=request.POST.get('duedate')
        if request.POST.get('peer')=="on":
            assignment.peer_grade=True
        else:
            assignment.peer_grade=False
        assignment.save()
        if assignment.peer_grade:
            peers=Peergrade()
            peers.class_code=assignment.class_code
            peers.assignment_id=assignment
            peers.number_of_peers=request.POST.get('numpeers')
            peers.save()
        return redirect('classroom', pk=pk, pk2=pk2)
    a=Assignments.objects.filter(class_code=pk2).order_by('-duedate')
    assign = []
    studs=[]
    class_data = ClassTeachers.objects.filter(teach_id=pk)
    for i in class_data:
        studs.append(len(ClassStudents.objects.filter(class_code=i.class_code)))
    totalStudents = studs[0]
    studs = []
    for i in a:
        s = SubmittedAssignments.objects.filter(assignment_id=i.assignment_id)
        assign.append([i, len(s)])
        strength=len(ClassStudents.objects.filter(class_code=pk2))
        studs.append(strength-len(s))
    total_studs_value=len(ClassStudents.objects.filter(class_code=pk2))
    return render(request, 'Teacher/classroom.html', {'assign': zip(assign, studs), 'pk': pk, 'pk2': pk2, 'total': total_studs_value, 'classroomName': classroomName})

def assignmentsub(request, pk, pk2, pk3):
    submitted_assignments = SubmittedAssignments.objects.filter(assignment_id=pk3)
    all_students = ClassStudents.objects.filter(class_code=pk2)
    students_not_submitted = []
    submitted_assignments_ids = [i.stud_id for i in submitted_assignments]
    for i in all_students:
        if i.stud_id not in submitted_assignments_ids:
            students_not_submitted.append(i)
    submitted=SubmittedAssignments.objects.filter(assignment_id=pk3)
    assign_grade=Assignments.objects.filter(assignment_id =pk3)
    lateSubmissions = [False for i in range(len(submitted))]
    k = 0
    for i in submitted:
        if timezone.localtime(i.sub_date) > timezone.localtime(assign_grade[0].duedate):
            lateSubmissions[k] = True  
        k += 1
    assign_flag=assign_grade[0].peer_grade
    submittedAssignmentData = []
    for i in range(len(submitted)):
        submittedAssignmentData.append([submitted[i], lateSubmissions[i]])
    # sort submittedAssignmentData by the second element of each sublist
    submittedAssignmentData.sort(key=lambda x: x[1])
    calc_assign=Assignments.objects.get(assignment_id=pk3)
    final_assigns=[]
    assign_map={}
    num_pee=0
    is_create="Y"
    quest_and_ans=[]
    ans_options=[]
    if calc_assign.peer_grade:
        temp_peer=Peergrade.objects.get(class_code=pk2, assignment_id=pk3)
        temp_check=PeerAssigns.objects.filter(peergrade_id=temp_peer.peergrade_id)
        num_pee=temp_peer.number_of_peers
        if temp_check:
            is_create="X"
            quest_and_ans=temp_peer.questions.split("*")
            ans_options.append(temp_peer.opt1.split("*"))
            ans_options.append(temp_peer.opt2.split("*"))
            ans_options.append(temp_peer.opt3.split("*"))
            for i in temp_check:
                if i.stud_id in assign_map:
                    assign_map[i.stud_id].append(i)
                else:
                    assign_map[i.stud_id]=[i]
    if(request.method=="POST"):
        pet=Peergrade.objects.get(class_code=pk2, assignment_id=pk3)
        pe=PeerAssigns.objects.filter(peergrade_id=pet.peergrade_id)
        sub_stud=SubmittedAssignments.objects.filter(assignment_id=pk3)
        studs=ClassStudents.objects.filter(class_code=pk2)
        num_peers=pet.number_of_peers
        student_list=[]
        for i in studs:
            student_list.append(i.stud_id.stud_id)
        peer_dict = {}
        for i in student_list:
            peer_dict[i]=[]
        b=num_peers*student_list
        random.shuffle(b)
        count=len(b)
        i=0
        j=0
        another_count=0
        while(count!=0):
            if b[j]!=student_list[i] and b[j] not in peer_dict[student_list[i]]:
                peer_dict[student_list[i]].append(b[j])
                b.remove(b[j])
                count=count-1
                if len(peer_dict[student_list[i]])==num_peers:
                    i=i+1
                    random.shuffle(b)
                    another_count=0
            if(len(b)==0):
                break
            j=(j-1)%len(b)
            if j==0:
                another_count=another_count+1
            if(another_count==2):
                b=num_peers*student_list
                i=0
                j=0
                count=len(b)
                another_count=0
                random.shuffle(b)
                for k in student_list:
                    peer_dict[k]=[]
        for i in peer_dict.keys():
            for j in peer_dict[i]:
                p_as_ings=PeerAssigns()
                p_as_ings.peergrade_id=pet
                p_as_ings.stud_id=Students.objects.get(stud_id=i)
                p_as_ings.assigned_stud_id=Students.objects.get(stud_id=j)
                p_as_ings.save()
        ques1=request.POST.get('ques1')
        ques2=request.POST.get('ques2')
        ques3=request.POST.get('ques3')
        opt11=request.POST.get('opt11')
        opt12=request.POST.get('opt12')
        opt13=request.POST.get('opt13')
        opt21=request.POST.get('opt21')
        opt22=request.POST.get('opt22')
        opt23=request.POST.get('opt23')
        opt31=request.POST.get('opt31')
        opt32=request.POST.get('opt32')
        opt33=request.POST.get('opt33')
        final_ques=ques1+"*"+ques2+"*"+ques3
        final_opt1=opt11+"*"+opt12+"*"+opt13
        final_opt2=opt21+"*"+opt22+"*"+opt23
        final_opt3=opt31+"*"+opt32+"*"+opt33
        pet.questions=final_ques
        pet.opt1=final_opt1
        pet.opt2=final_opt2
        pet.opt3=final_opt3
        pet.save()
        return redirect('assignmentteach', pk=pk, pk2=pk2, pk3=pk3)
    return render(request, 'Teacher/show_assignments.html', {'submit': submittedAssignmentData, 'pk': pk, 'pk2': pk2 ,'pk3': pk3, 'peerf': assign_flag, 'students_not_submitted': students_not_submitted, 'peer': assign_map, 'num': range(num_pee), 'is_create': is_create, 'quest_and_ans': zip(quest_and_ans, ans_options)})

def details(request, pk, pk2, pk3):
    pet=Peergrade.objects.get(class_code=pk2, assignment_id=pk3)
    pe=PeerAssigns.objects.filter(peergrade_id=pet.peergrade_id)
    if len(pe)>0:
        return JsonResponse({'message': 'P'})
    sub_stud=SubmittedAssignments.objects.filter(assignment_id=pk3)
    studs=ClassStudents.objects.filter(class_code=pk2)
    if(len(sub_stud)!=len(studs)):
        return JsonResponse({'message': 'S'})
    return JsonResponse({'message': 'X'})

def assignmentdelete(request, pk, pk2):
    Assignments.objects.get(assignment_id=request.POST.get('assignment_id')).delete()
    return redirect('classroom', pk=pk, pk2=pk2)

def viewgrades(request, pk, pk2, pk3):
    all_submit=SubmittedAssignments.objects.filter(assignment_id=pk3)
    assignment=Assignments.objects.get(assignment_id=pk3)
    final_list=[]
    for i in all_submit:
        data={}
        data['name']=i.stud_id.name
        if assignment.peer_grade:
            peergrade=Peergrade.objects.get(assignment_id=pk3)
            membs=PeerAssigns.objects.filter(peergrade_id=peergrade.peergrade_id, assigned_stud_id=i.stud_id.stud_id)
            temp_marks=0
            for j in membs:
                if j.marks:
                    temp_marks=temp_marks+float(j.marks)
                else:
                    temp_marks="X"
                    break
            if i.marks and temp_marks!="X":
                temp_marks=temp_marks+float(i.marks)*4
            if temp_marks!="X":
                temp_marks=temp_marks/(peergrade.number_of_peers + 4)
            data['marks']=temp_marks
        else:
            if i.marks:
                data['marks']=i.marks
            else:
                data['marks']="Y"
        if i.sub_date > assignment.duedate:
            data['status']="L"
        else:
            data['status']="O"
        final_list.append(data)
    return render(request, 'Teacher/viewgrades.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'all_submit': final_list, 'assignment': assignment})

def assignmentgrade(request, pk, pk2, pk3,pk4):
    submitted=SubmittedAssignments.objects.get(assignment_id=pk3,stud_id = pk4)
    assignment=Assignments.objects.get(assignment_id=pk3)
    stud = Students.objects.get(stud_id = pk4)
    file_url = "http://127.0.0.1:8000"+submitted.assign_file.url
    final_peer=[]
    if assignment.peer_grade:
        pet=Peergrade.objects.get(class_code=pk2, assignment_id=pk3)
        final_peer=PeerAssigns.objects.filter(peergrade_id=pet.peergrade_id, assigned_stud_id=pk4)
    if request.method=="POST":
        if(float(request.POST.get('marks')) <= float(assignment.max_marks)):
            submitted.marks=request.POST.get('marks')
            submitted.save()
            messages.error(request, "Marks updated successfully")
            return redirect('grade', pk=pk, pk2=pk2, pk3=pk3, pk4=pk4)
        else:
            messages.error(request, "Marks cant be greater than maximum marks")
            return redirect('grade', pk=pk, pk2=pk2, pk3=pk3, pk4=pk4)
    return render(request, 'Teacher/grade_assignments.html', {'student_name':stud.name,'file':file_url,'submit': submitted, 'pk': pk, 'pk2': pk2, 'pk3': pk3,'assign': assignment, 'peers': final_peer})

def announcement(request, pk, pk2):
    if (request.method == 'POST'):
        announcement = Announcements()
        announcement.announce_data = request.POST.get('announce_data')
        announcement.teach_id = Teachers.objects.get(teach_id=pk)
        announcement.class_code = ClassTeachers.objects.get(class_code=pk2)
        announcement.save()
        return redirect('announcementteach', pk=pk, pk2=pk2)
    announcement_data = Announcements.objects.filter(class_code = pk2).order_by('-date')
    return render(request, 'Teacher/announcement_teach.html', {'pk': pk, 'pk2': pk2, 'announcement_data': announcement_data})

def ann_delete(request, pk, pk2):
    delAnnouncement = Announcements.objects.get(ann_id=request.POST.get('ann_id'))
    delAnnouncement.delete()
    return redirect('announcementteach', pk=pk, pk2=pk2)

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
        # context['pk'] = pk1
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

def event(request,pk, pk2, id=None):
    instance = Schedule()
    if id:
        instance = get_object_or_404(Schedule, pk=id)
    else:
        instance = Schedule()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():

        eform = form.save(commit = False)
        eform.teach_id = Teachers.objects.get(teach_id=pk)
        eform.class_code = ClassTeachers.objects.get(class_code=pk2)
        eform.save()
        return redirect('schedule', pk=pk, pk2=pk2)
        # return HttpResponseRedirect(reverse('schedule', args=(instance.teach_id,instance.class_code)))
    return render(request, 'Teacher/event.html', {'form': form,'pk1':pk,'pk2':pk2, 'pk': pk})

def create_quiz(request, pk, pk2):
    '''
    Function to create quiz for a particular classroom with id = pk2
    rdc = number of options per question
    Data Sent to DB = {
        pk [teacher id],
        pk2 [classroom id / classCode],
        Quiz Name,
        Quiz Time,
        Question + Answer [for all the questions in the quiz] --> multiple values for single quiz,
    }
    '''   
    if request.POST:

        quizName = request.POST.get('quiz_name')
        quizdate = request.POST.get('quiz_date')
        quizTime = request.POST.get('quiz_time')
        count = request.POST.get('question_count')
        description = request.POST.get('desc')
        c = request.POST.get('radio_count')
        rdc = request.POST.get('rdc')
        rdc = rdc.split(",")
        finalRdc = []
        for i in range(0, len(rdc)-1, 2):
            finalRdc.append([rdc[i], rdc[i+1]])
        print(f"Finalrdc : {finalRdc}")
        secondValues = []
        for i in range(len(finalRdc)):
            secondValues.append(finalRdc[i][1])
        count, c = int(count), int(c)
        allRadioButtonState = []
        questions = []
        options = []
        correctOP = []
        print("secondvalue: " + str(secondValues))
        for i in finalRdc:
            val = request.POST.get('question' + i[0])
            questions.append(val)
            # op = request.POST.getlist('option'+ i[0])
            # options.append(op)
            temp = []
            opTemp = []
            radioTemp = []
            for j in range(1, int(i[1])+1):
                op = request.POST.get('option'+ i[0] + str(j))
                opTemp.append(op)
                rd = request.POST.get('acoption'+ i[0] + str(j))
                if rd == 'on':
                    temp.append(j)
                radioTemp.append(rd)
            options.append(opTemp)
            allRadioButtonState.append(radioTemp)
            correctOP.append(temp)
        # print(quizName)
        # print(quizTime)
        # print(allRadioButtonState)
        # print(questions)
        # print(options)
        # print(correctOP)
        quiz_object = Quiz(quiz_name = quizName, description = description, time_limit = quizTime,quiz_date = quizdate, teach_id = Teachers.objects.get(teach_id=pk), class_code = ClassTeachers.objects.get(class_code=pk2))
        quiz_object.save()
        markForEachQuestion = 1

        

        for i in range(len(questions)):
            question_object = Question(quiz = quiz_object, question_name = questions[i], marks = markForEachQuestion)
            question_object.save()

            img = request.FILES.getlist('question_img' + str(i+1))
            for j in img:
                img_object = QuestionImage(question = question_object, image = j)
                img_object.save()
            
            k = 0
            for j in options[i]:
                if k+1 in correctOP[i]:
                    # if correctOP[i][0]-1 == options[i].index(j):
                    option_object = Options(question = question_object, option_name = j, correct = True)
                    option_object.save()
                else:
                    option_object = Options(question = question_object, option_name = j, correct = False)
                    option_object.save()
                k += 1
        return redirect('create_quiz', pk=pk, pk2=pk2)
        
    allQuiz = Quiz.objects.filter(teach_id = pk, class_code = pk2)

    return render(request, 'Teacher/createQuiz.html', {'pk': pk, 'pk2': pk2, 'allQuiz': allQuiz})


def attendance(request, pk, pk2):
    global model
    all_att = Attendance.objects.filter(teacher_id=pk, class_id=pk2).order_by('-att_id')
    nums_studs_present=[]
    attdates=[]
    total_num = len(ClassStudents.objects.filter(class_code=pk2))
    for i in all_att:
        date_single = parse_datetime(i.start_time)
        attdates.append(date_single)
        single_num = len(AttStud.objects.filter(att_id=i.att_id))
        percent = (single_num / total_num) * 100
        nums_studs_present.append([single_num, percent])
    if request.method=="POST":
        new_att=Attendance()
        new_att.teacher_id=Teachers.objects.get(teach_id=pk)
        new_att.class_id=ClassTeachers.objects.get(class_code=pk2)
        new_att.start_time=request.POST.get('atttimes')
        new_att.end_time=request.POST.get('atttimee')
        new_att.code=str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 6)))
        new_att.save()
        att_list = request.FILES.getlist('attimg')
        count = 0
        image_folder_name = str(att_list[0]).split('.')[0]
        for i in att_list:
            attimg = Attendance_images()
            attimg.att_id = new_att
            attimg.att_image = i
            attimg.save()
            temp_i = str(i)
            count = gen_bounding_boxes(image_folder_name,temp_i,model,count)
        

        messages.success(request, 'Attendance created and code is = '+new_att.code)
        return redirect('attendance', pk=pk, pk2=pk2)
    return render(request, 'Teacher/attendance.html', {'pk': pk, 'pk2': pk2, 'all_att': zip(all_att, attdates, nums_studs_present)})

def deleteatt(request, pk, pk2):
    if request.method=="POST":
        Attendance.objects.get(att_id=request.POST.get('att_id')).delete()
        return redirect('attendance', pk=pk, pk2=pk2)

# def video_feed(request, pk):
#     return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

# def gen_frames():
#     camera = cv2.VideoCapture(0)

#     global capture,frame
#     while True:
#         success, frame = camera.read()
#         if success:
#             try:
#                 ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
#                 frame = buffer.tobytes()
#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                
#             except Exception as e:
#                 pass
#         else:
#             pass       

def view_att(request, pk, pk2, pk3):
    all_att_id=AttStud.objects.filter(att_id=pk3)
    all_att=[]
    att_obj = Attendance.objects.get(att_id=pk3)
    mainAttObj = Attendance_images.objects.filter(att_id=att_obj.att_id)
    all_a_images = [i.att_image.url.split('/')[0] + '/' + i.att_image.url.split('/')[1] + '/' + 'a' + i.att_image.url.split('/')[2] for i in mainAttObj]
    all_small_images = []
    all_small_uncropped_images = []
    for i in mainAttObj:
        folname = "."+i.att_image.url.split('/')[0] + '/' + i.att_image.url.split('/')[1] + '/' + mainAttObj[0].att_image.url.split('/')[2].split('.')[0] +'/'+ i.att_image.url.split('/')[2].split('.')[0]+"/"
        for j in os.listdir(folname):
            all_small_images.append(folname+j)
    
    folname = "."+i.att_image.url.split('/')[0] + '/' + i.att_image.url.split('/')[1] + '/'+ mainAttObj[0].att_image.url.split('/')[2].split('.')[0] +'/'
    for i in os.listdir(folname):
        if os.path.isfile(folname+i):
            all_small_uncropped_images.append(folname+i)
    
    print(all_small_uncropped_images)
    all_studs=ClassStudents.objects.filter(class_code=pk2)
    att_ids=[]
    cropped_image_att = []
    for i in all_att_id:
        indi_cropped_image_att = {}
        val={}
        if i.is_cropped:
            indi_cropped_image_att['name'] = i.stud_id.name
            indi_cropped_image_att['time'] = i.att_time
            indi_cropped_image_att['att_id'] = i.att_id.att_id
            indi_cropped_image_att['stud_id'] = i.stud_id.stud_id
            indi_cropped_image_att['is_approved'] = True
            indi_cropped_image_att['is_cropped'] = True
            for j in all_small_images:
                if i.img_number == int(j.split('/')[-1].split('.')[0]):
                    indi_cropped_image_att['image'] = j[1:]
                    break
            cropped_image_att.append(indi_cropped_image_att)
        else:
            val['name']=i.stud_id.name
            val['time']=i.att_time
            val['att_id']=i.att_id.att_id
            val['stud_id']=i.stud_id.stud_id
            val['is_approved']= True
            val['is_cropped'] = i.is_cropped
            for j in all_small_uncropped_images:
                if i.img_number == int(j.split('/')[-1].split('.')[0]):
                    val['image'] = j[1:]
                    break
            all_att.append(val)
        att_ids.append(i.stud_id.stud_id)
    stud_ids=[]
    for i in all_studs:
        stud_ids.append(i.stud_id.stud_id)
    all_stud_names_ids=[]
    for i in stud_ids:
        if i not in att_ids:
            try:
                stud=Students.objects.get(stud_id=i)
                single_stud={'stud_id': i, 'name': stud.name}
                all_stud_names_ids.append(single_stud)
            except:
                continue
    # print(all_stud_names_ids)
    if request.method == "POST":
        if 'student_id' in request.POST:
            if request.POST['student_id']=="none":
                messages.error(request, "Please select a valid option")
                return redirect('viewatt', pk=pk, pk2=pk2, pk3=pk3)
            tem=request.POST['student_id'].split("(")
            tem=tem[-1]
            tem=tem.split(")")
            temp=AttStud.objects.filter(att_id=pk3, stud_id=int(tem[0]))
            if len(temp)>0:
                messages.error(request, "Attendance already marked")
                return redirect('viewatt', pk=pk, pk2=pk2, pk3=pk3)
            att=AttStud()
            att.att_id=Attendance.objects.get(att_id=pk3)
            att.stud_id=Students.objects.get(stud_id=int(tem[0]))
            att.att_time=str(datetime.now())
            att.img_number=-1
            att.save()
            return redirect('viewatt', pk=pk, pk2=pk2, pk3=pk3)
        AttStud.objects.get(att_id=request.POST['att_id'], stud_id=request.POST['stud_id']).delete()
        messages.error(request, "Deleted successfully")
        return redirect('viewatt', pk=pk, pk2=pk2, pk3=pk3)
    return render(request, 'Teacher/view_att.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'all_att': all_att, 'all_stud': all_stud_names_ids, 'cropped_image_att': cropped_image_att, 'all_a_images': all_a_images})

def quiz_info(request, pk, pk2, pk3):
    quiz = Quiz.objects.get(id = pk3)
    quiz_responses = Quiz_marks.objects.filter(quiz = quiz)
    quiz_resp=[]
    for i in quiz_responses:
        quiz_resp.append(i.student_id)

    class_students = ClassStudents.objects.filter(class_code = pk2)
    answered_students = []
    stud_length = len(quiz_responses)
    not_answered_students = []
    for i in class_students:
        student = Students.objects.get(stud_id = i.stud_id.stud_id)
        if i.stud_id.stud_id in quiz_resp:
            quiz_marks = Quiz_marks.objects.get(quiz = quiz, student_id = i.stud_id.stud_id)
            answered_students.append(quiz_marks)

            # quiz_responses.append(student)
        else:
            not_answered_students.append(student)
    # print(answered_students)
    return render(request, 'Teacher/individual_quiz.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'quiz_responses': answered_students,'stud_length':stud_length, 'not_answered_students': not_answered_students})

def assignmentSimilarityCheck(request, pk, pk2, pk3):
    #global similarity_sentence_transformer_model
    data = []
    plag = []
    checkedAssignments = Plagarism.objects.filter(assignment_id = pk3)
    checkedAssignmentsLength = len(checkedAssignments)
    assignments = SubmittedAssignments.objects.filter(assignment_id=pk3)
    assignmentsLength = len(assignments)
    assignments = SubmittedAssignments.objects.filter(assignment_id=pk3)
    # data = []
    for i in assignments:
        student = Students.objects.filter(stud_id=i.stud_id.stud_id)
        data.append([i, student])

    all_assignments = SubmittedAssignments.objects.filter(assignment_id = pk3)
    files = []
    students = []
    for i in all_assignments:
        files.append(i.assign_file.url)
        students.append(i.stud_id.stud_id)
    if checkedAssignmentsLength == int((assignmentsLength * (assignmentsLength - 1)) / 2):
        print()
    else:
        files_text = getTextFromPDF(files)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(files_text).toarray()
        similarities = predict_similarity(tfidf_matrix,students)
        # print(similarities)
        for j in similarities:
            # print(j)
            plag = Plagarism()
            plag.assignment_id = Assignments.objects.get(assignment_id = pk3)
            plag.percentage_similarity = j['similarity_score']
            plag.stud_assignment1 = SubmittedAssignments.objects.get(stud_id=j['stud_1'], assignment_id=pk3)
            plag.stud_assignment2 = SubmittedAssignments.objects.get(stud_id=j['stud_2'], assignment_id=pk3)
            plag.save()
        for row in Plagarism.objects.all().reverse():
            if Plagarism.objects.filter(id=row.id).count() > 1:
                row.delete()
        plag = Plagarism.objects.filter(assignment_id = pk3)
        for i in plag:
            docUID = getUniqueDocumentID([i.stud_assignment1.assign_file.url, i.stud_assignment2.assign_file.url])
            valid_until = int(time.time() + 30 * 86400 )
            valid_until_time = valid_until
            uniqueID = DocumentUniqueID()
            uniqueID.plagarism_id = Plagarism.objects.get(id = i.id)
            uniqueID.doc_unique_id = docUID
            uniqueID.valid_until = valid_until_time
            uniqueID.url = "https://api.draftable.com/v1/comparisons/viewer/" + os.getenv("ACCOUNT_ID") + "/" + str(uniqueID.doc_unique_id) + "?valid_until=" + str(valid_until_time) + "&signature=" + str(get_viewer_url_signature(os.getenv("ACCOUNT_ID"), os.getenv("AUTH_TOKEN"), docUID, valid_until))
            uniqueID.save()
    plag = Plagarism.objects.filter(assignment_id = pk3)
    uniqueDocumentIDs = DocumentUniqueID.objects.filter(plagarism_id__assignment_id = pk3)
    plagarismData = []
    for i in range(len(uniqueDocumentIDs)):
        plagarismData.append([plag[i], uniqueDocumentIDs[i]])
    return render(request, 'Teacher/assignmentSimilarityCheck.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'assignments': data, 'plagData': plagarismData})

def getUniqueDocumentID(filePaths):
    url = "https://api.draftable.com/v1/comparisons"
    payload={'identifier': '',
    'left.display_name': '',
    'left.file_type': 'pdf',
    'right.display_name': '',
    'right.file_type': 'pdf',
    'public': 'false'}
    files=[
    ('left.file',(filePaths[0].split("/")[-1],open(filePaths[0][1:],'rb'),'application/pdf')),
    ('right.file',(filePaths[1].split("/")[-1],open(filePaths[1][1:],'rb'),'application/pdf'))
    ]
    headers = {
    'accept': 'application/json',
    'Authorization': f'Token {os.getenv("AUTH_TOKEN")}',
    # 'Cookie': os.getenv("COOKIE")
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response.json()['identifier']


def preprocess_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove non-alphabetic characters and other special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Convert the text to lowercase
    text = text.lower()
    
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Join the tokens back into a string
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text

def getTextFromPDF(files):
    data = []
    for f in files:
        # print(f)
        reader = PdfReader("." + f)

        header = os.path.commonprefix([i.extract_text() for i in reader.pages])
        pages = []

        for i in reader.pages:
            pages.append(preprocess_text(i.extract_text()[len(header):]))

        text = ' '.join(pages)
        data.append(text)

    return data

def predict_similarity(embeddings,students):
    similarities = []
    scores = cosine_similarity(embeddings)
    for i in range(len(embeddings)):
        for j in range(len(embeddings)):
            if i>=j:
                continue
            similarities.append({'stud_1':students[i],'stud_2':students[j],'similarity_score':scores[i][j]*100})
            # similarities.append({'stud_1':students[j],'stud_2':students[i],'similarity_score':score})
    return similarities

def projecttracking(request, pk, pk2):
    all_projs = Project.objects.filter(class_code=pk2)
    allstuds=ClassStudents.objects.filter(class_code=pk2)
    if request.method == "POST":
        proj = Project()
        proj.class_code=ClassTeachers.objects.get(class_code=pk2)
        proj.proj_name = request.POST.get('name')
        proj.proj_desc = request.POST.get('desc')
        proj.proj_due = request.POST.get('duedate')
        proj.prog_check = request.POST.get('proj_checks')
        proj.num_studs = request.POST.get('num_studs')
        proj.save()
        groups = []
        for i in range(len(allstuds)//int(proj.num_studs)):
            group=Groups()
            group.pro_id=proj
            group.save()
            groups.append(group)
        count=0
        for i in allstuds:
            member=Members()
            member.group_id=groups[count]
            member.stud_id=i.stud_id
            member.save()
            count=count+1
            if(count==len(groups)):
                count=0
        return redirect('projecttracking', pk=pk, pk2=pk2)
    return render(request, 'Teacher/projecttracking.html', {'pk': pk, 'pk2': pk2, 'all_projs': all_projs})

def deletepro(request, pk, pk2):
    if request.method == "POST":
        Project.objects.get(pro_id=request.POST.get('pro_id')).delete()
        return redirect('projecttracking', pk=pk, pk2=pk2)

def fetchcheck(request, pk, pk2):
    pro=Project.objects.get(pro_id=request.GET.get('pro_id'))
    checkpointsc = pro.prog_check.split("*")
    return JsonResponse({'name': pro.proj_name, 'checks': pro.prog_check, 'points': checkpointsc})

def view_groups(request, pk, pk2, pk3):
    pro=Project.objects.get(pro_id=pk3)
    groups = Groups.objects.filter(pro_id=pk3)
    student_names = []
    progressval = []
    for i in groups:
        members=Members.objects.filter(group_id=i.group_id)
        temp = []
        for j in members:
            temp.append(j.stud_id.name)
        student_names.append(temp)
        prog=Progress.objects.filter(group_id=i.group_id)
        if prog:
            total=pro.prog_check.split("\r")
            count=0
            for j in prog[0].prog:
                if j=="a":
                    count=count+1
            progressval.append([((count/len(total))*100), ((count/len(total))*100)*2.55])
        else:
            progressval.append([0, 0])
    return render(request, 'Teacher/view_group.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'groups': zip(groups, progressval, student_names)})

def group_details(request, pk, pk2, pk3, pk4):
    project=Project.objects.get(pro_id=pk3)
    group=Groups.objects.get(group_id=pk4)
    members=Members.objects.filter(group_id=pk4)
    pro=Progress.objects.filter(group_id=pk4)
    progress=None
    if pro:
        progress=list(pro[0].prog)
    else:
        progress=list("b"*len(project.prog_check.split('\r')))
    return render(request, 'Teacher/group_details.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'pk4': pk4, 'members': members, 'progress': progress, 'project': project, 'progr': zip(project.prog_check.split('\r'), progress)})

def grouppeergrading(request, pk, pk2):
    all_g_assigns=Grouppeers.objects.filter(class_code=pk2).order_by('-created_date')
    if request.method=="POST":
        group=Grouppeers()
        group.class_code=ClassTeachers.objects.get(class_code=pk2)
        group.gpeer_name=request.POST.get('name')
        group.gpeer_desc=request.POST.get('desc')
        group.gpeer_due=request.POST.get('duedate')
        group.num_studs=request.POST.get('num_studs')
        group.marks=request.POST.get('marks')
        group.num_peers=request.POST.get('num_peers')
        group.save()
        allstuds=ClassStudents.objects.filter(class_code=pk2)
        all_groups=[]
        for i in range(len(allstuds)//int(group.num_studs)):
            pgroup=PeerGroups()
            pgroup.gro_id=group
            pgroup.save()
            all_groups.append(pgroup)
        count=0
        for i in allstuds:
            member=Peermembers()
            member.pgro_id=all_groups[count]
            member.stud_id=i.stud_id
            member.save()
            count=count+1
            if(count==len(all_groups)):
                count=0
        return redirect('grouppeergrading', pk=pk, pk2=pk2)
    return render(request, 'Teacher/grouppeergrading.html', {'pk': pk, 'pk2': pk2, 'all_groups': all_g_assigns})

def delgroup(request, pk, pk2):
    if request.method=="POST":
        Grouppeers.objects.get(gro_id=request.POST.get('gro_id')).delete()
        return JsonResponse({'message': 'deleted'})

def showpeergroups(request, pk, pk2, pk3):
    all_groups=PeerGroups.objects.filter(gro_id=pk3)
    assignment=Grouppeers.objects.get(gro_id=pk3)
    submitted=[]
    not_submitted=[]
    late=[]
    flag=True
    for i in all_groups:
        mems=Peermembers.objects.filter(pgro_id=i.group_id)
        if i.submit_file:
            submitted.append([i, mems])
            if i.submit_date > assignment.gpeer_due:
                late.append(i.group_id)
        else:
            not_submitted.append([i, mems, len(mems)])
            flag=False
    temppeer=PeergradeGroups.objects.filter(class_code=pk2, assignment_id=pk3)
    quest_and_ans=[]
    ans_options=[]
    questsadded=False
    assign_map={}
    temp_g_a_s={}
    for i in all_groups:
        membs=Peermembers.objects.filter(pgro_id=i.group_id)
        for j in membs:
            temp_g_a_s[j.stud_id.stud_id]=i.group_id
    if temppeer:
        flag=False
        quest_and_ans=temppeer[0].questions.split("*")
        ans_options.append(temppeer[0].opt1.split("*"))
        ans_options.append(temppeer[0].opt2.split("*"))
        ans_options.append(temppeer[0].opt3.split("*"))
        questsadded=True
        temp_peer=PeergradeGroups.objects.get(class_code=pk2, assignment_id=pk3)
        temp_check=PeerAssignsGroups.objects.filter(peergrade_id=temp_peer.peergrade_id)
        for i in temp_check:
            if i.stud_id in assign_map:
                assign_map[i.stud_id].append(i)
            else:
                assign_map[i.stud_id]=[temp_g_a_s[i.stud_id.stud_id], i]
    if request.method == "POST":
        student_list=[]
        group_and_studs={}
        for i in all_groups:
            membs=Peermembers.objects.filter(pgro_id=i.group_id)
            for j in membs:
                student_list.append(j.stud_id.stud_id)
                group_and_studs[j.stud_id.stud_id]=i.group_id
        num_peers=assignment.num_peers
        peer_dict = {}
        peer_dict2= {}
        for i in student_list:
            peer_dict[i]=[]
            peer_dict2[i]=[]
        b=num_peers*student_list
        random.shuffle(b)
        count=len(b)
        i=0
        j=0
        another_count=0
        while(count!=0):
            if (b[j]!=student_list[i]) and (b[j] not in peer_dict[student_list[i]]) and (group_and_studs[student_list[i]]!=group_and_studs[b[j]]) and (group_and_studs[b[j]] not in peer_dict2[student_list[i]]):
                peer_dict[student_list[i]].append(b[j])
                peer_dict2[student_list[i]].append(group_and_studs[b[j]])
                b.remove(b[j])
                count=count-1
                if len(peer_dict[student_list[i]])==num_peers:
                    i=i+1
                    random.shuffle(b)
                    another_count=0
            if(len(b)==0):
                break
            j=(j-1)%len(b)
            if j==0:
                another_count=another_count+1
            if(another_count==2):
                b=num_peers*student_list
                i=0
                j=0
                count=len(b)
                another_count=0
                random.shuffle(b)
                for k in student_list:
                    peer_dict[k]=[]
                    peer_dict2[k]=[]
        ques1=request.POST.get('ques1')
        ques2=request.POST.get('ques2')
        ques3=request.POST.get('ques3')
        opt11=request.POST.get('opt11')
        opt12=request.POST.get('opt12')
        opt13=request.POST.get('opt13')
        opt21=request.POST.get('opt21')
        opt22=request.POST.get('opt22')
        opt23=request.POST.get('opt23')
        opt31=request.POST.get('opt31')
        opt32=request.POST.get('opt32')
        opt33=request.POST.get('opt33')
        final_ques=ques1+"*"+ques2+"*"+ques3
        final_opt1=opt11+"*"+opt12+"*"+opt13
        final_opt2=opt21+"*"+opt22+"*"+opt23
        final_opt3=opt31+"*"+opt32+"*"+opt33
        peergr=PeergradeGroups()
        peergr.class_code=ClassTeachers.objects.get(class_code=pk2)
        peergr.assignment_id=assignment
        peergr.questions=final_ques
        peergr.opt1=final_opt1
        peergr.opt2=final_opt2
        peergr.opt3=final_opt3
        peergr.save()
        for i in peer_dict.keys():
            for j in peer_dict[i]:
                 new_assign=PeerAssignsGroups()
                 new_assign.peergrade_id=peergr
                 new_assign.stud_id=Students.objects.get(stud_id=i)
                 new_assign.assigned_stud_id=Students.objects.get(stud_id=j)
                 new_assign.group_id=PeerGroups.objects.get(group_id=group_and_studs[j])
                 new_assign.save()
        return redirect('showpeergroups', pk=pk, pk2=pk2, pk3=pk3)
    return render(request, 'Teacher/showpeer.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'submitted': submitted, 'not_submitted': not_submitted, 'late': late, 'flag': flag, 'quest_and_ans': zip(quest_and_ans, ans_options), 'ques': questsadded, 'num': range(assignment.num_peers), 'peer': assign_map})

def groupgrade(request, pk, pk2, pk3, pk4):
    assignment=Grouppeers.objects.get(gro_id=pk3)
    group=PeerGroups.objects.get(group_id=pk4)
    members=Peermembers.objects.filter(pgro_id=pk4)
    peergroup=PeergradeGroups.objects.filter(class_code=pk2, assignment_id=pk3)
    peers=[]
    if peergroup:
        peergroup=peergroup[0]
        for i in members:
            assigned=PeerAssignsGroups.objects.filter(peergrade_id=peergroup.peergrade_id, assigned_stud_id=i.stud_id.stud_id)
            peers.append([i, assigned])
    if request.method == "POST":
        marks=request.POST.get('marks')
        feedback=request.POST.get('feedback')
        if float(marks)>float(assignment.marks):
            messages.error(request, "Entered marks must be less than maximum marks")
        else:
            messages.error(request, "Marks and feedback saved successfully")
            group.marksbyteacher=float(marks)
            group.feedbackbyteacher=feedback
            group.save()
        return redirect('groupgrade', pk=pk, pk2=pk2, pk3=pk3, pk4=pk4)
    return render(request, 'Teacher/grouppeer_grade.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'pk4': pk4, 'group': group, 'members': members, 'assignment': assignment, 'peers': peers})

def view_grades(request, pk, pk2, pk3):
    assignment=Grouppeers.objects.get(gro_id=pk3)
    groups=PeerGroups.objects.filter(gro_id=pk3)
    all_submit=[]
    for i in groups:
        mems=Peermembers.objects.filter(pgro_id=i.group_id)
        for j in mems:
            data={}
            data['name']=j.stud_id.name
            data['group_id']=i.group_id
            if i.submit_file:
                if i.submit_date > assignment.gpeer_due:
                    data['date']="L"
                else:
                    data['date']="O"
            else:
                data['date']="Not Submitted"
            data['marks']="Y"
            if i.marksbyteacher:
                total_marks=float(i.marksbyteacher)*4
                peeron=PeergradeGroups.objects.filter(assignment_id=assignment.gro_id)
                if peeron:
                    peeron=peeron[0]
                    peermembr=PeerAssignsGroups.objects.filter(peergrade_id=peeron.peergrade_id, assigned_stud_id=j.stud_id.stud_id)
                    for k in peermembr:
                        if k.marks:
                            total_marks=total_marks+float(k.marks)
                        else:
                            total_marks="X"
                            break
                if total_marks != "X":
                    print(total_marks-i.marksbyteacher*4)
                    data['marks']=total_marks/(assignment.num_peers+4)
            all_submit.append(data)
    return render(request, 'Teacher/view_grades.html', {'pk': pk, 'pk2': pk2, 'pk3': pk3, 'assignment': assignment, 'all_submit': all_submit})

def teacher_analytics(request, pk, pk2):
    classroom=ClassTeachers.objects.get(class_code=pk2)
    attends=Attendance.objects.filter(class_id=pk2).order_by('-start_time')
    strength=len(ClassStudents.objects.filter(class_code=pk2))
    data=[]
    count=0
    total_classes=0
    atts=0
    for i in attends:
        n=len(AttStud.objects.filter(att_id=i.att_id))
        data.append([n, i.start_time[0:10]])
        total_classes=total_classes+1
        atts=atts+n/strength
        count=count+1
        if count == 7:
            break
    perct="X"
    if total_classes:
        perct=float(atts/total_classes)*100
    if count!=7:
        while count!=7:
            data.append([0, "None"])
            count=count+1
    data.reverse()
    all_assignments=Assignments.objects.filter(class_code=pk2).order_by('-duedate')
    total2=len(all_assignments)
    graph2_data=[]
    pending_tasks=[]
    for i in all_assignments:
        all_subm=SubmittedAssignments.objects.filter(assignment_id=i.assignment_id)
        count=0
        for j in all_subm:
            if not j.marks:
                count=count+1
        if count > 0:
            pending_tasks.append([i.assignment_name, count])
    print(pending_tasks)
    count=0
    per=0
    for i in all_assignments:
        n=len(SubmittedAssignments.objects.filter(assignment_id=i.assignment_id))
        graph2_data.append([i.assignment_name, n])
        per=per+n/strength
        count=count+1
        if count == 7:
            break
    perct2="X"
    if total2:
        perct2=float(per/total2)*100
    if count!=7:
        while count!=7:
            graph2_data.append(["None", 0])
            count=count+1
    graph2_data.reverse()
    group_peers=[]
    all_peers=Grouppeers.objects.filter(class_code=pk2)
    for i in all_peers:
        all_gs=PeerGroups.objects.filter(gro_id=i.gro_id)
        count=0
        for j in all_gs:
            if not j.marksbyteacher:
                count=count+1
        group_peers.append([i.gpeer_name, count])
    return render(request, 'Teacher/teacher_analytics.html', {'pk': pk, 'pk2': pk2, 'class_info': classroom, 'att_data': data, 'perct': perct, 'total': total_classes, 'graph2': graph2_data, 'total2': total2, 'perct2': perct2, 'pending': pending_tasks, 'groups': group_peers})

def logout(request, pk):
    request.session.flush()
    return redirect('home')


def checkpointsupdate(request, pk, pk2):
    if request.method == "POST":
        project = Project.objects.get(pro_id=request.POST.get('pro_id'))
        project.prog_check = request.POST.get('data')
        project.save()
        return JsonResponse({'status': 'success'})