from flask import Flask, render_template, request, escape
from flask import copy_current_request_context
from vsearch import search4letters # importing search4letters
from DBcm import UseDatabase, ConnectionError, CredentialsError, SQLError
from threading import Thread
from time import sleep



app = Flask(__name__)


app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'IAmEnough',
                          'database': 'vsearchlogDB', }

def log_request(req: 'flask request', res: str) -> None:
    """Log details of the web request and the results."""
        
    
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log
            (phrase, letters, ip, browser_string, results)
            values
            (%s, %s, %s, %s, %s)"""

        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res, ))
    
    

@app.route('/search4', methods=['POST']) # decorator
def do_search() -> 'html':
    @copy_current_request_context #decorator applied to log_request
    def log_request(req: 'flask_request', res: str) -> None: #log_request nested inside the do_search function
        sleep(15) #This makes log_request really slow...
        with UseDatabase(app.config['dbconfig']) as cursor:
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
    title = 'Here are your results: '
    results = str(search4letters(phrase, letters))
    try:
        t = Thread(target=log_request, args=(request, results))	# creating a new "Thread" object, which identifies the target function to execute as well as any function falues-log request function call
        t.start() #calling "start", the function assicated with the "t" thread is scheduled for execution by the "threading" module
    except Exception as err:
        print('***** Logging failed with this error:', str(err))
    
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results,)


@app.route('/') # decorator
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', # name of the template to render
                           the_title='Welcome to search4letters on the web!') #value to associate with title argument



@app.route('/viewlog')  #viewlog page decorator
def view_the_log() -> 'html': #view log function
    """Display the contents of the log file as a HTML table."""
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results
                        from log"""
            cursor.execute(_SQL)
            contents = cursor.fetchall() #Send the query to the server, then fetch the reults. Note assignment of the fetched data to "contents."
        titles = ( 'Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
    except ConnectionError as err:
        print('Is your database switched on? Error:', str(err))
    except CredentialsError as err:
        print('User-id/Password issues. Error:', str(err))
    except SQLError as err:
        print('Is your query correct? Error:', str(err))
    
    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=contents,)

if __name__== '__main__':
    app.run(debug=True)
