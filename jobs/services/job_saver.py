

# 스크래핑 데이터 저장 메서드
def save_jobs_to_db(jobs):
    from jobs.models import JobPost

    saved_count = 0

    for job_date in jobs:
        # 해당 공고 url이 존재하지 않으면
        if not JobPost.objects.filter(url=job_date["url"]).exists():
            JobPost.objects.create(
                title=job_date["title"],
                company=job_date["company"],
                location_experience=job_date["location_experience"],
                url=job_date["url"],
                description=job_date["description"],
            )
            saved_count = saved_count + 1
            
    print(f"DB에 저장된 공고 : {saved_count}건")
