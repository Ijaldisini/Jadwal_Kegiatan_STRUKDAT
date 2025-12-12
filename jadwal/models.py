from django.db import models


class Kegiatan(models.Model):
    tanggal = models.DateField()
    waktu_mulai = models.TimeField()
    waktu_selesai = models.TimeField()
    nama = models.CharField(max_length=255)
    tempat = models.CharField(max_length=255)
    deskripsi = models.TextField()

    class Meta:
        # Menggantikan logika pengurutan pada show_all_controller.py
        ordering = ["tanggal", "waktu_mulai"]

    def __str__(self):
        return f"{self.nama} - {self.tanggal}"
