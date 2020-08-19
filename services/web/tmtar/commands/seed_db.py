from ..users.service import UserService
from typing import List
from ..project.types import RoleType


def seed_db(user_emails: List[str]):
    for email in user_emails:
        UserService.get_or_new_by_email(email, role=RoleType[2])
    print("Successfully seeded root users", ' '.join(user_emails))
