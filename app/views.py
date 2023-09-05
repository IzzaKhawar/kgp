from django.shortcuts import render, redirect
from django.views import View
from . import models
from django.contrib import messages

# For Random Password
import names
import random
# For Date and Time
from datetime import datetime
# Create your views here.


class Signup_view(View):
    def get(self, request):
        try:
            rq_user = request.session.get("kfueit_username")
        except:
            pass
        if rq_user != None:
            return redirect('home')
        else:
            return render(request, 'signup.html')


    def post(self, request):
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        u = email.replace('@kfueit.edu.pk', '')
        username = u.lower()
        number_list = ['*', '!', '$', '&', '#', '=', '%', '+', '-', '_', '@']
        password = str(names.get_first_name()) + str(random.choice(number_list)) + str(
            random.randint(111, 999)) + str(random.choice(number_list))
        values = {
            'fname': fname,
            'lname': lname,
            'email': email,
        }
        re = email.endswith("@kfueit.edu.pk")
        if re:
            sign_up = models.SignUp(
                fname=fname,
                lname=lname,
                email=email,
                password=password,
                user_name=username,
            )
            error_msg = self.ValidateUser(sign_up)
            if not error_msg:
                sent = self.sendmail(email, username, password, fname, lname)
                if sent:
                    sign_up.register()
                    messages.success(request, 'username and password has been sent to your email. Check Inbox.')
                    return redirect('login')
                    # return render(request, 'login.html', {'msg': 'username and password has been sent to your email. Check Inbox.'})
                                
                else:
                    data = {
                        "error": "Enter a Valid email",
                        "values": values,
                    }
                    return render(request, 'signup.html', data)
            else:
                data = {
                    "error": error_msg,
                    "values": values,
                }
                return render(request, 'signup.html', data)
        else:
            data = {
                "error": 'Please Provide Correct University email',
                "values": values,
            }
            return render(request, 'signup.html', data)

    def ValidateUser(self, sign_up):
        error_msg = None

        if not sign_up.fname:
            error_msg = "First Name Required!"
        elif not sign_up.lname:
            error_msg = "Last Name Required!"
        elif not sign_up.email:
            error_msg = "Email Required!"
        elif sign_up.isExists():
            error_msg = "Email already exists"

        return error_msg


    def sendmail(self, email, username, password, fname, lname):
        sent = False

        from email.message import EmailMessage
        import ssl
        import smtplib

        # Authentication
        sender_email = "customer.kgp@gmail.com"
        # sender_email_password = 'cwvmklxvrhwksszm'
        sender_email_password = 'wfhxwptcoavmjywp'
        receiver_email = email

        subject = "KGP Credentials"

        body = f"""Dear {fname} {lname}
        \nWe are happy to inform you that your KGP(KFUEIT GRIEVANCES PORTAL) login has been activated.
        \nPlease find the login details below.
        \n\nYour Logins are:
        \n Username:{username}
        \n Password:{password}
        \n\nHow to login?
        \n\nPlease follow the following steps to access the KFUEIT GRIEVANCES PORTAL. 
        \n• Head over to http://kgp.pythonanywhere.com/
        \n• Enter your username and password mentioned above.
        \n\nNote: If you are having trouble while loging into your account, kindly manually type username and password or contact us at customer.kgp+accountissue@gmail.com .
        \n\n Best regards,
        \nKGP Support Team
        """

        em = EmailMessage()

        em['From'] = sender_email
        em['To'] = receiver_email
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_email_password)
            smtp.sendmail(sender_email, receiver_email, em.as_string())
            sent = True

        return sent



