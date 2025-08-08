import os

import boto3
from loguru import logger

from ...domain.task_list import TaskCount, TaskList, TaskListId, TaskListName
from ...domain.task_list_repository import TaskListRepository
from ...domain.user import UserId


def get_dynamodb_task_list_repository() -> TaskListRepository:
    """Get the task list repository instance."""

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
    return DynamoDBTaskListRepository(table)


class DynamoDBTaskListRepository(TaskListRepository):
    def __init__(self, table):
        self._table = table

    def store(self, task_list: TaskList) -> None:
        """Save a task list to the repository."""

        self._table.put_item(
            Item={
                "PK": f"USER#{task_list.user_id}",
                "SK": f"TASK_LIST#{task_list.id}",
                "GSI1PK": f"TASK_LIST#{task_list.id}",
                "GSI1SK": f"TASK_LIST#{task_list.id}",
                "user_id": str(task_list.user_id),
                "task_list_id": str(task_list.id),
                "name": str(task_list.name),
                "count": int(task_list.count),
            }
        )

    def find_by_id(self, task_list_id: TaskListId) -> TaskList | None:
        """Find a task list by its ID."""
        resp = self._table.query(
            Key={
                "GSI1PK": f"TASK_LIST#{task_list_id}",
                "GSI1SK": f"TASK_LIST#{task_list_id}",
            }
        )
        items = resp["Items"]

        if not items:
            return None

        return TaskList(
            id=TaskListId(str(items[0]["id"])),
            user_id=UserId(str(items[0]["user_id"])),
            name=TaskListName(str(items[0]["name"])),
            count=TaskCount(int(items[0]["count"])),
        )

    def delete(self, task_list_id: TaskListId) -> None:
        """Delete a task list by its ID."""
        self._table.delete_item(
            Key={
                "GSI1PK": f"TASK_LIST#{task_list_id}",
                "GSI1SK": f"TASK_LIST#{task_list_id}",
            }
        )

    def list_all(self, user_id: UserId) -> list[TaskList]:
        """List all task lists in the repository."""
        resp = self._table.query(
            KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
            ExpressionAttributeValues={
                ":pk": f"USER#{user_id}",
                ":sk": "TASK_LIST#",
            },
        )
        items = resp["Items"]

        return [
            TaskList(
                id=TaskListId(str(item["task_list_id"])),
                user_id=UserId(str(item["user_id"])),
                name=TaskListName(str(item["name"])),
                count=TaskCount(int(item["count"])),
            )
            for item in items
        ]
