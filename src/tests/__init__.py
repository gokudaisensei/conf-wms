from app.api.deps import get_password_hash

ROLE_ENUM = {
    'SuperAdmin': 1,
    'Admin': 2,
    'Coordinator': 3,
    'Editor': 4,
    'AssociateEditor': 5,
    'Reviewer': 6,
    'Author': 7
}


def create_users(role: str, count: int) -> list[dict]:
    return [
        {
            'name': f'{role.capitalize()} {i}',
            'email': f'{role.lower()}{i}@example.com',
            'password': get_password_hash(f'password{i}'),
            'roleID': role
        } for i in range(1, count + 1)
    ]