class Login_view(View):
    def get(self, request):
        try:
            rq_user = request.session.get("kfueit_username")
        except:
            pass
        if rq_user != None:
            return redirect('home')
        else:
            return render(request, 'login.html',{'msg': messages.get_messages(request)})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = models.SignUp.objects.get(user_name=username)
            re = True
        except:
            re = False
        if re:
            if user.password == password:
                request.session["kfueit_username"] = user.user_name
                now = datetime.now()
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                hr_str_to_replace = dt_string[11:14]
                hr_str = dt_string[11:13]
                hr_int = int(hr_str)
                new_hr_str = str(hr_int+5)
                server_time = dt_string.replace(hr_str_to_replace,(new_hr_str+":"))
                try:
                    u = models.LoginActivity.objects.get(user_id=user.id)
                    r = True
                except:
                    r = False
                if r:
                    models.LoginActivity.objects.filter(user_id=user.id).update(last_login=server_time)
                else:
                    login_activity = models.LoginActivity(user_id=user,last_login=server_time)
                    login_activity.register()
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Incorrect Password', 'username': username})
        else:
            return render(request, 'login.html', {'error': 'Incorrect Username', 'username': username})


class ForgotPassword_view(View):
    def get(self, request):
        try:
            rq_user = request.session.get("kfueit_username")
        except:
            pass
        if rq_user != None:
            return redirect('home')
        else:
            return render(request, 'forgotpassword.html')

    def post(self, request):
        email = request.POST.get('email')
        re = email.endswith("@kfueit.edu.pk")
        if re:
            try:
                sign = models.SignUp.objects.get(email=email)
                obj = True
            except:
                obj = False
            if obj:
                otp = random.randint(111111, 999999)
                sent = self.sendmail(email, otp)
                if sent:
                    models.SignUp.objects.filter(email=email).update(otp=otp)
                    return redirect('reset_otp', email=email)
                else:
                    return render(request, 'forgotpassword.html', {'error': "We are facing some issue. Please Try again later.", 'email': email})
            else:
                return render(request, 'forgotpassword.html', {'error': "Account doesn't exits on provided Email", 'email': email})
        else:
            return render(request, 'forgotpassword.html', {'error': 'Incorrect Email', 'email': email})

    def sendmail(self, email, otp,):
        sent = False

        from email.message import EmailMessage
        import ssl
        import smtplib

        # Authentication
        sender_email = "customer.kgp@gmail.com"
        # sender_email_password = 'cwvmklxvrhwksszm'
        sender_email_password = 'wfhxwptcoavmjywp'
        receiver_email = email

        subject = "KGP Password Reset OTP"

        body = f"""You have Requested Password Reset For Account {email} at KGP.
        \nYour OTP For Password Reset is {otp}
        \n\n Best regards,
        \nKGP Support Team
        """

        em = EmailMessage()

        em['From'] = sender_email
        em['To'] = receiver_email
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_email_password)
            smtp.sendmail(sender_email, receiver_email, em.as_string())
            sent = True

        return sent


class ResetOtp_view(View):
    def get(self, request, email):
        try:
            rq_user = request.session.get("kfueit_username")
        except:
            pass
        if rq_user != None:
            return redirect('home')
        else:
            return render(request, 'resetotp.html')

    def post(self, request, email):
        otp = request.POST.get('otp')
        obj = models.SignUp.objects.get(email=email)
        if obj.otp == otp:
            number_list = ['*', '!', '$', '&',
                           '#', '=', '%', '+', '-', '_', '@']
            password = str(names.get_first_name()) + str(random.choice(number_list)) + \
                str(random.randint(111, 999)) + str(random.choice(number_list))
            sent = self.sendmail(email, password)
            if sent:
                models.SignUp.objects.filter(email=email).update(
                    password=password, otp=None)
                return render(request, 'resetotp.html', {'msg': 'Password Reset Successfully and has been sent to your email.  '})
        else:
            return render(request, 'resetotp.html', {'error': 'Incorrect OTP'})

    def sendmail(self, email, password):
        sent = False

        from email.message import EmailMessage
        import ssl
        import smtplib

        # Authentication
        sender_email = "customer.kgp@gmail.com"
        # sender_email_password = 'cwvmklxvrhwksszm'
        sender_email_password = 'wfhxwptcoavmjywp'
        receiver_email = email

        subject = "KGP Password Reset"

        body = f"""
        \nWe are happy to inform you that your KGP(KFUEIT GRIEVANCES PORTAL) Password has been Reset for acoount {email}.
        \n\nYour New Password is:
        \n Password:{password}
        \n\nNote: If you are having trouble while loging into your account, kindly manually type username and password or contact us at customer.kgp+accountissue@gmail.com .
        \n\n Best regards,
        \nKGP Support Team
        """

        em = EmailMessage()

        em['From'] = sender_email
        em['To'] = receiver_email
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_email_password)
            smtp.sendmail(sender_email, receiver_email, em.as_string())
            sent = True

        return sent



