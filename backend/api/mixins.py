from rest_framework import permissions
from .permissions import IsStaffEditorPermission    

class StaffEditorPermissionMixIn():
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]