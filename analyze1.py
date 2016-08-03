# Just a first crack at analyzing the LinkedIn data
# This script figures out the first job each person had after GA
# and the last job they had before GA
# then writes all that to a spreadsheet.

# imports
import json
import os
from collections import Counter
import xlwt
from bs4 import BeautifulSoup

# functions
def open_json(ToOpen):
    if os.path.isfile(ToOpen) and os.path.getsize(ToOpen) > 0:
        with open(ToOpen) as data_file:    
            return json.load(data_file)
    else:
        return 0

def GA_date(dude):
    grad_from_GA = 3000
    for each_school in dude['educations']:
        if each_school['schoolName'] == 'General Assembly':
            try:
                # some people went to GA more than once
                # let's look at their last grad date
                if each_school['endDateYear'] < grad_from_GA:
                    grad_from_GA = each_school['endDateYear']
            except KeyError:
                # no date given for GA
                grad_from_GA = 1
    return grad_from_GA

def fake_job(company_name, title):
    company_name = str.lower(company_name)
    title = str.lower(title)
    if "freelance" in company_name:
        return True
    if "freelance" in title:
        return True
    if "independent contractor" in company_name:
        return True
    if "general ass" in company_name:
        return True
    return False

def unbold(html_shit):
    soup = BeautifulSoup(html_shit, 'html.parser')
    return soup.get_text()

def first_job_out(dude,grad_from_GA):
    sorty_list = []
    first_company = 'None'
    first_year = 3000
    first_month = 12
    job_list = dude['pastPositions'] 
    # sometimes they don't have current positions...
    try:
        job_list += dude['currentPositions']
    except KeyError:
        pass

    for each_job in job_list:
        try:
            start_year = int(each_job['startDateYear'])
        except KeyError:
            # no start date on this job so ignore it
            # it's probably old, but either way it's useless
            continue
        
        try: 
            start_month = int(each_job['startDateMonth'])
        except KeyError:
            start_month = 12
        
        company = each_job['companyName']
        
        try:
            first_title = unbold(each_job['title'])
        except KeyError:
            first_title = ""        
        # companyID also avaiable here

        # sorty list is a list of all their jobs past and current
        # with slight cleanup, eg absent title reduced to blank
        sorty_list.append({'company':company,"start_year":start_year,"start_month":start_month,"title":first_title})
    
    for each_job in sorty_list:
        if fake_job(each_job['company'],each_job['title']):
            continue
        # ignore jobs before GA
        if each_job['start_year'] >= grad_from_GA:
            # if job start year = what we thought was first, check months
            if each_job['start_year'] == first_year:
                if each_job['start_month'] < first_month:
                    first_year = each_job['start_year']
                    first_month = each_job['start_month']
                    first_company = each_job['company']
                    first_title = each_job['title']
            # else if job start year < first year of job after GA, 
            # this is the first job
            elif each_job['start_year'] < first_year:
                first_year = each_job['start_year']
                first_month = each_job['start_month']
                first_company = each_job['company']
                first_title = each_job['title']
    if first_year == 3000:
        # maybe never left their old job
        # maybe never got a job
        # but honestly everyone has a bullshit line here anyway about being
        # CEO of Nothing Inc.
        if verbose: print("")
    else:
        if verbose: print(first_company, "title:", first_title)
    return [first_company, first_title]

def get_first_employers(people):
        employers = []
        titles = []
        entries = 0
        for profile in people:
            if verbose: 
                try:
                    print(profile["firstName"],profile["lastName"], end=": ")
                except KeyError:
                    print("anonymous", end=": ")
            # find what year this person graduated from GA
            class_year = GA_date(profile)
            if class_year == 0:
                if verbose: print("No record of attending GA")
            if class_year == 1:
                if verbose: print("No graduation date listed for GA")
            if class_year > 1:
                # find what jobs she had that year
                the_company, the_job = first_job_out(profile,class_year)
                employers.append(the_company)
                titles.append(the_job)
            entries += 1
        if entries != 25: print(entries+"/25 records")
        return employers, titles