# main


class Home(View):
    def get(self,request):
        try:
            rq_user = request.session.get("kfueit_username")
        except:
            pass
        if rq_user != None:
            dbuser = models.SignUp.objects.get(user_name=rq_user)
            carouselmain = models.CarouselImages.objects.earliest('id')
            carouselimages = models.CarouselImages.objects.exclude(pk=carouselmain.id)
            data = {
                "logged": True,
                "fname": dbuser.fname,
                "lname": dbuser.lname,
                "carouselmain":carouselmain,
                "carouselimages":carouselimages,
            }
            return render(request, 'main/index.html', data)
        else:
            return redirect("login")
        
    def post(self,request):
        obj = request.POST
        name = obj.get('name')
        email = obj.get('email')
        message = obj.get('message')
        sent = self.sendmail(name,email, message)


        rq_user = request.session.get("kfueit_username")
        dbuser = models.SignUp.objects.get(user_name=rq_user)
        carouselmain = models.CarouselImages.objects.earliest('id')
        carouselimages = models.CarouselImages.objects.exclude(pk=carouselmain.id)
        data = {
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            "carouselmain":carouselmain,
            "carouselimages":carouselimages,
            "success":"Your message has been sent."
        }
        return render(request, 'main/index.html', data)


    def sendmail(self, name,email, message):
        sent = False

        from email.message import EmailMessage
        import ssl
        import smtplib

        # Authentication
        sender_email = "customer.kgp@gmail.com"
        sender_email_password = 'wfhxwptcoavmjywp'
        receiver_email = "customer.kgp@gmail.com"

        subject = f"{name} Contacted"

        body = f"""Dear Developer,
        \n{name} having mail: {email} has contacted you as he is might experiencing an issue.
        \nMessage is :
        \n{message}
        \n\n Best regards,
        \nKGP Support Team
        """

        em = EmailMessage()

        em['From'] = sender_email
        em['To'] = receiver_email
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_email_password)
            smtp.sendmail(sender_email, receiver_email, em.as_string())
            sent = True

        return sent

def selectdepartment(request):
    try:
        rq_user = request.session.get("kfueit_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.SignUp.objects.get(user_name=rq_user)
        user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)
        departments = models.Department.objects.all()
        data = {
            "login_activity":user_activity,
            'pgname': 'Select Department',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            "departments":departments
        }
        return render(request,'main/selectdepartment.html',data)
    else:
        return redirect("login")

