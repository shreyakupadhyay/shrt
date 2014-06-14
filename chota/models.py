from chota import db


class Url(db.Model):
    """
    Class for creating models via SQLAlchemy
    """
    __tablename__ = "Url"
    id = db.Column('url_id', db.Integer, primary_key=True)
    random_code = db.Column(db.String(80), unique=True)
    url = db.Column(db.String(120), unique=False)

    def __init__(self, random_code, url):
        self.random_code = random_code
        self.url = url

    def __repr__(self):
        return '<url %r>' % self.url
