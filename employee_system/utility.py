import logging

from datetime import datetime
from employee_system.constants import Error,Roles, Success, Permissions
from django.core.cache import cache
from employee_system.models import Employee, LeaveRequest, Permission
from employee_system.keys import get_employee_by_id, CacheNameSpace
from employee_system.serializers import LeaveRequestSerializer, EmployeeSerializer
from employee_system.response import SuccessResponse, ErrorResponse


logger = logging.getLogger(__name__)


def to_dict(obj):
    """Represent instance of a class as dict.
        Arguments:
        obj -- any object
        Return:
        dict
        """

    def serialize(obj):
        """Recursively walk object's hierarchy."""
        if isinstance(obj, (bool, int, float)):
            return obj
        elif isinstance(obj, dict):
            obj = obj.copy()
            for key in obj:
                obj[key] = serialize(obj[key])
            return obj
        elif isinstance(obj, list):
            return [serialize(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(serialize([item for item in obj]))
        elif hasattr(obj, '__dict__'):
            return serialize(obj.__dict__)
        else:
            return repr(obj)

    return serialize(obj)


def create_employee(**kwargs):
    try:
        created_by = None
        data = None

        if 'created_by' in kwargs:
            created_by = kwargs.get('created_by')

        if 'data' in kwargs:
            data = kwargs.get('data')

        if created_by is not None and Employee.objects.filter(id=created_by).exists():
            emp_obj = Employee.objects.get(id=created_by)

            fname = data.get("fname", "")
            lname = data.get("lname", "")
            email = data.get("email", "")
            role_id = int(data.get("role_id"))
            manager_id = None

            if emp_obj.role_id == Roles.MANAGER:
                manager_id = emp_obj.id

            permission = Permission.objects.filter(role__id=emp_obj.role_id, id=Permissions.ADD).first()

            if permission and (emp_obj.role_id == Roles.ADMIN or
                               (emp_obj.role_id == Roles.MANAGER and role_id == Roles.EXECUTIVE)):

                create_emp_resp = Employee.objects.create(fname=fname, lname=lname, email=email,
                                                          role_id=role_id, manager_id=manager_id)
                emp_serialized_obj = EmployeeSerializer(create_emp_resp)

                return SuccessResponse(msg=Success.EMPLOYEE_CREATE_SUCCESS, results=emp_serialized_obj.data)

            else:
                return ErrorResponse(msg=Error.EMPLOYEE_CREATION_UNAUTHORIZED)
        else:
            return ErrorResponse(msg=Error.EMPLOYEE_NOT_EXIST)

    except Exception as e:
        logger.error(Error.EMPLOYEE_CREATION_ERROR + str(e))
        return None


def delete_employee(**kwargs):
    try:
        deleted_by = None
        emp_id = None
        if 'deleted_by' in kwargs:
            deleted_by = kwargs.get('deleted_by')

        if 'emp_id' in kwargs:
            emp_id = kwargs.get('emp_id')

        if deleted_by and Employee.objects.filter(id=deleted_by).exists() and \
                Employee.objects.filter(id=emp_id).exists():

            emp_obj = Employee.objects.get(id=deleted_by)
            permission = Permission.objects.filter(id=Permissions.REMOVE, role__id=emp_obj.role_id).first()

            emp_delete_obj = Employee.objects.get(id=emp_id)

            if permission and emp_obj.role_id == Roles.ADMIN or (emp_obj.role_id == Roles.MANAGER
                and emp_delete_obj.role_id == Roles.EXECUTIVE and emp_delete_obj.manager_id == emp_obj.id):

                emp_delete_obj.delete()
                return SuccessResponse(msg=Success.EMPLOYEE_DELETE_SUCCESS)

            else:
                return ErrorResponse(msg=Error.EMPLOYEE_DELETION_UNAUTHORIZED)

        else:
            return ErrorResponse(msg=Error.EMPLOYEE_NOT_EXIST)

    except Exception as e:
        logger.error(Error.EMPLOYEE_DELETION_ERROR + str(e))
        return None


def get_employee_data(emp_id):
    try:
        emp_serialized_obj=None
        emp_serialized_obj = cache.get(get_employee_by_id(str(emp_id)))

        if emp_serialized_obj:
            logger.info("Getting employee data from cache")
        else:
            logger.info("Getting employee data from database.")

            if Employee.objects.filter(id=emp_id).exists():

                emp_obj = Employee.objects.get(id=emp_id)
                permission = Permission.objects.filter(role__id=emp_obj.role_id, id=Permissions.VIEW).first()

                if permission:
                    emp_serialized_obj = EmployeeSerializer(emp_obj)
                    cache.set(get_employee_by_id(str(emp_id)), emp_serialized_obj, CacheNameSpace.EMPLOYEE_DATA[1])
                else:
                    return ErrorResponse(msg=Error.EMPLOYEE_VIEWING_UNAUTHORIZED)

        return SuccessResponse(msg=Success.EMPLOYEE_FETCHED_SUCCESS, results=emp_serialized_obj.data)

    except Exception as e:
        logger.error(Error.EMPLOYEE_FETCHING_ERROR + str(e), exc_info=True)
        return None


def create_leave_request(**kwargs):
    try:
        created_by = None
        data = None
        if 'created_by' in kwargs:
            created_by = kwargs.get('created_by')

        if 'data' in kwargs:
            data = kwargs.get('data')

        if created_by and Employee.objects.filter(id=created_by).exists():
            emp_obj = Employee.objects.get(id=created_by)
            if emp_obj.role_id != Roles.ADMIN:
                leave_reason = data.get('reason', None)
                date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()

                leave_obj_resp = LeaveRequest.objects.create(requested_by_id=created_by,
                                                             leave_reason=leave_reason, date=date)
                leave_serialized_obj = LeaveRequestSerializer(leave_obj_resp)

                return SuccessResponse(msg=Success.LEAVE_REQUEST_CREATED, results=leave_serialized_obj.data)
            else:
                return ErrorResponse(msg=Error.LEAVE_REQUEST_CREATION_UNAUTHORIZED)
        else:
            return ErrorResponse(msg=Error.EMPLOYEE_NOT_EXIST)

    except Exception as e:
        logger.error(Error.LEAVE_REQUEST_CREATION_ERROR + str(e))
        return None




