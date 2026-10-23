# Workflow & Tahapan Pembangunan Proyek REST API Flask (Dari Awal sampai Selesai)

Dokumen ini merangkum alur kerja sistematis (*step-by-step workflow*) dalam merancang, membangun, menguji, hingga men-deploy proyek backend **Gacha Character & Team Builder REST API** ke Vercel dan Supabase.

Panduan ini dapat digunakan sebagai referensi pribadi saat presentasi maupun untuk memandu teman yang sedang mengerjakan tugas serupa.

---

## 1. Perancangan Skema & Database Cloud (Supabase PostgreSQL)

Langkah awal berfokus pada pemodelan data sebelum menulis kode aplikasi:

1. **Desain ERD & Relasi Antar Tabel**:
   - Menentukan entitas master: `elements`, `weapons`, `characters`.
   - Menentukan entitas junction & relasi: `skills_talents`, `party_teams`, `party_members`, `player_inventory`.
   - Memastikan ada relasi 1:1, 1:N, dan N:N serta *foreign key constraint* (`ON DELETE RESTRICT` untuk mencegah data terhapus sembarangan).
2. **Setup Cloud Database di Supabase**:
   - Membuat / mengaktifkan project di Supabase.
   - Menjalankan skrip DDL SQL di **SQL Editor** Supabase (membuat tabel, view, dan data awal/seed).
   - Mengambil connection string PostgreSQL:
     - Menggunakan **Session / Transaction Pooler** (port `6543` / `5432`) dengan format:
       `postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres`

---

## 2. Inisialisasi Repositori Git & Struktur Folder Proyek

Menyiapkan direktori proyek agar rapi dan kompatibel dengan Vercel Serverless:

1. **Struktur Direktori**:
   ```text
   gacha-builder-api-learninglabs/
   ├── api/
   │   ├── index.py        # Entrypoint Flask WSGI serverless
   │   └── db.py           # Koneksi database & fallback in-memory
   ├── .env.example        # Template konfigurasi tanpa password
   ├── .gitignore          # Mengabaikan .env, venv, __pycache__
   ├── app.py              # Runner lokal (python app.py)
   ├── postman_collection.json # Koleksi pengujian Postman
   ├── requirements.txt    # Dependencies (Flask, psycopg2-binary, dll)
   ├── test_api.py         # Automated test suite (36 tests)
   └── vercel.json         # Routing rewrite Vercel
   ```
2. **Inisialisasi Git**:
   ```bash
   git init
   git branch -M main
   git remote add origin https://github.com/USERNAME/REPO_NAME.git
   ```

---

## 3. Pembangunan Backend REST API (Flask & psycopg2)

Menulis logika API secara modular dan defensif:

1. **Modul Database (`api/db.py`)**:
   - Membaca `DATABASE_URL` dari environment variable secara aman.
   - Menggunakan cursor `RealDictCursor` agar query PostgreSQL langsung menghasilkan format dictionary/JSON.
   - Menambahkan mekanisme *fallback in-memory mock* agar aplikasi tetap berjalan saat koneksi cloud lambat atau terputus.
2. **Implementasi Endpoint CRUD (`/api/characters`)**:
   - `GET /api/characters`: Mengambil semua data dengan query filter (`?element=...&rarity=...`) dan sorting dinamis yang aman dari SQL Injection.
   - `GET /api/characters/<id>`: Mengambil detail satu karakter beserta relasi skill/talent.
   - `POST /api/characters`: Menambahkan karakter baru dengan validasi ketat (cek tipe data, cek keberadaan foreign key, nilai batas stat). Menghasilkan `201 Created`.
   - `PUT /api/characters/<id>`: Mengupdate sebagian atau seluruh atribut karakter. Menghasilkan `200 OK`.
   - `DELETE /api/characters/<id>`: Menghapus karakter. Jika data masih terkait dengan tabel lain, mengembalikan status `409 Conflict` (bukan crash 500).
3. **Endpoint Tambahan & Monitoring**:
   - `GET /api/elements` & `GET /api/weapons`: Master catalog data.
   - `GET /api/teams`: Menampilkan komposisi tim multi-tabel melalui PostgreSQL View.
   - `GET /api/health`: Health-check untuk monitoring server uptime dan status database.
   - Standardisasi response JSON dan penanganan error (`400`, `404`, `405`, `409`, `500`).

---

## 4. Pengujian Sistematis (Automated Tests & Postman)

Sebelum deployment, seluruh fungsionalitas diuji secara lokal:

1. **Automated Unit Testing (`test_api.py`)**:
   - Membuat 36 skenario test otomatis menggunakan `unittest`.
   - Menguji *happy path* (200, 201) dan *unhappy path / edge cases* (400, 404, 409, SQL injection attempt).
   - Menjalankan test:
     ```bash
     python test_api.py
     ```
2. **Koleksi Postman / Thunder Client (`postman_collection.json`)**:
   - Menyusun 16 request HTTP yang dikelompokkan ke dalam folder.
   - Menambahkan JavaScript assertions (`pm.test`) pada setiap request untuk validasi otomatis status code dan payload JSON.

---

## 5. Deployment ke Vercel Serverless & Debugging Routing

Menghubungkan repositori GitHub ke Vercel dan menyelesaikan kendala serverless:

1. **Konfigurasi `vercel.json`**:
   - Mengatur serverless builds Python dan rewrite rules.
2. **Solusi Masalah WSGI Routing Vercel (`404 Not Found`)**:
   - *Isu*: Rewrite default Vercel sering kali menimpa WSGI `PATH_INFO` menjadi `/api/index`, sehingga Flask gagal mengenali rute asli.
   - *Solusi*: 
     - Pada `vercel.json`, arahkan rewrite dengan query path: `destination: "/api/index?__path=/$1"`.
     - Pada `api/index.py`, pasang middleware `VercelPathMiddleware` untuk mengembalikan rute asli dari parameter `__path`.
3. **Konfigurasi Environment Variables di Vercel Dashboard**:
   - Masuk ke menu **Project Settings -> Environment Variables**.
   - Tambahkan key `DATABASE_URL` dengan connection string Supabase.
   - Lakukan redeploy untuk menerapkan environment variable.

---

## 6. Dokumentasi & Finalisasi Penyerahan

1. **README.md Komprehensif**:
   - Memuat diagram relasi database (Mermaid ERD).
   - Katalog lengkap endpoint REST API (Method, URL, Query params, Request body, Sample response).
   - Panduan menjalankan secara lokal dan cara deploy.
   - Tabel evaluasi pemenuhan syarat tugas: **Persyaratan Minimum vs Fitur Tambahan (Extras)**.
2. **Penyerahan Tugas**:
   - Menyediakan berkas ringkas `SUBMISSION.md` berisi 4 poin utama (link repo, link Vercel, link dokumentasi, dan link export collection).
