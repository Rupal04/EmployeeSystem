# -*- coding: utf-8 -*-

import logging
from datetime import datetime


from rest_framework import viewsets, status
from employee_system.constants import Error, Warn, Roles, Success
from rest_framework.response import Response
from employee_system.response import ServerErrorResponse, SuccessResponse, ErrorResponse
from employee_system.utility import to_dict, get_employee_data
from employee_system.models import Employee, LeaveRequest


logger = logging.getLogger(__name__)


class EmployeeViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            data = request.data
            created_by = request.query_params.get('id',None)
            if created_by is not None and Employee.objects.filter(id=created_by).exists():
                emp_obj= Employee.objects.get(id=created_by)

                if emp_obj.role_id == Roles.ADMIN or emp_obj.role_id == Roles.MANAGER:

                    fname = data.get("fname", "")
                    lname = data.get("lname", "")
                    email = data.get("email", "")
                    role_id = int(data.get("role_id"))
                    manager_id = None
                    if emp_obj.role_id == Roles.MANAGER:
                        manager_id = emp_obj.id

                    create_emp_resp = Employee.objects.create(fname=fname, lname=lname, email=email,
                                                              role_id=role_id, manager_id=manager_id)

                    response = SuccessResponse(msg=Success.EMPLOYEE_CREATE_SUCCESS, results=create_emp_resp)
                    return Response(to_dict(response), status=status.HTTP_201_CREATED)
                else:
                    response = ErrorResponse(msg=Error.EMPLOYEE_CREATION_UNAUTHORIZED)
                    return Response(to_dict(response), status=status.HTTP_401_UNAUTHORIZED)
            else:
                response = ErrorResponse(msg=Error.EMPLOYEE_NOT_EXIST)
                return Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(Error.EXCEPTION + str(e))
            response = ServerErrorResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self,request, pk=None):
        try:
            if not pk:
                logger.warning(Warn.EMPLOYEE_ID_REQUIRED)
                response = SuccessResponse(msg=Error.EMPLOYEE_ID_MISSING)
                return Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)

            emp_id = pk
            deleted_by = request.query_params.get('id', None)

            if deleted_by and Employee.objects.filter(id=deleted_by).exists() and\
                    Employee.objects.filter(id=emp_id).exists():

                emp_obj = Employee.objects.get(id=deleted_by)
                emp_delete_obj = Employee.objects.get(id=emp_id)

                if emp_obj.role_id == Roles.ADMIN or \
                    (emp_obj.role_id == Roles.MANAGER
                     and emp_delete_obj.role_id == Roles.EXECUTIVE
                     and emp_delete_obj.manager_id == emp_obj.id):

                    emp_delete_obj.delete()
                    response = SuccessResponse(msg=Success.EMPLOYEE_DELETE_SUCCESS)
                    return Response(to_dict(response), status=status.HTTP_200_OK)
                else:

                    response = ErrorResponse(msg=Error.EMPLOYEE_DELETION_UNAUTHORIZED)
                    return Response(to_dict(response), status=status.HTTP_401_UNAUTHORIZED)
            else:

                response = ErrorResponse(msg=Error.EMPLOYEE_NOT_EXIST)
                return Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(Error.EXCEPTION + str(e))
            response = ServerErrorResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            if not pk:
                logger.warning(Warn.EMPLOYEE_ID_REQUIRED)
                response = SuccessResponse(msg=Error.EMPLOYEE_ID_MISSING)
                return Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)

            emp_id = pk
            employee_response = get_employee_data(emp_id)

            if employee_response is not None:

                response = SuccessResponse(msg=Success.EMPLOYEE_FETCHED_SUCCESS, results=employee_response)
                return Response(to_dict(response), status=status.HTTP_200_OK)
            else:

                response = ErrorResponse(msg=Error.EMPLOYEE_FETCHING_ERROR)
                return Response(to_dict(response), status=status.HTTP_501_NOT_IMPLEMENTED)

        except Exception as e:
            logger.error(Error.EXCEPTION + str(e))
            response = ServerErrorResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LeaveViewSet(viewsets.ViewSet):
    def create(self,request):
        try:
            data=request.data
            created_by = request.query_params.get('id', None)

            if created_by and Employee.objects.filter(id=created_by).exists():

                emp_obj = Employee.objects.get(id=created_by)
                if emp_obj.role_id == Roles.EXECUTIVE:

                    leave_reason = data.get('reason', None)
                    date = datetime.strptime(data.get('date'), '%Y-%m-%d')

                    leave_obj_resp = LeaveRequest.objects.create(requested_by_id=created_by,
                                                                 leave_reason=leave_reason, date=date)

                    response = SuccessResponse(msg=Success.LEAVE_REQUEST_CREATED, results=leave_obj_resp)
                    return Response(to_dict(response), status=status.HTTP_201_CREATED)
                else:

                    response = ErrorResponse(msg=Error.LEAVE_REQUEST_CREATION_UNAUTHORIZED)
                    return Response(to_dict(response), status=status.HTTP_401_UNAUTHORIZED)
            else:

                response = ErrorResponse(msg=Error.EMPLOYEE_NOT_EXIST)
                return Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(Error.EXCEPTION + str(e))
            response = ServerErrorResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

