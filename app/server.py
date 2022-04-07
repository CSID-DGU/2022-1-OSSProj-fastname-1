from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def main():
   return render_template('main.html')

@app.route('/login', methods = ['GET','POST'])
def login():
   error = None
   if request.method == 'POST':
      if request.form['username'] != 'ossp' or request.form['password'] != 'ossp1234': #error 변수에 'Error 메시지 내용'을 대입
         error = '입력오류! 다시 입력해주세요.'
      else:
         return render_template('application_form.html')

   return render_template("login.html", error = error)

@app.route('/sign_up')
def sign():
   return render_template('sign_up.html')

@app.route('/application_form')
def apllication():
   return render_template('application_form.html')

@app.route('/detail', methods = ['POST', 'GET'])
def detail():
   if request.method == 'POST':
      result = request.form
      return render_template("detail.html",result = result)

@app.route('/submit')
def submit():
   return render_template("submit.html")

if __name__ == '__main__':
   app.run(host="0.0.0.0", debug=True, port=80)
