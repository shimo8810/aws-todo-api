import os

import boto3

from ...domain.task import TaskId
from ...domain.task_list import TaskList, TaskListId, TaskListName
from ...domain.task_list_repository import TaskListRepository


def get_dynamodb_task_list_repository() -> TaskListRepository:
    """Get the task list repository instance."""
    return DynamoDBTaskListRepository()


class DynamoDBTaskListRepository(TaskListRepository):
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

    def store(self, task_list: TaskList) -> None:
        """Save a task list to the repository."""

        with self._table.batch_writer() as batch:
            batch.put_item(
                Item={
                    "PK": f"TASK_LIST#{task_list.id}",
                    "SK": "attr",
                    "id": str(task_list.id),
                    "title": str(task_list.name),
                }
            )
            for task_id in task_list.tasks:
                batch.put_item(
                    Item={
                        "PK": f"TASK_LIST#{task_list.id}",
                        "SK": f"TASK#{task_id}",
                        "id": str(task_id),
                    }
                )

    def find_by_id(self, task_list_id: TaskListId) -> TaskList | None:
        """Find a task list by its ID."""
        resp = self._table.query(
            KeyConditionExpression="PK = :pk",
            ExpressionAttributeValues={":pk": f"TASK_LIST#{task_list_id}"},
        )
        items = resp["Items"]

        attr = next((i for i in items if i["SK"] == "attr"), None)

        if attr is None:
            return None

        return TaskList(
            id=TaskListId(str(attr["id"])),
            name=TaskListName(str(attr["title"])),
            tasks=[
                TaskId(str(i["id"]))
                for i in items
                if str(i["SK"]).startswith("TASK#")
            ],
        )

    def delete(self, task_list_id: TaskListId) -> None:
        """Delete a task list by its ID."""
        self._table.delete_item(
            Key={
                "PK": f"TASK_LIST#{task_list_id}",
                "SK": "attr",
            }
        )

    def list_all(self) -> list[TaskList]:
        """List all task lists in the repository."""
        resp = self._table.scan(
            FilterExpression="begins_with(PK, :pk)",
            ExpressionAttributeValues={":pk": "TASK_LIST#"},
        )
        items = resp["Items"]

        task_lists = {}

        for item in items:
            if item["SK"] == "attr":
                task_list_id = TaskListId(str(item["id"]))
                task_lists[task_list_id] = TaskList(
                    id=task_list_id,
                    name=TaskListName(str(item["title"])),
                    tasks=[],
                )
            elif str(item["SK"]).startswith("TASK#"):
                task_list_id = TaskListId(str(item["PK"]).split("#")[1])
                if task_list_id in task_lists:
                    task_lists[task_list_id].tasks.append(
                        TaskId(str(item["id"]))
                    )

        return list(task_lists.values())
