import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    #div에 있는 class인 s-pagination에 가서 <a>를 찾음

    last_pages = pages[-2].get_text(strip=True)
    #-1은 next니까 그 이전(마지막 페이지)를 부르려면 -2를 하면 됨!
    #get.text로 <a>에서 페이지 넘버만 뽑아오고, strip=True로 whitespace들을 없앰
    return int(last_pages)  #get_text는 string, int로 변환해줌


def extract_jobs(last_page):
    #indeed의 extract_indeed_jobs하고 비슷함
    jobs = []

    for page in range(
            last_page):  #range는 string을 accept안함. 그래서 int(last_pages)를 했던것
        print(f"Scrapping SO : Page - {page+1}")
        result = requests.get(f"{URL}&pg={page+1}")
        #print(result.status_code)  #정상적으로 작동하면 200을 프린트
        #그래서 last_page의 수만큼 200을 프린트함
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        #div에서 class가 -job을 가진것을 모두 찾음
        for job_result in results:
            #print(job_result["data-jobid"])
            #그리고 같은 공간<div>에서 data-jobid라는 것을 찾아 프린트
            job = find_jobs(job_result)
            jobs.append(job)
    return jobs


def find_jobs(html):  #find title
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]

    try:
        #python에선 리스트 안에 2개의 item이 들어있다면 company,location처럼 두개로 나눠서 넣을 수 있음 (따로 변수 생성 안하고 한꺼번에 가능
        company, location = html.find("h3", {
            "class": "mb4"
        }).find_all("span", resursive=False)
        #find_all은 조건이 맞으면 html이 얼마나 깊던지 간에 다 프린트함
        #span이란게 있으면 그 span안에 뭐가 더 들어있던 일단 가져오고 봄
        #그래서 recursive=False로 전부 가져오는걸 방지!

        company = company.get_text(strip=True)
        location = location.get_text(strip=True)
        job_id = html["data-jobid"]

    except ValueError:  #가끔 span이 3개인 경우일때 ValueError을 catch
        company, location, _ = html.find("h3", {
            "class": "mb4"
        }).find_all("span", resursive=False)
        company = company.get_text(strip=True)
        location = location.get_text(strip=True)
        _ = _.get_text(strip=True)  #3번째 span이 들어갈 곳을 만듦
        job_id = html["data-jobid"]


    return {
        'title': title,
        'company': company,
        'location': location,
        'apply_link': f"https://stackoverflow.com/jobs/{job_id}"
    }


def get_SO_jobs():
    last_page = get_last_page()  #returns last_pages
    jobs = extract_jobs(last_page)
    return jobs
