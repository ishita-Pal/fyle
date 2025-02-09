import json
from flask import request
from core.libs import assertions
from functools import wraps

class AuthPrincipal:
    def __init__(self, user_id, student_id=None, teacher_id=None, principal_id=None):
        self.user_id = user_id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.principal_id = principal_id

    def __repr__(self):
        return f"<AuthPrincipal(user_id={self.user_id}, student_id={self.student_id}, teacher_id={self.teacher_id}, principal_id={self.principal_id})>"


def accept_payload(func):
    """Decorator to extract JSON payload from request and pass it to the function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        incoming_payload = request.json
        if incoming_payload is None:
            return {"error": "Invalid JSON payload"}, 400

        return func(incoming_payload, *args, **kwargs)

    return wrapper


def authenticate_principal(func):
    """Decorator to authenticate principal, teacher, or student"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        p_str = request.headers.get('X-Principal')

        print(f"Debug: Raw X-Principal Header = {p_str}")

        if not p_str:
            return {"error": "principal not found"}, 403

        try:
            p_dict = json.loads(p_str)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in X-Principal header"}, 400

        p = AuthPrincipal(
            user_id=p_dict.get('user_id'),
            student_id=p_dict.get('student_id'),
            teacher_id=p_dict.get('teacher_id'),
            principal_id=p_dict.get('principal_id')
        )

        print(f"Debug: Parsed X-Principal = {p}")
        if request.path.startswith('/student'):
            if not p.student_id:
                return {"error": "requester should be a student"}, 403
        elif request.path.startswith('/teacher'):
            if not p.teacher_id:
                return {"error": "requester should be a teacher"}, 403
        elif request.path.startswith('/principal'):
            if not p.principal_id:
                return {"error": "requester should be a principal"}, 403
        else:
            return {"error": "No such API"}, 404

        return func(p, *args, **kwargs)

    return wrapper
