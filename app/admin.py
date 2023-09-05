from django.contrib import admin
from . import models


admin.site.site_header = "KGP ADMIN"
admin.site.site_title = "KGP ADMIN PORTAL"
admin.site.index_title = "WELCOME TO KGP ADMIN PORTAL"
# Register your models here.

@admin.register(models.CarouselImages)
class CarouselImagesAdmin(admin.ModelAdmin):
    list_display = ['id','image',]

@admin.register(models.HODSignUp)
class HODSignUpAdmin(admin.ModelAdmin):
    list_display = ['id','department_id','fname','lname','user_name','email','password',]

@admin.register(models.FacultySignUp)
class FacultySignUpAdmin(admin.ModelAdmin):
    list_display = ['id','hod_id','fname','lname','user_name','email','password']

@admin.register(models.SignUp)
class UserSignUpAdmin(admin.ModelAdmin):
    list_display = ['id','fname','lname','user_name','email','password','otp']


@admin.register(models.LoginActivity)
class LoginActivityAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','last_login']

@admin.register(models.ComplaintCategory)
class ComplaintCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id','name','image']

@admin.register(models.HODSignUpEmail)
class HODSignUpEmailAdmin(admin.ModelAdmin):
    list_display = ['id','hod_id','status']

@admin.register(models.FacultySignUpEmail)
class FacultySignUpEmailAdmin(admin.ModelAdmin):
    list_display = ['id','faculty_id','status']

@admin.register(models.Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','hod_id','faculty_id','department_id','complaint_category_id',
                    'complaint_id','title','details','hide_identity','image','video','declaration',
                    'created_at','forwarded_at','closed_at','cancel_at','withdrawn_at','is_pending','is_forwarded',
                    'is_canceled','is_withdrawn','is_completed','is_completed_resolved','forwarded_msg','canceled_msg',
                    'additional_info_msg','completed_msg','is_reviewed']
    
@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','complaint_id','resolution_status','satisfaction_status','feedback','stars','created_at']