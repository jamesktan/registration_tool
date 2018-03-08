from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, Field, RadioField, SelectMultipleField, IntegerField, FieldList
from wtforms.validators import DataRequired, Email, ValidationError, URL
from wtforms.widgets import TextArea, CheckboxInput,ListWidget

class RegistrationForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired(), Email()])
	phone = StringField("Phone", validators=[DataRequired()])
	community = StringField("Community Name", validators=[DataRequired()])
	days = SelectMultipleField('Attending Days',choices=[
		('0','Friday, April 27'),
		('1','Saturday, April 28'),
		('2','Sunday, April 29')
		],
		option_widget=CheckboxInput(),widget=ListWidget(prefix_label=False))
	dietary = SelectMultipleField('Dietary Restrictions',choices=[
		('0','None'),
		('1','Vegetarian'),
		('2','Gluten Free'),
		('3','Dairy Free')
		],
		option_widget=CheckboxInput(),widget=ListWidget(prefix_label=False))
	dietary_other = StringField("Other Dietary")
	food_allergies = StringField("Food Allergies")
	number_of_family = IntegerField("Number of Family Members", validators=[DataRequired()])
	family_names = FieldList(StringField('Family Member Name'), min_entries=1, max_entries=7)
	family_ages = FieldList(StringField('Family Member Age'), min_entries=1, max_entries=7)