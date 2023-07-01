from sqlalchemy import BigInteger, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, and_
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.associationproxy import association_proxy
from typing import List, Optional


class Base(DeclarativeBase):
    pass


USER_ID = 'users.userID'
CONFERENCE_ID = 'conferences.conferenceID'
PAPER_ID = 'papers.paperID'


class Institution(Base):
    __tablename__ = 'institutions'

    institutionID: Mapped[int] = mapped_column(BigInteger,
                                               primary_key=True, autoincrement=True)
    institutionName: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    institutionAddress: Mapped[str] = mapped_column(Text, nullable=False)
    emailID: Mapped[str] = mapped_column(String(255), nullable=False)
    contactNum: Mapped[str] = mapped_column(String(10), nullable=False)
    membership: Mapped[Enum] = mapped_column(
        Enum('Choice1', 'Choice2'), nullable=False)


class User(Base):
    __tablename__ = 'users'

    userID: Mapped[BigInteger] = mapped_column(BigInteger,
                                               primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    roleID: Mapped[Optional[Enum]] = mapped_column(
        Enum(
            'SuperAdmin',
            'Admin',
            'Coordinator',
            'Editor',
            'AssociateEditor',
            'Reviewer',
            'Author'
        )
    )
    institutionID: Mapped[Optional[int]] = mapped_column(BigInteger,
                                                         ForeignKey('institutions.institutionID'))

    institution: Mapped["Institution"] = relationship(
        "Institution", backref="users")


class Conference(Base):
    __tablename__ = 'conferences'

    conferenceID: Mapped[int] = mapped_column(BigInteger,
                                              primary_key=True, autoincrement=True)
    conferenceTheme: Mapped[str] = mapped_column(String(255), nullable=False)
    inCharge: Mapped[int] = mapped_column(BigInteger,
                                          ForeignKey(USER_ID), nullable=False)
    conferenceTrack: Mapped[str] = mapped_column(String(255), nullable=False)
    chairDesignation: Mapped[str] = mapped_column(String(255), nullable=False)
    chairName: Mapped[str] = mapped_column(String(255), nullable=False)
    coChairDesignation: Mapped[Optional[str]] = mapped_column(String(255))
    conferenceBoardDesignation: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True)
    conferenceBoardName: Mapped[Optional[str]] = mapped_column(
        String(255))
    organizingCommittee: Mapped[Optional[str]] = mapped_column(
        String(255))
    internationalAdvisoryBoard: Mapped[Optional[str]] = mapped_column(
        String(255))

    coordinator: Mapped["User"] = relationship("User", uselist=False)

    conferenceEditors: Mapped[List["ConferenceEditor"]] = relationship(
        "ConferenceEditor")
    editors: Mapped[List["User"]] = association_proxy(
        # type: ignore
        'conferenceEditors', 'editor', creator=lambda editor: ConferenceEditor(editor=editor)
    )

    conferenceAssociateEditors: Mapped[List["ConferenceAssociateEditor"]] = relationship(
        "ConferenceAssociateEditor")
    associateEditors: Mapped[List["User"]] = association_proxy(  # type: ignore
        'conferenceAssociateEditors', 'associateEditor', creator=lambda associateEditor: ConferenceEditor(associateEditor=associateEditor)
    )

    conferenceReviewers: Mapped[List["ConferenceReviewer"]] = relationship(
        "ConferenceReviewer")
    reviewers: Mapped[List["User"]] = association_proxy(  # type: ignore
        "conferenceReviewers", "reviewer", creator=lambda reviewer: ConferenceReviewer(reviewer=reviewer))

    conferenceAuthors: Mapped[List["ConferenceRoster"]] = relationship(
        "ConferenceRoster")
    authors: Mapped[List["User"]] = association_proxy(  # type: ignore
        "conferenceAuthors", "author", creator=lambda author: ConferenceRoster(author=author))

    submissions: Mapped[List["Submission"]] = relationship("Submission")


