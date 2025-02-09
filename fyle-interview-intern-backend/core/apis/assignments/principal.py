from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.libs import assertions 

from .schema import AssignmentSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """
    Returns a list of assignments submitted or graded
    """
    principals_assignments = Assignment.get_assignments_by_principal()
    principals_assignments_dump = AssignmentSchema().dump(principals_assignments, many=True)
    return APIResponse.respond(data=principals_assignments_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    assertions.assert_found(assignment, "Assignment not found")
    if assignment.state == AssignmentStateEnum.DRAFT:
       if assignment.state == AssignmentStateEnum.DRAFT:
        return APIResponse.respond(data={"error": "Cannot grade an assignment in DRAFT state"}), 400  
    assertions.assert_valid(
        assignment.state in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED],
        "Only submitted or graded assignments can be graded"
    )

    assignment.grade = grade_assignment_payload.grade
    assignment.state = AssignmentStateEnum.GRADED
    db.session.commit()

    assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=assignment_dump)


@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of teachers"""
    principal = Principal.get_by_id(p["principal_id"])
    if not principal:
        return APIResponse.respond(message="Principal not found", status=403)

    teachers = Teacher.get_all_teachers()
    teachers_dump = [{"id": t.id, "user_id": t.user_id, "created_at": t.created_at, "updated_at": t.updated_at} for t in teachers]

    return APIResponse.respond(data=teachers_dump)
