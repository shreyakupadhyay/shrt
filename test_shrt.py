import unittest
from app import db, app
from app.models import Url
from app.views import random_key

import os
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class TestShrt(unittest.TestCase):

    test_url = 'http://google.com'

    def setUp(self):
        self.client = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = db_path
        app.config['TESTING'] = True
        self.key = random_key(self.test_url)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_form(self):
        form = {'url': self.test_url}
        r = self.client.post('/form', data=form)
        l = Url.query.filter_by(url=self.test_url).first()
        self.assertIsNotNone(l)
        self.assertEqual(l.random_code, self.key)

    def test_expand_shortened_link(self):
        self.test_form()
        r = self.client.get(self.key)
        self.assertEqual(r.status_code, 302)
        assert "http://google.com" and "redirected" in r.data

    def test_expand_unshortened_link(self):
        r = self.client.get('abcd')
        self.assertEqual(r.status_code, 302)
        assert "/" and "redirected" in r.data

if __name__ == '__main__':
    unittest.main()
