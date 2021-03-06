from flask import Flask, render_template, request, redirect, escape, session
from vsearch import search4letters
from DBcm import UseDataBase, ConnectionError, CredentialError, SQLError
from checker import check_logged_in
from threading import Thread
from flask import copy_current_request_context

app = Flask(__name__)


app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'vsearchpasswd',
                          'database': 'vsearchlogDB', }


@app.route('/search4', methods=['post'])
def do_search() -> 'html':

    @copy_current_request_context
    def log_request(req: 'flask_request', res: str) -> None:
        """Journal web-request and return results."""
        with UseDataBase(app.config['dbconfig']) as cursor:
            _SQL = """insert into log
                      (phrase, letters, ip, browser_string, results)
                      values
                      (%s, %s, %s, %s, %s)"""
            cursor.execute(_SQL, (req.form['phrase'],
                                  req.form['letters'],
                                  req.remote_addr,
                                  req.user_agent.browser,
                                  res, ))

    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    try:
        t = Thread(target=log_request, args=(request, results))
        t.start()
    except Exception as err:
        print('***** Logging failed with this error:', str(err))
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results,)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    try:
        with UseDataBase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, Results
                      from log"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ('phrase', 'letters', 'Remote_addr', 'browser', 'Results')
        return render_template('viewlog.html',
                               the_title='View Log',
                               the_row_titles=titles,
                               the_data=contents,)
    except ConnectionError as err:
        print('Is your database switchd on? Error:', str(err))
    except CredentialError as err:
        print('User-id/Password issues. Error', str(err))
    except SQLError as err:
        print('Is your query correct? Error:', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))


@app.route('/login')
def do_login():
    session['logged in'] = True
    return 'You are now logged in.'


app.secret_key = 'YouWillNeverGuessMySecretKey'


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')


if __name__ == '__main__':
    app.run(debug=True)
