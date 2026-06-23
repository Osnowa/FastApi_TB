from enum import Enum, StrEnum

class Status(StrEnum):
    new = "new"
    in_progress = "in_progress"
    done = "done"

class Priority(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"

class SortOrderId(StrEnum):
    id_asc = "id_asc"
    id_desc = "id_desc"