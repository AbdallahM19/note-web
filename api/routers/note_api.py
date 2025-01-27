"""note_api.py"""

from typing import Union, Optional, Annotated
from fastapi import APIRouter, Path, Depends, HTTPException, status
from api.app import note_model
from api.models.notes import NoteField, CreateNote, UpdateNote, NoteDetails
from api.utils.session import SessionManager, get_session_manager

router = APIRouter(
    prefix='/api/notes',
    tags=['note-api']
)


@router.get("/{field}")
async def get_notes_by_field(
    field: NoteField,
    query: Optional[str] = None,
    note_id: Optional[int] = None,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
) -> Union[dict, NoteDetails, list[NoteDetails]]:
    """Get notes by field"""
    try:
        notes_data = None

        match field:
            case 'id' if note_id:
                notes_data = note_model.get_note_by_id(note_id)
            case 'list':
                notes_data = note_model.get_all_notes(skip=skip, limit=limit)
            case 'title' | 'content' if query:
                notes_data = note_model.search_notes(
                    field=field, query=query, skip=skip, limit=limit
                )
            case 'title' | 'content' if query is None:
                notes_data = f"Invalid query for field: {field}."
            case _:
                notes_data = f"Invalid field: {field}. Must be 'title', 'content', 'list' or 'id'."

        if isinstance(notes_data, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=notes_data
            )

        return notes_data
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) from e


@router.post("/create", response_model=NoteDetails, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: CreateNote, session: SessionManager = Depends(get_session_manager)
) -> dict:
    """Create a new note."""
    try:
        if note_data.user_id == 0 or not note_data.user_id:
            note_data.user_id = session.user_id

        new_note = note_model.create_a_new_note(note_data)

        return new_note
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) from e


@router.put("/{note_id}/update", response_model=NoteDetails)
async def update_note(
    note_id: Annotated[
        int, Path(
            title="The ID of the note to be updated",
            description="The ID of the note to be updated",
            gt=0
        )
    ],
    note_data: UpdateNote
):
    """Update a note."""
    try:
        updated_note = note_model.update_note_data(note_id, note_data)
        return updated_note
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) from e


@router.delete("/{note_id}/delete")
async def delete_note_data_permanently(
    note_id: Annotated[
        int, Path(
            title="The ID of the note to be deleted",
            description="The ID of the note to be deleted",
            gt=0
        )
    ]
) -> dict:
    """Delete note data permanently."""
    try:
        note_model.delete_note_by_id(note_id)
        return {
            "message": f"Note with id {note_id} has been deleted permanently."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) from e
