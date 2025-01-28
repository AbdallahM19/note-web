"""note_api.py"""

from typing import Union, Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from api.app import note_model
from api.models.notes import NoteField, NoteDetails
# from api.utils.session import SessionManager, get_session_manager

router = APIRouter(
    prefix='/api/notes',
    tags=['note-api']
)


@router.get("/{field}")
async def get_notes_by_field(
    field: NoteField,
    query: Optional[str] = None,
    note_id: Optional[int] = None,
    user_id: Optional[int] = None,
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
            case 'user_id' if user_id:
                notes_data = note_model.get_notes_by_user_id(
                    user_id=user_id
                )
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
    note_data: Annotated[
        NoteDetails,
        Depends(note_model.create_a_new_note)
    ],
) -> dict:
    """Create a new note."""
    try:
        return note_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) from e


@router.put("/{note_id}/update", response_model=NoteDetails)
async def update_note(
    note_data: Annotated[
        NoteDetails, Depends(note_model.update_note_data)
    ]
):
    """Update a note."""
    try:
        return note_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) from e


@router.delete("/{note_id}/delete")
async def delete_note_data_permanently(
    note_id: Annotated[
        int, Depends(note_model.delete_note_by_id)
    ]
) -> dict:
    """Delete note data permanently."""
    try:
        return {
            "message": f"Note with id {note_id} has been deleted permanently."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) from e
