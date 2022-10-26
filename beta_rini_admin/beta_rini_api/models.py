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
    
    def __str__(self):
        return f'{self._get_pk_val()}-{self.nomor_rm}-{self.nama_lengkap}'

class Spesialis(models.Model):
    nilai = models.CharField(max_length=50)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diubah = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self._get_pk_val()}-{self.nilai}'

class Dokter(models.Model):
    kode_dokter = models.CharField(max_length=10, unique=True)
    nama_lengkap = models.CharField(max_length=100)
    jenis_kelamin = models.ForeignKey(JenisKelamin, on_delete=models.SET_NULL, null=True, blank=True, related_name='dokter')
    spesialis = models.ForeignKey(Spesialis, on_delete=models.SET_NULL, null=True, blank=True, related_name='dokter')
    alamat = models.TextField(blank=True, null=True)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diubah = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self._get_pk_val()}-{self.kode_dokter}-{self.nama_lengkap}'

class Hari(models.Model):
    nilai = models.CharField(max_length=10)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diubah = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self._get_pk_val()}-{self.nilai}'

class Jadwal(models.Model):
    hari = models.ForeignKey(Hari, on_delete=models.CASCADE, related_name='jadwal')
    dokter = models.ForeignKey(Dokter, on_delete=models.CASCADE, related_name='jadwal')
    waktu_mulai = models.TimeField()
    waktu_selesai = models.TimeField()
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diubah = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self._get_pk_val()}-{self.hari.nilai}-{self.dokter.kode_dokter}-{self.dokter.nama_lengkap}'

class Poli(models.Model):
    nilai = models.CharField(max_length=20)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diubah = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self._get_pk_val()}-{self.nilai}'

class Pendaftaran(models.Model):
    nomor_registrasi = models.CharField(max_length=30, unique=True)
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE, related_name='pendaftaran')
    poli = models.ForeignKey(Poli, on_delete=models.SET_NULL, null=True, blank=True, related_name='pendaftaran')
    dokter = models.ForeignKey(Dokter, on_delete=models.SET_NULL, null=True, blank=True, related_name='pendaftaran')
    tanggal_registrasi = models.DateField()
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diubah = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self._get_pk_val()}-{self.nomor_registrasi}-{self.tanggal_registrasi}'
