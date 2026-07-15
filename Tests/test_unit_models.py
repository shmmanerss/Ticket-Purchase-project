import ast
import os
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "tickets.db")


def test_userdb_declares_fields():
    path = os.path.join("ticket_complete_project", "event_ticketing", "models", "user.py")
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    user_class = next(
        node for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "UserDB")

    assigned_names = []
    for stmt in ast.walk(user_class):
        if isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name):
                    assigned_names.append(target.id)

    for field in ["id", "name", "email", "phone", "password_hash"]:
        assert field in assigned_names


