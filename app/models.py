from django.db import models
from django.db.models.deletion import CASCADE
import datetime


# Create your models here.

class CarouselImages(models.Model):
    image = models.ImageField(upload_to='carousel/images')


class SignUp(models.Model):
    # profile_image = models.ImageField(upload_to ='profile')
    fname = models.CharField(max_length=250)
    lname = models.CharField(max_length=250)
    user_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    otp = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user_name
    
    def register(self):
        self.save()


    def isExists(self):
        try:
            if SignUp.objects.get(email=self.email):
                return True
        except:
            return False


class LoginActivity(models.Model):
    user_id = models.ForeignKey(
        SignUp, related_name='signup', on_delete=CASCADE)
    last_login = models.DateTimeField()

    def register(self):
        self.save()


class ComplaintCategory(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='department/images')

    def __str__(self):
        return self.name


class HODSignUp(models.Model):
    department_id = models.ForeignKey(Department, on_delete=CASCADE)
    fname = models.CharField(max_length=250)
    lname = models.CharField(max_length=250)
    user_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.user_name


class HODSignUpEmail(models.Model):
    hod_id = models.ForeignKey(HODSignUp, on_delete=CASCADE)
    status = models.BooleanField(default=False)


class FacultySignUp(models.Model):
    hod_id = models.ForeignKey(HODSignUp, on_delete=CASCADE)
    fname = models.CharField(max_length=250)
    lname = models.CharField(max_length=250)
    user_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.user_name


class FacultySignUpEmail(models.Model):
    faculty_id = models.ForeignKey(FacultySignUp, on_delete=CASCADE)
    status = models.BooleanField(default=False)


class Complaint(models.Model):
    user_id = models.ForeignKey(SignUp, on_delete=CASCADE)
    hod_id = models.ForeignKey(HODSignUp, on_delete=CASCADE)
    faculty_id = models.ForeignKey(
        FacultySignUp, on_delete=CASCADE, blank=True, null=True)
    department_id = models.ForeignKey(Department, on_delete=CASCADE)
    complaint_category_id = models.ForeignKey(
        ComplaintCategory, on_delete=CASCADE)
    complaint_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    details = models.CharField(max_length=250)
    hide_identity = models.BooleanField(default=False)
    image = models.ImageField(upload_to='complaint/images',null=True,blank=True)
    video = models.FileField(upload_to='complaint/videos',null=True,blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.today)

    declaration = models.BooleanField(default=False)
    
    forwarded_at = models.DateTimeField(default=datetime.datetime.today, blank=True, null=True)
    closed_at = models.DateTimeField(default=datetime.datetime.today, blank=True, null=True)
    cancel_at = models.DateTimeField(default=datetime.datetime.today, blank=True, null=True)
    withdrawn_at = models.DateTimeField(default=datetime.datetime.today, blank=True, null=True)

    is_pending = models.BooleanField(default=True)
    is_forwarded = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    is_withdrawn = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_completed_resolved = models.BooleanField(default=False)
    Resolved = models.BooleanField(default=False)
    forwarded_msg = models.CharField(max_length=500, null=True, blank=True)
    canceled_msg = models.CharField(max_length=500, null=True, blank=True)
    additional_info_msg = models.CharField(
        max_length=500, null=True, blank=True)
    completed_msg = models.CharField(max_length=500, null=True, blank=True)

    is_reviewed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.complaint_id


class Review(models.Model):
    user_id = models.ForeignKey(SignUp, on_delete=CASCADE)
    faculty_id = models.ForeignKey(FacultySignUp, on_delete=CASCADE,null=True, blank=True,default=1)
    hod_id = models.ForeignKey(HODSignUp, on_delete=CASCADE,null=True, blank=True,default=1)
    complaint_id = models.CharField(max_length=200)
    resolution_status = models.BooleanField(default=False)
    satisfaction_status = models.BooleanField(default=False)
    feedback = models.CharField(max_length=200)
    stars = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.datetime.today)

