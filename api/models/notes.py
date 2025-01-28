"""notes.py"""

from typing import Optional, Annotated
from datetime import datetime
# from sqlalchemy import and_, or_
from enum import Enum
from pydantic import BaseModel, Field
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Path, Depends
from api.database import NoteDb, get_db, UserDb
from api.utils.session import SessionManager, get_session_manager


NoteId = Annotated[int, Path(gt=0)]
TimeChanged = Annotated[Optional[datetime], Field(default_factory=datetime.utcnow)]

SessionRequest = Annotated[SessionManager, Depends(get_session_manager)]


# Predefined values
class NoteField(str, Enum):
    """Enum for note fields"""
    ID = "id"
    USERID = "user_id"
    TITLE = "title"
    CONTENT = "content"


class BaseNote(BaseModel):
    """Note model"""
    title: Optional[str] = None
    content: str


class CreateNote(BaseNote):
    """Create note model"""
    user_id: Optional[int] = None
    time_created: TimeChanged
    time_edition: TimeChanged


class UpdateNote(BaseNote):
    """Update note model"""
    time_edition: TimeChanged


class NoteDetails(CreateNote):
    """Class note with additional fields [id]"""
    id: NoteId


class Note():
    """Note Class"""
    def __init__(self):
        self.sess = next(get_db())

    def get_note_by_id(self, note_id: int):
        """Fetches a note by its id."""
        try:
            note = self.sess.query(NoteDb).filter(NoteDb.id == note_id).first()
            if note:
                return note
            return f"Note (id = {note_id}) not found"
        except Exception as e:
            raise SQLAlchemyError(
                f"An error occurred while fetching note by id: {e}"
            ) from e

    def get_notes_by_user_id(self, user_id: int):
        """Fetches all notes by user id."""
        try:
            user_exists = self.sess.query(UserDb).filter(UserDb.id == user_id).first()
            if not user_exists:
                return f"User with id {user_id} does not exist."

            notes = self.sess.query(NoteDb).filter(NoteDb.user_id == user_id).all()
            if notes:
                return notes

            return f"No notes found for user (id = {user_id})"
        except Exception as e:
            raise SQLAlchemyError(
                f"An error occurred while fetching notes by user id: {e}"
            ) from e

    def get_all_notes(self, skip: Optional[int] = None, limit: Optional[int] = None):
        """Fetches all notes from the database."""
        try:
            notes = self.sess.query(NoteDb)

            if skip is not None and limit is not None:
                notes = notes.offset(skip).limit(limit)
            elif skip is None and limit:
                notes = notes.offset(0).limit(limit)
            elif skip and limit is None:
                notes = notes.offset(skip).limit(10)

            notes = notes.all()

            if not notes:
                return "No notes found"

            if isinstance(notes, list) and len(notes) == 1:
                return notes[0]
            return notes
        except Exception as e:
            raise SQLAlchemyError(
                f"An error occurred while fetching note by id: {e}"
            ) from e

    def search_notes(
        self, field: str, query: str,
        skip: Optional[int] = None, limit: Optional[int] = None
    ):
        """Search notes based on field and query."""
        try:
            notes = None
            q = query.lower()

            notes = self.sess.query(NoteDb).filter(
                getattr(NoteDb, field).like(f'%{q}%')
            )

            if not notes:
                return "No notes found"

            if skip is not None and limit is not None:
                notes = notes.offset(skip).limit(limit).all()
            elif skip is not None:
                notes = notes.offset(skip).limit(10).all()
            elif limit is not None:
                notes = notes.limit(limit).all()
            else:
                notes = notes.all()

            if not notes:
                return f"No notes found '{query}' for the search query."

            if isinstance(notes, list) and len(notes) == 1:
                return notes[0]
            return notes
        except Exception as e:
            raise SQLAlchemyError(
                f"An error occurred while searching notes: {e}"
            ) from e

    def create_a_new_note(self, item: CreateNote, session: SessionRequest) -> NoteDetails:
        """Creates a new note with the given content and title."""
        try:
            if item.user_id == 0 or not item.user_id:
                item.user_id = session.user_id

            new_note = NoteDb(**item.model_dump())

            self.sess.add(new_note)
            self.sess.commit()
            self.sess.refresh(new_note)

            return new_note
        except Exception as e:
            raise SQLAlchemyError(f"An error occurred while creating a new note: {e}") from e

    def update_note_data(self, note_id: NoteId, note_data: UpdateNote) -> NoteDetails:
        """Updates the note data in the database."""
        try:
            old_note = self.sess.query(NoteDb).filter(
                NoteDb.id == note_id
            ).first()

            if old_note is None:
                raise ValueError(f"No note found with id {note_id}")

            for key, value in note_data.model_dump(exclude_unset=True).items():
                setattr(old_note, key, value)

            self.sess.commit()
            self.sess.refresh(old_note)

            return old_note
        except Exception as e:
            raise SQLAlchemyError(f"An error occurred while updating note data: {e}") from e

    def delete_note_by_id(self, note_id: NoteId):
        """Deletes a note by its ID."""
        try:
            note = self.sess.query(NoteDb).filter(NoteDb.id == note_id).first()

            if note is None:
                raise ValueError(f"No note found with id {note_id}")

            self.sess.delete(note)
            self.sess.commit()
        except ValueError as ve:
            raise ve
        except Exception as e:
            self.sess.rollback()
            raise SQLAlchemyError(f"An error occurred while deleting note by ID: {e}") from e

    @classmethod
    def convert_class_note_to_object(cls, note: NoteDb) -> dict:
        """Converts a Note_db object to a Note dict"""
        return {
            "id": note.id,
            "user_id": note.user_id,
            "title": note.title,
            "content": note.content,
            "time_created": note.time_created,
            "time_edition": note.time_edition,
        }
