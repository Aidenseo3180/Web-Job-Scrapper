import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode = "w")
  #open file as write only
  writer = csv.writer(file) #writer 설정
  writer.writerow(["title", "company", "location", "link"])
  for job in jobs:
    writer.writerow(list(job.values()))
    #writerow는 한줄로 jobs.csv파일에 써줌 (우리가 그렇게 설정했으니까)
    #job은 dictionary, 그래서 job.values()를 사용해서 바로 value를 얻어올 수 있음
    #이걸 list로 형변환해서 프린트함 (dict 타입은 좀 지저분해서)
  return

