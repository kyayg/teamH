from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import Required, Email


class Register(Form):

    username = StringField(validators=[Required()])
    email = StringField(validators=[Required(),Email()])
    pswd1 = PasswordField()
    pswd2 = PasswordFiedl(validators=[EqualTo(pswd1)])
