from django.urls import path 
from . import views
from .views import  TrackCreateView, TrackDetailView, TrackListView,TrackDeleteView, CompareCreateView, CompareListView, CompareDetailView, CompareDeleteView

urlpatterns = [
	path('', views.home, name = 'home'),
	#path('form/', views.upload, name = 'form'),
	#path('files/', views.file_list, name='file_list'),
	#path('map/', FoliumView.as_view(), name='map'),
	path('files/', TrackListView.as_view(), name='track-list'),
	path('files/new/',TrackCreateView.as_view(), name = 'create-track'),
	path('gpxtrack/<int:pk>/', TrackDetailView.as_view(), name='gpxtrack-detail'),
	path('gpxtrack/<int:pk>/delete/', TrackDeleteView.as_view(), name='gpxtrack-delete'),
	path('compare/new/', CompareCreateView.as_view(), name='create-compare'),
	path('compare/', CompareListView.as_view(), name='compare-list'),
	path('gpxcompare/<int:pk>/', CompareDetailView.as_view(), name='compare-detail'),
	path('compare/<int:pk>/delete/', CompareDeleteView.as_view(), name='compare-delete'),
]