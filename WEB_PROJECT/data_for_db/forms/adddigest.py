from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, FieldList
from wtforms import BooleanField, SubmitField, FormField, Form
from wtforms.validators import DataRequired


class LinkForm(Form):
    link = URLField('Link', validators=[DataRequired()])
    description = TextAreaField("Comment to link")


class DigestsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField("Content")
    all_links = FieldList(FormField(LinkForm), min_entries=3)
    is_private = BooleanField("is private")
    submit = SubmitField('Submit')
