import random

from flask import render_template, redirect, session, request
from xkcdpass import xkcd_password as xp

from app import db, app
from app.models import Draft, User


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/draft/create', methods=['POST'])
def create_draft():
    # Generate draftroom name
    wordfile = xp.locate_wordfile()
    words = xp.generate_wordlist(wordfile=wordfile, min_length=5, max_length=8)
    draft_id = xp.generate_xkcdpassword(words, acrostic=random.choice(app.config['ALPHABET']))

    # Create Draft in the database
    draft = Draft(draft_key=draft_id)
    db.session.add(draft)

    # Create the user and add to the Draft
    user = User(name=request.form.get('username'), ip=request.remote_addr)
    db.session.add(user)

    db.session.commit()

    session['draft_id'] = draft_id
    session['username'] = request.form.get('username')
    session['draft_owner'] = True
    return redirect('/draft')


@app.route('/draft/join', methods=['POST'])
def join_draft():
    draft_key = request.form.get('passphrase')
    username = request.form.get('username')
    draft = Draft.query.filter_by(draft_key=draft_key).first()
    if draft is None or username is None:
        print('Draft not found: {}'.format(draft_key))
        return redirect('/')
    if session.get('draft_id', None) == draft_key and session.get('username') == username:
        session['draft_owner'] == session.get('draft_owner', False)
    else:
        session['draft_id'] = draft_key
        session['username'] = username
        session['draft_owner'] = False
    return redirect('/draft')


@app.route('/draft', methods=['GET'])
def draft():
    return render_template('draft.html')
