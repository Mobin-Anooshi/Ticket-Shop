from django.db import models
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from A.accounts.models import Vehicle


class Travel(models.Model):
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    departure_time = models.DateTimeField()
    available_seats = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.origin} to {self.destination}'


class TravelDetails(models.Model):
    travel_id = models.OneToOneField('Travel',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.IntegerField()
    vehicle_id = models.ForeignKey('Vehicle',on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    driver_id = models.ForeignKey('Driver_Documents',on_delete=models.CASCADE)
    distance_id = models.ForeignKey('Distance', on_delete=models.CASCADE)


    def __str__(self):
        return f'{str(self.travel_id)} {self.created}'

@receiver(post_save,sender=TravelDetails)
def set_vehicle_seats(sender, instance, created, **kwargs):
    travel = instance.travel_id
    vehicle = instance.vehicle_id
    travel.available_seats = vehicle.seats
    travel.save()


class Distance(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance = models.IntegerField(default=0)

class Ticket(models.Model):
    travel_id = models.ForeignKey('Travel',on_delete=models.CASCADE,related_name='tickets')
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        travel_details = TravelDetails.objects.get(travel=self.travel_id)
        self.total_price = travel_details.price * self.quantity
        super().save(*args, **kwargs)

@receiver(post_save, sender=Ticket)
def change_seats_num(sender, instance, created, **kwargs):
    travel = instance.travel_id

    if created:
        travel.available_seats -= instance.quantity
        travel.save()
    else:
        previous_ticket = Ticket.objects.get(pk=instance.pk)
        difference = instance.quantity - previous_ticket.quantity
        travel.available_seats -= difference
        travel.save()

@receiver(post_delete, sender=Ticket)
def return_seats_on_delete(sender, instance, **kwargs):
    travel = instance.travel_id
    travel.available_seats += instance.quantity
    travel.save()