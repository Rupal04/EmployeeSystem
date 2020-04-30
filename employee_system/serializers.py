from rest_framework.serializers import ModelSerializer
from employee_system.models import LeaveRequest, Employee


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class LeaveRequestSerializer(ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['id','requested_by', 'leave_reason', 'date']
