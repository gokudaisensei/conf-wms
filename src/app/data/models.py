from sqlalchemy import Column, BigInteger, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

USER_ID = 'users.userID'
CONFERENCE_ID = 'conferences.conferenceID'
PAPER_ID = 'papers.paperID'


class Institution(Base):
    __tablename__ = 'institutions'

    institutionID = Column(BigInteger, primary_key=True, autoincrement=True)
    institutionName = Column(String(255), nullable=False)
    institutionAddress = Column(Text, nullable=False)
    emailID = Column(String(255), nullable=False)
    contactNum = Column(String(10), nullable=False)
    membership = Column(Enum('Choice1', 'Choice2'), nullable=False)


class User(Base):
    __tablename__ = 'users'

    userID = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    roleID = Column(Enum(
        'SuperAdmin',
        'Admin',
        'Coordinator',
        'Editor',
        'AssociateEditor',
        'Reviewer',
        'Author'
    ))
    institutionID = Column(BigInteger, ForeignKey(
        'institutions.institutionID'))

    institution = relationship("Institution")


class Conference(Base):
    __tablename__ = 'conferences'

    conferenceID = Column(BigInteger, primary_key=True, autoincrement=True)
    conferenceTheme = Column(String(255), nullable=False)
    inCharge = Column(BigInteger, ForeignKey(USER_ID), nullable=False)
    conferenceTrack = Column(String(255), nullable=False)
    chairDesignation = Column(String(255), nullable=False)
    chairName = Column(String(255), nullable=False)
    coChairDesignation = Column(String(255))
    conferenceBoardDesignation = Column(String(255))
    conferenceBoardName = Column(String(255))
    organizingCommittee = Column(String(255))
    internationalAdvisoryBoard = Column(String(255))


class ConferenceEditorReviewer(Base):
    __tablename__ = 'conference_editors_reviewers'

    conferenceEditorReviewerID = Column(
        BigInteger, primary_key=True, autoincrement=True)
    conferenceID = Column(BigInteger, ForeignKey(
        CONFERENCE_ID), nullable=False)
    editorID = Column(BigInteger, ForeignKey(USER_ID), nullable=False)
    associateEditorID = Column(BigInteger, ForeignKey(USER_ID))
    reviewerID = Column(BigInteger, ForeignKey(USER_ID), nullable=False)

    conference = relationship("Conference")
    editor = relationship("User", foreign_keys=[editorID])
    associateEditor = relationship("User", foreign_keys=[associateEditorID])
    reviewer = relationship("User", foreign_keys=[reviewerID])


class ConferenceRoster(Base):
    __tablename__ = 'conference_roster'

    rosterID = Column(BigInteger, primary_key=True, autoincrement=True)
    conferenceID = Column(BigInteger, ForeignKey(
        CONFERENCE_ID), nullable=False)
    authorID = Column(BigInteger, ForeignKey(USER_ID), nullable=False)

    conference = relationship("Conference")
    author = relationship("User")


class Paper(Base):
    __tablename__ = 'papers'

    paperID = Column(BigInteger, primary_key=True, autoincrement=True)
    paperName = Column(String(255), nullable=False)
    authorID = Column(BigInteger, ForeignKey(
        'conference_roster.authorID'), nullable=False)
    paperLink = Column(String(255), nullable=False)

    author = relationship("ConferenceRoster")


class Submission(Base):
    __tablename__ = 'submissions'

    submissionID = Column(BigInteger, primary_key=True, autoincrement=True)
    ifPubApplicable = Column(Boolean, nullable=False)
    plagPolicy = Column(Integer, nullable=False)
    samplePaper = Column(String(255), nullable=False)
    conferenceID = Column(BigInteger, ForeignKey(
        CONFERENCE_ID), nullable=False)
    submissionDeadline = Column(DateTime, nullable=False)

    conference = relationship("Conference")


class SubmittedPapers(Base):
    __tablename__ = 'submitted_papers'

    submissionID = Column(BigInteger, ForeignKey(
        'submissions.submissionID'), nullable=False, primary_key=True)
    paperID = Column(BigInteger, ForeignKey(PAPER_ID),
                     nullable=False, primary_key=True)

    submission = relationship("Submission")
    paper = relationship("Paper")


