from flask import render_template, redirect, session, request
from flask import flash

from app import db, app
from app.decorators import announce, templated
from app.exceptions import MTGException, JoinDraftException
from app.models.draft import Draft, Player


@app.route('/', methods=['GET'])
@templated()
def home():
    '''Default homepage'''
    return {}


@app.route('/draft/create', methods=['POST'])
def create_draft():
    '''Creates a new draft for other players to join into'''
    # Create Draft in the database
    draft = Draft()
    db.session.add(draft)
    # Create the user and add to the Draft
    player = Player(name=request.form.get('username'),
                    owner=True)
    player.draft = draft
    db.session.add(player)
    db.session.commit()

    session['draft_key'] = draft.key
    session['draft_owner'] = player.owner
    session['player_name'] = player.name
    session['player_id'] = player.id
    return redirect('/draft')


@app.route('/draft/join', methods=['POST'])
@announce(MTGException)
def join_draft():
    '''Adds a  player into an existing draft'''
    draft_key = request.form.get('passphrase')
    username = request.form.get('username')

    # Get the draft
    draft = Draft.query.filter_by(key=draft_key).first()
    if draft is None:
        raise(JoinDraftException('Unable to locate draft: {}'.format(draft_key)))

    # Get the user
    if username is None:
        raise(JoinDraftException('Please specify a username inorder to join the draft'))
    player_id = session.get('player_id', None)
    player = Player.get_joined_player(name=username, draft_id=draft.id, player_id=player_id)
    if player is None:
        player = Player(name=username)
        player.draft = draft
        db.session.add(player)
        db.session.commit()

    # Renew session values
    session['draft_key'] = draft.key
    session['draft_owner'] = player.owner
    session['player_name'] = player.name
    session['player_id'] = player.id
    return redirect('/draft')


@app.route('/draft', methods=['GET'])
@announce(MTGException)
@templated()
def draft():
    '''Page where the draft occurs'''
    if session.get('draft_key', None) is None:
        raise(MTGException('Seems that you have wondered here by mistake...'))
