from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('uploadfile/', views.FileUploadView.as_view()),
    path('labels/', views.LabelListAPIView.as_view(), name='label-list'),
    path('addvideo/', views.AddVideoView.as_view()),
    path('getvideodetail/', views.GetVideoDetailView.as_view()),
    path('getbannerlist/', views.BannerListView.as_view()),
    path('getrecommandlist/', views.RecommandListView.as_view()),
    path('getvideolist/', views.GetVideoList.as_view()),
    path('addhistoryrecord/', views.AddHistoryRecord.as_view()),
    path('getlabelvideolist/', views.GetLableVideoListView.as_view()),
    path('gethistoryrecordlist/', views.GetHistoryRecordList.as_view()),
    path('getuserinfo/', views.GetUserInfo.as_view()),
    path('subscribe/', views.Subscribe.as_view()),
    path("getsubscribestatus/", views.getSubscribeStatus.as_view()),
    path("cancelsubscribe/", views.CancelSubscribe.as_view()),
    path("getcreatorvideolist/", views.GetCreatorVideoList.as_view()),
    path("getsubscribelist/", views.GetSubscribeList.as_view()),
    path("updateuserinfo/", views.UpdateUserInfo.as_view()),
    path("getuploadvideolist/", views.GetUploadVideoList.as_view())
]
 