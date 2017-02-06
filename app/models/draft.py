import random

from xkcdpass import xkcd_password as xp

from app import app, db
from app.exceptions import JoinDraftException


class Draft(db.Model):
    '''Object that represents a draft'''
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(10))
    completed = db.Column(db.Boolean())
    players = db.relationship('Player', backref='draft')

    def __init__(self, key=None):
        if key is not None:
            self.key = key
        else:
            self.key = self._generate_key()
        self.completed = False

    def _generate_key(self):
        wordfile = xp.locate_wordfile()
        words = xp.generate_wordlist(wordfile=wordfile, min_length=5, max_length=10)
        while True:
            new_key = xp.generate_xkcdpassword(words, acrostic=random.choice(app.config['ALPHABET']))
            active = Draft.query.filter_by(completed=False) \
                .filter_by(key=new_key) \
                .first()
            if active is None:
                return new_key

    def __repr__(self):
        return 'Draft(id: {})'.format(self.key)


class Player(db.Model):
    '''Object that describes a player in the draft.
    Unique players should be determined by draft_key, player_name pairs

    No draft should have 2 players with the sane name
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    draft_id = db.Column(db.Integer, db.ForeignKey('draft.id'))
    owner = db.Column(db.Boolean)

    def __init__(self, name='', owner=False, player_uuid=None):
        self.name = name
        self.owner = owner

    def __repr__(self):
        return 'Player({}, {})'.format(self.name, self.draft.key)

    @staticmethod
    def get_joined_player(name, draft_id, player_id):
        '''Method used to find active players in draft incase of disconnect
        This should not be actively called from the class object

        Usage:
            Players.get_joined_player(...)
        '''
        active_players = Player.query.filter_by(name=name) \
            .filter_by(draft_id=draft_id).all()
        if len(active_players) == 0:
            # Create a new player for the draft
            return None
        elif len(active_players) == 1:
            player = active_players[0]
            if player.id == player_id:
                return player
        raise(JoinDraftException('There was an error joining the draft, '
                                 'please assert that your name is not taken '
                                 'and try again.'))

