import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def extract_indeed_pages(): #maximum page number을 찾음
    result = requests.get(URL)  #페이지 txt를 가져옴

    soup = BeautifulSoup(result.text, "html.parser")
    #그리고 이 페이지txt에 있는 html를 가져오고 soup으로 만듦

    next_button = soup.find("a", {"aria-label": "Next"})

    count = 0  #count the number of while loops
    start = 0  #start number
    while (next_button):
        Last_URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}&start={(start)}"
        Last_result = requests.get(Last_URL)  #txt를 가져옴
        Last_soup = BeautifulSoup(Last_result.text, "html.parser")
        #이 txt에서 html가져옴

        next_button = Last_soup.find("a", {"aria-label": "Next"})
        #여기서 arial-label이 Next인가? 를 찾음

        count += 1  #count the pages

        start = int(start) + 50  #add start+50 to move to the next page

        if (next_button == None):  #exit when there's no more next_button
            break  #end the loop

    return count

    #pagination = soup.find("div",{"class" : "pagination"})
    #soup을 이용해서 div에서 클래스명이 pagination인걸 찾음

# links = []
#while (True) :
#   links = pagination.find_all('a')
#그리고 <a>를 찾음 (링크를 포함한 pagination에 있던 <a></a>))
#이 a를 anchor이라 함

#pages = []  #빈 문자열
#for link in links[0:-1]:
#pages.append(link.find("span").string)
#그리고 이 <a>안에는 span이라는것이 있음
#그래서 이 빈 문자열에 page에서 span이 앞에 있는걸들을 찾고,
#.string으로 내용을 가져옴

#  pages.append(int(link.string))
#근데 이렇게 그냥 anchor에서도 찾을 수 있음
#만약 anchor에 string이 1개면 이렇게 쉽게 가능함!
#그리고 찾은걸 int형으로 변환함


#  max_page = pages[-1]  #max_page 인 5가 들어감 (-1인 뒤에서 1개 세는것)
#  return max_page


def extract_indeed_jobs(last_page):  #직업 찾는데 쓸 것
  jobs = []
  for page in range(last_page):
  #range(last_page)하면 0~last_page라는 말
    print(f"Scrapping Indeed : Page - {page + 1}")
    #to see what page we're at

    result = requests.get(f"{URL}&start={page*LIMIT}")
    #page의 URL을 이용해서 각 페이지의 request (txt)를 받아옴
    #그리고 이걸 result에 넣음

    #print(result.status_code) #status 200가 나오면 정상적으로 잘 된것!
    #그래서 이 status가 200이 5개(끝 페이지)나오면 성공적으로 된것

    soup = BeautifulSoup(result.text, "html.parser")
    #직업을 찾으려면 먼저 soup으로 html을 가져와야 함!

    results = soup.find_all("div", {"class": "slider_container"})

    for result in results:  #하나씩 꺼냄
        job = extract_jobs(result)
        jobs.append(job)

  return jobs


def extract_jobs(html):  #soup을 매개변수로 받음 (이 경우 div slider)
  #company이름을 불러옴
  company = html.find("span", {"class": "companyName"})
  company_anchor = company.find("a")

  title = html.find("h2", {"class": "jobTitle"})
  #h2에서 class가 jobTitle인것들을 가져옴 (results에 넣음)

  #all_title = title.find("span")
  #span이란 곳을 먼저 찾음 (알고 보니 찾을 필요 없었음)

  for each_title in title:  #for title
      if each_title.get("title") is not None:  #if not None
          spans_title = each_title.get("title")
      #모든 title들을 찾음

  if company_anchor is not None:
      company = str(company_anchor.string)
  else:
      company = str(company.string)

  #location
  location = html.select_one("pre > div").text
  #pre > div는 <pre>안에 있는 <div>를 가져온다는 뜻!
  #그래서 <pre>에 있는 <div class="companyLocation">에 들어가서 location을 가져올 수 있는것
  #select_one : finds only the first tag that matches a selector

  #job id
  job_id = html.parent["data-jk"]
  #html의 parent, 즉 div slider_container의 parent인 <a>에서 가져온다는 뜻. 이 경우, data-jk를 가져옴 (['data-jk']로 attribute 설정하는것)

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