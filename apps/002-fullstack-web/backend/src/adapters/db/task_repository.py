from sqlmodel import SQLModel, Field, Session, select
from sqlalchemy import ForeignKey
from typing import Optional
from typing import Optional, List
from src.domain.entities.priority import Priority
from src.domain.entities.task_status import TaskStatus
from src.domain.entities.task import Task as DomainTask
from datetime import datetime, UTC
from src.domain.ports.storage_port import StoragePort
import uuid
from sqlalchemy import case

class TaskTable(SQLModel, table=True):
    __tablename__ = "tasks"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    tags: str # Stored as comma-separated values for simplicity in this baseline
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    user_id: str = Field(sa_column_kwargs={"nullable": False})  # Foreign key to users table

    def to_domain(self) -> DomainTask:
        return DomainTask(
            id=self.id,
            title=self.title,
            description=self.description,
            status=TaskStatus(self.status),  # Use as-is (lowercase)
            priority=Priority(self.priority),  # Use as-is (lowercase)
            tags=self.tags.split(",") if self.tags else [],
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_domain(task: DomainTask, user_id: str) -> "TaskTable":
        return TaskTable(
            id=task.id or str(uuid.uuid4()),
            title=task.title,
            description=task.description,
            status=task.status.value.lower(),  # Store as lowercase
            priority=task.priority.value.lower(),  # Store as lowercase
            tags=",".join(task.tags),
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_id=user_id
        )

class SQLModelTaskRepository(StoragePort):
    def __init__(self, session: Session):
        self.session = session

    def save(self, task: DomainTask) -> DomainTask:
        # This method should not be used directly for user-specific tasks
        # Use save_for_user instead for authenticated tasks
        raise NotImplementedError("Use save_for_user for authenticated tasks")

    def save_for_user(self, task: DomainTask, user_id: str) -> DomainTask:
        """Save a task for a specific user."""
        db_task = TaskTable.from_domain(task, user_id)
        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return db_task.to_domain()

    def get_all_for_user(self, user_id: str) -> list[DomainTask]:
        """Get all tasks for a specific user."""
        statement = select(TaskTable).where(TaskTable.user_id == user_id)
        results = self.session.exec(statement)
        return [db_task.to_domain() for db_task in results]

    def get(self, task_id: str) -> Optional[DomainTask]:
        db_task = self.session.get(TaskTable, task_id)
        return db_task.to_domain() if db_task else None

    def get_all(
        self,
        search: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        tag: Optional[str] = None,
        sort_by: Optional[str] = None,
    ) -> List[DomainTask]:
        """
        Retrieve all tasks with optional filtering and sorting.

        Args:
            search: Filter by keyword in title or description
            status: Filter by status (PENDING or COMPLETED)
            priority: Filter by priority (LOW, MEDIUM, or HIGH)
            tag: Filter by tag
            sort_by: Sort by field (created_at, updated_at, title, priority)

        Returns:
            List of filtered and sorted tasks
        """
        statement = select(TaskTable)

        # Apply filters
        if search:
            statement = statement.where(
                (TaskTable.title.contains(search))
                | (TaskTable.description.contains(search))
            )

        if status:
            statement = statement.where(TaskTable.status == status)

        if priority:
            statement = statement.where(TaskTable.priority == priority)

        if tag:
            statement = statement.where(TaskTable.tags.contains(tag))

        # Apply sorting
        if sort_by:
            if sort_by == "created_at":
                statement = statement.order_by(TaskTable.created_at)
            elif sort_by == "updated_at":
                statement = statement.order_by(TaskTable.updated_at)
            elif sort_by == "title":
                statement = statement.order_by(TaskTable.title)
            elif sort_by == "priority":
                # Priority sorting: HIGH -> MEDIUM -> LOW
                from sqlalchemy import case
                priority_order = case(
                    (TaskTable.priority == "HIGH", 1),
                    (TaskTable.priority == "MEDIUM", 2),
                    (TaskTable.priority == "LOW", 3),
                )
                statement = statement.order_by(priority_order)
            elif sort_by == "-priority":
                # Reverse priority sorting: LOW -> MEDIUM -> HIGH
                from sqlalchemy import case
                priority_order = case(
                    (TaskTable.priority == "LOW", 1),
                    (TaskTable.priority == "MEDIUM", 2),
                    (TaskTable.priority == "HIGH", 3),
                )
                statement = statement.order_by(priority_order)

        results = self.session.exec(statement)
        return [db_task.to_domain() for db_task in results]

    def update(self, task_id: str, task: DomainTask) -> DomainTask:
        # This method should not be used directly for user-specific tasks
        # Use update_for_user instead for authenticated tasks
        raise NotImplementedError("Use update_for_user for authenticated tasks")

    def update_for_user(self, task_id: str, task: DomainTask, user_id: str) -> DomainTask:
        """Update a task for a specific user."""
        db_task = self.session.get(TaskTable, task_id)
        if not db_task:
            raise ValueError(f"Task with ID {task_id} not found")

        # Check if the task belongs to the user
        if db_task.user_id != user_id:
            raise ValueError(f"Task with ID {task_id} does not belong to user {user_id}")

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
        # This method should not be used directly for user-specific tasks
        # Use delete_for_user instead for authenticated tasks
        raise NotImplementedError("Use delete_for_user for authenticated tasks")

    def delete_for_user(self, task_id: str, user_id: str) -> None:
        """Delete a task for a specific user."""
        db_task = self.session.get(TaskTable, task_id)
        if not db_task:
            raise ValueError(f"Task with ID {task_id} not found")

        # Check if the task belongs to the user
        if db_task.user_id != user_id:
            raise ValueError(f"Task with ID {task_id} does not belong to user {user_id}")

        self.session.delete(db_task)
        self.session.commit()

    def exists(self, task_id: str) -> bool:
        db_task = self.session.get(TaskTable, task_id)
        return db_task is not None

    def exists_for_user(self, task_id: str, user_id: str) -> bool:
        """Check if a task exists for a specific user."""
        db_task = self.session.get(TaskTable, task_id)
        if not db_task:
            return False
        return db_task.user_id == user_id