class Make_a_Complaint(View):
    def get(self,request,id=None):
        try:
            rq_user = request.session.get("kfueit_username")
        except:
            pass
        if rq_user != None:
            try:
                department = models.Department.objects.get(pk=id)
                hod = models.HODSignUp.objects.filter(department_id=id)
                dbuser = models.SignUp.objects.get(user_name=rq_user)
                user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)
                complaintcategories = models.ComplaintCategory.objects.all()
                data = {
                    "login_activity":user_activity,
                    'pgname': 'Make a Complaint',
                    "logged": True,
                    "fname": dbuser.fname,
                    "lname": dbuser.lname,
                    "department":department,
                    "hod":hod,
                    "complaintcategories":complaintcategories,
                }
                return render(request,'main/makeacomplaint.html',data)
            except:
                return redirect('page-not-found')

        else:
            return redirect("login")
        
    def post(self,request,id=None):
        import random
        ran1 = random.randint(0,99999)
        ran2= random.randint(0,999999)
        try:
            rq_user = request.session.get("kfueit_username")
        except:
            pass
        if rq_user != None:
            obj = request.POST
            hod_id = obj.get('hod_id')
            cat_id = obj.get('cat_id')

            user = models.SignUp.objects.get(user_name=rq_user)
            hod_id = models.HODSignUp.objects.get(id=hod_id)
            department = models.Department.objects.get(id=id)
            complaint_cat = models.ComplaintCategory.objects.get(name=cat_id)
            complaintid = "KGP"+str(ran1)+"-"+str(ran2)        
            title = obj.get('title')
            complaint_description = obj.get('complaint_description')
            hide = obj.get('hide')

            user_activity = models.LoginActivity.objects.get(user_id=user.id)

            if hide == "on":
                hi = True
            else:
                hi = False
            image = request.FILES.get('image')
            video = request.FILES.get('video')
            declaration = obj.get('declaration')
            if declaration == "on":
                dec = True
            else:
                dec = False

            hod = models.HODSignUp.objects.filter(department_id=id)
            dbuser = models.SignUp.objects.get(user_name=rq_user)
            complaintcategories = models.ComplaintCategory.objects.all()
            data = {
                    'pgname': 'Make a Complaint',
                    "login_activity":user_activity,
                    "logged": True,
                    "fname": dbuser.fname,
                    "lname": dbuser.lname,
                    "hod":hod,
                    "complaintcategories":complaintcategories,
                    'success':'Your Complaint has been Lodged Successfully',
                }

            if hi:
                if image:
                    if video:
                        complaint = models.Complaint(user_id=user,hod_id=hod_id,department_id=department,
                        complaint_category_id=complaint_cat,complaint_id=complaintid,title=title,
                        details=complaint_description,hide_identity=hi,image=image,video=video,declaration=dec,)
                        complaint.save()
                        return render(request,'main/makeacomplaint.html',data)
                    else:
                        complaint = models.Complaint(user_id=user,hod_id=hod_id,department_id=department,complaint_category_id=complaint_cat,complaint_id=complaintid,title=title,details=complaint_description,hide_identity=hi,image=image,declaration=dec,)
                        complaint.save()
                        return render(request,'main/makeacomplaint.html',data)
                elif video:
                    if image:
                        complaint = models.Complaint(user_id=user,hod_id=hod_id,department_id=department,complaint_category_id=complaint_cat,complaint_id=complaintid,title=title,details=complaint_description,hide_identity=hi,image=image,video=video,declaration=dec,)
                        complaint.save()
                        return render(request,'main/makeacomplaint.html',data)
                    else:
                        complaint = models.Complaint(user_id=user,hod_id=hod_id,department_id=department,complaint_category_id=complaint_cat,complaint_id=complaintid,title=title,details=complaint_description,hide_identity=hi,video=video,declaration=dec,)
                        complaint.save()
                        return render(request,'main/makeacomplaint.html',data)
                else:
                    complaint = models.Complaint(user_id=user,hod_id=hod_id,department_id=department,complaint_category_id=complaint_cat,complaint_id=complaintid,title=title,details=complaint_description,hide_identity=hi,declaration=dec,)
                    complaint.save()
                    return render(request,'main/makeacomplaint.html',data)

            else:
                if image:
                    if video:
                        complaint = models.Complaint(user_id=user,hod_id=hod_id,department_id=department,complaint_category_id=complaint_cat,complaint_id=complaintid,title=title,details=complaint_description,hide_identity=hi,image=image,video=video,declaration=dec,)
                        complaint.save()
                        return render(request,'main/makeacomplaint.html',data)
                    else:
                        complaint = models.Complaint(user_id=user,hod_id=hod_id,department_id=department,complaint_category_id=complaint_cat,complaint_id=complaintid,title=title,details=complaint_description,hide_identity=hi,image=image,declaration=dec,)
                        complaint.save()
                        return render(request,'main/makeacomplaint.html',data)
                elif video:
                    if image:
                        complaint = models.Complaint(user_id=user,hod_id=hod_id,department_id=department,complaint_category_id=complaint_cat,complaint_id=complaintid,title=title,details=complaint_description,hide_identity=hi,image=image,video=video,declaration=dec,)
                        complaint.save()
                        return render(request,'main/makeacomplaint.html',data)
                    else:
                        complaint = models.Complaint(user_id=user,hod_id=hod_id,department_id=department,complaint_category_id=complaint_cat,complaint_id=complaintid,title=title,details=complaint_description,hide_identity=hi,video=video,declaration=dec,)
                        complaint.save()
                        return render(request,'main/makeacomplaint.html',data)
                else:
                    complaint = models.Complaint(user_id=user,hod_id=hod_id,department_id=department,complaint_category_id=complaint_cat,complaint_id=complaintid,title=title,details=complaint_description,hide_identity=hi,declaration=dec,)
                    complaint.save()
                    return render(request,'main/makeacomplaint.html',data)
        else:
            return redirect("login")


