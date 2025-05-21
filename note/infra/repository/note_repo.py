from http.client import HTTPException

from sqlalchemy.orm import joinedload  # 연관 테이블을 데이터를 함께 가져옴

from database import SessionLocal
from note.domain.note import Note as NoteVO
from note.domain.repository.note_repo import InterfaceNoteRepository
from note.infra.db_models.note import Note
from utils.db_utils import row_to_dict


class NoteRepository(InterfaceNoteRepository):
    def get_notes(self, user_id: str, page: int,
                  items_per_page: int) -> tuple[int, list[Note]]:
        with SessionLocal() as db:
            query = (
                db.query(Note)
                .options(joinedload(Note.tags))
                .filter(Note.user_id == user_id)
            )
        total_count = query.count()
        notes = (
            query.offset((page - 1) * items_per_page)
                 .limit(items_per_page).all()
        )

        note_vos = [NoteVO(**row_to_dict(note)) for note in notes]
        return total_count, note_vos

    def find_by_id(self, user_id: str, note: Note) -> Note:
        with SessionLocal() as db:
            note = (
                db.query(Note).options(joinedload(Note.tags))
                .filter(Note.user_id == user_id, Note.id == id)
                .first()
            )
            if not note:
                raise HTTPException(status_code=422)

        return NoteVO(**row_to_dict(note))

    def save(self, user_id: str, note: Note) -> Note:
        pass

    def update(self, user_id: str, note: Note) -> Note:
        pass

    def delete(self, user_id: str, id: str):
        pass

    def delete_tags(self, user_id: str, id: str):
        pass

    def get_notes_by_tag_name(self, user_id: str, tag_name: str,
                              page: int, items_per_page: int) -> tuple[int, list[Note]]:
        pass
