import os
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key
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
        logger.info(f"Finding task by ID: {task_id}")

        resp = self._table.query(
            IndexName="GSI1",
            KeyConditionExpression=Key("GSI1PK").eq(f"TASK#{task_id}")
            & Key("GSI1SK").eq(f"TASK#{task_id}"),
        )
        items = resp["Items"]

        if not items:
            return None

        return Task(
            id=TaskId(str(items[0]["task_id"])),
            task_list_id=TaskListId(str(items[0]["task_list_id"])),
            title=TaskTitle(str(items[0]["title"])),
            description=TaskDescription(str(items[0]["description"])),
            status=TaskStatus(str(items[0]["status"])),
            created_at=datetime.fromisoformat(str(items[0]["created_at"])),
        )

    def delete(self, task_id: TaskId) -> None:
        """Delete a task by its ID."""
        resp = self._table.query(
            IndexName="GSI1",
            KeyConditionExpression=Key("GSI1PK").eq(f"TASK#{task_id}"),
        )
        items = resp.get("Items", [])

        if not items:
            return

        self._table.delete_item(
            Key={
                "PK": items[0]["PK"],
                "SK": items[0]["SK"],
            }
        )

    def list_all(self, task_list_id: TaskListId) -> list[Task]:
        """List all tasks in the repository."""
        resp = self._table.query(
            KeyConditionExpression=Key("PK").eq(f"TASK_LIST#{task_list_id}")
            & Key("SK").begins_with("TASK#"),
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
