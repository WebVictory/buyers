from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()
# Модель чека
class Check(models.Model):
    buyer = models.CharField( verbose_name="Покупатель", max_length=250)
    # если номер состит только из цифр имеет смысл использовать числовое поле,
    # но в нем также могут быть и нечисловые символы поэтому я использовал текстовое поле
    number = models.CharField(verbose_name="Номер чека", max_length=250, unique=True)
    store = models.CharField( verbose_name="Магазин", max_length=250)
    issue_date = models.DateTimeField("Время выдачи чека")
    check_amount = models.IntegerField("Сумма чека")

# Модель одной позиции в чеке
class PositionCheck(models.Model):
    name = models.CharField( verbose_name="Наименование", max_length=250)
    count = models.IntegerField(verbose_name="Количество")
    price = models.IntegerField(verbose_name="Цена")
    position_amount = models.IntegerField("Сумма")
    parent_check = models.ForeignKey("Check", verbose_name="Чек", related_name='positions', on_delete=models.CASCADE)