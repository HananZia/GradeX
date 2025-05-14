import datetime
import json
import os

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from gradex_app.models import Staffs
from .models import Students, Subjects
from gradex_app.EmailBackEnd import EmailBackEnd
from gradex_app.models import CustomUser, Courses, SessionYearModel
from GradeX import settings
from .models import Courses


def showDemoPage(request):
    return render(request,"demo.html")

def ShowLoginPage(request):
    return render(request,"login_page.html")

# def doLogin(request):
#     if request.method!="POST":
#         return HttpResponse("<h2>Method Not Allowed</h2>")
#     else:
#         captcha_token=request.POST.get("g-recaptcha-response")
#         cap_url="https://www.google.com/recaptcha/api/siteverify"
#         cap_secret="6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"
#         cap_data={"secret":cap_secret,"response":captcha_token}
#         cap_server_response=requests.post(url=cap_url,data=cap_data)
#         cap_json=json.loads(cap_server_response.text)

#         if cap_json['success']==False:
#             messages.error(request,"Invalid Captcha Try Again")
#             return HttpResponseRedirect("/")

#         user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
#         if user!=None:
#             login(request,user)
#             if user.user_type=="1":
#                 return HttpResponseRedirect('/admin_home')
#             elif user.user_type=="2":
#                 return HttpResponseRedirect(reverse("staff_home"))
#             else:
#                 return HttpResponseRedirect(reverse("student_home"))
#         else:
#             messages.error(request,"Invalid Login Details")
#             return HttpResponseRedirect("/")

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>", status=405)
    
    captcha_token = request.POST.get("g-recaptcha-response")
    cap_url = "https://www.google.com/recaptcha/api/siteverify"
    cap_secret = "6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"  # It's better to store this in settings.py
    cap_data = {"secret": cap_secret, "response": captcha_token}
    
    # Send the request to Google for CAPTCHA verification
    cap_server_response = requests.post(url=cap_url, data=cap_data)
    cap_json = cap_server_response.json()  # Using .json() directly
    
    if not cap_json.get('success', False):
        messages.error(request, "Invalid Captcha. Please try again.")
        return redirect("/")  # Redirect to the same page with error message
    
    # Authenticate the user using the email and password
    user = authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
    
    if user is not None:
        login(request, user)
        
        # Redirect user based on their type
        if user.user_type == "1":
            return redirect('/admin_home')
        elif user.user_type == "2":
            return redirect(reverse("staff_home"))
        else:
            return redirect(reverse("student_home"))
    else:
        # Invalid login details, show error message
        messages.error(request, "Invalid login details. Please try again.")
        return redirect("/")  # Redirect to the login page with error message
    

def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "YOUR_API_KEY",' \
         '        authDomain: "FIREBASE_AUTH_URL",' \
         '        databaseURL: "FIREBASE_DATABASE_URL",' \
         '        projectId: "FIREBASE_PROJECT_ID",' \
         '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
         '        messagingSenderId: "FIREBASE_SENDER_ID",' \
         '        appId: "FIREBASE_APP_ID",' \
         '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")

def Testurl(request):
    return HttpResponse("Ok")

def signup_admin(request):
    return render(request,"signup_admin_page.html")

def signup_student(request):
    courses=Courses.objects.all()
    session_years=SessionYearModel.object.all()
    return render(request,"signup_student_page.html",{"courses":courses,"session_years":session_years})

def signup_staff(request):
    return render(request,"signup_staff_page.html")

def do_admin_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1)
        user.save()
        messages.success(request,"Successfully Created Admin")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Admin")
        return HttpResponseRedirect(reverse("show_login"))

def do_staff_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
        user.staffs.address=address
        user.save()
        messages.success(request,"Successfully Created Staff")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Staff")
        return HttpResponseRedirect(reverse("show_login"))

def do_signup_student(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    session_year_id = request.POST.get("session_year")
    course_id = request.POST.get("course")
    sex = request.POST.get("sex")

    profile_pic = request.FILES['profile_pic']
    fs = FileSystemStorage()
    filename = fs.save(profile_pic.name, profile_pic)
    profile_pic_url = fs.url(filename)

    #try:
    user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name,
                                    first_name=first_name, user_type=3)
    user.students.address = address
    course_obj = Courses.objects.get(id=course_id)
    user.students.course_id = course_obj
    session_year = SessionYearModel.objects.get(id=session_year_id)
    user.students.session_year_id = session_year
    user.students.gender = sex
    user.students.profile_pic = profile_pic_url
    user.save()
    messages.success(request, "Successfully Added Student")
    return HttpResponseRedirect(reverse("show_login"))
    #except:
    #   messages.error(request, "Failed to Add Student")
    #  return HttpResponseRedirect(reverse("show_login"))


def terms_of_service(request):
    return render(request, "hod_template/terms.html")

def privacy_policy(request):
    return render(request, "hod_template/privacy_policy.html")

def student_view_subjects(request):
    from gradex_app.models import Subjects
    subjects = Subjects.objects.all()
    return render(request, "student_template/student_view_subjects.html", {"subjects": subjects})


def delete_staff(request, id):  # Here, use `id` as the parameter
    staff = get_object_or_404(Staffs, id=id)
    user = staff.admin
    staff.delete()
    user.delete()  # Assuming Staff is linked to CustomUser via OneToOneField
    messages.success(request, "Staff deleted successfully.")
    return redirect('manage_staff')  # Adjust to your actual redirect URL

def manage_student(request):
    students = Students.objects.all()
    return render(request, 'manage_student.html', {'students': students})

def delete_student(request, id):
    try:
        # Get the student object
        student = get_object_or_404(Students, id=id)
        user = student.admin
        
        # Delete the student and the associated user
        student.delete()
        user.delete()
        
        messages.success(request, "Student deleted successfully.")
        
        # Redirect to the manage_students view
        return redirect('manage_student')
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('manage_student')
    

def delete_course(request, course_id):
    course = get_object_or_404(Courses, id=course_id)  # Using string for course_id
    course.delete()
    messages.success(request, "Course deleted successfully.")
    return redirect('manage_course')

def delete_subject(request, subject_id):
    subject = get_object_or_404(Subjects, id=subject_id)
    subject.delete()
    messages.success(request, "Subject deleted successfully.")
    return redirect('manage_subject')