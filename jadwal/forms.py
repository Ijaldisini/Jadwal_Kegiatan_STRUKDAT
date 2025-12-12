from django import forms
from .models import Kegiatan
from datetime import datetime


class KegiatanForm(forms.ModelForm):
    class Meta:
        model = Kegiatan
        fields = "__all__"
        widgets = {
            "tanggal": forms.DateInput(attrs={"type": "date"}),
            "waktu_mulai": forms.TimeInput(attrs={"type": "time"}),
            "waktu_selesai": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tgl = cleaned_data.get("tanggal")
        w1 = cleaned_data.get("waktu_mulai")
        w2 = cleaned_data.get("waktu_selesai")

        if w1 and w2 and w2 <= w1:
            raise forms.ValidationError("Waktu selesai harus setelah waktu mulai.")

        # Logika Overlap (diadaptasi dari delete_controller.py logic)
        # Mencari apakah ada kegiatan di waktu yang sama
        konflik = Kegiatan.objects.filter(
            tanggal=tgl, waktu_mulai__lt=w2, waktu_selesai__gt=w1
        ).exclude(
            pk=self.instance.pk
        )  # Kecualikan diri sendiri saat update

        if konflik.exists():
            raise forms.ValidationError(
                "Peringatan: Jadwal bentrok dengan kegiatan lain!"
            )

        return cleaned_data
