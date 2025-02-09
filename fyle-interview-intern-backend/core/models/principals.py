from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from core import db

class Principal(db.Model):
    __tablename__ = 'principals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Principal {self.id}>"

    @classmethod
    def get_by_id(cls, principal_id):
        return cls.query.filter_by(id=principal_id).first()


principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of teachers"""
    teachers = Teacher.get_all_teachers()
    teachers_dump = [{"id": t.id, "user_id": t.user_id, "created_at": t.created_at, "updated_at": t.updated_at} for t in teachers]

    return APIResponse.respond(data=teachers_dump)
