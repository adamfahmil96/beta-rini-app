import logging
import traceback
from django.db import models
from django.forms import ValidationError

logger = logging.getLogger('betarini.custom')

# Create your models here.

class JenisKelamin(models.Model):
    nilai = models.CharField(max_length=10)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diubah = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self._get_pk_val()}-{self.nilai}'

class Pasien(models.Model):
    nomor_rm = models.CharField(max_length=10)
    nama_lengkap = models.CharField(max_length=100)
    nik = models.CharField(max_length=20, blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    telepon = models.CharField(max_length=15)
    jenis_kelamin = models.ForeignKey(JenisKelamin, on_delete=models.SET_NULL, null=True, blank=True, related_name='pasien')
    alamat = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=30, blank=True, null=True)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diubah = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = ('nomor_rm', 'username')
    
    def clean(self, *args, **kwargs):
        try:
            # set username automatically if not any
            if not self.username and len(self.nama_lengkap) >= 6:
                self.username = str(self.nama_lengkap)[:6]
            elif not self.username and len(self.nama_lengkap) < 6:
                self.username = str(self.nama_lengkap)[:len(self.nama_lengkap)]

            super(Pasien, self).clean(*args, **kwargs)

        except Exception as error:
            err_message = f'Error on clean method of Pasien model: {error}'
            logger.exception(f'{err_message} | {traceback.format_exc()}')
            raise ValidationError(err_message)

class Spesialis(models.Model):
    nilai = models.CharField(max_length=50)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diubah = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self._get_pk_val()}-{self.nilai}'
