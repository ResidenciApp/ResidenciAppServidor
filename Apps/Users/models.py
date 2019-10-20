from django.db import models


class Owner(models.Model):
    documentNumber = models.IntegerField()

    DOCUMENT_TYPE_CHOICES = [
        ('CC', 'Cedula de Ciudadania'),
        ('TI', 'Tarjeta de Identidad'),
    ]

    documentType = models.CharField(
        max_length=2,
        choices=DOCUMENT_TYPE_CHOICES,
        default='CC',
    )

    def __str__(self):
        return '{}: {}'.format(
            self.documentType,
            self.documentNumber
        )


class Role(models.Model):
    name = models.CharField(max_length=63)
    description = models.CharField(max_length=511)

    def __str__(self):
        return '{}'.format(self.name)


from django.contrib.auth.models import User

class People(User):
    # Hereda los Siguiente Atributos de el modelo User
    # username
    # first_name
    # last_name
    # password
    # email

    age = models.IntegerField()
    avatar = models.CharField(max_length=255)

    # PK
    role = models.ForeignKey(Role, null=False, blank=False, on_delete=models.CASCADE)
    owner = models.OneToOneField(Owner, null=True, blank=True, on_delete=models.CASCADE)

    SEX_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    sex = models.CharField(
        max_length=2,
        choices=SEX_CHOICES,
        default='O',
    )

    def __str__(self):
        return '{} {}'.format(self.name, self.lastName)
