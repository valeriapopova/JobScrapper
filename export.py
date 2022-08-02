import csv


def save_to_csv(jobs):
    file = open('vacancies.csv', mode='w')
    writer = csv.writer(file)
    writer.writerow(['title', 'company', 'location', 'date',  'link'])
    for job in jobs:
        writer.writerow(list(job.values()))
    return
