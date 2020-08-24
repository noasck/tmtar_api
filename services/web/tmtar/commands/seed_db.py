from ..users.service import UserService
from typing import List
from ..project.types import RoleType


def seed_db(user_emails: List[str]):
    for email in user_emails:
        res = 'new' if UserService.get_or_new_by_email(email, role=RoleType[2]) else 'old'
        print(f"Successfully seeded {res} root user", email)
