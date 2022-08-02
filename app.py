from flask import Flask, render_template, request, redirect, send_file
from parser import get_job
from export import save_to_csv

app = Flask('parser')
db = {}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/report')
def report():
    keyword = request.args.get('keyword')
    if keyword is not None:
        keyword = keyword.lower()
        getDB = db.get(keyword)
        if getDB:
            jobs = getDB
        else:
            jobs = get_job(keyword)
            db[keyword] = jobs
    else:
        return redirect('/')
    return render_template('report.html', searchBy=keyword, jobs=jobs, num_results=len(jobs))


@app.route('/export')
def export():
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            raise Exception()
        keyword = keyword.lower()
        jobs = db.get(keyword)
        if not jobs:
            raise Exception
        save_to_csv(jobs)
        return send_file('vacancies.cvs')
    except:
        return redirect('/')


if __name__ == '__main__':
    app.run()
