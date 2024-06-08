from flask import Flask, render_template, request, flash, url_for
from forms import FileForm, TextForm
from utils import allowed_file, process_txt, process_media, predict_category, remove_file, preprocess
from werkzeug.utils import secure_filename
import os
import requests

from predictions import load_model
app = Flask(__name__)
app.config['SECRET_KEY'] = 'pie'
app.config['UPLOAD_FOLDER'] = 'uploads'

    

@app.route('/', methods=['GET','POST'])
def home():
    file_form = FileForm()
    text_form = TextForm()
    result = ""
    if request.method == 'POST':
        if request.form['button']=="file_button" and file_form.validate_on_submit():
            print("inside file form")
            file = file_form.upload.data
            print(file)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                file_extension = filename.rsplit('.', 1)[1]

                if file_extension=="txt":
                    text = process_txt(file_path)
                    preprocessed_text = preprocess(text)
                    result = load_model(preprocessed_text)                    
                    remove_file(file_path)
                    return render_template('result.html',text=text, result=result, filename=filename)
                else:
                    text = process_media(file_path)
                    preprocessed_text = preprocess(text)
                    result = load_model(text)
                    remove_file(file_path)
                    return render_template('result.html', result=result, text = text, filename=filename)
            else:
                print("error")
                flash("Only files with Mp3, Mp4 and txt extensions are allowed", category="error")
                return render_template('index.html', file_form=file_form, text_form=text_form)

        if request.form['button']=="text_button" and  text_form.validate_on_submit():
            text = text_form.text.data
            preprocessed_text = preprocess(text)
            result = load_model(text)        
            return render_template('result.html', text=text, result=result)

    return render_template('index.html', file_form=file_form, text_form=text_form)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/try',methods=['GET'])
def demo():
    result = load_model("hello world")
    print("from demo")
    print(result)
    return "demo page"

if __name__ == "__main__":
    app.run(debug=1)