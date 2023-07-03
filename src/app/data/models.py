import datetime
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

    def __repr__(self):
        return f"Institution(institutionID={self.institutionID}, institutionName='{self.institutionName}', institutionAddress='{self.institutionAddress}', emailID='{self.emailID}', contactNum='{self.contactNum}', membership='{self.membership}')"


class User(Base):
    __tablename__ = 'users'

    userID: Mapped[int] = mapped_column(BigInteger,
                                               primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(
        String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
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

    def __repr__(self):
        return f"User(userID={self.userID}, name='{self.name}', email='{self.email}', password='{self.password}', roleID={self.roleID}, institutionID={self.institutionID})"


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

    def __repr__(self):
        return f"Conference(conferenceID={self.conferenceID}, conferenceTheme='{self.conferenceTheme}', inCharge={self.inCharge}, conferenceTrack='{self.conferenceTrack}', chairDesignation='{self.chairDesignation}', chairName='{self.chairName}', coChairDesignation='{self.coChairDesignation}', conferenceBoardDesignation='{self.conferenceBoardDesignation}', conferenceBoardName='{self.conferenceBoardName}', organizingCommittee='{self.organizingCommittee}', internationalAdvisoryBoard='{self.internationalAdvisoryBoard}')"


class ConferenceEditor(Base):
    __tablename__ = 'conference_editors'

    conferenceEditorID: Mapped[int] = mapped_column(BigInteger,
                                                    primary_key=True, autoincrement=True)
    conferenceID: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(CONFERENCE_ID), nullable=False)
    editorID: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(USER_ID), nullable=False, unique=True)

    editor: Mapped["User"] = relationship("User")

    def __repr__(self):
        return f"ConferenceEditor(conferenceEditorID={self.conferenceEditorID}, conferenceID={self.conferenceID}, editorID={self.editorID})"


class ConferenceAssociateEditor(Base):
    __tablename__ = 'conference_associate_editors'

    conferenceAssociateEditorID: Mapped[int] = mapped_column(BigInteger,
                                                             primary_key=True, autoincrement=True)
    conferenceID: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(CONFERENCE_ID), nullable=False)
    associateEditorID: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(USER_ID), nullable=False, unique=True)

    associateEditor: Mapped["User"] = relationship("User")

    def __repr__(self):
        return f"ConferenceAssociateEditor(conferenceAssociateEditorID={self.conferenceAssociateEditorID}, conferenceID={self.conferenceID}, associateEditorID={self.associateEditorID})"


class ConferenceReviewer(Base):
    __tablename__ = 'conference_reviewers'

    conferenceReviewerID: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    conferenceID: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(CONFERENCE_ID), nullable=False)
    reviewerID: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(USER_ID), nullable=False, unique=True)

    reviewer: Mapped["User"] = relationship("User")

    def __repr__(self):
        return f"ConferenceReviewer(conferenceReviewerID={self.conferenceReviewerID}, conferenceID={self.conferenceID}, reviewerID={self.reviewerID})"


class ConferenceRoster(Base):
    __tablename__ = 'conference_roster'

    rosterID: Mapped[int] = mapped_column(BigInteger,
                                          primary_key=True, autoincrement=True)
    conferenceID: Mapped[int] = mapped_column(BigInteger,
                                              ForeignKey(CONFERENCE_ID), nullable=False)
    authorID: Mapped[int] = mapped_column(BigInteger,
                                          ForeignKey(USER_ID), nullable=False)

    author: Mapped["User"] = relationship("User")

    def __repr__(self):
        return f"ConferenceRoster(rosterID={self.rosterID}, conferenceID={self.conferenceID}, authorID={self.authorID})"


class Paper(Base):
    __tablename__ = 'papers'

    paperID: Mapped[int] = mapped_column(BigInteger,
                                         primary_key=True, autoincrement=True)
    paperName: Mapped[str] = mapped_column(String(255), nullable=False)
    authorID: Mapped[int] = mapped_column(BigInteger,
                                          ForeignKey('conference_roster.authorID'), nullable=False)
    paperLink: Mapped[str] = mapped_column(String(255), nullable=False)

    author = relationship("ConferenceRoster")

    def __repr__(self):
        return f"Paper(paperID={self.paperID}, paperName='{self.paperName}', authorID={self.authorID}, paperLink='{self.paperLink}')"


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

    submittedPaper: Mapped[List["SubmittedPaper"]
                           ] = relationship("SubmittedPaper", backref="submission")
    papers: Mapped[List["Paper"]] = association_proxy(  # type: ignore
        "submittedPaper", "paper", creator=lambda paper: SubmittedPaper(paper=paper))

    def __repr__(self):
        return f"Submission(submissionID={self.submissionID}, ifPubApplicable={self.ifPubApplicable}, plagPolicy={self.plagPolicy}, samplePaper='{self.samplePaper}', conferenceID={self.conferenceID}, submissionDeadline='{self.submissionDeadline}')"


