# ⚽ SoccerID — Football Shop Web Application

**Mata Kuliah**: Pemrograman Berbasis Platform (PBP)  
**Semester**: Ganjil 2025/2026  

- 👤 **Nama**: Jonathan Yitskhaq Rundjan  
- 🆔 **NPM**: 2406435231  
- 🏫 **Kelas**: PBP C  
- 🔗 **[Link ke SoccerID](https://jonathan-yitskhaq-soccerid.pbp.cs.ui.ac.id)**

---
## Tugas 3
### Pentingnya Data Delivery dalam sebuah platform
Dalam mengembangkan suatu platform, kita perlu mengirimkan data dari satu stack ke stack lainnya. Hal ini menjadi penting karena: 

1. Pertukaran data yang lebih mudah antara client dan server.

2. Bagian frontend dan backend dapat dikerjakan secara terpisah, sehingga data delivery menjadi hal penting.

3. Data bisa digunakan untuk aplikasi mobile, HTML, dsb.

4. Dapat diakses dan terintegrasi dengan third-party

---
### XML vs JSON, mana yang lebih baik & mengapa JSON lebih populer?

Hal ini bergantung pada kebutuhan developer aplikasi, namun JSON biasanya digunakan karena lebih praktis.

###  Perbedaan JSON vs XML 

| Aspek              | **JSON (JavaScript Object Notation)** | **XML (Extensible Markup Language)** |
|--------------------|----------------------------------------|--------------------------------------|
| **Format**         | Struktur **key–value** (mirip map/dictionary). | Struktur **tree dengan tag** (parent–child elements). |
| **Sintaks**        | Ringkas, mudah dibaca/tulis, tanpa tag penutup. | Verbose, harus pakai tag pembuka/penutup, karakter tertentu perlu entity (`&lt;`, `&gt;`). |
| **Parsing**        | Bisa langsung dengan fungsi JavaScript (`JSON.parse()`), lebih cepat & sederhana. | Butuh XML parser khusus, parsing lebih berat. |
| **Schema**         | Ada JSON Schema, relatif sederhana & fleksibel. | XML Schema (XSD) lebih kompleks & ketat, cocok untuk validasi struktur besar. |
| **Tipe data**      | String, number, object, array, boolean. | Mendukung tipe kompleks tambahan: boolean, date, timestamp, binary, namespace. |
| **Ukuran file**    | Lebih kecil → lebih cepat ditransmisikan. | Lebih besar karena struktur tag. |
| **Kemudahan**      | Simpel, readable, populer di API modern. | Lebih kompleks, verbose, lebih sulit dibaca manusia. |
| **Keamanan**       | Parsing relatif aman. | Rentan ke **XML External Entity (XXE)** atau **DTD attack** jika parser tidak dikonfigurasi dengan aman. |
| **Kapan digunakan**| Cocok untuk API, mobile apps, web apps, data exchange ringan & cepat. | Cocok untuk dokumen kompleks, konfigurasi besar, integrasi enterprise/legacy systems. |

**Kenapa JSON Lebih Populer?**
- Native support di hampir semua bahasa modern
- Sintaks mudah dipahami dan lebih sederhana
- Memiliki ukuran data yang lebih kecil


---
### Peran `is_valid()` dalam Django Form
`settings.py` dalam  Django Form berfungsi untuk: 
- Mengecek validasi bawaan.
- Mengembalikan `True` `False` sesuai dengan data.
- Setelah `is_valid()` dipanggil, kita bisa mengakses `form.celaned_data` untuk mengambil data yang sudah bersih.


---
### Mengapa perlu `{% csrf_token %}` pada form? Apa risikonya jika tidak? 

1. Proteksi CSRF: token unik dimasukkan ke form lalu diverifikasi di server.
2. Tanpa token, seorang hacker bisa melakukan **Cross-Site Request Forgery** yang mmembuat halaman berisi form tersebunyi yang auto-submit menggunakan cookie korban.
3. Dengan token, request palsu bisa dihindari.

Seluruh proses ini bertujuan untuk memastikan struktur database pada program sinkron dengan model yang telah didefinsikan.

---
### Step-by-step Implementasi Checklist

1. **Setup proyek & app**
   - Buat virtual environment: `python -m venv env` lalu aktifkan.
   - Install Django: `pip install django`.
   - Buat proyek: `django-admin startproject SoccerID`.
   - Buat app: `python manage.py startapp main`.
   
2. **Membuat Model `Product`**
   - Field yang digunakan:
     - `name` (CharField)
     - `price` (IntegerField)
     - `description` (TextField)
     - `thumbnail` (URLField)
     - `category` (CharField)
     - `is_featured` (BooleanField)
   - Jalankan `python manage.py makemigrations` dan `python manage.py migrate`.

3. **Membuat Form**
   - Tambahkan `ProductForm` (ModelForm) di `forms.py` agar field di atas otomatis terbentuk input HTML.

4. **Membuat Views**
   - `show_main` → menampilkan semua produk dalam template `main.html`.
   - `add_product` → menampilkan form tambah produk dan menyimpan ke database jika valid.
   - `product_detail` → menampilkan detail produk tertentu.
   - `show_json`, `show_xml`, `show_json_by_id`, `show_xml_by_id` → mengembalikan data dalam format JSON atau XML.

5. **Routing**
   - `SoccerID/urls.py` → gunakan `include("main.urls")`.
   
6. **Membuat Templates**
   - `add_product.html` → halaman form tambah produk (gunakan `{% csrf_token %}`).
   - `product_detail.html` → halaman detail produk.

7. **Migrasi Database**
   - Menjalankan `python manage.py makemigrations` dan `python manage.py migrate`.

7. **Testing dan Deployment**
   - Jalankan `python manage.py runserver`.
   - Men-deploy ke PWS.


---
### Feedback untuk Asisten Dosen
Menurut saya, bantuan asisten dosen hingga saat ini sudah sangat cukup membantu bagi saya.

---
###  Bukti Screenshoot Postman
Postman XML
![Postman XML](xml.png)
Postman XML by ID
![Postman XML by ID](xml_id.png)
Postman JSON
![Postman JSON](json.png)
Postman JSON by ID
![Postman JSON by ID](json_id.png)

### Referensi
Pada pembuatan model, saya menggunakan GPT untuk memberikan bentuk model terbaik dan penempatan size yang sesuai. 

---

## Tugas 4
### Pengertian Django `AuthenticationForm`, Kelebihan dan Kekurangan

AuthenticationForm` adalah form bawaan Django untuk autentikasi username dan password.  

**Kelebihan:**
- Siap pakai, validasi sudah tersedia.
- Terintegrasi dengan sistem auth Django (`authenticate`, `login`).
- Aman secara default (hashing password).

**Kekurangan:**
- Tampilan standar, perlu di-custom agar lebih user-friendly.
- Hanya mendukung username/password, login via email/OTP harus form custom.
- Tidak ada fitur tambahan seperti “remember me” atau 2FA.

## Perbedaan Autentikasi dan Otorisasi
- **Autentikasi** → proses verifikasi identitas (*siapa kamu*).  
  Django: `AuthenticationMiddleware`, `authenticate()`, `login()`, `logout()`.
- **Otorisasi** → proses menentukan hak akses (*boleh ngapain*).  
  Django: `user.is_staff`, `user.is_superuser`, `user.has_perm()`, decorator `@permission_required`.

**Contoh:**
```python
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def dashboard(request):
    ...

@permission_required('main.change_product', raise_exception=True)
def edit_product(request, pk):
    ...
```

## Kelebihan & Kekurangan Session dan Cookies
**Session (server-side)**
- Kelebihan: Data state aman di server, tidak terkena batas 4KB, bisa invalidasi/ rotasi, lebih sulit untuk dimanipulasi user.
- Kekurangan: Perlu storage, skalabilitas (replication), overhead query.

---
**Cookies (client-side)**
- Kelebihan: Stateless di server, cepat, dan hemat storage server.
- Kekurangan: Batas ukuran 4KB, rentan untuk dimodifikasi jika tidak terenkripsi, rawan XSS/mitm jika tak pakai Secure/ HtppOnly, sinkronisasi & invalidasi lebih sulit

---
## Apakah Cookies "Aman secara Default"? Risiko dan Mitigasi Django

Secara umum, Cookies tidak otomatis aman. Risiko yang umum: 
- XSS: Pencurian cookie/ session.
- Tanpa HTTPS: Cookie bisa disadap.
- CSRF: Request palsu memakai cookie sesi korban.
- Session Fixation: Penyerang memaksa korban memakai session ID tertentu.

**Mitigasi Keamanan di Django (Production Hardening)**

Tambahkan pengaturan berikut pada `settings.py` (khusus mode produksi):

```python
# settings.py (production hardening)

# Cookie hanya dikirim via HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Cookie tidak bisa diakses JavaScript (hindari XSS)
SESSION_COOKIE_HTTPONLY = True
# CSRF_COOKIE_HTTPONLY = True   # aktifkan jika tidak perlu akses token via JS

# Batasi pengiriman cookie hanya untuk same-site request
SESSION_COOKIE_SAMESITE = "Lax"   # atau "Strict" sesuai kebutuhan
CSRF_COOKIE_SAMESITE = "Lax"

# Paksa semua request ke HTTPS
SECURE_SSL_REDIRECT = True

# (Opsional) Rotasi sesi setelah login untuk cegah session fixation
# di view login: request.session.flush() atau django.contrib.auth.login() otomatis rotate session
```

---
### Step-by-step Implementasi Checklist

1. **Membuat Model & Migrasi**
   - Buat `Product` dengan field: `name, price, description, thumbnail, category, stock, is_featured, user`.
   - Menjalankan `makemigrations` + `migrate`

2. **Form**
   - `ProductForm` (ModelForm) hanya mencakup field produk tanpa `user`

3. **Views HTML**
   - Membuat agar bisa memfilter berdasarkan product user yaitu my product dan all product

4. **Auth**
   - Register: `UserCreationForm`
   - Login: `AuthenticationForm`, `login()`, set cookie `last_login`
   - Logout: `logout()`, hapus cookie `last_login`
   
5. **Keamanan**
   - Gunakan `{% csrf_token %}` di semua form.
   - Set `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, dan cookie secure saat deploy.




