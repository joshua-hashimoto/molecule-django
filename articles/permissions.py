from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404


class AccessPermissionToUsers(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_authenticated:
            return True
        raise Http404


class PublishPermission(UserPassesTestMixin):

    def test_func(self):
        obj = self.get_object()
        if self.request.user.is_authenticated or obj.is_published:
            return True
        raise PermissionDenied
