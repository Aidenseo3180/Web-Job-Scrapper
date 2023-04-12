import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def extract_indeed_pages():
    result = requests.get(URL) 

    soup = BeautifulSoup(result.text, "html.parser")

    next_button = soup.find("a", {"aria-label": "Next"})

    count = 0  #count the number of while loops
    start = 0  #start number
    while (next_button):
        Last_URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}&start={(start)}"
        Last_result = requests.get(Last_URL)  #txt를 가져옴
        Last_soup = BeautifulSoup(Last_result.text, "html.parser")

        next_button = Last_soup.find("a", {"aria-label": "Next"})

        count += 1  #count the pages

        start = int(start) + 50  #add start+50 to move to the next page

        if (next_button == None):  #exit when there's no more next_button
            break  #end the loop

    return count

def extract_indeed_jobs(last_page):  #직업 찾는데 쓸 것
  jobs = []
  for page in range(last_page):
    print(f"Scrapping Indeed : Page - {page + 1}")

    result = requests.get(f"{URL}&start={page*LIMIT}")
    
    soup = BeautifulSoup(result.text, "html.parser")

    results = soup.find_all("div", {"class": "slider_container"})

    for result in results:  #하나씩 꺼냄
        job = extract_jobs(result)
        jobs.append(job)

  return jobs


def extract_jobs(html): 
  company = html.find("span", {"class": "companyName"})
  company_anchor = company.find("a")

  title = html.find("h2", {"class": "jobTitle"})

  for each_title in title:  #for title
      if each_title.get("title") is not None:  #if not None
          spans_title = each_title.get("title")

  if company_anchor is not None:
      company = str(company_anchor.string)
  else:
      company = str(company.string)

  location = html.select_one("pre > div").text

  #job id
  job_id = html.parent["data-jk"]

  return {
      'job': spans_title,
      'company': company,
      'location': location,
      'link': f"https://www.indeed.com/viewjob?jk={job_id}&from=serp&vjs=3"
  }

def get_indeed_jobs():
  last_page = extract_indeed_pages()
  jobs = extract_indeed_jobs(last_page)
  return jobs
