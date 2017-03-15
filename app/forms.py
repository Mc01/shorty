from wtforms import Form, StringField, validators


class SubmitTagForm(Form):
    url = StringField('Url link', [
        validators.DataRequired(),
        validators.Length(min=4, max=1000)
    ])
