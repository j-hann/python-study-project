import os
import time

import django
from playwright.sync_api import sync_playwright
from jobs.services.job_saver import save_jobs_to_db

# Django 환경 세팅
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_study_project.settings')
django.setup()

# 필터링 키워드 목록
block_keywords = ["프론트엔드", "frontend", "React", "스마트팩토리"]

# TODO : 우대사항 추가 예정
# 상세 설명 데이터 목록
description_keywords = ["주요업무", "자격요건"]


# 상세 설명 데이터 스크래핑 - 주요업무, 자격요건, 우대사항
# def scrape_description_selections(context, url):
#     try:
#         detail_page = context.new_page()
#         detail_page.goto(url)
#         detail_page.wait_for_selector("div.JobDescription_JobDescription__paragraph__87w8I", timeout=5000)
#
#         blocks = detail_page.query_selector_all("div.JobDescription_JobDescription__paragraph__87w8I")
#         extracted = {}
#
#         for block in blocks:
#             heading = block.query_selector("h3")
#
#             if heading:
#                 title = heading.inner_text().strip()
#                 if title in description_keywords:
#                     # h3 제외한 나머지 텍스트 추출
#                     full_text = block.inner_text().strip()
#                     content_text = full_text.replace(title, "").strip()
#                     extracted[title] = content_text.replace("\n", "\nㆍ")
#
#         detail_page.close()
#
#         parts = []
#         for label in description_keywords:
#             if label in extracted:
#                 parts.append(f"[{label}]\n{extracted[label]}")
#
#         return "\n\n".join(parts)
#
#     except Exception as e:
#         print(f"상세 설명 파싱 실패 ({url}):", e)
#         return ""

# 원티드 공고 스크래핑
def scrape_wanted_jobs():
    with sync_playwright() as p:
        # TODO : headless 환경 실행 해결하기 - 배포시 True 설정 필수
        # 크롬 브라우저 백그라운드 실행 유무 (False - 백그라운드 실행)
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context()
        page = context.new_page()

        # 조건 : 지역 - 서울, 직무 - 서버 개발자, 웹 개발자, 자바 개발자, 경력 - 0 ~ 3년차, 정렬 - 인기순
        url = (
            "https://www.wanted.co.kr/wdlist/518"
            "?country=kr"
            "&job_sort=job.popularity_order"
            "&years=0&years=3"
            "&selected=660&selected=872&selected=873"
            "&locations=seoul.all"
        )
        page.goto(url)
        try:
            # 공고 로딩 완료 대기
            page.wait_for_selector("li.Card_Card__aaatv", state="attached")
        except:
            print("로딩 실패")

        # 페이지 로딩 2초 대기
        time.sleep(2)
        # 스크롤 내리기 - 2번
        # scroll_down(page)

        # 공고 리스트 항목 가져오기
        cards = page.query_selector_all("li.Card_Card__aaatv")

        # 채용 공고 하나씩 가져와서 정보 추출
        results = []
        for card in cards:
            try:
                # 공고 제목 가져오기
                title_el = card.query_selector("span.JobCard_JobCard__body__position__NLhOu")
                # 회사 이름 가져오기
                company_el = card.query_selector(
                    "span.CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__company__ByVLu")
                # 회사 위치 & 경력 가져오기
                loc_exp_el = card.query_selector(
                    "span.CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__location__4_w0l")
                # 공고 상세 페이지 링크
                link_el = card.query_selector("a[href^='/wd/']")

                # 텍스트 추출
                if title_el and company_el and loc_exp_el and link_el:
                    title = title_el.inner_text().strip()

                    # 공고 제목 필터링 - 소문자로 변환해서 비교
                    if any(word.lower() in title.lower() for word in block_keywords):
                        continue

                    company = company_el.inner_text().strip()
                    location_experience = loc_exp_el.inner_text().strip()
                    link = link_el.get_attribute("href").strip()
                    full_url = f"https://www.wanted.co.kr{link}"

                    # 상세 설명 스크래핑 메서드 호출
                    description = scrape_description_selections(context, full_url)

                    # 결과 리스트 저장
                    results.append({
                        "title": title,
                        "company": company,
                        "location_experience": location_experience,
                        "url": full_url,
                        "description": description,
                    })

            except Exception as e:
                print("파싱 오류 : ", e)
                continue

        print(f"스크래핑 완료 : {len(results)}건")
        browser.close()
        # 공고 목록 리스트 반환
        return results


# 스크롤 내려주는 메서드
def scroll_down(page, times=2, delay=1.5):
    for _ in range(times):
        # 세로 방향으로 휠 내리기
        page.mouse.wheel(0, 10000)
        time.sleep(delay)


# 상세 설명 데이터 스크래핑 - 주요업무, 자격요건
def scrape_description_selections(context, url):
    try:
        detail_page = context.new_page()
        detail_page.goto(url)
        detail_page.wait_for_selector("div.JobDescription_JobDescription__paragraph__87w8I", timeout=5000)

        blocks = detail_page.query_selector_all("div.JobDescription_JobDescription__paragraph__87w8I")
        extracted = {}

        for block in blocks:
            heading = block.query_selector("h3")
            content = block.query_selector("span span")

            if heading and content:
                title = heading.inner_text().strip()
                if title in description_keywords:
                    text = content.inner_text().strip()
                    extracted[title] = text.replace("\n", "\nㆍ")

        detail_page.close()

        parts = []
        for label in description_keywords:
            if label in extracted:
                parts.append(f"[{label}]\n{extracted[label]}")

        return "\n\n".join(parts)

    except Exception as e:
        print(f"상세 설명 파싱 실패 ({url}):", e)
        return ""


# 실행 메서드
if __name__ == "__main__":
    # 스크래핑 메서드 호출
    jobs = scrape_wanted_jobs()
    # 스크래핑 데이터 저장 메서드 호출
    save_jobs_to_db(jobs)

    # 결과 출력
    for job in jobs:
        print(job)
