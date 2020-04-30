import logging

from employee_system.constants import Error
from django.core.cache import cache
from employee_system.models import Employee
from employee_system.keys import get_employee_by_id, CacheNameSpace

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


def get_employee_data(emp_id):
    try:
        emp_obj=None
        emp_obj = cache.get(get_employee_by_id(str(emp_id)))
        if emp_obj:
            logger.info("Getting employee data from cache")
        else:
            logger.info("Getting employee data from database.")
            if Employee.objects.filter(id=emp_id).exists():
                emp_obj = Employee.objects.get(id=emp_id)
                cache.set(get_employee_by_id(str(emp_id)), emp_obj,
                          CacheNameSpace.EMPLOYEE_DATA[1])
        return emp_obj

    except Exception as e:
        logger.error(Error.EMPLOYEE_FETCHING_ERROR + str(e), exc_info=True)
        return None

