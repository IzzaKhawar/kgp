from django.contrib import admin
from django.urls import path
from . import views
from kgp.settings import MEDIA_ROOT,MEDIA_URL
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login/', views.Login_view.as_view(),name="hodlogin"),


    # main
    path('home/',views.Home.as_view(),name='hodhome'),

    path('all/',views.all,name='hodall'),
    path('open/',views.open,name='hodopen'),
    path('closed/',views.closed,name='hodclosed'),
    path('cancelled/',views.canceled,name='hodcanceled'),
    path('forwarded/',views.forwarded,name='hodforwarded'),
    path('feedback/',views.feedback,name='hodfeedback'),
    path('feedbacks-details/',views.feedback_detail,name='hodfeedbackdetails'),

    path('complaint-views/complaint=<uuid>',views.viewcomplaint,name='hodviewcomplaints'),
    path('complaint-views/close-complaint=<uuid>',views.Close_Complaint_View.as_view(),name='hodclosecomplaints'),
    path('complaint-views/cancel-complaint=<uuid>',views.Cancel_Complaint_View.as_view(),name='hodcancelcomplaints'),
    path('complaint-views/forward-complaint=<uuid>',views.Forward_Complaint_View.as_view(),name='hodforwardcomplaints'),
    #path('dropcomplaints/complaint=<uuid>',views.dropcomplaints,name='hoddropcomplaints'),
   
    path('page-not-found/',views.page_not_found,name='hodpage-not-found'),
    path('logout/',views.logout,name='hodlogout'),
]
