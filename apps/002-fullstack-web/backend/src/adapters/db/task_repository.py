from sqlmodel import SQLModel, Field, Session, select
from typing import Optional, List
from src.domain.entities.priority import Priority
from src.domain.entities.task_status import TaskStatus
from src.domain.entities.task import Task as DomainTask
from datetime import datetime, UTC
from src.domain.ports.storage_port import StoragePort
import uuid

class TaskTable(SQLModel, table=True):
    __tablename__ = "tasks"

    id: str = Field(primary_key=True)
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    tags: str # Stored as comma-separated values for simplicity in this baseline
    created_at: datetime
    updated_at: datetime

    def to_domain(self) -> DomainTask:
        return DomainTask(
            id=self.id,
            title=self.title,
            description=self.description,
            status=TaskStatus(self.status),
            priority=Priority(self.priority),
            tags=self.tags.split(",") if self.tags else [],
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_domain(task: DomainTask) -> "TaskTable":
        return TaskTable(
            id=task.id or str(uuid.uuid4()),
            title=task.title,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
            tags=",".join(task.tags),
            created_at=task.created_at,
            updated_at=task.updated_at
        )

class SQLModelTaskRepository(StoragePort):
    def __init__(self, session: Session):
        self.session = session

    def save(self, task: DomainTask) -> DomainTask:
        db_task = TaskTable.from_domain(task)
        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return db_task.to_domain()

    def get(self, task_id: str) -> Optional[DomainTask]:
        db_task = self.session.get(TaskTable, task_id)
        return db_task.to_domain() if db_task else None

    def get_all(self) -> List[DomainTask]:
        statement = select(TaskTable)
        results = self.session.exec(statement)
        return [db_task.to_domain() for db_task in results]

    def update(self, task_id: str, task: DomainTask) -> DomainTask:
        db_task = self.session.get(TaskTable, task_id)
        if not db_task:
            raise ValueError(f"Task with ID {task_id} not found")

        db_task.title = task.title
        db_task.description = task.description
        db_task.status = task.status.value
        db_task.priority = task.priority.value
        db_task.tags = ",".join(task.tags)
        db_task.updated_at = datetime.now(UTC)

        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return db_task.to_domain()

    def delete(self, task_id: str) -> None:
        db_task = self.session.get(TaskTable, task_id)
        if not db_task:
            raise ValueError(f"Task with ID {task_id} not found")
        self.session.delete(db_task)
        self.session.commit()

    def exists(self, task_id: str) -> bool:
        db_task = self.session.get(TaskTable, task_id)
        return db_task is not None