class PaperRevision(Base):
    __tablename__ = 'paper_revisions'

    revisionID = Column(BigInteger, primary_key=True, autoincrement=True)
    paperID = Column(BigInteger, ForeignKey(PAPER_ID), nullable=False)
    revisionNumber = Column(Integer, nullable=False)
    revisionLink = Column(String(255), nullable=False)
    revisionDateTime = Column(DateTime, nullable=False)
    submissionID = Column(BigInteger, ForeignKey(
        'submitted_papers.submissionID'))

    paper = relationship("Paper")


class PaperStatus(Base):
    __tablename__ = 'paper_status'

    statusID = Column(BigInteger, primary_key=True, autoincrement=True)
    paperID = Column(BigInteger, ForeignKey(PAPER_ID), nullable=False)
    isFinalRevision = Column(Boolean, default=False)
    toPublish = Column(Boolean, default=False)
    presentationStatus = Column(
        Enum('Accept', 'Reject', 'Soft Accept', 'Soft Reject'))

    paper = relationship("Paper")


class Review(Base):
    __tablename__ = 'reviews'

    reviewID = Column(BigInteger, primary_key=True, autoincrement=True)
    editorID = Column(BigInteger, ForeignKey(
        'conference_editors_reviewers.editorID'), nullable=False)
    associateEditorID = Column(BigInteger, ForeignKey(
        'conference_editors_reviewers.associateEditorID'))
    reviewerID = Column(BigInteger, ForeignKey(
        'conference_editors_reviewers.reviewerID'), nullable=False)
    revisionID = Column(BigInteger, ForeignKey(
        'paper_revisions.revisionID'), nullable=False)
    process = Column(Enum('Single Blind Review',
                     'Double Blind Review'), nullable=False)
    reviewEndDeadline = Column(DateTime, nullable=False)

    editor = relationship("ConferenceEditorReviewer", foreign_keys=[editorID])
    associateEditor = relationship(
        "ConferenceEditorReviewer", foreign_keys=[associateEditorID])
    reviewer = relationship("ConferenceEditorReviewer",
                            foreign_keys=[reviewerID])
    revision = relationship("PaperRevision")


class ReviewComment(Base):
    __tablename__ = 'review_comments'

    reviewCommentID = Column(BigInteger, primary_key=True, autoincrement=True)
    reviewID = Column(BigInteger, ForeignKey(
        'reviews.reviewID'), nullable=False)
    comment = Column(Text)
    commentDateTime = Column(DateTime, nullable=False)

    review = relationship("Review")


class Event(Base):
    __tablename__ = 'events'

    eventID = Column(BigInteger, primary_key=True, autoincrement=True)
    eventName = Column(String(255), nullable=False)
    venue = Column(String(255), nullable=False)
    regOpen = Column(DateTime, nullable=False)
    regClose = Column(DateTime, nullable=False)
    eventStart = Column(DateTime, nullable=False)
    eventEnd = Column(DateTime, nullable=False)
    maxParticipants = Column(Integer, nullable=False)
    conferenceID = Column(BigInteger, ForeignKey(CONFERENCE_ID))

    conference = relationship("Conference")


class Journal(Base):
    __tablename__ = 'journals'

    journalID = Column(BigInteger, primary_key=True, autoincrement=True)
    journalName = Column(String(255), nullable=False)
    journalAddress = Column(Text, nullable=False)
    emailID = Column(String(255), nullable=False)
    contactNum = Column(BigInteger, nullable=False)


class JournalSubmission(Base):
    __tablename__ = 'journal_submissions'

    jSubmissionID = Column(BigInteger, primary_key=True, autoincrement=True)
    journalID = Column(BigInteger, ForeignKey('journals.journalID'))
    revisionChanges = Column(Enum(
        'Revise with Major Changes',
        'Revise with Minor Changes',
        'Accepted'
    ))
    currentRevisionID = Column(
        BigInteger, ForeignKey('paper_revisions.revisionID'))

    journal = relationship("Journal")
    currentRevision = relationship("PaperRevision")