def last_job_before(dude,grad_from_GA):
    sorty_list = []
    last_company = 'None'
    last_title = 'None'
    last_year = 3000
    last_month = 12
    job_list = dude['pastPositions'] 
    # sometimes they don't have current positions...
    try:
        job_list += dude['currentPositions']
    except KeyError:
        pass

    for each_job in job_list:
        try:
            start_year = int(each_job['startDateYear'])
        except KeyError:
            # no start date on this job so ignore it
            # it's probably old, but either way it's useless
            continue
        
        try: 
            start_month = int(each_job['startDateMonth'])
        except KeyError:
            start_month = 12
        
        company = each_job['companyName']
        
        try:
            first_title = unbold(each_job['title'])
        except KeyError:
            first_title = ""        
        # companyID also avaiable here

        # sorty list is a list of all their jobs past and current
        # with slight cleanup, eg absent title reduced to blank
        sorty_list.append({'company':company,"start_year":start_year,"start_month":start_month,"title":first_title})
    
    for each_job in sorty_list:
        # if they listed GA as a job also ignore that
        if 'general ass' in str.lower(each_job['company']):
            continue
        
        # only look at jobs before GA
        if each_job['start_year'] <= grad_from_GA:
            # if job start year = what we thought was first, check months
            if each_job['start_year'] == last_year:
                if each_job['start_month'] < last_month:
                    last_year = each_job['start_year']
                    last_month = each_job['start_month']
                    last_company = each_job['company']
                    last_title = each_job['title']
            # else if job start year < first year of job after GA, 
            # this is the first job
            elif each_job['start_year'] < last_year:
                last_year = each_job['start_year']
                last_month = each_job['start_month']
                last_company = each_job['company']
                last_title = each_job['title']
    if last_year == 3000:
        # maybe had not job before
        if verbose: print("")
    else:
        if verbose: print(last_company, "title:", last_title)
    return [last_company, last_title]

def get_last_job(people):
        entries = 0
        page_of_last_jobs = []
        for profile in people:
            if verbose: 
                try:
                    print(profile["firstName"],profile["lastName"], end=": ")
                except KeyError:
                    print("anonymous", end=": ")
            # find what year this person graduated from GA
            class_year = GA_date(profile)
            if class_year == 0:
                if verbose: print("No record of attending GA")
            if class_year == 1:
                if verbose: print("No graduation date listed for GA")
            if class_year > 1:
                # find what jobs she had that year
                the_old_job = last_job_before(profile,class_year)
                page_of_last_jobs.append(the_old_job)
            entries += 1
        if entries != 25: print(entries+"/25 records")
        return page_of_last_jobs




def write_jobs_to_excel(companies, titles, old_jobs, fn):
    
    wb = xlwt.Workbook()
    ws = wb.add_sheet('First Jobs')

    for i, company in enumerate(companies):
        ws.write(i, 0, company)
        ws.write(i, 1, companies[company])
    
    ws = wb.add_sheet('First Titles')

    for i, title in enumerate(titles):
        ws.write(i, 0, title)
        ws.write(i, 1, titles[title])

    ws = wb.add_sheet('Previous Jobs')

    for i, job in enumerate(old_jobs):
        ws.write(i, 0, job[0])
        ws.write(i, 1, job[1])
    


    wb.save(fn)





# variables for main loop
jsondir = 'json/'
employers = []
titles = []
main_last_jobs = []
verbose = input("Verbose?")
if verbose == 1 or verbose == "yes" or verbose =="y":
    verbose = True
else:
    verbose = False

# main loop
for each_file in os.listdir(jsondir):
    # open the json file
    full_data = open_json(jsondir + each_file)
    # get the list of usually 25 people. it's a list
    people = full_data["data"]["result"]["searchResults"]
    # look at each entry on this list. each entry = 1 person.
    print("\nScanning file",each_file)
    
    # grab slice of data
    the_employers, the_titles = get_first_employers(people)
    employers.extend(the_employers)
    titles.extend(the_titles)
    
    main_last_jobs.extend(get_last_job(people))


# save slice of data
ranked_employers = Counter(employers)
ranked_titles = Counter(titles)
write_jobs_to_excel(ranked_employers, ranked_titles, main_last_jobs, "UXDI_Careers.xls")
