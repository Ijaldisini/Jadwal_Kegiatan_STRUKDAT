from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Kegiatan
from .forms import KegiatanForm
from django.core.paginator import Paginator


# Menggantikan show_all_controller.py
def daftar_kegiatan(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'asc')  # Default urutan terlama (asc)

    # 1. Ambil data & Filter Pencarian
    if query:
        semua_kegiatan = Kegiatan.objects.filter(nama__icontains=query)
    else:
        semua_kegiatan = Kegiatan.objects.all()

    # 2. Logika Pengurutan
    if sort == 'desc':
        semua_kegiatan = semua_kegiatan.order_by('-tanggal', '-waktu_mulai')
    else:
        semua_kegiatan = semua_kegiatan.order_by('tanggal', 'waktu_mulai')

    # 3. Paginasi (10 data)
    paginator = Paginator(semua_kegiatan, 10)
    page_number = request.GET.get('page')
    kegiatan_list = paginator.get_page(page_number)

    return render(request, 'jadwal/index.html', {
        'kegiatan_list': kegiatan_list,
        'query': query,
        'sort': sort,
    })


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
