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

db.create_all()
