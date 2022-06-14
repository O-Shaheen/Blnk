from rest_framework import permissions

class Is_loaner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("req userrr: ", request.user)
        print("Here-----------------------------")
        if request.user.is_loaner == True:
            return True
        return False