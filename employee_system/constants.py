class Success(object):
    SUCCESS_RESPONSE = "Successful"

    EMPLOYEE_FETCHED_SUCCESS = "Employee fetched successfully."
    EMPLOYEE_CREATE_SUCCESS = "Employee added successfully."
    EMPLOYEE_DELETE_SUCCESS = "Employee removed successfully."

    LEAVE_REQUEST_CREATED = "Leave Request added successfully."


class Error(object):
    ERROR_RESPONSE = "Error"
    SERVER_ERROR_5XX = "SERVER ERROR"
    EXCEPTION = "Some Unexpected Exception Occured. Error is "

    EMPLOYEE_ID_MISSING="Employee ID is missing"
    EMPLOYEE_CREATION_UNAUTHORIZED = "You are an executive and thus not authorized to add this employee."
    EMPLOYEE_DELETION_UNAUTHORIZED = "You are not authorized to remove this employee."
    EMPLOYEE_FETCH_ERROR = "Erro in fetching Employee"

    LEAVE_REQUEST_CREATION_UNAUTHORIZED = "You are not authorized to create this leave request."

    EMPLOYEE_NOT_EXIST = "Employee does not exist."

    EMPLOYEE_FETCHING_ERROR = "Error in fetching employee"

class Warn(object):
    EMPLOYEE_ID_REQUIRED = "Employee ID required "


class Roles(object):
    ADMIN = 1
    MANAGER = 2
    EXECUTIVE =3