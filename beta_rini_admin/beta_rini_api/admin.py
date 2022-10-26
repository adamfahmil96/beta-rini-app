import logging
from django.contrib import admin
from beta_rini_api.models import JenisKelamin, Spesialis, Hari, Poli, \
    Pasien, Dokter, Jadwal, Pendaftaran

logger = logging.getLogger('betarini.custom')

# Register your models here.

@admin.register(JenisKelamin)
class JenisKelaminAdmin(admin.ModelAdmin):
    list_display = ('id', 'nilai')

@admin.register(Spesialis)
class SpesialisAdmin(admin.ModelAdmin):
    list_display = ('id', 'nilai')
    search_fields = ('nilai',)

@admin.register(Hari)
class HariAdmin(admin.ModelAdmin):
    list_display = ('id', 'nilai')

@admin.register(Poli)
class PoliAdmin(admin.ModelAdmin):
    list_display = ('id', 'nilai')
    search_fields = ('nilai',)

@admin.register(Pasien)
class PasienAdmin(admin.ModelAdmin):
    list_display = ('id', 'nomor_rm', 'nama_lengkap', 'nik', 'tanggal_dibuat', 'tanggal_diubah')
    search_fields = ('nomor_rm', 'nama_lengkap', 'nik')

@admin.register(Dokter)
class DokterAdmin(admin.ModelAdmin):
    list_display = ('id', 'kode_dokter', 'nama_lengkap', 'spesialis', 'tanggal_dibuat', 'tanggal_diubah')
    search_fields = ('kode_dokter', 'nama_lengkap')

@admin.register(Jadwal)
class JadwalAdmin(admin.ModelAdmin):
    list_display = ('id', 'hari', 'dokter', 'waktu_mulai', 'waktu_selesai')

@admin.register(Pendaftaran)
class PendaftaranAdmin(admin.ModelAdmin):
    list_display = ('id', 'nomor_registrasi', 'pasien', 'poli', 'dokter', 'tanggal_registrasi')
    search_fields = ('nomor_registrasi', 'pasien__nomor_rm', 'pasien__nama_lengkap', 'dokter__kode_dokter', 'dokter__nama_lengkap')