def all(request):
    try:
        rq_user = request.session.get("kfueit_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.SignUp.objects.get(user_name=rq_user)
        user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)
        complaints = models.Complaint.objects.filter(user_id=dbuser.id).all().order_by("-created_at")
        data = {
            "login_activity":user_activity,
            'pgname': 'All Complaints',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            "complaints":complaints,
        }
        return render(request, 'main/all.html', data)
    else:
        return redirect("login")

def open(request):
    try:
        rq_user = request.session.get("kfueit_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.SignUp.objects.get(user_name=rq_user)
        user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)
        complaints = models.Complaint.objects.filter(user_id=dbuser.id,is_canceled=False,is_withdrawn=False,is_completed=False,is_completed_resolved=False).all().order_by("-created_at")
        data = {
            "login_activity":user_activity,
            'pgname': 'Open Complaints',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            "complaints":complaints,
        }
        return render(request, 'main/open.html', data)
    else:
        return redirect("login")
    

def closed(request):
    try:
        rq_user = request.session.get("kfueit_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.SignUp.objects.get(user_name=rq_user)
        user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)
        complaints = models.Complaint.objects.filter(user_id=dbuser.id,is_pending=False,is_forwarded=False,is_canceled=False,is_withdrawn=False).all().order_by("-created_at")
        data = {
            "login_activity":user_activity,
            'pgname': 'Closed Complaints',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            "complaints":complaints,
        }
        return render(request, 'main/closed.html', data)
    else:
        return redirect("login")
    

def dropped(request):
    try:
        rq_user = request.session.get("kfueit_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.SignUp.objects.get(user_name=rq_user)
        user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)
        complaints = models.Complaint.objects.filter(user_id=dbuser.id,is_pending=False,is_forwarded=False,is_completed=False,is_completed_resolved=False).all().order_by("-created_at")
        data = {
            "login_activity":user_activity,
            'pgname': 'Dropped Complaints',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            "complaints":complaints,
        }
        return render(request, 'main/dropped.html', data)
    else:
        return redirect("login")
    

def positive(request):
    try:
        rq_user = request.session.get("kfueit_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.SignUp.objects.get(user_name=rq_user)
        user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)
        feedbacks = models.Review.objects.filter(user_id=dbuser.id,stars__gte=3).all().order_by('-id')
        print(feedbacks)
        data = {
            "login_activity":user_activity,
            'pgname': 'Positive Feedbacks',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            'feedbacks':feedbacks,
        }
        return render(request, 'main/positive.html', data)
    else:
        return redirect("login")
    

def negative(request):
    try:
        rq_user = request.session.get("kfueit_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.SignUp.objects.get(user_name=rq_user)
        user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)
        feedbacks = models.Review.objects.filter(user_id=dbuser.id,stars__lte=2).all().order_by('-id')
        print(feedbacks)
        data = {
            "login_activity":user_activity,
            'pgname': 'Negative Feedbacks',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            'feedbacks':feedbacks,
        }
        return render(request, 'main/negative.html', data)
    else:
        return redirect("login")
    

