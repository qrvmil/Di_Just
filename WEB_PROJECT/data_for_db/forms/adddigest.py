from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class DigestsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField("Content")
    link = URLField('Link', validators=[DataRequired()])
    description = TextAreaField("Comment to link")
    is_private = BooleanField("is private")
    submit = SubmitField('Submit')