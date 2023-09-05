from django.shortcuts import render, redirect
from django.views import View
from app import models



# For Date and Time
from datetime import datetime,timedelta
# Create your views here.

# Current Server Time
def current_server_time(hours):
    current_time = datetime.now()
    future_time = current_time + timedelta(hours=hours)
    return future_time


class Login_view(View):
    def get(self, request):
        try:
            rq_user = request.session.get("hod_username")
        except:
            pass
        if rq_user != None:
            return redirect('hodhome')
        else:
            return render(request, 'hod/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = models.HODSignUp.objects.get(user_name=username)
            re = True
        except:
            re = False
        if re:
            if user.password == password:
                request.session["hod_username"] = user.user_name
                # server_time = current_server_time(5)
                return redirect('hodhome')
            else:
                return render(request, 'hod/login.html', {'error': 'Incorrect Password', 'username': username})
        else:
            return render(request, 'hod/login.html', {'error': 'Incorrect Username', 'username': username})




# main


class Home(View):
    def get(self,request):
        try:
            rq_user = request.session.get("hod_username")
        except:
            pass
        if rq_user != None:
            dbuser = models.HODSignUp.objects.get(user_name=rq_user)
            carouselmain = models.CarouselImages.objects.earliest('id')
            carouselimages = models.CarouselImages.objects.exclude(pk=carouselmain.id)
            data = {
                "logged": True,
                "fname": dbuser.fname,
                "lname": dbuser.lname,
                "carouselmain":carouselmain,
                "carouselimages":carouselimages,
            }
            return render(request, 'hod/main/index.html', data)
        else:
            return redirect("hodlogin")
        
    def post(self,request):
        obj = request.POST
        name = obj.get('name')
        email = obj.get('email')
        message = obj.get('message')
        sent = self.sendmail(name,email, message)


        rq_user = request.session.get("hod_username")
        dbuser = models.HODSignUp.objects.get(user_name=rq_user)
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
        return render(request, 'hod/main/index.html', data)


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



def all(request):
    try:
        rq_user = request.session.get("hod_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.HODSignUp.objects.get(user_name=rq_user)
        complaints = models.Complaint.objects.filter(hod_id=dbuser.id).all().order_by("-created_at").exclude(is_withdrawn=True)
        data = {
            'pgname': 'All Complaints',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            "complaints":complaints,
        }
        return render(request, 'hod/main/complaints.html', data)
    else:
        return redirect("hodlogin")

def open(request):
    try:
        rq_user = request.session.get("hod_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.HODSignUp.objects.get(user_name=rq_user)
        complaints = models.Complaint.objects.filter(hod_id=dbuser.id,is_pending=True).all().order_by("-created_at")
        data = {
            'pgname': 'Open Complaints',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            "complaints":complaints,
        }
        return render(request, 'hod/main/complaints.html', data)
    else:
        return redirect("hodlogin")
    

def closed(request):
    try:
        rq_user = request.session.get("hod_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.HODSignUp.objects.get(user_name=rq_user)
        from django.db.models import Q
        complaints = models.Complaint.objects.filter(Q(is_completed=True) | Q(is_completed_resolved=True),hod_id=dbuser.id).all().order_by("-created_at")
        data = {
            'pgname': 'Closed Complaints',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            "complaints":complaints,
        }
        return render(request, 'hod/main/complaints.html', data)
    else:
        return redirect("hodlogin")
    

def canceled(request):
    try:
        rq_user = request.session.get("hod_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.HODSignUp.objects.get(user_name=rq_user)
        complaints = models.Complaint.objects.filter(is_canceled=True,hod_id=dbuser.id).all().order_by("-created_at")
        data = {
            'pgname': 'Canceled Complaints',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            "complaints":complaints,
        }
        return render(request, 'hod/main/complaints.html', data)
    else:
        return redirect("hodlogin")
    
def forwarded(request):
    try:
        rq_user = request.session.get("hod_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.HODSignUp.objects.get(user_name=rq_user)
        complaints = models.Complaint.objects.filter(is_forwarded=True,hod_id=dbuser.id).all().order_by("-created_at")
        data = {
            'pgname': 'Forwarded Complaints',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            "complaints":complaints,
        }
        return render(request, 'hod/main/complaints.html', data)
    else:
        return redirect("hodlogin")
    

def feedbacks(request):
    try:
        rq_user = request.session.get("hod_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.HODSignUp.objects.get(user_name=rq_user)
        user_activity = models.LoginActivity.objects.get(user_id=dbuser.id)
        feedbacks = models.Review.objects.filter(hod_id=dbuser.id).all().order_by('-id')
        print(feedbacks)
        data = {
            "login_activity":user_activity,
            'pgname': 'Feedbacks',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            'feedbacks':feedbacks,
        }
        return render(request, 'hod/main/feedbacks.html', data)
    else:
        return redirect("hodlogin")
    
def feedback(request):
    try:
        rq_user = request.session.get("hod_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.HODSignUp.objects.get(user_name=rq_user)
        feed= models.Review.objects.filter(hod_id=dbuser.id).all().order_by("-created_at")
        data = {
            'pgname': 'Feedbacks',
            "logged": True,
            "fname": dbuser.fname,
            "lname": dbuser.lname,
            "feedbacks":feed,
        }
        return render(request, 'hod/main/feedbacks.html', data)
    else:
        return redirect("hodlogin")
      


def page_not_found(request):
    try:
        rq_user = request.session.get("hod_username")
    except:
        pass
    if rq_user != None:
        dbuser = models.HODSignUp.objects.get(user_name=rq_user)
        data = {
        'pgname': 'Page Not Found',
        "logged": True,
        "fname": dbuser.fname,
        "lname": dbuser.lname,
        }
        return render(request, 'hod/main/404.html',data)
    else:
        return render(request, 'hod/main/404.html')


def feedback_detail(request,complaint_id=None):
    try:
        rq_user = request.session.get("hod_username")
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
        return render(request, 'hod/main/feedbackdetail.html',data)
    else:
        return redirect('hodlogin')
    

def logout(request):
    if not request.session.get("hod_username"):
        return redirect('hodlogin')
    else:
        del request.session['hod_username']
        return redirect('hodlogin')

def viewcomplaint(request,uuid=None):
    try:
        rq_user = request.session.get("hod_username")
    except:
        pass
    if rq_user != None:
        try:
            dbuser = models.HODSignUp.objects.get(user_name=rq_user)
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
            return render(request,'hod/main/complaintview.html',data)
        except:
            return redirect('hodpage-not-found')

    else:
        return redirect("hodlogin")
    

class Close_Complaint_View(View):
    def get(self,request,uuid=None):
        return render(request,'hod/main/close.html')
    def post(self,request,uuid=None):
        completedmsg = request.POST.get('completedmsg')
        resolved = request.POST.get('resolved')
        if resolved == "on":
            models.Complaint.objects.filter(complaint_id=uuid).update(closed_at=datetime.now(),completed_msg=completedmsg,is_pending=False,is_forwarded=False,is_canceled=False,is_withdrawn=False,is_completed=False,is_completed_resolved=True)
        else:
            models.Complaint.objects.filter(complaint_id=uuid).update(closed_at=datetime.now(),completed_msg=completedmsg,is_pending=False,is_forwarded=False,is_canceled=False,is_withdrawn=False,is_completed=True,is_completed_resolved=False)
        return redirect('hodall')
    
class Cancel_Complaint_View(View):
    def get(self,request,uuid=None):
        return render(request,'hod/main/cancel.html')
    def post(self,request,uuid=None):
        cancel = request.POST.get('cancel')
        models.Complaint.objects.filter(complaint_id=uuid).update(cancel_at=datetime.now(),canceled_msg=cancel,is_pending=False,is_forwarded=False,is_canceled=True,is_withdrawn=False,is_completed=False,is_completed_resolved=False)
        return redirect('hodall')

class Forward_Complaint_View(View):
    def get(self,request,uuid=None):
        try:
           rq_user = request.session.get("hod_username")
        except:
           pass
        if rq_user != None:
            try:  
                dbuser = models.HODSignUp.objects.get(user_name=rq_user)
                faculty= models.FacultySignUp.objects.filter(hod_id=dbuser.id).all().order_by('id')
                data={
                    "pgname":"Forward",
                    "faculty": faculty, 
                }
                return render(request,'hod/main/forward.html', data)
            except:
               return redirect("hodpage-not-found")
        else:
           return redirect("hodlogin")

    def post(self,request,uuid=None):
        msg = request.POST.get('forward')
        Facultyname = request.POST.get('faculty_id')
        Faculty=models.FacultySignUp.objects.get(user_name=Facultyname)
        models.Complaint.objects.filter(complaint_id=uuid).update(faculty_id=Faculty.id,forwarded_at=datetime.now(),forwarded_msg=msg,is_pending=False
            ,is_forwarded=True,is_canceled=False,is_withdrawn=False,is_completed=False,is_completed_resolved=False)

        return redirect('hodall')

