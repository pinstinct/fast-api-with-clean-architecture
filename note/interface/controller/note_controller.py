from dataclasses import asdict
from datetime import datetime
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from common.auth import CurrentUser, get_current_user
from containers import Container
from note.application.note_service import NoteService

router = APIRouter(prefix="/notes")


class NoteResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    memo_date: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime


class CreateNoteBody(BaseModel):
    title: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1)
    memo_date: str = Field(min_length=8, max_length=8)
    tags: list[str] | None = Field(default=None, min_length=1, max_length=32,)


@router.post("", status_code=201, response_model=NoteResponse)
@inject
def create_note(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        body: CreateNoteBody,
        note_service: NoteService = Depends(Provide[Container.note_service]),):
    note = note_service.create_note(
        user_id=current_user.id,
        title=body.title,
        content=body.content,
        memo_date=body.memo_date,
        tag_names=body.tags if body.tags else [],
    )

    response = asdict(note)  # dataclass는 asdict 함수를 이용해서 손쉽게 딕셔너리로 변환
    """태그의 데이터 타입이 우리가 정의한 도메인 모델과 불일치한다.
    이런 데이터 가공을 위해 매퍼(mapper)를 따로 구현하기도 한다. 여기서는 매퍼의 역할을 컨트롤러에서 직접 처리한다.
    """
    response.update({"tags": [tag.name for tag in note.tags]})

    return response


class GetNotesResponse(BaseModel):
    total_count: int
    page: int
    notes: list[NoteResponse]


@router.get("", response_model=GetNotesResponse)
@inject
def get_notes(page: int = 1, items_per_page: int = 10,
              current_user: CurrentUser = Depends(get_current_user),
              note_service: NoteService = Depends(Provide[Container.note_service]),):
    total_count, notes = note_service.get_notes(
        user_id=current_user.id,
        page=page,
        items_per_page=items_per_page,
    )

    res_notes = []
    for note in notes:
        note_dict = asdict(note)
        note_dict.update({"tags": [tag.name for tag in note.tags]})
        res_notes.append(note_dict)

    return {"total_count": total_count, "page": page, "notes": res_notes}


@router.get("/{id}", response_model=NoteResponse)
@inject
def get_note(id: str, current_user: Annotated[CurrentUser, Depends(get_current_user)],
             note_service: NoteService = Depends(Provide[Container.note_service]),):
    note = note_service.get_note(user_id=current_user.id, id=id)
    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})
    return response


class UpdateNoteBody(BaseModel):
    """null이 전달되면 업데이트 하지 않고 기존 데이터를 유지한다. """
    title: str | None = Field(default=None, min_length=1, max_length=64)
    content: str | None = Field(default=None, min_length=1)
    memo_date: str | None = Field(default=None, min_length=8, max_length=8)
    tags: list[str] | None = Field(default=None)


@router.post("/{id}", response_model=NoteResponse)
@inject
def update_note(
        id: str,
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        body: UpdateNoteBody,
        note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = note_service.update_note(
        user_id=current_user.id,
        id=id,
        title=body.title,
        content=body.content,
        memo_date=body.memo_date,
        tag_names=body.tags,
    )

    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})
    return response


@router.delete("/{id}", status_code=204)
@inject
def delete_note(
        id: str,
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note_service.delete_note(user_id=current_user.id, id=id)


@router.get("/tags/{tag_name}/notes", response_model=GetNotesResponse)
@inject
def get_notes_by_tags(
        tag_name: str,
        page: int = 1,
        items_per_page: int = 10,
        current_user: CurrentUser = Depends(get_current_user),
        note_service: NoteService = Depends(Provide[Container.note_service]),
):
    total_count, notes = note_service.get_notes_by_tag(
        user_id=current_user.id,
        tag_name=tag_name,
        page=page,
        items_per_page=items_per_page,
    )

    res_notes = []
    for note in notes:
        note_dict = asdict(note)
        note_dict.update({"tags": [tag.name for tag in note.tags]})
        res_notes.append(note_dict)

    return {
        "total_count": total_count,
        "page": page,
        "notes": res_notes
    }
