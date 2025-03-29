from django.contrib.auth.models import User
from django.db import models


# 채용 공고 모델
class JobPost(models.Model):

    # 공고 제목
    title = models.CharField(max_length=255)
    # 회사명
    company = models.CharField(max_length=255)
    # 회사 위치, 경력
    location_experience = models.CharField(max_length=255)
    # url 주소
    url = models.URLField()
    # 설명
    description = models.TextField()
    # 스크랩 날짜 (자동 추가)
    scraped_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"[{self.company}] {self.title}"


# 찜하기 모델
class Favorite(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta :
        # 중복 찜 방지
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} likes {self.job.title}"