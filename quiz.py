# Здесь будет код веб-приложения
from flask import Flask, session, request, redirect, url_for
from db_scripts import get_question_after, get_quises

def start_quis(quiz_id):
   session['quiz'] = quiz_id
   session['last_question'] = 0

def end_quiz():
   session.clear()

def quiz_form():

   html_beg = '''<html><body><h2>Выберите викторину:</h2><form method="post" action="index"><select name="quiz">'''
   frm_submit = '''<p><input type="submit" value="Выбрать"> </p>'''
  
   html_end = '''</select>''' + frm_submit + '''</form></body></html>'''
   options = ''' '''
   q_list = get_quises()
  
   for id, name in q_list:
       option_line = ('''<option value="''' +str(id) + '''">''' +str(name) + '''</option> ''')
       options = options + option_line
   return html_beg + options + html_end
     
def index():
   if request.method == 'GET':
       # викторина не выбрана, сбрасываем id викторины и показываем форму выбора
       start_quis(-1)
       return quiz_form()
   else:
       # получили дополнительные данные в запросе! Используем их:
       quest_id = request.form.get('quiz') # выбранный номер викторины
       start_quis(quest_id)
       return redirect(url_for('test'))

def test():
   '''возвращает страницу вопроса'''
   # что если пользователь без выбора викторины пошел сразу на адрес '/test'?
   if not ('quiz' in session) or int(session['quiz']) < 0:
       return redirect(url_for('index'))
   else:
       result = get_question_after(session['last_question'], session['quiz'])
       if result is None or len(result) == 0:
           return redirect(url_for('result'))
       else:
           session['last_question'] = result[0]
           result_form = '<h1>' + str(session['quiz']) +'<p>' +str(result[1])+ '</p>'+'<ol>'  + '<li>'+str(result[2])+'</li>' +'<li>'+str(result[3])+'</li>'+'<li>'+str(result[4])+'</li>' +'<li>'+str(result[5])+'</li>' +'</ol>' + '</h1>'           
           return  result_form
def result():
   end_quiz()
   return "все вопросы зкончелись <br> <a href ='/'>вернуться к началу теста</a>"

# Создаём объект веб-приложения:
app = Flask(__name__) 
app.add_url_rule('/', 'index', index)   # создаёт правило для URL '/'
app.add_url_rule('/index', 'index', index, methods=['post', 'get']) # правило для '/index'

app.add_url_rule('/test', 'test', test) # создаёт правило для URL '/test'
app.add_url_rule('/result1', 'result', result) # создаёт правило для URL '/test'
# Устанавливаем ключ шифрования:
app.config['SECRET_KEY'] = 'gjgjhghjghjghgfdtrd'
if __name__ == "__main__":
   # Запускаем веб-сервер:
   app.run()