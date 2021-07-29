from indeed import get_indeed_jobs
from so import get_SO_jobs
from save import save_to_file

#For Indeed (Python)
indeed_jobs = get_indeed_jobs()

#For stack over flow (python)
stack_jobs = get_SO_jobs()

jobs = stack_jobs+indeed_jobs  #for excel spread sheet
save_to_file(jobs)




