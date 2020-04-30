# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Permission(models.Model):
    class Meta(object):
        db_table = 'permission'

    pname = models.CharField(max_length=400, blank=False, unique=True)


class Role(models.Model):
    class Meta(object):
        db_table = 'role'

    role_name = models.CharField(max_length=200, blank=False, unique=True)
    permission = models.ManyToManyField(Permission,blank=True, null=True)


class Employee(models.Model):
    class Meta(object):
        db_table = 'employee'

    fname = models.CharField(max_length=100, blank=False)
    lname = models.CharField(max_length=100, blank=False)
    email = models.CharField(max_length=200, blank=True, unique=True)
    role = models.ForeignKey(Role, blank=True, on_delete=models.CASCADE)
    manager = models.ForeignKey('self', blank=True, null=True, related_name='employee', on_delete=models.CASCADE)


class LeaveRequest(models.Model):
    class Meta(object):
        db_table = 'leave_request'

    requested_by = models.ForeignKey(Employee, blank=False, null=False,on_delete=models.CASCADE)
    leave_reason = models.TextField()
    date = models.DateField(null=False)




