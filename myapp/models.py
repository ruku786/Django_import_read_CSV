from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=20)

    def ____str(self):
        return self.name


class Person_detail(models.Model):
    address = models.CharField(max_length=50)
    person_id = models.OneToOneField(Person, on_delete=models.CASCADE)
    #email = models.ForeignKey(Person, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True, default='')
    phone = models.IntegerField()

    def ____str(self):
        return self.address
