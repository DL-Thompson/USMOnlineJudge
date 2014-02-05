from wtforms import Form, TextField, IntegerField, validators


class DBExerciseUploadForm(Form):
    title = TextField('Title', [validators.Length(min=1, max=60)])
    difficulty = IntegerField('Difficulty')
    category = TextField('Category', [validators.Length(min=1, max=20)])
    content = TextField('Content', [validators.Length(min=1, max=5000)])