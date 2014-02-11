from wtforms import Form, TextField, IntegerField, TextAreaField, validators


class DBExerciseUploadForm(Form):
    title = TextField('Title', [validators.Length(min=1, max=60)])
    difficulty = IntegerField('Difficulty')
    category = TextField('Category', [validators.Length(min=1, max=20)])
    content = TextAreaField('Content', [validators.Length(min=1, max=5000)])


class DBPageUploadForm(Form):
    title = TextField('PageTitle', [validators.Length(min=1, max=60)])
    content = TextAreaField('Content', [validators.Length(min=1, max=5000)])