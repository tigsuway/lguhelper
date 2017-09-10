import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER_RESOLUTIONS = 'app/static/uploads/resolutions'
UPLOAD_FOLDER_ORDINANCES = 'app/static/uploads/ordinances'
UPLOAD_FOLDER_OTHERS = 'app/static/uploads/others'
ALLOWED_EXTENSIONS = ['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg']
SQLALCHEMY_DATABASE_URI = 'mysql://lguadmin:S0l3mry$@localhost/lguhelper'
ALLOWED_EXTENSIONS_OTHERS = ['xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx', 'pdf']
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
WTF_CSRF_ENABLED = True
SECRET_KEY = 'S0l3mry$'
