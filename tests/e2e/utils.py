from flask import g, session
from src.models import *

def reset_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
