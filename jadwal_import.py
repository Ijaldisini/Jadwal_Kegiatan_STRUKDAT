import json
import os
from jadwal.models import Kegiatan


def impor_data():
    # 1. Cari file JSON
    path_file = "jadwal.json"
    if not os.path.exists(path_file):
        path_file = "data/jadwal.json"  # Cek di folder data jika di root tidak ada

    if not os.path.exists(path_file):
        print(f"File {path_file} tidak ditemukan!")
        return

    # 2. Baca data
    with open(path_file, "r") as f:
        data_list = json.load(f)

    print(f"Ditemukan {len(data_list)} data. Memulai proses...")

    for item in data_list:
        try:
            # Pecah waktu "08:00-10:00" menjadi dua bagian
            waktu_full = item.get("waktu", "00:00-00:00")
            mulai, selesai = waktu_full.split("-")

            # Masukkan ke database Django
            # Kita gunakan update_or_create agar jika ID sudah ada, datanya diperbarui (bukan error)
            Kegiatan.objects.update_or_create(
                id=item["id"],
                defaults={
                    "tanggal": item["tanggal"],
                    "waktu_mulai": mulai,
                    "waktu_selesai": selesai,
                    "nama": item["nama"],
                    "tempat": item["tempat"],
                    "deskripsi": item.get("deskripsi", ""),
                },
            )
            print(f"Berhasil: {item['nama']}")
        except Exception as e:
            print(f"Gagal impor {item.get('nama')}: {e}")

    print("\n--- SELESAI! Silakan cek browser Anda ---")


if __name__ == "__main__":
    impor_data()
