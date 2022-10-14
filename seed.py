from app import app
from models import db, User


db.drop_all()
db.create_all()

u1 = User.signup(
    username="Emily",
    password="supersecret",
    email="lsdfsafs@sadfsdf.com"
)

u2 = User.signup(
    username="Pasha",
    password="doublesecret",
    email="lsafs@saf.com"
)

# db.session.add_all([u1, u2])
db.session.commit()