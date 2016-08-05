from wtforms.validators import ValidationError

class returningUser(object):
    def __init__(self, model, field, message=u'This username is not in our system.'):
        self.model = model
        self.field = field

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if not check:
            raise ValidationError(self.message)

class uniqueUser(object):
    def __init__(self, model, field, message=u'This username already exists in our system.'):
        self.model = model
        self.field = field

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)