def pendingfeedbacks(request):
    try:
        rq_user = request.session.get("kfueit_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.SignUp.objects.get(user_name=rq_user)
        user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)
        complaints = models.Complaint.objects.filter(user_id=dbuser.id,is_pending=False,is_forwarded=False,is_canceled=False,is_withdrawn=False,is_reviewed=False).all().order_by("-created_at")
        data = {
            "login_activity":user_activity,
            'pgname': 'Pending Feedbacks',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            "complaints":complaints,
        }
        return render(request, 'main/pendingfeedbacks.html', data)
    else:
        return redirect("login")
    
class Feedbacks(View):
    def get(self,request,complaint_id=None):
        try:
            rq_user = request.session.get("kfueit_username")
        except:
            pass
        if rq_user != None:
            dbuser = models.SignUp.objects.get(user_name=rq_user)
            user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)
            data = {
                "login_activity":user_activity,
                'pgname': 'Feedbacks',
                "logged": True,
                "fname": dbuser.fname,
                "lname": dbuser.lname,
                'complaint_id':complaint_id
            }
            return render(request,'main/feedback.html',data)
        else:
            return redirect("login")
        
    def post(self,request,complaint_id=None):
        rq_user = request.session.get("kfueit_username")
        dbuser = models.SignUp.objects.get(user_name=rq_user)
        user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)

        satisfaction = request.POST.get('satisfaction')
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')

        if rating:
            if satisfaction == "on":
                models.Complaint.objects.filter(user_id=dbuser.id,is_pending=False,is_forwarded=False,is_canceled=False,is_withdrawn=False,is_reviewed=False).update(is_reviewed=True)        
                feed = models.Review(user_id=dbuser,complaint_id=complaint_id,satisfaction_status=True,feedback=feedback,stars=rating)
                feed.save()
                data = {
                    "login_activity":user_activity,
                    'pgname': 'Feedbacks',
                    "logged": True,
                    "fname": dbuser.fname,
                    "lname": dbuser.lname,
                    'complaint_id':complaint_id,
                    'success':'Success! Thanks for your feedback'
                }
                return render(request,'main/feedback.html',data)
            else:
                models.Complaint.objects.filter(user_id=dbuser.id,is_pending=False,is_forwarded=False,is_canceled=False,is_withdrawn=False,is_reviewed=False).update(is_reviewed=True)        
                feed = models.Review(user_id=dbuser,complaint_id=complaint_id,satisfaction_status=False,feedback=feedback,stars=rating)
                feed.save()
                data = {
                    "login_activity":user_activity,
                    'pgname': 'Feedbacks',
                    "logged": True,
                    "fname": dbuser.fname,
                    "lname": dbuser.lname,
                    'complaint_id':complaint_id,
                    'success':'Success! Thanks for your feedback'
                }
                return render(request,'main/feedback.html',data)
        else:
            data = {
                "login_activity":user_activity,
                'pgname': 'Feedbacks',
                "logged": True,
                "fname": dbuser.fname,
                "lname": dbuser.lname,
                'complaint_id':complaint_id,
                'error':'Please select stars First'
            }
            return render(request,'main/feedback.html',data)


def page_not_found(request):
    try:
        rq_user = request.session.get("kfueit_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.SignUp.objects.get(user_name=rq_user)
        user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)
        data = {
        "login_activity":user_activity,
        'pgname': 'Page Not Found',
        "logged": True,
        "fname": dbuser.fname,
        "lname": dbuser.lname,
        }
        return render(request, 'main/404.html',data)
    else:
        return render(request, 'main/404.html')


def feedback_detail(request,complaint_id=None):
    try:
        rq_user = request.session.get("kfueit_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.SignUp.objects.get(user_name=rq_user)
        user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)
        feed = models.Review.objects.get(user_id=dbuser.id,complaint_id=complaint_id)
        data = {
        "login_activity":user_activity,
        'pgname': 'Complaint Feedback',
        "logged": True,
        "fname": dbuser.fname,
        "lname": dbuser.lname,
        "feed":feed,
        }
        return render(request, 'main/feedbackdetail.html',data)
    else:
        return redirect('login')
    

