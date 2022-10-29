import html
import mysql.connector
from importlib.resources import contents
from flask import Flask, render_template, request, escape
app = Flask(__name__)

def search4letters(phrase: str, letters: str = 'aeiou') -> set:
    """Return a set of the 'letters' found in 'phrase'."""
    return set(letters).intersection(set(phrase))

def log_request(req: 'flask_request', res: str) -> None:
    """Log details of the web request and the results."""
    dbconfig = { 'host': 'mysql',
                 'user': 'root',
                 'password': 'root',
                 'database': 'vsearchlogDB', }
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()

    _SQL = """insert into log
              (phrase, letters, ip, browser_string, results)
              values
              (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL, (req.form['phrase'],
                          req.form['letters'],
                          req.remote_addr,
                          req.user_agent.browser,
                          res, ))

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Aqui estão os resultados!'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html', 
                            the_phrase=phrase, 
                            the_letters=letters, 
                            the_title=title, 
                            the_results=results,)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', 
                            the_title='Bem-vindo(a) ao search4letters para web!')

@app.route('/viewlog')
def view_the_log() -> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results',)
    return render_template('viewlog.html', 
                            the_title='Registros', 
                            the_row_titles=titles, 
                            the_data=contents,)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')