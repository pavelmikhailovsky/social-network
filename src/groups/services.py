from django.contrib.auth import get_user_model

from .models import Groups

User = get_user_model()


class CheckingRoleUserCurrentGroup:
    def __init__(self, groups_id, users_id):
        self.__group = Groups.objects.get(id=groups_id)
        self.__user = users_id

    def is_owner(self):
        return True if self.__group.owner_id == self.__user else False

    def is_administrator(self):
        return True if self.__group.administrators.filter(id=self.__user) else False

    def is_redactor(self):
        return True if self.__group.redactors.filter(id=self.__user) else False

    def is_subscriber(self):
        return True if self.__group.subscribers.filter(id=self.__user) else False


class GetObjectsQuerySet:
    """
    Returns objects users and groups.
    """

    def __init__(self, users_id=None, groups_id=None):
        if users_id:
            self.user = self._queryset_user(users_id)
        if groups_id:
            self.group = self._queryset_group(groups_id)

    @staticmethod
    def _queryset_user(users_id):
        try:
            user = User.objects.get(id=users_id)
            return user
        except Exception as e:
            print(e)

    @staticmethod
    def _queryset_group(groups_id):
        try:
            group = Groups.objects.get(id=groups_id)
            return group
        except Exception as e:
            print(e)
