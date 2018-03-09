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

	number_of_adults = IntegerField("Number of Adults Attending", validators=[DataRequired()])
	names_of_adults = StringField("Names of Adults")

	number_of_children = IntegerField("Number of Children Attending", validators=[DataRequired()])
	names_of_children = StringField("Names of Children")

	number_of_jy = IntegerField("Number of Youth Attending", validators=[DataRequired()])
	names_of_jy = StringField("Names of JY")
