from django.contrib.auth.mixins import UserPassesTestMixin
# from django.core.exceptions import PermissionDenied
from django.http import Http404


class AccessPermissionToUsersMixin(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_authenticated:
            return True
        raise Http404
