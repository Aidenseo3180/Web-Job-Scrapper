import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")

    last_pages = pages[-2].get_text(strip=True)
    
    return int(last_pages)  #get_text는 string, int로 변환해줌


def extract_jobs(last_page):
    jobs = []

    for page in range(
            last_page):  
        print(f"Scrapping SO : Page - {page+1}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for job_result in results:
            
            job = find_jobs(job_result)
            jobs.append(job)
    return jobs


def find_jobs(html):  #find title
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]

    try:
        company, location = html.find("h3", {
            "class": "mb4"
        }).find_all("span", resursive=False)
        
        company = company.get_text(strip=True)
        location = location.get_text(strip=True)
        job_id = html["data-jobid"]

    except ValueError: 
        company, location, _ = html.find("h3", {
            "class": "mb4"
        }).find_all("span", resursive=False)
        company = company.get_text(strip=True)
        location = location.get_text(strip=True)
        _ = _.get_text(strip=True)  
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
