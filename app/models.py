from app import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class UserInfo(db.Model):
    __tablename__ = 'UserInfo'
    userid = db.Column('userid', db.Integer, primary_key=True)
    firstname = db.Column('firstname', db.String(30))
    lastname = db.Column('lastname', db.String(30))
    middlename = db.Column('middlename', db.String(30))
    birthdate = db.Column('birthdate', db.Date())
    username = db.Column('username', db.String(30), unique=True)
    password_hash = db.Column(db.String(256), index=True)
    address = db.Column('address',db.String(100))
    email = db.Column('email',db.String(50), unique=True)
    contact_number = db.Column('contact_number', db.String(30))
    role_id = db.Column(db.Integer, db.ForeignKey('Role.roleid'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, firstname, lastname, middlename, birthdate, address, email, contact_number, username, password_hash, role_id):
        self.firstname = firstname
        self.lastname = lastname
        self.middlename = middlename
        self.birthdate = birthdate
        self.address = address
        self.email = email
        self.contact_number = contact_number
        self.username = username
        self.password = password_hash
        self.role_id = role_id

    def __repr__(self):
        return "<UserInfo(firstname='%s', lastname='%s', middlename='%s', birthdate='%s', address='%s', email='%s', contact_number='%s', password_hash='%s', role_id='%s')>" % \
               (self.firstname, self.lastname, self.middlename, self.birthdate, self.address, self.email, self.contact_number, self.password, self.role_id)


class Role(db.Model):
    __tablename__ = 'Role'
    roleid = db.Column('roleid', db.Integer, primary_key=True)
    role_name = db.Column('role_name', db.String(20), unique=True)
    user = db.relationship('UserInfo', backref='UserRole', lazy='dynamic')

    def __init__(self, roleid, role_name):
        self.roleid = roleid
        self.role_name = role_name

    def __repr__(self):
        return "<Role(roleid='%s')>" % self.roleid


class Ordinance(db.Model):
    __tablename__ = 'Ordinance'
    ordinance_id = db.Column('ordinance_id', db.Integer(), primary_key=True)
    ordinance_num = db.Column('ordinance_number', db.Integer(), unique=True)
    series = db.Column('series', db.Integer())
    description = db.Column('description', db.Text())
    sponsor1 = db.Column('sponsor1', db.String(100))
    sponsor2 = db.Column('sponsor2', db.String(100))
    sponsor3 = db.Column('sponsor3', db.String(100))
    ordained_date = db.Column('ordained_date', db.Date())
    aff_by = db.Column('aff_by', db.String(100))
    att_by = db.Column('att_by', db.String(100))
    app_by = db.Column('app_by', db.String(100))
    up_by = db.Column(db.Integer, db.ForeignKey('UserInfo.userid'))
    filename = db.Column('filename', db.String(100))

    def __init__(self, ordinance_num, series, description, sponsor1, sponsor2, sponsor3, ordained_date,
                 aff_by, att_by, app_by, up_by, filename):
        self.ordinance_num = ordinance_num
        self.series = series
        self.description = description
        self.sponsor1 = sponsor1
        self.sponsor2 = sponsor2
        self.sponsor3 = sponsor3
        self.ordained_date = ordained_date
        self.aff_by = aff_by
        self.att_by = att_by
        self.app_by = app_by
        self.up_by = up_by
        self.filename = filename

    def __repr__(self):
        return "Ordinance Number: %s" % self.ordinance_num


class Resolution(db.Model):
    __tablename__ = 'Resolution'
    resolution_id = db.Column('resolution_id', db.Integer(), primary_key=True)
    resolution_num = db.Column('resolution_num', db.Integer(), unique=True)
    series = db.Column('series', db.Integer())
    description = db.Column('description', db.Text())
    author1 = db.Column('author1', db.String(100))
    author2 = db.Column('author2', db.String(100))
    author3 = db.Column('author3', db.String(100))
    resolved_date = db.Column('resolved_date', db.Date())
    cert_by = db.Column('cert_by', db.String(100))
    att_by = db.Column('att_by', db.String(100))
    up_by = db.Column(db.Integer, db.ForeignKey('UserInfo.userid'))
    filename = db.Column('filename', db.String(100))

    def __init__(self, resolution_num, series, description, author1, author2, author3, resolved_date,
                 cert_by, att_by, up_by, filename):
        self.resolution_num = resolution_num
        self.series = series
        self.description = description
        self.author1 = author1
        self.author2 = author2
        self.resolved_date = resolved_date
        self.author3 = author3
        self.cert_by = cert_by
        self.att_by = att_by
        self.up_by = up_by
        self.filename = filename

    def __repr__(self):
        return "Resolution Number: %s" % self.resolution_num


class Other(db.Model):
    __tablename__ = 'Other'
    other_id = db.Column('other_id', db.Integer(), primary_key=True)
    document_name = db.Column('document_name', db.String(100), unique = True)
    description = db.Column('description', db.Text())
    creation_date = db.Column('creation_date', db.Date())
    created_by = db.Column('created_by', db.String(100))
    up_by = db.Column(db.Integer, db.ForeignKey('UserInfo.userid'))
    filename = db.Column('filename', db.String(100))


    def __init__(self, document_name, description, creation_date, created_by, up_by, filename):
        self.document_name = document_name
        self.description = description
        self.creation_date = creation_date
        self.created_by = created_by
        self.up_by = up_by
        self.filename = filename

    def __repr__(self):
        return "Document Name: %s" % self.document_name