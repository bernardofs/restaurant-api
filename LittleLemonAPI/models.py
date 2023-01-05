from django.db import models
from django.contrib.auth.models import User
from computedfields.models import ComputedFieldsModel, computed


class Category(models.Model):
  title = models.CharField(max_length=255, db_index=True)

  def __str__(self):
    return self.title


class MenuItem(models.Model):
  title = models.CharField(max_length=255, db_index=True)
  price = models.DecimalField(max_digits=8, decimal_places=2, db_index=True)
  category = models.ForeignKey(
    Category, related_name='category', on_delete=models.SET_NULL, null=True
  )
  featured = models.BooleanField()

  def __str__(self):
    return self.title


class Cart(ComputedFieldsModel):
  quantity = models.SmallIntegerField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  menu_item = models.ForeignKey(
    MenuItem, related_name='cart_menu_item', on_delete=models.CASCADE
  )

  @computed(models.DecimalField(max_digits=9, decimal_places=2))
  def total(self):
    return self.menu_item.price * self.quantity

  class Meta:
    unique_together = ['user', 'menu_item']


class Order(ComputedFieldsModel):
  status = models.SmallIntegerField(db_index=True)
  customer = models.ForeignKey(
    User, related_name='customer', on_delete=models.CASCADE
  )
  crew = models.ForeignKey(User, related_name='crew',
                           on_delete=models.SET_NULL, null=True
                           )

  @computed(models.DecimalField(max_digits=9, decimal_places=2))
  def total(self):
    items_cart = ItemOrder.objects.all().filter(order=self)
    return sum(item.total for item in items_cart)


class ItemOrder(ComputedFieldsModel):
  quantity = models.SmallIntegerField()
  menu_item = models.ForeignKey(
    MenuItem, related_name='item_order_menu_item', on_delete=models.RESTRICT
  )
  order = models.ForeignKey(
    Order, related_name='order', on_delete=models.CASCADE
  )

  @computed(models.DecimalField(max_digits=9, decimal_places=2))
  def total(self):
    return self.menu_item.price * self.quantity

  class Meta:
    unique_together = ['order', 'menu_item']
