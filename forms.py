from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import TextAreaField
from wtforms import validators

class FileForm(FlaskForm):
    upload = FileField('Upload File', validators=[FileAllowed(['txt', 'mp3', 'mp4'],'Only txt, mp3 and mp4 files are allowed!')])

class TextForm(FlaskForm):
    text = TextAreaField('Input Text') #, [validators.length(min=0,max=300)]