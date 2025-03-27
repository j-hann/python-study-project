
from django.urls import path
from jobs.views import JobPostListCreateView, JobPostRetrieveView

urlpatterns = [
    path('jobs/', JobPostListCreateView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobPostRetrieveView.as_view(), name='job-detail'),

]