def logout(request):
    if not request.session.get("kfueit_username"):
        return redirect('login')
    else:
        del request.session['kfueit_username']
        return redirect('login')

def viewcomplaint(request,uuid=None):
    try:
        rq_user = request.session.get("kfueit_username")
    except:
        pass
    if rq_user != None:
        try:
            dbuser = models.SignUp.objects.get(user_name=rq_user)
            complaintdetail=models.Complaint.objects.get(complaint_id=uuid)
            data = {
                'pgname': 'Complaint Views',
                #"logged": True,
                #"fname": dbuser.fname,
                #"lname": dbuser.lname,
                 "complaint":complaintdetail,
                # "department":department,
                # "hod":hod,
                # "complaintcategories":complaintdetails.complaint_category_id,
                # "complaint_id":complaintdetails.complaint_id,
                # "title":complaintdetails.title,
                # "details":complaintdetails.details,
                # "image":complaintdetails.image,
                # "video":complaintdetails.video,
                # "created_at":complaintdetails.created_at,
                # "forwarded_at":complaintdetails.forwarded_at,
                # "closed_at":complaintdetails.closed_at,
                # "cancel_at":complaintdetails.cancel_at,
                # "is_pending":complaintdetails.is_pending,
                # "is_forwarded":complaintdetails.is_forwarded,
                # "is_canceled":complaintdetails.is_canceled,
                # "is_completed":complaintdetails.is_completed,
                # "is_completed_resolved":complaintdetails.is_completed_resolved,
                # "forwarded_msg":complaintdetails.forwarded_msg,
                # "canceled_msg":complaintdetails.canceled_msg,
                # "additional_info_msg":complaintdetails.additional_info_msg,
                # "completed_msg":complaintdetails.completed_msg,
                
            }
            print(uuid)
            return render(request,'main/complaintview.html',data)
        except:
            return redirect('page-not-found')

    else:
        return redirect("login")
def seedetails(request,uuid=None):
    try:
        rq_user = request.session.get("kfueit_username")
    except:
        pass
    if rq_user != None:
        try:
            dbuser = models.SignUp.objects.get(user_name=rq_user)
            complaintdetail=models.Complaint.objects.get(complaint_id=uuid)
            data = {
                'pgname': 'Complaint Details',
                 "complaint":complaintdetail,
                
            }
            return render(request,'main/seedetails.html',data)
        except:
            return redirect('page-not-found')

    else:
        return redirect("login")


def dropcomplaints(request,uuid=None):
    status=True
    print(status)
    print(uuid)
    try:
        rq_user = request.session.get("kfueit_username")
    except:
        pass
    if rq_user != None:
        print(uuid)
        obj = request.POST        
        complaints = models.Complaint.objects.get(complaint_id=uuid)
        dbuser = models.SignUp.objects.get(user_name=rq_user)
        print(uuid)
        if status :
            complaints.is_withdrawn = True
            print(uuid)
            models.Complaint.objects.filter(user_id=dbuser,complaint_id=uuid,).update(is_withdrawn=True,withdrawn_at=datetime.now,is_pending=False,is_forwarded=False,is_canceled=False,is_reviewed=False,is_completed=False,is_completed_resolved=False)

        else:
            complaints.is_withdrawn = False
        
        user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)
        carouselmain = models.CarouselImages.objects.earliest('id')
        carouselimages = models.CarouselImages.objects.exclude(pk=carouselmain.id)
        data = {
                'pgname': 'Home',
                "login_activity":user_activity,
                "logged": True,
                "fname": dbuser.fname,
                "lname": dbuser.lname,
                "carouselmain":carouselmain,
                "carouselimages":carouselimages,
                'success':'Your Complaint has been Dropped Successfully',
            }
        return render(request,"main/index.html",data)
                
    else:
        return redirect("login")