
from rest_framework import generics

from jobs.models import JobPost
from jobs.serializers import JobPostSerializer


# 전체 목록 조회(GET) & 등록(POST)
class JobPostListCreateView(generics.ListCreateAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer

# 상세 조회(GET)
class JobPostRetrieveView(generics.RetrieveAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
