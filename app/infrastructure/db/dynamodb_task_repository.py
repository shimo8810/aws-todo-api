import os
from datetime import datetime

import boto3
from loguru import logger

from ...domain.task import Task, TaskDescription, TaskId, TaskStatus, TaskTitle
from ...domain.task_list import TaskListId
from ...domain.task_repository import TaskRepository


def get_dynamodb_task_repository() -> TaskRepository:
    """Get the task repository instance."""

    table_name = os.getenv("DYNAMODB_TABLE_NAME", "todo-dev-table")
    logger.info(f"Using DynamoDB table: {table_name}")
    logger.info(
        f"Using AWS region: {os.getenv('AWS_REGION', 'ap-northeast-1')}"
    )
    logger.info(f"Using AWS endpoint: {os.getenv('APP_ENV', 'local')}")

    if os.getenv("APP_ENV", "local") == "local":
        dynamodb = boto3.resource(
            "dynamodb",
            region_name=os.getenv("AWS_REGION", "ap-northeast-1"),
            endpoint_url="http://localhost:9000/",
            aws_access_key_id="DUMMY",
            aws_secret_access_key="DUMMY",
        )
    else:
        dynamodb = boto3.resource(
            "dynamodb",
            region_name=os.getenv("AWS_REGION", "ap-northeast-1"),
        )
    table = dynamodb.Table(table_name)

    return DynamoDBTaskRepository(table)


class DynamoDBTaskRepository(TaskRepository):
    def __init__(self, table):
        self._table = table

    def store(self, task: Task) -> None:
        """Save a task to the repository."""
        self._table.put_item(
            Item={
                "PK": f"TASK_LIST#{task.task_list_id}",
                "SK": f"TASK#{task.id}",
                "GSI1PK": f"TASK#{task.id}",
                "GSI1SK": f"TASK#{task.id}",
                "task_list_id": str(task.task_list_id),
                "task_id": str(task.id),
                "title": str(task.title),
                "description": str(task.description),
                "status": str(task.status),
                "created_at": task.created_at.isoformat(),
            }
        )

    def find_by_id(
        self,
        task_id: TaskId,
    ) -> Task | None:
        """Find a task by its ID."""
        # use gsi1pk
        resp = self._table.get_item(
            Key={
                "GSI1PK": f"TASK#{task_id}",
                "GSI1SK": f"TASK#{task_id}",
            }
        )
        item = resp.get("Item")
        if item is None:
            return None

        return Task(
            id=TaskId(str(item["id"])),
            task_list_id=TaskListId(str(item["task_list_id"])),
            title=TaskTitle(str(item["title"])),
            description=TaskDescription(str(item["description"])),
            status=TaskStatus(str(item["status"])),
            created_at=datetime.fromisoformat(str(item["created_at"])),
        )

    def delete(self, task_id: TaskId) -> None:
        """Delete a task by its ID."""
        self._table.delete_item(
            Key={
                "GSI1PK": f"TASK#{task_id}",
                "GSI1SK": f"TASK#{task_id}",
            }
        )

    def list_all(self, task_list_id: TaskListId) -> list[Task]:
        """List all tasks in the repository."""
        resp = self._table.query(
            KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
            ExpressionAttributeValues={
                ":pk": f"TASK_LIST#{task_list_id}",
                ":sk": "TASK#",
            },
        )

        items = resp["Items"]

        return [
            Task(
                id=TaskId(str(item["task_id"])),
                task_list_id=TaskListId(str(item["task_list_id"])),
                title=TaskTitle(str(item["title"])),
                description=TaskDescription(str(item["description"])),
                status=TaskStatus(str(item["status"])),
                created_at=datetime.fromisoformat(str(item["created_at"])),
            )
            for item in items
        ]
