from django.contrib import admin
from django.urls import path,include
from app import views
from .settings import MEDIA_ROOT,MEDIA_URL
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("hod/", include("hodapp.urls") , name="hod"),
    path("faculty/", include("facultyapp.urls") , name="faculty"),
    path('', views.Login_view.as_view(),name="login"),
    path('signup/', views.Signup_view.as_view(), name="signup"),
    path('forgotpassword/', views.ForgotPassword_view.as_view(),name="forgotpassword"),
    path('forgotpassword/<email>', views.ResetOtp_view.as_view() ,name="reset_otp"),


    # main
    
    path('home/',views.Home.as_view(),name='home'),
    path('select-department/',views.selectdepartment,name='selectdepartment'),
    path('make-a-complaint/',views.Make_a_Complaint.as_view(),name='makeacomplaint'),
    path('make-a-complaint/<id>',views.Make_a_Complaint.as_view(),name='makeacomplaint'),
    path('all/',views.all,name='all'),
    path('open/',views.open,name='open'),
    path('closed/',views.closed,name='closed'),
    path('dropped/',views.dropped,name='dropped'),
    path('positive/',views.positive,name='positive'),
    path('negative/',views.negative,name='negative'),
    path('pendingfeedbacks/',views.pendingfeedbacks,name='pendingfeedbacks'),
    path('feedbacks/<complaint_id>',views.Feedbacks.as_view(),name='feedbacks'),
    path('feedback-details/<complaint_id>',views.feedback_detail,name='feedbackdetails'),
    path('complaint-views/complaint=<uuid>',views.viewcomplaint,name='viewcomplaints'),
    path('dropcomplaints/complaint=<uuid>',views.dropcomplaints,name='dropcomplaints'),
    path('see-details/complaint=<uuid>',views.seedetails,name='seedetails'),
   
    path('page-not-found/',views.page_not_found,name='page-not-found'),
    path('logout/',views.logout,name='logout'),
]
urlpatterns += static(MEDIA_URL,document_root=MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)