class ConferenceEditor(Base):
    __tablename__ = 'conference_editors'

    conferenceEditorID: Mapped[int] = mapped_column(BigInteger,
                                                    primary_key=True, autoincrement=True)
    conferenceID: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(CONFERENCE_ID), nullable=False)
    editorID: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(USER_ID), nullable=False, unique=True)

    editor: Mapped["User"] = relationship("User")


class ConferenceAssociateEditor(Base):
    __tablename__ = 'conference_associate_editors'

    conferenceAssociateEditorID: Mapped[int] = mapped_column(BigInteger,
                                                             primary_key=True, autoincrement=True)
    conferenceID: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(CONFERENCE_ID), nullable=False)
    associateEditorID: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(USER_ID), nullable=False, unique=True)

    associateEditor: Mapped["User"] = relationship("User")


class ConferenceReviewer(Base):
    __tablename__ = 'conference_reviewers'

    conferenceReviewerID: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    conferenceID: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(CONFERENCE_ID), nullable=False)
    reviewerID: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(USER_ID), nullable=False, unique=True)

    reviewer: Mapped["User"] = relationship("User")


class ConferenceRoster(Base):
    __tablename__ = 'conference_roster'

    rosterID: Mapped[int] = mapped_column(BigInteger,
                                          primary_key=True, autoincrement=True)
    conferenceID: Mapped[int] = mapped_column(BigInteger,
                                              ForeignKey(CONFERENCE_ID), nullable=False)
    authorID: Mapped[int] = mapped_column(BigInteger,
                                          ForeignKey(USER_ID), nullable=False)

    author: Mapped["User"] = relationship("User")


class Paper(Base):
    __tablename__ = 'papers'

    paperID: Mapped[int] = mapped_column(BigInteger,
                                         primary_key=True, autoincrement=True)
    paperName: Mapped[str] = mapped_column(String(255), nullable=False)
    authorID: Mapped[int] = mapped_column(BigInteger,
                                          ForeignKey('conference_roster.authorID'), nullable=False)
    paperLink: Mapped[str] = mapped_column(String(255), nullable=False)

    author = relationship("ConferenceRoster")


class Submission(Base):
    __tablename__ = 'submissions'

    submissionID: Mapped[int] = mapped_column(BigInteger,
                                              primary_key=True, autoincrement=True)
    ifPubApplicable: Mapped[bool]
    plagPolicy: Mapped[int]
    samplePaper: Mapped[str] = mapped_column(String(255))
    conferenceID: Mapped[int] = mapped_column(BigInteger,
                                              ForeignKey(CONFERENCE_ID), nullable=False)
    submissionDeadline: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False)

    papers: Mapped[List["Paper"]] = relationship("Paper", backref="submission")


# class SubmittedPapers(Base):
#     __tablename__ = 'submitted_papers'

#     submissionID: Mapped[BigInteger] = mapped_column(ForeignKey(
#         'submissions.submissionID'), nullable=False, primary_key=True)
#     paperID: Mapped[BigInteger] = mapped_column(
#         ForeignKey(PAPER_ID), nullable=False, primary_key=True)

#     submission = relationship("Submission")
#     paper = relationship("Paper")


# class PaperRevision(Base):
#     __tablename__ = 'paper_revisions'

#     revisionID: Mapped[BigInteger] = mapped_column(
#         primary_key=True, autoincrement=True)
#     paperID: Mapped[BigInteger] = mapped_column(
#         ForeignKey(PAPER_ID), nullable=False)
#     revisionNumber: Mapped[int] = mapped_column(Integer, nullable=False)
#     revisionLink: Mapped[str] = mapped_column(String(255), nullable=False)
#     revisionDateTime: Mapped[DateTime] = mapped_column(
#         DateTime, nullable=False)
#     submissionID: Mapped[BigInteger] = mapped_column(
#         ForeignKey('submitted_papers.submissionID'))

#     paper = relationship("Paper")


# class PaperStatus(Base):
#     __tablename__ = 'paper_status'

