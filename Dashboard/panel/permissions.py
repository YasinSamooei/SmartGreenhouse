# from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


# class HasAdminAccessPermission(UserPassesTestMixin):
#
#     def test_func(self):
#         if self.request.user.is_authenticated:
#             return self.request.user.is_superuser == True
#         return False

class AuthenticatedMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("panel:home")
        return super().dispatch(request, *args, **kwargs)