class SubmittedPaper(Base):
    __tablename__ = 'submitted_papers'

    submittedPaperID: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    submissionID: Mapped[int] = mapped_column(BigInteger, ForeignKey(
        'submissions.submissionID'), nullable=False, primary_key=True)
    paperID: Mapped[BigInteger] = mapped_column(
        ForeignKey(PAPER_ID), nullable=False, primary_key=True)

    paper: Mapped["Paper"] = relationship("Paper")

    def __repr__(self):
        return f"SubmittedPaper(submittedPaperID={self.submittedPaperID}, submissionID={self.submissionID}, paperID={self.paperID})"


class PaperRevision(Base):
    __tablename__ = 'paper_revisions'

    revisionID: Mapped[int] = mapped_column(BigInteger,
                                            primary_key=True, autoincrement=True)
    revisionNumber: Mapped[int]
    revisionLink: Mapped[str] = mapped_column(String(255))
    revisionDateTime: Mapped[datetime.datetime] = mapped_column(DateTime)
    submittedPaperID: Mapped[int] = mapped_column(BigInteger,
                                                  ForeignKey('submitted_papers.submittedPaperID'))

    submittedPaper: Mapped["SubmittedPaper"] = relationship("SubmittedPaper")
    paper: Mapped["Paper"] = association_proxy(  # type:ignore
        "submittedPaper", "paper", creator=lambda paper: SubmittedPaper(paper=paper))
    submission: Mapped["Paper"] = association_proxy(  # type:ignore
        "submittedPaper", "submission", creator=lambda submission: SubmittedPaper(submission=submission))


class PaperStatus(Base):
    __tablename__ = 'paper_status'

    statusID: Mapped[int] = mapped_column(BigInteger,
                                          primary_key=True, autoincrement=True)
    paperID: Mapped[BigInteger] = mapped_column(
        ForeignKey(PAPER_ID))
    isFinalRevision: Mapped[bool] = mapped_column(Boolean, default=False)
    toPublish: Mapped[bool] = mapped_column(Boolean, default=False)
    presentationStatus: Mapped[Enum] = mapped_column(
        Enum('Accept', 'Reject', 'Soft Accept', 'Soft Reject'))

    paper = relationship("Paper")


class Review(Base):
    __tablename__ = 'reviews'

    reviewID: Mapped[int] = mapped_column(BigInteger,
                                          primary_key=True, autoincrement=True)
    editorID: Mapped[int] = mapped_column(BigInteger, ForeignKey(
        'conference_editors.conferenceEditorID'))
    associateEditorID: Mapped[Optional[int]] = mapped_column(BigInteger,
                                                             ForeignKey('conference_associate_editors.conferenceAssociateEditorID'))
    reviewerID: Mapped[int] = mapped_column(BigInteger, ForeignKey(
        'conference_reviewers.conferenceReviewerID'))
    revisionID: Mapped[int] = mapped_column(BigInteger,
                                            ForeignKey('paper_revisions.revisionID'))
    process: Mapped[Enum] = mapped_column(
        Enum('Single Blind Review', 'Double Blind Review'))
    reviewEndDeadline: Mapped[datetime.datetime] = mapped_column(
        DateTime)

    reviewEditor: Mapped["ConferenceEditor"] = relationship(
        "ConferenceEditor", uselist=False)
    reviewAssociateEditor: Mapped["ConferenceAssociateEditor"] = relationship(
        "ConferenceAssociateEditor", uselist=False)
    reviewReviewer: Mapped["ConferenceReviewer"] = relationship(
        "ConferenceReviewer", uselist=False)
    editor: Mapped["User"] = association_proxy(
        "reviewEditor", "editor", creator=lambda editor: ConferenceEditor(editor=editor))  # type: ignore
    associateEditor: Mapped["User"] = association_proxy(
        "reviewAssociateEditor", "associateEditor", creator=lambda associateEditor: ConferenceEditor(associateEditor=associateEditor))  # type: ignore
    reviewer: Mapped["User"] = association_proxy(
        "reviewReviewer", "reviewer", creator=lambda reviewer: ConferenceEditor(reviewer=reviewer))  # type: ignore

    revision: Mapped["PaperRevision"] = relationship("PaperRevision")


class ReviewComment(Base):
    __tablename__ = 'review_comments'

    reviewCommentID: Mapped[int] = mapped_column(BigInteger,
        primary_key=True, autoincrement=True)
    reviewID: Mapped[int] = mapped_column(BigInteger,
        ForeignKey('reviews.reviewID'))
    comment: Mapped[str] = mapped_column(Text)
    commentDateTime: Mapped[datetime.datetime] = mapped_column(DateTime)

    review: Mapped["Review"] = relationship("Review", backref="comments")


class Event(Base):
    __tablename__ = 'events'

    eventID: Mapped[int] = mapped_column(BigInteger,
                                         primary_key=True, autoincrement=True)
    eventName: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    venue: Mapped[str] = mapped_column(String(255))
    regOpen: Mapped[datetime.datetime] = mapped_column(DateTime)
    regClose: Mapped[datetime.datetime] = mapped_column(DateTime)
    eventStart: Mapped[datetime.datetime] = mapped_column(DateTime)
    eventEnd: Mapped[datetime.datetime] = mapped_column(DateTime)
    maxParticipants: Mapped[Optional[int]]
    conferenceID: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(CONFERENCE_ID))

    conference: Mapped["Conference"] = relationship(
        "Conference", backref='event', uselist=False)


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
