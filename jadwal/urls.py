from django.urls import path
from . import views

urlpatterns = [
    path("", views.daftar_kegiatan, name="daftar_kegiatan"),
    path("tambah/", views.tambah_kegiatan, name="tambah_kegiatan"),
    path("edit/<int:pk>/", views.edit_kegiatan, name="edit_kegiatan"),
    path("hapus/<int:pk>/", views.hapus_kegiatan, name="hapus_kegiatan"),
]
