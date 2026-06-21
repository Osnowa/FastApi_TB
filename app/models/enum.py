from enum import Enum

class Status(str, Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"