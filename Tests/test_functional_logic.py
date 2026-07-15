import os
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "tickets.db")
import ast

def test_ticketdb_declares_fields():
    path = os.path.join("ticket_complete_project", "event_ticketing", "models", "ticket.py")
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    ticket_class = next(
        node for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "TicketDB")

    assigned_names = []
    for stmt in ast.walk(ticket_class):
        if isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name):
                    assigned_names.append(target.id)

    for field in ["id", "event_id", "user_id", "price", "reserved_at"]:
        assert field in assigned_names


