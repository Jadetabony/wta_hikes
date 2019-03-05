from flask_wtf import Form
from wtforms import BooleanField, StringField, FloatField, SelectField, SubmitField
from wtforms.validators import AnyOf, Length, DataRequired, Required
from validators import returningUser, uniqueUser
#from .models import Users

class ratingForm(Form):

    def __init__(self, hikes, returning=False):
        self.hikes = hikes
        if returning:
            returningUsername = StringField('Username', description='Returning users may input their username in order to get better recommendations.')
            hikeName = SelectField(u'Hike Name', choices=self.hikes, validators = [Required()])
            tripReport = StringField('Trip Report', validators=None, description='Optional input of a trip report so that the recommender can get an idea of what is important to the user.')
            starRating = FloatField('Star Rating', validators=[DataRequired()])
            submit = SubmitField('Get Recommendations!')
        else:
            newUsername = StringField('New Username')
            hikeName = SelectField(u'Field name', choices=self.hikes, validators = [Required()])
            tripReport = StringField('Trip Report', validators=None, description='Optional input of a trip report so that the recommender can get an idea of what is important to the user.')
            starRating = FloatField('Star Rating', validators=[DataRequired()])
            submit = SubmitField('Get Recommendations!')
