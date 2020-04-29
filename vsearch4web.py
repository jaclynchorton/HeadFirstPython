from flask import Flask, render_template, request, escape
from vsearch import search4letters # importing search4letters
from DBcm import UseDatabase, ConnectionError

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
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results: '
    results = str(search4letters(phrase, letters))
    try:
        log_request(request, results)	# log request function call
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
    
    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=contents,)

if __name__== '__main__':
    app.run(debug=True)
