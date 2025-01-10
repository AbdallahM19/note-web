"""notes.py"""

from typing import Union, Optional
from datetime import datetime
# from sqlalchemy import and_, or_
from pydantic import BaseModel, Field
from sqlalchemy.exc import SQLAlchemyError
from api.database import NoteDb, get_session



class BaseNote(BaseModel):
    """Class to handle Note data operations"""
    user_id: Optional[int] = None
    title: Optional[str] = None
    content: str
    time_created: Optional[datetime] = Field(default_factory=datetime.utcnow)
    time_edition: Optional[datetime] = Field(default_factory=datetime.utcnow)


class NoteDetails(BaseNote):
    """Class note with additional fields [id]"""
    id: int


class Note():
    """Note Class"""
    def __init__(self):
        self.sess = get_session()

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
        finally:
            self.sess.close()

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
        finally:
            self.sess.close()

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
        finally:
            self.sess.close()

    def create_a_new_note(self, item: BaseNote) -> NoteDetails:
        """Creates a new note with the given content and title."""
        try:
            new_note = NoteDb(
                user_id=item.user_id,
                content=item.content,
                title=item.title,
                time_created=item.time_created,
                time_edition=item.time_edition,
            )

            self.sess.add(new_note)
            self.sess.commit()
            
            self.sess.refresh(new_note)

            return new_note
        except Exception as e:
            raise SQLAlchemyError(f"An error occurred while creating a new note: {e}") from e
        finally:
            self.sess.close()

    def update_note_data(
        self,
        note_id: int,
        content: str,
        time_edition: datetime,
        title: Union[str, None] = None,
    ) -> NoteDetails:
        """Updates the note data in the database."""
        try:
            old_note = self.sess.query(NoteDb).filter(
                NoteDb.id == note_id
            ).first()

            if old_note is None:
                raise ValueError(f"No note found with id {note_id}")

            old_note.content = content
            old_note.title = title
            old_note.time_edition = time_edition

            self.sess.commit()
            self.sess.refresh(old_note)

            return old_note
        except Exception as e:
            raise SQLAlchemyError(f"An error occurred while updating note data: {e}") from e
        finally:
            self.sess.close()

    def delete_note_by_id(self, note_id: int):
        """Deletes a note by its ID."""
        try:
            self.sess.query(NoteDb).filter(
                NoteDb.id == note_id
            ).delete()
            self.sess.commit()
        except Exception as e:
            self.sess.rollback()
            raise SQLAlchemyError(f"An error occurred while deleting note by ID: {e}") from e
        finally:
            self.sess.close()

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
