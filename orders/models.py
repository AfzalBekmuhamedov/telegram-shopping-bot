from django.db import models

class Order(models.Model):
    user_id = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=40, default="pending")

    def __str__(self):
        return f"Order {self.pk}"

