from app import db


class Draft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    draft_key = db.Column(db.String(8))
    completed = db.Column(db.Boolean())

    def __init__(self, draft_key=''):
        self.draft_key = draft_key
        self.completed = False

    def __repr__(self):
        return 'Draft(id: {})'.format(self.draft_key)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    ip = db.Column(db.String(16))  # used for resuming state on disconnect (presumably)

    def __init__(self, name='', ip=''):
        self.name = name
        self.ip = ip

    def __repr__(self):
        return 'User({}, {})'.format(self.name, self.ip_)
