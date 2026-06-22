from enum import Enum

class Status(str, Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class SortOrderId(str, Enum):
    ID_ASC = "id_asc"
    ID_DESC = "id_desc"