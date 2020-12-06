from ..users.service import UserService
from typing import List
from ..project.types import RoleType


def seed_db(user_emails: List[str]):
    res = [('new', email) if UserService.get_or_new_by_email(email, role=RoleType[2]) else ('old', email)
           for email in user_emails]
    return res
