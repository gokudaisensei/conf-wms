from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models import Base, Institution, User, Conference, ConferenceEditor, ConferenceAssociateEditor, ConferenceReviewer
from random import choice
from tests import ROLE_ENUM, create_users
import os

# Define the mock data
institutions_data = [
    {
        'institutionName': 'Institution 1',
        'institutionAddress': 'Address 1',
        'emailID': 'institution1@example.com',
        'contactNum': '1234567890',
        'membership': 'Choice1'
    },
    {
        'institutionName': 'Institution 2',
        'institutionAddress': 'Address 2',
        'emailID': 'institution2@example.com',
        'contactNum': '9876543210',
        'membership': 'Choice2'
    },
    # Add more institutions as needed
]

# Create a database engine and session
engine = create_engine(os.getenv('TESTING_DATABASE_URL'),  # type: ignore
                       echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Create the database tables
Base.metadata.create_all(engine)

# Populate the Institution table
institutions = []
for data in institutions_data:
    institution = Institution(**data)
    institutions.append(institution)
    session.add(institution)

session.commit()

# Populate the User table
users = []
user_count = 5
for role in ROLE_ENUM.keys():
    users = create_users(role, count=user_count)
    for user in users:
        session.add(User(**user))

session.commit()

admins = [_ for _ in session.query(User).filter(User.roleID == 2).all()]
coordinators = [_ for _ in session.query(User).filter(User.roleID == 3).all()]
editors = [_ for _ in session.query(User).filter(User.roleID == 4).all()]
associate = [_ for _ in session.query(User).filter(User.roleID == 5).all()]
reviewers = [_ for _ in session.query(User).filter(User.roleID == 6).all()]
authors = [_ for _ in session.query(User).filter(User.roleID == 7).all()]
institutions = [_ for _ in session.query(Institution).all()]

for admin, coordinator in zip(admins, coordinators):
    admin.institutionID = choice(institutions).institutionID
    coordinator.institutionID = choice(institutions).institutionID

session.commit()

conferences_data = [
    {
        'conferenceTheme': 'Conference 1 Theme',
        'conferenceTrack': 'Conference 1 Track',
        'chairDesignation': 'Chair 1',
        'chairName': 'Chair Name 1',
    },
    {
        'conferenceTheme': 'Conference 2 Theme',
        'conferenceTrack': 'Conference 2 Track',
        'chairDesignation': 'Chair 2',
        'chairName': 'Chair Name 2',
    },
    {
        'conferenceTheme': 'Conference 3 Theme',
        'conferenceTrack': 'Conference 3 Track',
        'chairDesignation': 'Chair 3',
        'chairName': 'Chair Name 3',
    },
    {
        'conferenceTheme': 'Conference 4 Theme',
        'conferenceTrack': 'Conference 4 Track',
        'chairDesignation': 'Chair 4',
        'chairName': 'Chair Name 4',
    },
    {
        'conferenceTheme': 'Conference 5 Theme',
        'conferenceTrack': 'Conference 5 Track',
        'chairDesignation': 'Chair 5',
        'chairName': 'Chair Name 5',
    },
    {
        'conferenceTheme': 'Conference 6 Theme',
        'conferenceTrack': 'Conference 6 Track',
        'chairDesignation': 'Chair 6',
        'chairName': 'Chair Name 6',
    }
]
for data in conferences_data:
    data['inCharge'] = choice(coordinators).userID  # type: ignore
    conference = Conference(**data)
    session.add(conference)

session.commit()
conferences = [_ for _ in session.query(Conference).all()]

for editor, aeditor, reviewer in zip(editors, associate, reviewers):
    session.add(ConferenceEditor(editorID=editor.userID,
                conferenceID=choice(conferences).conferenceID))
    session.add(ConferenceAssociateEditor(associateEditorID=aeditor.userID,
                conferenceID=choice(conferences).conferenceID))
    session.add(ConferenceReviewer(reviewerID=reviewer.userID,
                conferenceID=choice(conferences).conferenceID))

session.commit()
