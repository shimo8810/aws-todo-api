from dataclasses import dataclass


@dataclass(frozen=True)
class UserId:
    value: str

    def __str__(self) -> str:
        return self.value


@dataclass
class User:
    id: UserId
