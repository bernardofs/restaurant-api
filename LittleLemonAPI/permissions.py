
from rest_framework.permissions import BasePermission


def is_admin(user):
  return user.is_staff


class IsAdminPermission(BasePermission):
  def has_permission(self, request, views):
    try:
      return is_admin(request.user)
    except Exception as e:
      return False


def is_manager(user):
  return user.groups.filter(name='Manager').exists() or user.is_staff


class IsManagerPermission(BasePermission):
  def has_permission(self, request, views):
    try:
      return is_manager(request.user)
    except Exception as e:
      return False


def is_delivery_crew(user):
  return user.groups.filter(name='DeliveryCrew').exists()


def is_customer(user):
  return not is_manager(user) and not is_delivery_crew(user)


class IsCustomerPermission(BasePermission):
  def has_permission(self, request, views):
    try:
      return is_customer(request.user)
    except Exception as e:
      return False


class OrderPermission(BasePermission):
  def has_permission(self, request, views):
    try:
      if views.action == 'list':
        return True
      elif views.action in ['create', 'retrieve']:
        return is_customer(request.user)
      elif views.action in ['update', 'destroy']:
        return is_manager(request.user)
      elif views.action == 'partial_update':
        return is_manager(request.user) or is_delivery_crew(request.user)
      else:
        return False
    except Exception as e:
      return False
