class CacheNameSpace(object):
    EMPLOYEE_DATA = ["employee_data", 1800]


def get_employee_by_id(emp_id):
    return CacheNameSpace.EMPLOYEE_DATA[0]+ "-" + str(emp_id).replace(" ", "")