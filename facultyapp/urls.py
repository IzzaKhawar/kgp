
from django.urls import path
from facultyapp import views


urlpatterns = [
    path('login/', views.Login_view.as_view(),name="facultylogin"),
 
    # main
    path('home/',views.Home.as_view(),name='facultyhome'),
    path('all/',views.all,name='facultyall'),
    path('open/',views.open,name='facultyopen'),
    path('closed/',views.closed,name='facultyclosed'),
    path('canceled/',views.canceled,name='facultycanceled'), 
    path('feedback/',views.feedback,name='facultyfeedback'),
    path('feedbacks-details/',views.feedback_detail,name='facultyfeedbackdetails'),

    path('complaint-views/complaint=<uuid>',views.viewcomplaint,name='facultyviewcomplaints'),
    path('complaint-views/close-complaint=<uuid>',views.Close_Complaint_View.as_view(),name='facultyclosecomplaints'),
    path('complaint-views/cancel-complaint=<uuid>',views.Cancel_Complaint_View.as_view(),name='facultycancelcomplaints'),
   
    path('page-not-found/',views.page_not_found,name='facultypage-not-found'),
    path('logout/',views.logout,name='facultylogout'),
]