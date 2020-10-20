import re

from flask import redirect, render_template, url_for, request, session
from flask_login import current_user, logout_user
import tweepy as twp

from app.main import main
from app.main.methods.api_engine import authenticate, extract_tweets_from_q

from app.main.forms import SearchForm
from app.main.preprocesser import Preprocesser

import pandas as pd
import datetime as dt
from numpy.random import rand
@main.route("/")
def home():
    try:
        session.pop('host')
    except KeyError:
        pass
    return render_template("main/home.html")


@main.route("/search/set/<host>", methods=["POST", "GET"])
def set_host(host):
    session['host'] = host
    if host == 'client':
        if current_user.is_authenticated:
            return redirect(authenticate(host=host))
        return redirect(url_for('auth.login'))
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('main.search', host=host))


@main.route("/search/<host>", methods=["POST", "GET"])
def search(host):
    form = SearchForm()
    if request.method == "POST":
        return redirect(url_for('main.print_scores', host=host, q=form.build_query()))
    if request.values.get('oauth_verifier') is not None:
        session['oauth_verifier'] = request.values.get('oauth_verifier')
        return redirect(url_for('main.search', host=host))
    return render_template("main/search.html", form=form)


@main.route("/search/<host>/<q>", methods=["GET", "POST"])
def print_scores(host, q):
    if request.method == 'GET':
        if ('handled_q' in session.keys()) and (session['handled_q'] == q):
            return render_template('main/visualization.html', auth=authenticate(host=host, on_callback=True if host == 'client' else False), host=host, q=q, scores=session['results'])
        if re.search("\w", q) is None:
            return redirect(url_for('main.search', host=host))
        auth = authenticate(host=host, on_callback=True if host == 'client' else False)
        if True:  # always run the demo
            date_time_obj = [dt.date.today() - dt.timedelta(days=1),
                             dt.date.today() - dt.timedelta(days=2),
                             dt.date.today() - dt.timedelta(days=3),
                             dt.date.today() - dt.timedelta(days=4),
                             dt.date.today() - dt.timedelta(days=5),
                             dt.date.today() - dt.timedelta(days=6),
                             dt.date.today() - dt.timedelta(days=7)
                             ]
            dummy_data = [[rand(),rand(),rand(),rand(),date_time_obj[i]] for i in range(len(date_time_obj))]
            dummy_data = pd.DataFrame(dummy_data,columns=["neg_sent","pos_sent","comp_sent","polarity","date"])
            dummy_data["date"] = pd.to_datetime(dummy_data["date"])
            preprocesser = Preprocesser(dummy_data)
            session['results'] = {
                'd_7_mean_scores': preprocesser.simple_mean(to_json=True),
                'd_7_means_by_date': preprocesser.by_date_mean(unix=True, to_json=True)
            }
            session['handled_q'] = q
            return render_template('main/visualization.html', auth=auth, host=host, q=q, scores=session['results'])
        else:
            from app.main.methods.sentiment_engine import analyze_sentiments
            try:
                preprocesser = Preprocesser(analyze_sentiments(extract_tweets_from_q(query=q, api=twp.API(auth, wait_on_rate_limit=True), use_pages=False, num=200)))
            except TypeError:
                return render_template('main/visualization.html', auth=auth, host=host, q=q, form=SearchForm(submit_label='Try again'))
            else:
                session['results'] = {
                                        'd_7_mean_scores': preprocesser.simple_mean(to_json=True),
                                        'd_7_means_by_date': preprocesser.by_date_mean(unix=True, to_json=True)
                                      }
                print(session['results'])
                session['handled_q'] = q
                return render_template('main/visualization.html', auth=auth, host=host, q=q, scores=session['results'])
    return redirect(url_for('main.print_scores', host=host, q=SearchForm(submit_label='Try again').build_query()))
