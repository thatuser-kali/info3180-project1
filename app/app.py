from .__init__ import application as app
from .__init__ import *
from flask import render_template, request, flash, redirect, url_for
from .upload import Profile
import os
from werkzeug.utils import secure_filename
from models import Profile as Pro
from glob import glob
from datetime import datetime
import re

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))
            
def locate_photo(unique_id):
    file = glob(os.path.join(
            app.config['UPLOAD_FOLDER'], str(unique_id) + "_*"
        ))[0]
    print(file[file.index("profiles"):])
    return file[file.index("profiles"):]
    
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile', methods=('GET', 'POST'))
def profile():
    form = Profile()
    
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        
        if not re.match(r'.*\.(jpg|png|jpeg)$', filename):
            flash("Invalid file. File is not an image")
            return render_template('profile.html', form=form)
            
        profile = Pro(firstname=form.firstname.data,
        lastname=form.lastname.data,
        email=form.email.data,
        location=form.location.data,
        gender=form.gender.data,
        biography=form.biography.data, created_on=datetime.now())
        
        session.add(profile)
        session.commit()

        f.save(os.path.join(
            app.config['UPLOAD_FOLDER'], str(profile.id) + "_" + filename
        ))
        
        flash("Profile successfully created")
        return redirect(url_for('profiles'))
        
    elif request.method == 'POST':
        flash_errors(form)
    return render_template('profile.html', form=form)

@app.route('/profiles', defaults={'userid': None})
@app.route('/profiles/<userid>')
def profiles(userid):
    if not userid:
        profiles = [(profile.id, locate_photo(profile.id), profile.firstname, profile.lastname, 
        profile.gender, profile.location) for profile in Pro.query.all()]
        return render_template('profiles.html', profiles=profiles)
    else:
        try:
            user = Pro.query.filter_by(id=userid).first()
        
            return render_template('details.html', name=user.firstname + " " + user.lastname,
            email=user.email, location=user.location, bio=user.biography, photo=locate_photo(user.id), 
            registered=user.created_on.strftime('%B %d, %Y'))
        
        except:
            return render_template("404.html")