import os
from datetime import datetime

import boto3

from ...domain.task import Task, TaskDescription, TaskId, TaskStatus, TaskTitle
from ...domain.task_list import TaskListId
from ...domain.task_repository import TaskRepository


def get_dynamodb_task_repository() -> TaskRepository:
    """Get the task repository instance."""
    return DynamoDBTaskRepository()


class DynamoDBTaskRepository(TaskRepository):
    def __init__(self):
        self._table_name = os.getenv("DYNAMODB_TABLE_NAME", "todo-dev-table")

        if os.getenv("APP_ENV", "local") == "local":
            self._dynamodb = boto3.resource(
                "dynamodb",
                region_name=os.getenv("AWS_REGION", "ap-northeast-1"),
                endpoint_url="http://localhost:9000/",
                aws_access_key_id="DUMMY",
                aws_secret_access_key="DUMMY",
            )
        else:
            self._dynamodb = boto3.resource(
                "dynamodb",
                region_name=os.getenv("AWS_REGION", "ap-northeast-1"),
            )
        self._table = self._dynamodb.Table(self._table_name)

    def store(self, task_list_id: TaskListId, task: Task) -> None:
        """Save a task to the repository."""
        self._table.put_item(
            Item={
                "PK": f"TASK_LIST#{task_list_id}",
                "SK": f"TASK#{task.id}",
                "id": str(task.id),
                "title": str(task.title),
                "description": str(task.description),
                "status": str(task.status),
                "created_at": task.created_at.isoformat(),
            }
        )

    def find_by_id(
        self,
        task_list_id: TaskListId,
        task_id: TaskId,
    ) -> Task | None:
        """Find a task by its ID."""

        resp = self._table.get_item(
            Key={
                "PK": f"TASK_LIST#{task_list_id}",
                "SK": f"TASK#{task_id}",
            }
        )
        item = resp.get("Item")
        if item is None:
            return None

        return Task(
            id=TaskId(str(item["id"])),
            title=TaskTitle(str(item["title"])),
            description=TaskDescription(str(item["description"])),
            status=TaskStatus(str(item["status"])),
            created_at=datetime.fromisoformat(str(item["created_at"])),
        )

    def delete(self, task_list_id: TaskListId, task_id: TaskId) -> None:
        """Delete a task by its ID."""
        self._table.delete_item(
            Key={
                "PK": f"TASK_LIST#{task_list_id}",
                "SK": f"TASK#{task_id}",
            }
        )

    def list_all(self, task_list_id: TaskListId) -> list[Task]:
        """List all tasks in the repository."""
        resp = self._table.query(
            KeyConditionExpression="PK = :pk",
            ExpressionAttributeValues={":pk": f"TASK_LIST#{task_list_id}"},
        )
        items = resp["Items"]

        return [
            Task(
                id=TaskId(str(item["id"])),
                title=TaskTitle(str(item["title"])),
                description=TaskDescription(str(item["description"])),
                status=TaskStatus(str(item["status"])),
                created_at=datetime.fromisoformat(str(item["created_at"])),
            )
            for item in items
            if str(item["SK"]).startswith("TASK#")
        ]
