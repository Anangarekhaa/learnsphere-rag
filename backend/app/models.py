from sqlalchemy import Column, String, Text, ForeignKey, Float, Integer
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(String, ForeignKey("users.id"))  

    chunks = relationship("DocumentChunk", back_populates="document")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    chunk_text = Column(Text, nullable=False)
    embedding = Column(ARRAY(Float))

    # Relationship
    document = relationship("Document", back_populates="chunks")

class QuestionnaireRun(Base):
    __tablename__ = "questionnaire_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey("users.id"))
    filename = Column(String, nullable=False)

    user = relationship("User")
    answers = relationship("QuestionAnswer", back_populates="run")


class QuestionAnswer(Base):
    __tablename__ = "question_answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    run_id = Column(UUID(as_uuid=True), ForeignKey("questionnaire_runs.id"))
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    confidence = Column(String)
    citation = Column(String)

    run = relationship("QuestionnaireRun", back_populates="answers")