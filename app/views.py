from werkzeug.utils import secure_filename
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask import session
from flask import send_from_directory
from app.models import UserInfo
from app.models import Role
from app.models import Ordinance
from app.models import Resolution
from app.models import Other
from app import app
from app import db
import os
import uuid


def generate_random_string():
    return str(uuid.uuid4())


def allowed_file(filename, extensions):
    return filename.rsplit('.')[1] in extensions


@app.route('/login.html', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            username = str(request.form['username'])
            password = str(request.form['password'])
            user = UserInfo.query.filter_by(username=username).first()
            if username == user.username and UserInfo.verify_password(user, password):
                session['userid'] = user.userid
                session['username'] = str(user.username)
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password!', 'danger')
                return redirect(url_for('login'))
        except AttributeError:
            flash(session['username'], 'info')
            flash('Invalid username or password!', 'danger')
    return render_template('login.html', title='Login')


@app.route('/logout')
def logout():
    if 'username' in session:
        session.clear()
        flash("You have successfully logged out.", 'success')
    else:
        flash("You have not logged-in.", 'info')
    return redirect(url_for('login'))


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
@app.route('/index.html', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if 'username' in session:
            return render_template('index.html', title='Home')
    else:
        if 'username' in session:
            return render_template('index.html', title='Home')
        else:
            return redirect(url_for('login'))
    flash('Unauthorize access!', 'info')
    return redirect(url_for('login'))


@app.route('/adduser', methods=['POST', 'GET'])
def adduser():
    form = []

    if 'username' in session:
        if request.method == 'POST' and request.form['password'] == request.form['cpassword']:
            user_info = UserInfo(request.form['firstname'], request.form['lastname'], request.form['middlename'],
                                 request.form['birthdate'], request.form['address'], request.form['cemail'],
                                 request.form['cnumber'], request.form['username'], request.form['password'],
                                 request.form['role'])
            db.session.add(user_info)
            db.session.commit()
            message = 'New user was added.'
            status = 'success'
        elif request.method == 'POST' and request.form['password'] != request.form['cpassword']:
            form = [request.form['firstname'], request.form['lastname'], request.form['middlename'],
                    request.form['birthdate'], request.form['address'], request.form['cemail'],
                    request.form['cnumber'], request.form['username'], request.form['password'],
                    request.form['role']]
            message = 'Password doesn\'t match!'
            status = 'fail'
        else:
            message = 'Please fill all fields with asterisk (*).'
            status = 'none'

        return render_template('adduser.html', title='Add User', form=form)
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/viewuser', methods=['POST', 'GET'])
def viewuser():
    if 'username' in session:
        x = 0
        users_info = {}
        users = UserInfo.query.all()

        while x < len(users):
            users_info[x] = {'user': UserInfo.query.filter_by(userid=users[x].userid).first(),
                             'role': Role.query.filter_by(roleid=users[x].role_id).first().role_name
                            }
            x += 1

        return render_template('viewuser.html', title="View User", users_info=users_info)
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/viewordinance', methods=['POST', 'GET'])
def viewordinance():
    if 'username' in session:
        x = 0
        ord_query = Ordinance.query.order_by(Ordinance.ordinance_num.asc()).all()
        ordinances = {}

        while x < len(ord_query):
            ordinances[x] = {'ordinance_id': ord_query[x].ordinance_id,
                             'ordinance_num': ord_query[x].ordinance_num,
                             'series': ord_query[x].series,
                             'description': ord_query[x].description,
                             'sponsor1': ord_query[x].sponsor1,
                             'sponsor2': ord_query[x].sponsor2,
                             'sponsor3': ord_query[x].sponsor3,
                             'ordained_date': ord_query[x].ordained_date,
                             'aff_by': ord_query[x].aff_by,
                             'app_by': ord_query[x].app_by,
                             'filename': ord_query[x].filename
                            }
            x += 1

        return render_template('viewordinance.html', title="View Ordinance", ordinances=ordinances)
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/viewresolution', methods=['POST', 'GET'])
def viewresolution():
    if 'username' in session:
        x = 0
        res_query = Resolution.query.order_by(Resolution.resolution_num.asc()).all()
        resolution = {}

        while x < len(res_query):
            resolution[x] = {'resolution_id': res_query[x].resolution_id,
                             'resolution_num': res_query[x].resolution_num,
                             'series': res_query[x].series,
                             'description': res_query[x].description,
                             'author1': res_query[x].author1,
                             'author2': res_query[x].author2,
                             'author3': res_query[x].author3,
                             'resolved_date': res_query[x].resolved_date,
                             'cert_by': res_query[x].cert_by,
                             'att_by': res_query[x].att_by,
                             'filename': res_query[x].filename
                            }
            x += 1

        return render_template('viewresolution.html', title="View Resolution", resolution=resolution)
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/viewother', methods=['POST', 'GET'])
def viewother():
    if 'username' in session:
        x = 0
        oth_query = Other.query.order_by(Other.other_id.asc()).all()
        other = {}

        while x < len(oth_query):
            up_by = UserInfo.query.filter_by(userid=oth_query[x].up_by).first()
            other[x] = {'other_id': oth_query[x].other_id, 'document_name': oth_query[x].document_name,
                                'description': oth_query[x].description, 'creation_date': oth_query[x].creation_date,
                                'created_by': oth_query[x].created_by, 'up_by': up_by.firstname + " " + up_by.middlename + " " + up_by.lastname,
                                'filename': oth_query[x].filename
                               }
            x += 1

        return render_template('viewother.html', title="View Other Documents", other=other)
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/edituser/<username>', methods=['POST', 'GET'])
def edituser(username):
    if 'username' in session:
        user_info = UserInfo.query.filter_by(username=username).first()

        if request.method == 'POST':
            user_info.firstname = request.form['firstname']
            user_info.lastname = request.form['lastname']
            user_info.middlename = request.form['middlename']
            user_info.birthdate = request.form['birthdate']
            user_info.address = request.form['address']
            user_info.email = request.form['cemail']
            user_info.contact_number = request.form['cnumber']
            user_info.password = request.form['password']
            user_info.role_id = request.form['role']
            db.session.commit()
            flash(user_info.username + '\'s information was updated...', 'info')
            return redirect(url_for('viewuser'))

        return render_template('edituser.html', title="Edit User", user_info=user_info)
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/editordinance/<ordinance_id>', methods=['POST', 'GET'])
def editordinance(ordinance_id):
    if 'username' in session:
        ordinance = Ordinance.query.filter_by(ordinance_id=ordinance_id).first()

        if request.method == 'POST':
            flag = 1
            my_file = request.files['upfile']
            if ordinance.series != long(request.form['series']):
                ordinance.series = request.form['series']
                flag = flag * 0
            if str(ordinance.description) != str(request.form['description']):
                ordinance.description = request.form['description']
                flag = flag * 0
            if ordinance.sponsor1 != str(request.form['sponsor1']):
                ordinance.sponsor1 = request.form['sponsor1']
                flag = flag * 0
            if ordinance.sponsor2 != str(request.form['sponsor2']):
                ordinance.sponsor2 = request.form['sponsor2']
                flag = flag * 0
            if ordinance.sponsor3 != str(request.form['sponsor3']):
                ordinance.sponsor3 = request.form['sponsor3']
                flag = flag * 0
            if unicode(ordinance.ordained_date) != request.form['ordained_date']:
                ordinance.ordained_date = request.form['ordained_date']
                flag = flag * 0
            if ordinance.aff_by != str(request.form['aff_by']):
                ordinance.aff_by = request.form['aff_by']
                flag = flag * 0
            if ordinance.att_by != str(request.form['att_by']):
                ordinance.att_by = request.form['att_by']
                flag = flag * 0
            if ordinance.app_by != str(request.form['app_by']):
                ordinance.app_by = request.form['app_by']
                flag = flag * 0
            if my_file and allowed_file(my_file.filename, app.config['ALLOWED_EXTENSIONS']):
                if os.path.isfile(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_ORDINANCES'], ordinance.filename)):
                    os.remove(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_ORDINANCES'], ordinance.filename))
                extension = my_file.filename.rsplit('.')[1]
                filename = secure_filename("MON-" + request.form['ordinance_num'] + "." + extension)
                ordinance.filename = filename
                my_file.save(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_ORDINANCES'], filename))
                flag = flag * 0

            if flag == 0:
                db.session.commit()
                flash("Ordinance " + str(ordinance.ordinance_num) + '\'s information was updated successfully.', 'success')

            else:
                flash('You have made no changes.', 'info')
            return redirect(url_for('viewordinance'))
        return render_template('editordinance.html', title="Edit Ordinance", ordinance=ordinance)

    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/editresolution/<resolution_id>', methods=['POST', 'GET'])
def editresolution(resolution_id):
    if 'username' in session:
        resolution = Resolution.query.filter_by(resolution_id=resolution_id).first()

        if request.method == 'POST':
            flag = 1
            my_file = request.files['upfile']
            if resolution.series != long(request.form['series']):
                resolution.series = request.form['series']
                flag = flag * 0
            if str(resolution.description) != str(request.form['description']):
                resolution.description = request.form['description']
                flag = flag * 0
            if resolution.author1 != str(request.form['author1']):
                resolution.author1 = request.form['author1']
                flag = flag * 0
            if resolution.author2 != str(request.form['author2']):
                resolution.author2 = request.form['author2']
                flag = flag * 0
            if resolution.author3 != str(request.form['author3']):
                resolution.author3 = request.form['author3']
                flag = flag * 0
            if unicode(resolution.resolved_date) != request.form['resolved_date']:
                resolution.resolved_date = request.form['resolved_date']
                flag = flag * 0
            if resolution.cert_by != str(request.form['cert_by']):
                resolution.cert_by = request.form['cert_by']
                flag = flag * 0
            if resolution.att_by != str(request.form['att_by']):
                resolution.att_by = request.form['att_by']
                flag = flag * 0
            if my_file:
                if allowed_file(my_file.filename, app.config['ALLOWED_EXTENSIONS']):
                    if os.path.isfile(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_RESOLUTIONS'], resolution.filename)):
                        os.remove(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_RESOLUTIONS'], resolution.filename))
                    extension = my_file.filename.rsplit('.')[1]
                    filename = secure_filename("MRN-" + request.form['resolution_num'] + "." + extension)
                    resolution.filename = filename
                    my_file.save(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_RESOLUTIONS'], filename))
                    flag = flag * 0
                else:
                    flag = 1
                    flash("Uploaded file type invalid! Please upload: ['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg']", 'danger')
                    return redirect(url_for('viewresolution'))

            if flag == 0:
                db.session.commit()
                flash("Resolution " + str(resolution.resolution_num) + '\'s information was updated.', 'success')

            else:
                flash('No changes made.', 'info')
            return redirect(url_for('viewresolution'))
        return render_template('editresolution.html', title="Edit Resolution", resolution=resolution)

    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/editother/<other_id>', methods=['POST', 'GET'])
def editother(other_id):
    if 'username' in session:
        other = Other.query.filter_by(other_id=other_id).first()

        if request.method == 'POST':
            flag = 1
            my_file = request.files['upfile']
            if str(other.document_name) != str(request.form['document_name']):
                other.document_name = request.form['document_name']
                flag = flag * 0
            if str(other.description) != str(request.form['description']):
                other.description = request.form['description']
                flag = flag * 0
            if unicode(other.creation_date) != request.form['creation_date']:
                other.creation_date = request.form['creation_date']
                flag = flag * 0
            if other.created_by != str(request.form['created_by']):
                other.created_by = request.form['created_by']
                flag = flag * 0
            if my_file:
                if allowed_file(my_file.filename, app.config['ALLOWED_EXTENSIONS_OTHERS']):
                    if os.path.isfile(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_OTHERS'], other.filename)):
                        os.remove(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_OTHERS'], other.filename))
                    extension = my_file.filename.rsplit('.')[1]
                    filename = secure_filename(request.form['document_name'] + "." + extension)
                    other.filename = filename
                    my_file.save(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_OTHERS'], filename))
                    flag = flag * 0
                else:
                    flag = 1
                    flash("Uploaded file type invalid! Please upload: ['xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx', 'pdf']", 'danger')
                    return redirect(url_for('viewother'))

            if flag == 0:
                db.session.commit()
                flash("Document " + str(other.document_name) + '\'s information was updated.', 'success')

            else:
                flash('No changes made.', 'info')
            return redirect(url_for('viewother'))
        return render_template('editother.html', title="Edit Other Document", other=other)

    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/deleteuser/<username>')
def deleteuser(username):
    if 'username' in session:
        user = UserInfo.query.filter_by(username=username).first()
        del_user = user.username
        UserInfo.query.filter_by(username=username).delete()
        db.session.commit()
        flash(del_user + ' user was successfully deleted...', 'info')
        return redirect(url_for('viewuser'))
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/deleteordinance/<ordinance_id>')
def deleteordinance(ordinance_id):
    if 'username' in session:
        ordinance = Ordinance.query.filter_by(ordinance_id=ordinance_id).first()
        del_ordinance = ordinance.ordinance_num
        if ordinance.filename:
            os.remove(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_ORDINANCES'], ordinance.filename))
        Ordinance.query.filter_by(ordinance_id=ordinance_id).delete()
        db.session.commit()
        flash('Ordinance "' + str(del_ordinance) + '" was successfully deleted...', 'success')
        return redirect(url_for('viewordinance'))
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/deleteresolution/<resolution_id>')
def deleteresolution(resolution_id):
    if 'username' in session:
        resolution = Resolution.query.filter_by(resolution_id=resolution_id).first()
        del_resolution = resolution.resolution_num
        if resolution.filename:
            os.remove(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_RESOLUTIONS'], resolution.filename))
        Resolution.query.filter_by(resolution_id=resolution_id).delete()
        db.session.commit()
        flash('Resolution "' + str(del_resolution) + '" was successfully deleted...', 'success')
        return redirect(url_for('viewresolution'))
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/deleteother/<other_id>')
def deleterother(other_id):
    if 'username' in session:
        other = Other.query.filter_by(other_id=other_id).first()
        del_other = other.other_id
        if other.filename:
            os.remove(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_OTHERS'], other.filename))
        Other.query.filter_by(other_id=other_id).delete()
        db.session.commit()
        flash('Other Document "' + str(del_other) + '" was successfully deleted...', 'success')
        return redirect(url_for('viewother'))
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))

@app.route('/addordinance', methods=['POST', 'GET'])
def addordinance():
    if 'username' in session:
        if request.method == 'POST':
            my_file = request.files['upfile']
            filename = ''
            ret_val = {}
            ord_num = Ordinance.query.filter_by(ordinance_num=request.form['ordinance_num']).first()

            if ord_num:
                flash(str(ord_num) + " already exist!", 'danger')
                ret_val['ordinance_num'] = str(request.form['ordinance_num'])
                ret_val['series'] = str(request.form['series'])
                ret_val['description'] = str(request.form['description']).lstrip()
                ret_val['sponsor1'] = str(request.form['sponsor1'])
                ret_val['sponsor2'] = str(request.form['sponsor2'])
                ret_val['sponsor3'] = str(request.form['sponsor3'])
                ret_val['ordained_date'] = str(request.form['ordained_date'])
                ret_val['aff_by'] = str(request.form['aff_by'])
                ret_val['att_by'] = str(request.form['att_by'])
                ret_val['app_by'] = str(request.form['app_by'])
                return render_template('addordinance.html', title='Add Ordinance', ret_val=ret_val)

            if my_file.filename == '':
                message = 'Please upload a file!'
            elif my_file and allowed_file(my_file.filename, app.config['ALLOWED_EXTENSIONS']):
                extension = my_file.filename.rsplit('.')[1]
                filename = secure_filename("MON-" + request.form['ordinance_num']+ "." + extension)

            ordinance = Ordinance(request.form['ordinance_num'], request.form['series'], request.form['description'],
                                  request.form['sponsor1'], request.form['sponsor2'], request.form['sponsor3'],
                                  request.form['ordained_date'], request.form['aff_by'], request.form['att_by'],
                                  request.form['app_by'], session['userid'], filename)
            db.session.add(ordinance)
            db.session.commit()
            my_file.save(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_ORDINANCES'], filename))
            flash(str(ordinance) + " was successfully added!", 'success')

        return render_template('addordinance.html', title='Add Ordinance')
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/addresolution', methods=['POST', 'GET'])
def addresolution():
    if 'username' in session:
        if request.method == 'POST':
            my_file = request.files['upfile']
            filename = ''
            ret_val = {}
            res_num = Resolution.query.filter_by(resolution_num=request.form['resolution_num']).first()

            if res_num:
                flash(str(res_num) + " already exist!", 'danger')
                ret_val['resolution_num'] = str(request.form['resolution_num'])
                ret_val['series'] = str(request.form['series'])
                ret_val['description'] = str(request.form['description']).lstrip()
                ret_val['author1'] = str(request.form['author1'])
                ret_val['author2'] = str(request.form['author2'])
                ret_val['author3'] = str(request.form['author3'])
                ret_val['resolved_date'] = str(request.form['resolved_date'])
                ret_val['cert_by'] = str(request.form['cert_by'])
                ret_val['att_by'] = str(request.form['att_by'])
                return render_template('addresolution.html', title='Add Resolution', ret_val=ret_val)

            if my_file and allowed_file(my_file.filename, app.config['ALLOWED_EXTENSIONS']):
                extension = my_file.filename.rsplit('.')[1]
                filename = secure_filename("MRN-" + request.form['resolution_num']+ "." + extension)
            else:
                flash("Uploaded file type invalid! Please upload: ['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg']", 'danger')
                ret_val['resolution_num'] = str(request.form['resolution_num'])
                ret_val['series'] = str(request.form['series'])
                ret_val['description'] = str(request.form['description']).lstrip()
                ret_val['author1'] = str(request.form['author1'])
                ret_val['author2'] = str(request.form['author2'])
                ret_val['author3'] = str(request.form['author3'])
                ret_val['resolved_date'] = str(request.form['resolved_date'])
                ret_val['cert_by'] = str(request.form['cert_by'])
                ret_val['att_by'] = str(request.form['att_by'])
                return render_template('addresolution.html', title='Add Resolution', ret_val=ret_val)

            resolution = Resolution(request.form['resolution_num'], request.form['series'], request.form['description'],
                                  request.form['author1'], request.form['author2'], request.form['author3'],
                                  request.form['resolved_date'], request.form['cert_by'], request.form['att_by'], session['userid'], filename)
            db.session.add(resolution)
            db.session.commit()
            my_file.save(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_RESOLUTIONS'], filename))
            flash(str(resolution) + " was successfully added!", 'success')

        return render_template('addresolution.html', title='Add Resolution')
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/addother', methods=['POST', 'GET'])
def addother():
    if 'username' in session:
        if request.method == 'POST':
            my_file = request.files['upfile']
            filename = ''
            ret_val = {}
            oth_doc = Other.query.filter_by(document_name=request.form['document_name']).first()

            if oth_doc:
                flash(str(oth_doc) + " already exist!", 'danger')
                ret_val['document_name'] = str(request.form['document_name'])
                ret_val['description'] = str(request.form['description']).lstrip()
                ret_val['creation_date'] = str(request.form['creation_date'])
                ret_val['created_by'] = str(request.form['created_by'])
                return render_template('addother.html', title='Add Other Documents', ret_val=ret_val)

            if my_file and allowed_file(my_file.filename, app.config['ALLOWED_EXTENSIONS_OTHERS']):
                extension = my_file.filename.rsplit('.')[1]
                filename = secure_filename(request.form['document_name']+ "." + extension)
            else:
                flash("Uploaded file type invalid! Please upload: ['xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx', 'pdf']", 'danger')
                ret_val['document_name'] = str(request.form['document_name'])
                ret_val['description'] = str(request.form['description']).lstrip()
                ret_val['creation_date'] = str(request.form['creation_date'])
                ret_val['created_by'] = str(request.form['created_by'])
                return render_template('addother.html', title='Add Other Documents', ret_val=ret_val)

            other = Other(request.form['document_name'], request.form['description'], request.form['creation_date'], request.form['created_by'], session['userid'], filename)
            db.session.add(other)
            db.session.commit()
            my_file.save(os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_OTHERS'], filename))
            flash(str(other) + " was successfully added!", 'success')

        return render_template('addother.html', title='Add Other Documents')
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/download/ordinance/<filename>', methods=['GET'])
def downloadordinance(filename):
    if 'username' in session:
        filepath = os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_ORDINANCES'])
        return send_from_directory(directory=filepath, filename=filename)
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/download/resolution/<filename>', methods=['GET'])
def downloadresolution(filename):
    if 'username' in session:
        filepath = os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_RESOLUTIONS'])
        return send_from_directory(directory=filepath, filename=filename)
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))


@app.route('/download/other/<filename>', methods=['GET'])
def downloadother(filename):
    if 'username' in session:
        filepath = os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER_OTHERS'])
        return send_from_directory(directory=filepath, filename=filename)
    else:
        flash('Unauthorize access!', 'info')
        return redirect(url_for('login'))
