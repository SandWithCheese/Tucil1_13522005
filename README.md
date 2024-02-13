# Tugas Kecil 1 Strategi Algoritma

## Cyberpunk 2077 Breach Protocol Solver dengan Mengimplementasi Algoritma Brute Force

Aplikasi ini mengimplementasikan algoritma brute force untuk menyelesaikan breach protocol dari game Cyberpunk 2077. Program dibuat dengan menggunakan bahasa Python. Proses input dan output dari program diimplementasikan dengan menggunakan GUI dari library customtkinter. Program lalu di-compile menjadi executable yang dapat dijalankan pada sistem operasi linux dan windows dengan menggunakan pyinstaller.

## Requirements

- customtkinter
- pyinstaller (jika ingin me-compile program)

## How to Compile

```bash
pyinstaller --noconfirm --onedir --windowed --add-data "<CustomTkinter Location>/customtkinter:customtkinter/"  "<Path to Python Script>"
```

## How to Run

Run the source code

```bash
python src/app.py
```

Run the executable

Linux

```bash
./bin/linux/dist/app/app
```

Windows

Jalankan executable yang ada di ./bin/windows/dist/app/app.exe

## Anggota

- Ahmad Naufal Ramadan (13522005)