#     statusID: Mapped[BigInteger] = mapped_column(
#         primary_key=True, autoincrement=True)
#     paperID: Mapped[BigInteger] = mapped_column(
#         ForeignKey(PAPER_ID), nullable=False)
#     isFinalRevision: Mapped[bool] = mapped_column(Boolean, default=False)
#     toPublish: Mapped[bool] = mapped_column(Boolean, default=False)
#     presentationStatus: Mapped[Enum] = mapped_column(
#         Enum('Accept', 'Reject', 'Soft Accept', 'Soft Reject'))

#     paper = relationship("Paper")


# class Review(Base):
#     __tablename__ = 'reviews'

#     reviewID: Mapped[BigInteger] = mapped_column(
#         primary_key=True, autoincrement=True)
#     editorID: Mapped[BigInteger] = mapped_column(ForeignKey(
#         'conference_editors_reviewers.editorID'), nullable=False)
#     associateEditorID: Mapped[BigInteger] = mapped_column(
#         ForeignKey('conference_editors_reviewers.associateEditorID'))
#     reviewerID: Mapped[BigInteger] = mapped_column(ForeignKey(
#         'conference_editors_reviewers.reviewerID'), nullable=False)
#     revisionID: Mapped[BigInteger] = mapped_column(
#         ForeignKey('paper_revisions.revisionID'), nullable=False)
#     process: Mapped[Enum] = mapped_column(
#         Enum('Single Blind Review', 'Double Blind Review'), nullable=False)
#     reviewEndDeadline: Mapped[DateTime] = mapped_column(
#         DateTime, nullable=False)

#     editor = relationship("ConferenceEditorReviewer", foreign_keys=[editorID])
#     associateEditor = relationship(
#         "ConferenceEditorReviewer", foreign_keys=[associateEditorID])
#     reviewer = relationship("ConferenceEditorReviewer",
#                             foreign_keys=[reviewerID])
#     revision = relationship("PaperRevision")


# class ReviewComment(Base):
#     __tablename__ = 'review_comments'

#     reviewCommentID: Mapped[BigInteger] = mapped_column(
#         primary_key=True, autoincrement=True)
#     reviewID: Mapped[BigInteger] = mapped_column(
#         ForeignKey('reviews.reviewID'), nullable=False)
#     comment: Mapped[Text] = mapped_column(Text)
#     commentDateTime: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

#     review = relationship("Review")


# class Event(Base):
#     __tablename__ = 'events'

#     eventID: Mapped[BigInteger] = mapped_column(
#         primary_key=True, autoincrement=True)
#     eventName: Mapped[str] = mapped_column(
#         String(255), nullable=False, unique=True)
#     venue: Mapped[str] = mapped_column(String(255), nullable=False)
#     regOpen: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
#     regClose: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
#     eventStart: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
#     eventEnd: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
#     maxParticipants: Mapped[int] = mapped_column(Integer, nullable=False)
#     conferenceID: Mapped[BigInteger] = mapped_column(ForeignKey(CONFERENCE_ID))

#     conference = relationship("Conference")


# class Journal(Base):
#     __tablename__ = 'journals'

#     journalID: Mapped[BigInteger] = mapped_column(
#         primary_key=True, autoincrement=True)
#     journalName: Mapped[str] = mapped_column(String(255), nullable=False)
#     journalAddress: Mapped[Text] = mapped_column(Text, nullable=False)
#     emailID: Mapped[str] = mapped_column(String(255), nullable=False)
#     contactNum: Mapped[BigInteger] = mapped_column(BigInteger, nullable=False)


# class JournalSubmission(Base):
#     __tablename__ = 'journal_submissions'

#     jSubmissionID: Mapped[BigInteger] = mapped_column(
#         primary_key=True, autoincrement=True)
#     journalID: Mapped[BigInteger] = mapped_column(
#         ForeignKey('journals.journalID'))
#     revisionChanges: Mapped[Enum] = mapped_column(
#         Enum('Revise with Major Changes', 'Revise with Minor Changes', 'Accepted')
#     )
#     currentRevisionID: Mapped[BigInteger] = mapped_column(
#         ForeignKey('paper_revisions.revisionID')
#     )

#     journal = relationship("Journal")
#     currentRevision = relationship("PaperRevision")
