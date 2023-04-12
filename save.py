import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode = "w")
  #open file as write only
  writer = csv.writer(file) #writer 설정
  writer.writerow(["title", "company", "location", "link"])
  for job in jobs:
    writer.writerow(list(job.values()))
   
  return

