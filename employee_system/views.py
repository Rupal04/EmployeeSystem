# -*- coding: utf-8 -*-
import logging

from rest_framework import viewsets, status
from employee_system.constants import Error, Warn
from rest_framework.response import Response
from employee_system.response import ServerErrorResponse, SuccessResponse, ErrorResponse
from employee_system.utility import to_dict, get_employee_data, create_leave_request, create_employee, delete_employee

logger = logging.getLogger(__name__)


class EmployeeViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            data = request.data
            created_by = request.query_params.get('id', None)

            response = create_employee(**{"data": data, "created_by": created_by})

            if not response:
                response = ErrorResponse(msg=Error.EMPLOYEE_CREATION_ERROR)
                return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if response and response.success is False:
                return Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)

            return Response(to_dict(response), status=status.HTTP_201_CREATED)

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

            response = delete_employee(**{"deleted_by": deleted_by, "emp_id": emp_id})

            if not response:
                response = ErrorResponse(msg=Error.EMPLOYEE_DELETION_ERROR)
                return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if response and response.success is False:
                return Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)

            return Response(to_dict(response), status=status.HTTP_201_CREATED)

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
            response = get_employee_data(emp_id)

            if not response:
                response = ErrorResponse(msg=Error.EMPLOYEE_FETCHING_ERROR)
                return Response(to_dict(response), status=status.HTTP_501_NOT_IMPLEMENTED)

            return Response(to_dict(response), status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(Error.EXCEPTION + str(e))
            response = ServerErrorResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LeaveViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            data = request.data
            created_by = request.query_params.get('id', None)

            response = create_leave_request(**{"created_by": created_by, "data": data})

            if not response:
                response = ErrorResponse(msg=Error.LEAVE_REQUEST_CREATION_ERROR)
                return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if response and response.success is False:
                return Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)

            return Response(to_dict(response), status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(Error.EXCEPTION + str(e))
            response = ServerErrorResponse()
            return Response(to_dict(response), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
