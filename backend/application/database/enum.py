from enum import Enum


class ActJob(Enum):
    pending = 'В ожидании'
    start = 'В работе'
    finish = 'Выполнено'


class LevelProblem(Enum):
    minimal = 'Не важно'
    normal = "Второстепенная"
    hard = 'Важно'


class UserPermission(Enum):
    admin_user = 'Председатель'
    default_user = 'Жилец'
    job_user = 'Работник'
