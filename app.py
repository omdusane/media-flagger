from flask import Flask, render_template, request
from forms import FileForm, TextForm
from utils import allowed_file, process_txt, process_media, predict_category, remove_file
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pie'
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/', methods=['GET','POST'])
def home():
    file_form = FileForm()
    text_form = TextForm()
    result = ""
    # print("1")
    if request.method == 'POST':
        # print('2')
        if file_form.validate_on_submit():
            file = file_form.upload.data
            print(file)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                file_extension = filename.rsplit('.', 1)[1]

                if file_extension=="txt":
                    text = process_txt(file_path)
                    result = predict_category(text)
                    print(text)
                    remove_file(file_path)
                    return render_template('result.html',text=text, result=result)
                else:
                    text = process_media(file_path)
                    result = predict_category(text)
                    print(text, result)
                    remove_file(file_path)
                    return render_template('result.html', result=result, text = text)



        if text_form.validate_on_submit():
            # print('3')
            text = text_form.text.data
            result = predict_category(text)
            return render_template('result.html', text=text, result=result)
            # print(text)

    return render_template('index.html', file_form=file_form, text_form=text_form)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=1)