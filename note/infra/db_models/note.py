from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Table, Text
from sqlalchemy.orm import relationship

from database import Base

"""노트와 태그 테이블은 다대다 관계 """

note_tag_association = Table(  # 다대다 관계를 나타내기 위한 연결 테이블
    "Note_Tag",
    Base.metadata,
    Column("note_id", String(36), ForeignKey("Note.id")),
    Column("tag_id", String(36), ForeignKey("Tag.id")),
)


class Note(Base):
    __tablename__ = "Note"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    title = Column(String(64), nullable=False)
    content = Column(Text, nullable=False)
    memo_date = Column(String(8), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )
    # relationship 함수를 이용해 다대다 관계를 맺는다.
    # back_populates 옵션을 이용해 노트 객체를 가져올 때 연관된 태그 객체도 모두 가져온다.
    tags = relationship("Tag", secondary=note_tag_association, back_populates="notes")


class Tag(Base):
    __tablename__ = "Tag"

    id = Column(String(36), primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )
    notes = relationship("Note", secondary=note_tag_association, back_populates="tags")
