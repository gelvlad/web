from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from webproject import models


def check_course_author(func):
    def inner(self, *args, **kwargs):
        course = get_object_or_404(models.Course, id=self.kwargs['course_pk'])
        if not course.author == self.request.user:
            raise PermissionDenied
        return func(self, *args, **kwargs)
    return inner


def check_test_author(func):
    def inner(self, *args, **kwargs):
        test = get_object_or_404(models.Test, id=self.kwargs['test_pk'])
        if not test.course.id == self.kwargs['course_pk']:
            raise PermissionDenied
        if not test.course.author == self.request.user:
            raise PermissionDenied
        return func(self, *args, **kwargs)
    return inner


def check_course_kwarg(func):
    def inner(self, *args, **kwargs):
        test = get_object_or_404(models.Test, id=self.kwargs['test_pk'])
        if not test.course.id == self.kwargs['course_pk']:
            raise PermissionDenied
        return func(self, *args, **kwargs)
    return inner


def check_taken_by_user(func):
    def inner(self, *args, **kwargs):
        if not self.object:
            self.object = self.get_object()
        if not self.object.taken_by == self.request.user:
            raise PermissionDenied
        return func(self, *args, **kwargs)
    return inner


def check_result_is_active(func):
    def inner(self, *args, **kwargs):
        if not self.object:
            self.object = self.get_object()
        if not self.object.isActive:
            raise PermissionDenied
        return func(self, *args, **kwargs)
    return inner
