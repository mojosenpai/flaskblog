from app import app, db
from app import User, Post, Tag, post_tag
from faker import Faker
import random

fake = Faker()
with app.app_context():
    db.drop_all()
    db.create_all()

roles = ['Author', 'Admin', 'Editor']

users = []
tags = []
posts = []
post_tag = []

for _ in range(10):
    user = User(name=fake.name(), username=fake.name(), password=fake.password(), role=random.choice(roles))
    users.append(user)


# user1 = User(name='Admin1', username='admin1', password='123456', role='Admin')
# post1 = Post(title='Intro', content='fda;dahgjdahsg')
# tag1 = Tag(name='politics')
# post1.labels.append(tag1)
# post1.author=user1

with app.app_context():
    # db.session.add(user1)
    # db.session.add(post1)
    # db.session.add(tag1)
    db.session.add_all(users)
    db.session.commit()