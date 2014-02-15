from wtforms import Form, TextField, IntegerField, TextAreaField, validators, BooleanField

class DBExerciseUploadForm(Form):
    title = TextField('Title', [validators.Length(min=1, max=60)])
    difficulty = IntegerField('Difficulty')
    category = TextField('Category', [validators.Length(min=1, max=20)])
    content = TextAreaField('Content', [validators.Length(min=1, max=5000)])


class DBPageUploadForm(Form):
    title = TextField('PageTitle', [validators.Length(min=1, max=60)])
    content = TextAreaField('Content', [validators.Length(min=1, max=5000)])


class ProfileForm(Form):
    show_public = BooleanField("show_public", default=False)

    full_name = TextField("full_name", [validators.Optional(strip_whitespace=True),
                                   validators.Length(min=1, max=120, message="Maximum of 120 characters allowed.")])

    location = TextField("location", [validators.Optional(strip_whitespace=True),
                                      validators.Length(min=1, max=120, message="Maximum of 120 characters allowed.")])

    homepage = TextField("homepage", [validators.Optional(strip_whitespace=True),
                                      validators.URL(require_tld=True, message="Invalid URL."),
                                      validators.Length(min=1, max=120, message="Maximum of 120 characters allowed.")])

    company = TextField("company", [validators.Optional(strip_whitespace=True),
                                    validators.Length(min=1, max=120, message="Maximum of 120 characters allowed.")])

    school = TextField("school", [validators.Optional(strip_whitespace=True),
                                  validators.Length(min=1, max=120, message="Maximum of 120 characters allowed.")])


    public_email = TextField("public_email", [validators.Optional(strip_whitespace=True),
                                              validators.Length(min=1, max=120, message="Maximum of 120 characters allowed."),
                                              validators.Email(message="The email address is not valid.")])

