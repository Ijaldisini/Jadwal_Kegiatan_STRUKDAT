from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Kegiatan
from .forms import KegiatanForm


# Menggantikan show_all_controller.py
def daftar_kegiatan(request):
    query = request.GET.get("q")  # Untuk fitur cari (search_controller.py)
    if query:
        kegiatan_list = Kegiatan.objects.filter(
            Q(nama__icontains=query)
            | Q(tempat__icontains=query)
            | Q(tanggal__icontains=query)
        )
    else:
        kegiatan_list = Kegiatan.objects.all()

    return render(
        request, "jadwal/index.html", {"kegiatan_list": kegiatan_list, "query": query}
    )


# Menggantikan add_controller.py
def tambah_kegiatan(request):
    if request.method == "POST":
        form = KegiatanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("daftar_kegiatan")
    else:
        form = KegiatanForm()
    return render(
        request, "jadwal/form.html", {"form": form, "title": "Tambah Kegiatan"}
    )


# Menggantikan update_controller.py
def edit_kegiatan(request, pk):
    kegiatan = get_object_or_404(Kegiatan, pk=pk)
    if request.method == "POST":
        form = KegiatanForm(request.POST, instance=kegiatan)
        if form.is_valid():
            form.save()
            return redirect("daftar_kegiatan")
    else:
        form = KegiatanForm(instance=kegiatan)
    return render(request, "jadwal/form.html", {"form": form, "title": "Edit Kegiatan"})


# Menggantikan delete_controller.py
def hapus_kegiatan(request, pk):
    kegiatan = get_object_or_404(Kegiatan, pk=pk)
    kegiatan.delete()
    return redirect("daftar_kegiatan")
