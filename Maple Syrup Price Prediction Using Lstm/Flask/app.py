from flask import Flask, render_template, request, session, redirect
from sklearn import model_selection
import pickle
import secrets

app = Flask(__name__, template_folder='template')
app.secret_key = secrets.token_hex(16)

try:
    with open('model1.pkl', 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    print("Error loading the model:", e)
    model = None

@app.route('/')
def first_page():
    return render_template('first_page.html')

@app.route('/form_page.html')
def form_page():
    return render_template('form_page.html')

@app.route('/predict_page.html')
def predict_page():
    prediction_text = session.get('output', '')
    print("Session Output (in predict_page):", prediction_text)
    return render_template('predict_page.html', prediction_text=prediction_text)

@app.route('/form_page.html', methods=['GET', 'POST'])
def guest():
    if request.method == 'POST':
        a = float(request.form['a'])
        b = float(request.form['b'])
        c = float(request.form['c'])
        d = float(request.form['d'])
        e = float(request.form['e'])
        f = float(request.form['f'])
        g = float(request.form['g'])

        print("Form Data:", a, b, c, d, e, f, g)

        data = [[a, b, c, d, e, f, g]]
        if model:
            try:
                prediction = model.predict(data)
                predicted_value = float(prediction[0])
                session['output'] = 'The predicted average price is {} US dollars'.format(round(predicted_value, 4))
                print("Session Output (before redirect):", session['output'])
                return redirect('/predict_page.html')
            except Exception as e:
                print("Error making prediction:", e)
                session['output'] = 'Error making prediction, please try again'
                print("Session Output (before redirect - exception):", session['output'])
                return redirect('/predict_page.html')
        else:
            session['output'] = 'Error loading the model'
            return redirect('/predict_page.html')

    return render_template('form_page.html')

if __name__ == '__main__':
    app.run(debug=True)
