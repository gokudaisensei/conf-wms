from typing import Optional
from pydantic import BaseModel
from enum import Enum


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class MembershipEnum(str, Enum):
    Choice1 = 'Choice1'
    Choice2 = 'Choice2'


class RoleEnum(str, Enum):
    SuperAdmin = 'SuperAdmin'
    Admin = 'Admin'
    Coordinator = 'Coordinator'
    Editor = 'Editor'
    AssociateEditor = 'AssociateEditor'
    Reviewer = 'Reviewer'
    Author = 'Author'


class PresentationStatusEnum(str, Enum):
    Accept = 'Accept'
    Reject = 'Reject'
    SoftAccept = 'Soft Accept'
    SoftReject = 'Soft Reject'


class ProcessEnum(str, Enum):
    SingleBlindReview = 'Single Blind Review'
    DoubleBlindReview = 'Double Blind Review'


class RevisionChangesEnum(str, Enum):
    ReviseWithMajorChanges = 'Revise with Major Changes'
    ReviseWithMinorChanges = 'Revise with Minor Changes'
    Accepted = 'Accepted'


class InstitutionBase(BaseModel):
    institutionName: str
    institutionAddress: str
    emailID: str
    contactNum: int
    membership: MembershipEnum


class InstitutionCreate(InstitutionBase):
    pass


class InstitutionUpdate(InstitutionBase):
    pass


class Institution(InstitutionBase):
    institutionID: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str
    roleID: Optional[RoleEnum]
    institution: Optional[Institution]


class UserCreate(UserBase):
    password: str
    enabled: Optional[bool]


class UserUpdate(UserBase):
    pass


class User(UserBase):
    userID: int
    enabled: bool

    class Config:
        orm_mode = True


class ConferenceBase(BaseModel):
    conferenceTheme: str
    inCharge: int
    conferenceTrack: str
    chairDesignation: str
    chairName: str
    coChairDesignation: str
    conferenceBoardDesignation: str
    conferenceBoardName: str
    organizingCommittee: str
    internationalAdvisoryBoard: str


class ConferenceCreate(ConferenceBase):
    pass


class ConferenceUpdate(ConferenceBase):
    pass


class Conference(ConferenceBase):
    conferenceID: int

    class Config:
        orm_mode = True


class ConferenceEditorReviewerBase(BaseModel):
    conferenceID: int
    editorID: int
    associateEditorID: int
    reviewerID: int


class ConferenceEditorReviewerCreate(ConferenceEditorReviewerBase):
    pass


class ConferenceEditorReviewerUpdate(ConferenceEditorReviewerBase):
    pass


class ConferenceEditorReviewer(ConferenceEditorReviewerBase):
    conferenceEditorReviewerID: int
    conference: Conference
    editor: User
    associateEditor: User
    reviewer: User

    class Config:
        orm_mode = True


class ConferenceRosterBase(BaseModel):
    conferenceID: int
    authorID: int


class ConferenceRosterCreate(ConferenceRosterBase):
    pass


class ConferenceRosterUpdate(ConferenceRosterBase):
    pass


class ConferenceRoster(ConferenceRosterBase):
    rosterID: int
    conference: Conference
    author: User

    class Config:
        orm_mode = True


class PaperBase(BaseModel):
    paperName: str
    authorID: int
    paperLink: str


class PaperCreate(PaperBase):
    pass


class PaperUpdate(PaperBase):
    pass


class Paper(PaperBase):
    paperID: int
    author: ConferenceRoster

    class Config:
        orm_mode = True


class SubmissionBase(BaseModel):
    ifPubApplicable: bool
    plagPolicy: int
    samplePaper: str
    conferenceID: int
    submissionDeadline: str


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionUpdate(SubmissionBase):
    pass


class Submission(SubmissionBase):
    submissionID: int
    conference: Conference

    class Config:
        orm_mode = True


class SubmittedPapersBase(BaseModel):
    submissionID: int
    paperID: int


class SubmittedPapersCreate(SubmittedPapersBase):
    pass


class SubmittedPapersUpdate(SubmittedPapersBase):
    pass


class SubmittedPapers(SubmittedPapersBase):
    submission: Submission
    paper: Paper

    class Config:
        orm_mode = True


class PaperRevisionBase(BaseModel):
    paperID: int
    revisionNumber: int
    revisionLink: str
    revisionDateTime: str
    submissionID: int


class PaperRevisionCreate(PaperRevisionBase):
    pass


class PaperRevisionUpdate(PaperRevisionBase):
    pass


class PaperRevision(PaperRevisionBase):
    revisionID: int
    paper: Paper

    class Config:
        orm_mode = True


class PaperStatusBase(BaseModel):
    paperID: int
    isFinalRevision: bool
    toPublish: bool
    presentationStatus: PresentationStatusEnum


class PaperStatusCreate(PaperStatusBase):
    pass


class PaperStatusUpdate(PaperStatusBase):
    pass


class PaperStatus(PaperStatusBase):
    statusID: int
    paper: Paper

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    editorID: int
    associateEditorID: int
    reviewerID: int
    revisionID: int
    process: ProcessEnum
    reviewEndDeadline: str


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    pass


class Review(ReviewBase):
    reviewID: int
    editor: ConferenceEditorReviewer
    associateEditor: ConferenceEditorReviewer
    reviewer: ConferenceEditorReviewer
    revision: PaperRevision

    class Config:
        orm_mode = True


class ReviewCommentBase(BaseModel):
    reviewID: int
    comment: str
    commentDateTime: str


class ReviewCommentCreate(ReviewCommentBase):
    pass


class ReviewCommentUpdate(ReviewCommentBase):
    pass


class ReviewComment(ReviewCommentBase):
    reviewCommentID: int
    review: Review

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    eventName: str
    venue: str
    regOpen: str
    regClose: str
    eventStart: str
    eventEnd: str
    maxParticipants: int
    conferenceID: int


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class Event(EventBase):
    eventID: int
    conference: Conference

    class Config:
        orm_mode = True


class JournalBase(BaseModel):
    journalName: str
    journalAddress: str
    emailID: str
    contactNum: int


class JournalCreate(JournalBase):
    pass


class JournalUpdate(JournalBase):
    pass


class Journal(JournalBase):
    journalID: int

    class Config:
        orm_mode = True


class JournalSubmissionBase(BaseModel):
    journalID: int
    revisionChanges: RevisionChangesEnum
    currentRevisionID: int


class JournalSubmissionCreate(JournalSubmissionBase):
    pass


class JournalSubmissionUpdate(JournalSubmissionBase):
    pass


class JournalSubmission(JournalSubmissionBase):
    jSubmissionID: int
    journal: Journal
    currentRevision: PaperRevision

    class Config:
        orm_mode = True
