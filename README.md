# 🌌 Gacha Character & Team Builder REST API

[![Vercel Deployment](https://img.shields.io/badge/Vercel-Serverless%20WSGI-black?logo=vercel)](https://vercel.com)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Flask Framework](https://img.shields.io/badge/Framework-Flask%203.1-green?logo=flask)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL%20(Supabase)-336791?logo=postgresql)](https://supabase.com)
[![Tests](https://img.shields.io/badge/Automated%20Tests-36%20Passed-brightgreen)](test_api.py)

Proyek ini merupakan implementasi **Tugas Akhir Learning Labs: Backend Development** yang mengusung arsitektur RESTful API skala produksi untuk platform manajemen karakter gacha, inventori pemain, dan pembentukan tim tempur (*team builder / Spiral Abyss*).

API ini dibangun menggunakan **Python Flask**, driver native **psycopg2** dengan `RealDictCursor`, serta di-deploy secara serverless pada **Vercel** dengan basis data **PostgreSQL di Supabase**.

---

## 📑 Daftar Isi

- [Arsitektur Sistem & Fitur Utama](#-arsitektur-sistem--fitur-utama)
- [Diagram Relasi Entitas (Mermaid ERD)](#-diagram-relasi-entitas-mermaid-erd)
- [Struktur Direktori Proyek](#-struktur-direktori-proyek)
- [Panduan Setup Database (Supabase)](#-panduan-setup-database-supabase)
- [Panduan Menjalankan Secara Lokal](#-panduan-menjalankan-secara-lokal)
- [Panduan Deployment ke Vercel](#-panduan-deployment-ke-vercel)
- [Dokumentasi Lengkap REST API](#-dokumentasi-lengkap-rest-api)
- [Pengujian Otomatis (Automated Testing)](#-pengujian-otomatis-automated-testing)
- [Impor Postman / Thunder Client](#-impor-postman--thunder-client)
- [Matriks Pemenuhan Kriteria Rubrik Tugas](#-matriks-pemenuhan-kriteria-rubrik-tugas)

---

## ⚡ Arsitektur Sistem & Fitur Utama

1. **Complete Character CRUD (`/api/characters`)**:
   - `GET /api/characters`: Mengambil semua karakter dengan query filter (`element`, `rarity`, `weapon_type`, `role`, `search`, `sort_by`, `order`).
   - `GET /api/characters/<id>`: Mengambil detail karakter lengkap beserta daftar talent/skill aktif & pasifnya.
   - `POST /api/characters`: Menambahkan karakter baru dengan validasi ketat terhadap domain constraint (tipe senjata, rarity, role, elemen valid).
   - `PUT /api/characters/<id>`: Memperbarui satu atau seluruh atribut karakter.
   - `DELETE /api/characters/<id>`: Menghapus karakter dengan proteksi integritas relasional (*menghasilkan HTTP 409 Conflict jika karakter masih terikat di inventori pemain*).
2. **Master Data & Analytic Views**:
   - `GET /api/elements`: Mengambil daftar 7 elemen master (*Pyro, Hydro, Anemo, Electro, Dendro, Cryo, Geo*).
   - `GET /api/weapons`: Mengambil katalog senjata dengan filter *rarity* dan *weapon type*.
   - `GET /api/teams`: Mengambil komposisi party tim lengkap yang menggabungkan data pemain, karakter, elemen, senjata, dan posisi slot melalui PostgreSQL View `v_party_team_details`.
3. **Reliability & Monitoring**:
   - `GET /api/health`: Pemantauan uptime server dan konektivitas live ke cluster PostgreSQL Supabase.
   - Global Error Handling berstandar JSON untuk status code `200`, `201`, `400`, `404`, `405`, `409`, dan `500`.
4. **Vercel Serverless Ready**:
   - Entrypoint serverless WSGI pada `api/index.py` dengan konfigurasi routing rewrite `vercel.json`.

---

## 📊 Diagram Relasi Entitas (Mermaid ERD)

Basis data dirancang dengan **14 Tabel Relasional** yang mencakup relasi 1:1, 1:N, dan N:N (junction table), dilengkapi *check constraints* dan *foreign key restrictions*.

```mermaid
erDiagram
    PLAYERS ||--|| PLAYER_PROFILES : "1:1 profile"
    PLAYERS ||--o{ PLAYER_INVENTORY_CHARACTERS : "owns"
    PLAYERS ||--o{ PLAYER_INVENTORY_WEAPONS : "owns"
    PLAYERS ||--o{ GACHA_PULL_HISTORY : "pulls"
    PLAYERS ||--o{ PARTY_TEAMS : "creates"
    
    ELEMENTS ||--o{ CHARACTERS : "categorizes"
    CHARACTERS ||--o{ SKILLS_TALENTS : "has"
    CHARACTERS ||--o{ PLAYER_INVENTORY_CHARACTERS : "instantiated_as"
    
    WEAPONS ||--o{ PLAYER_INVENTORY_WEAPONS : "instantiated_as"
    
    GACHA_BANNERS ||--o{ GACHA_PULL_HISTORY : "records"
    
    PARTY_TEAMS ||--o{ PARTY_MEMBERS : "contains"
    PARTY_TEAMS ||--o{ ABYSS_RUN_RECORDS : "evaluates"
    
    PLAYER_INVENTORY_CHARACTERS ||--o{ PARTY_MEMBERS : "slotted_in"
    PLAYER_INVENTORY_WEAPONS ||--o{ PARTY_MEMBERS : "equipped_in"

    PLAYERS {
        int id PK
        string username UK
        string email UK
        string in_game_uid UK
        string password_hash
        timestamp created_at
    }

    PLAYER_PROFILES {
        int id PK
        int id_player FK,UK
        string bio_status
        int adventure_rank
        int world_level
        int total_achievements
        string avatar_url
    }

    ELEMENTS {
        int id PK
        string nama_elemen UK
        string warna_hex
        text reaksi_efek
    }

    CHARACTERS {
        int id PK
        int id_elemen FK
        string nama_karakter
        int rarity
        string tipe_senjata
        string role_utama
        int base_hp
        int base_atk
        int base_def
        string ascension_stat
    }

    SKILLS_TALENTS {
        int id PK
        int id_character FK
        string nama_talent
        string tipe_talent
        text deskripsi
        numeric cooldown_seconds
        int energy_cost
    }

    WEAPONS {
        int id PK
        string nama_senjata
        string tipe_senjata
        int rarity
        int base_atk
        string substat_type
        numeric substat_value
        text pasif_deskripsi
    }

    ARTIFACT_SETS {
        int id PK
        string nama_set UK
        text efek_2_piece
        text efek_4_piece
    }

    PLAYER_INVENTORY_CHARACTERS {
        int id PK
        int id_player FK
        int id_character FK
        int character_level
        int constellation_level
        int friendship_level
        timestamp obtained_at
    }

    PLAYER_INVENTORY_WEAPONS {
        int id PK
        int id_player FK
        int id_weapon FK
        int weapon_level
        int refinement_rank
        boolean is_locked
        timestamp obtained_at
    }

    GACHA_BANNERS {
        int id PK
        string nama_banner
        string tipe_banner
        timestamp start_date
        timestamp end_date
        string rate_up_5star_featured
    }

    GACHA_PULL_HISTORY {
        int id PK
        int id_player FK
        int id_banner FK
        string item_type
        string item_name
        int rarity_pulled
        int pity_count
        boolean is_won_50_50
        timestamp pulled_at
    }

    PARTY_TEAMS {
        int id PK
        int id_player FK
        string nama_party
        string fokus_konten
        text deskripsi
        timestamp created_at
    }

    PARTY_MEMBERS {
        int id PK
        int id_party FK
        int id_inventory_character FK
        int id_inventory_weapon FK
        int slot_position
        string role_dalam_party
    }

    ABYSS_RUN_RECORDS {
        int id PK
        int id_party FK
        string floor_chamber
        int clear_time_seconds
        int stars_earned
        timestamp run_date
    }
```

---

## 📁 Struktur Direktori Proyek

```text
gacha-builder-api-learninglabs/
├── api/
│   ├── __init__.py           # Package marker
│   ├── db.py                 # Driver koneksi PostgreSQL, RealDictCursor, dan Mock Storage
│   └── index.py              # Serverless WSGI entrypoint Flask & seluruh rute REST API
├── database/
│   └── schema.sql            # File DDL SQL PostgreSQL 14+ lengkap (14 Tabel + View + Seed Data)
├── .env.example              # Template variabel lingkungan aman
├── .gitignore                # Aturan ignore file rahasia (.env, venv, cache)
├── app.py                    # Runner lokal Flask (python app.py)
├── postman_collection.json   # Koleksi Postman v2.1 siap pakai (1-Click Import)
├── requirements.txt          # Dependensi Python (flask, psycopg2-binary, python-dotenv)
├── test_api.py               # Test suite otomatis (30 skenario pengujian komprehensif)
├── vercel.json               # Konfigurasi routing serverless Vercel
└── README.md                 # Dokumentasi teknis proyek
```

---

## 🗄️ Panduan Setup Database (Supabase)

1. Buka dashboard [Supabase](https://supabase.com/) dan buat project baru.
2. Masuk ke menu **SQL Editor** pada sidebar kiri.
3. Buka file `database/schema.sql` pada repository ini, salin seluruh kodenya, lalu tempel (*paste*) ke dalam SQL Editor Supabase.
4. Klik tombol **Run**. Seluruh 14 tabel, view analitik `v_party_team_details`, dan data dummy awal akan dibuat.
5. Dapatkan Connection String:
   - Masuk ke **Project Settings** -> **Database**.
   - Pada bagian **Connection string**, pilih opsi **URI**.
   - Contoh format:
     ```text
     postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres?sslmode=require
     ```
   - Catat connection string ini untuk konfigurasi `.env` dan Vercel.

---

## 💻 Panduan Menjalankan Secara Lokal

### 1. Prasyarat
- Python 3.10 atau versi yang lebih baru
- Git

### 2. Kloning & Virtual Environment
```bash
# Kloning repositori
git clone https://github.com/lunizura/gacha-builder-api-learninglabs.git
cd gacha-builder-api-learninglabs

# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment
# Pada Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Pada Linux / macOS:
source venv/bin/activate

# Install dependensi
pip install -r requirements.txt
```

### 3. Konfigurasi Variabel Lingkungan
Salin `.env.example` menjadi `.env`:
```bash
copy .env.example .env     # Windows
cp .env.example .env       # Linux/macOS
```
Buka file `.env` dan masukkan `DATABASE_URL` Supabase Anda:
```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres?sslmode=require
PORT=5000
FLASK_ENV=development
```
*(Catatan: Jika `DATABASE_URL` dikosongkan, API secara otomatis beralih ke in-memory mock engine untuk pengujian offline).*

### 4. Menjalankan Server Lokal
```bash
python app.py
```
Akses server pada browser atau Postman: `http://127.0.0.1:5000`

---

## 🚀 Panduan Deployment ke Vercel

### Metode 1: Menggunakan Vercel Dashboard (Rekomendasi)
1. Push repository ini ke akun GitHub Anda:
   ```bash
   git push -u origin main
   ```
2. Buka dashboard [Vercel](https://vercel.com/) dan klik **Add New Project**.
3. Hubungkan akun GitHub Anda dan pilih repository `gacha-builder-api-learninglabs`.
4. Pada form konfigurasi:
   - **Framework Preset**: *Other*
   - **Root Directory**: `./` (Default)
5. Buka tab **Environment Variables** dan tambahkan:
   - **Key**: `DATABASE_URL`
   - **Value**: Connection string PostgreSQL Supabase Anda (pastikan menyertakan `?sslmode=require`).
6. Klik tombol **Deploy**. Vercel akan otomatis mendeteksi `api/index.py` dan mengeksekusi serverless WSGI.

### Metode 2: Menggunakan Vercel CLI
```bash
npm install -g vercel
vercel login
vercel
vercel env add DATABASE_URL
vercel --prod
```

---

## 📖 Dokumentasi Lengkap REST API

### Ringkasan Endpoint

| HTTP Method | Endpoint URL | Status Code Sukses | Deskripsi Singkat |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | `200 OK` | Katalog root metadata & navigasi API |
| `GET` | `/api/health` | `200 OK` / `503` | Status konektivitas database & uptime |
| `GET` | `/api/elements` | `200 OK` | Daftar 7 master elemen gacha |
| `GET` | `/api/weapons` | `200 OK` | Katalog senjata (filter rarity & type) |
| `GET` | `/api/teams` | `200 OK` | Komposisi tim party (`v_party_team_details`) |
| `GET` | `/api/characters` | `200 OK` | Daftar karakter (filter & sorting) |
| `GET` | `/api/characters/<id>` | `200 OK` | Detail karakter + daftar skills/talents |
| `POST` | `/api/characters` | `201 Created` | Tambah karakter baru dengan validasi |
| `PUT` | `/api/characters/<id>` | `200 OK` | Perbarui statistik/atribut karakter |
| `DELETE` | `/api/characters/<id>` | `200 OK` | Hapus karakter (proteksi FK conflict 409) |

---

### Detail Spesifikasi Endpoint

#### 1. GET `/api/characters`
Mengambil daftar seluruh karakter dengan dukungan filter query parameter.

- **Query Parameters**:
  - `element` *(string | integer, opsional)*: Nama elemen (misal `Pyro`) atau ID elemen (misal `1`).
  - `rarity` *(integer, opsional)*: Rarity bintang (`4` atau `5`).
  - `weapon_type` *(string, opsional)*: `Sword`, `Claymore`, `Polearm`, `Bow`, `Catalyst`.
  - `role` *(string, opsional)*: `Main DPS`, `Sub DPS`, `Support`, `Healer`, `Shielder`.
  - `search` *(string, opsional)*: Pencarian parsial substring pada nama karakter.
  - `sort_by` *(string, opsional)*: `id`, `nama_karakter`, `rarity`, `base_hp`, `base_atk`, `base_def` (default: `id`).
  - `order` *(string, opsional)*: `asc` atau `desc` (default: `asc`).

- **Contoh Request**:
  ```http
  GET /api/characters?element=Pyro&rarity=5 HTTP/1.1
  Host: 127.0.0.1:5000
  Accept: application/json
  ```

- **Contoh Response 200 OK**:
  ```json
  {
    "status": "success",
    "message": "Berhasil mengambil data karakter",
    "filters": {
      "element": "Pyro",
      "rarity": "5",
      "weapon_type": null,
      "role": null,
      "search": null,
      "sort_by": "id",
      "order": "asc"
    },
    "total": 1,
    "data": [
      {
        "id": 1,
        "nama_karakter": "Hu Tao",
        "rarity": 5,
        "tipe_senjata": "Polearm",
        "role_utama": "Main DPS",
        "base_hp": 15552,
        "base_atk": 106,
        "base_def": 876,
        "ascension_stat": "CRIT DMG",
        "id_elemen": 1,
        "nama_elemen": "Pyro",
        "warna_hex": "#FF4500"
      }
    ]
  }
  ```

---

#### 2. GET `/api/characters/<id>`
Mengambil data detail karakter berdasarkan ID numerik, beserta relasi talenta/skill dari tabel `skills_talents`.

- **Contoh Request**:
  ```http
  GET /api/characters/1 HTTP/1.1
  Host: 127.0.0.1:5000
  Accept: application/json
  ```

- **Contoh Response 200 OK**:
  ```json
  {
    "status": "success",
    "message": "Detail karakter berhasil ditemukan",
    "data": {
      "id": 1,
      "nama_karakter": "Hu Tao",
      "rarity": 5,
      "tipe_senjata": "Polearm",
      "role_utama": "Main DPS",
      "base_hp": 15552,
      "base_atk": 106,
      "base_def": 876,
      "ascension_stat": "CRIT DMG",
      "id_elemen": 1,
      "nama_elemen": "Pyro",
      "warna_hex": "#FF4500",
      "reaksi_efek": "Vaporize, Melt, Overloaded, Burgeon",
      "skills": [
        {
          "id": 1,
          "nama_talent": "Guide to Afterlife",
          "tipe_talent": "Elemental Skill",
          "deskripsi": "Masuk mode darah sekarat tapi ATK naik drastis",
          "cooldown_seconds": 16.0,
          "energy_cost": 0
        },
        {
          "id": 2,
          "nama_talent": "Spirit Soother",
          "tipe_talent": "Elemental Burst",
          "deskripsi": "Ngemper damage api nuklir sekalian heal tipis-tipis",
          "cooldown_seconds": 15.0,
          "energy_cost": 60
        }
      ]
    }
  }
  ```

- **Contoh Response 404 Not Found**:
  ```json
  {
    "status": "error",
    "message": "Karakter dengan ID 9999 tidak ditemukan"
  }
  ```

---

#### 3. POST `/api/characters`
Menambahkan data karakter baru. Dilengkapi validasi tipe data dan constraint basis data.

- **Request Body (JSON)**:
  ```json
  {
    "nama_karakter": "Navia",
    "id_elemen": 7,
    "rarity": 5,
    "tipe_senjata": "Claymore",
    "role_utama": "Main DPS",
    "base_hp": 12650,
    "base_atk": 352,
    "base_def": 793,
    "ascension_stat": "CRIT DMG"
  }
  ```

- **Contoh Response 201 Created**:
  ```json
  {
    "status": "success",
    "message": "Karakter 'Navia' berhasil dibuat",
    "data": {
      "id": 8,
      "id_elemen": 7,
      "nama_karakter": "Navia",
      "rarity": 5,
      "tipe_senjata": "Claymore",
      "role_utama": "Main DPS",
      "base_hp": 12650,
      "base_atk": 352,
      "base_def": 793,
      "ascension_stat": "CRIT DMG",
      "nama_elemen": "Geo",
      "warna_hex": "#DAA520"
    }
  }
  ```

- **Contoh Response 400 Bad Request (Validasi Gagal)**:
  ```json
  {
    "status": "error",
    "message": "Validasi input gagal",
    "errors": [
      "Field 'rarity' wajib bernilai 4 atau 5",
      "Field 'tipe_senjata' harus salah satu dari: Bow, Catalyst, Claymore, Polearm, Sword",
      "Field 'base_hp' wajib berupa integer positif (> 0)"
    ]
  }
  ```

---

#### 4. PUT `/api/characters/<id>`
Memperbarui statistik atau data dari karakter yang sudah ada.

- **Request Body (JSON)**:
  ```json
  {
    "base_atk": 350,
    "role_utama": "Main DPS",
    "ascension_stat": "Pyro DMG Bonus"
  }
  ```

- **Contoh Response 200 OK**:
  ```json
  {
    "status": "success",
    "message": "Data karakter ID 7 berhasil diperbarui",
    "data": {
      "id": 7,
      "id_elemen": 1,
      "nama_karakter": "Bennett",
      "rarity": 4,
      "tipe_senjata": "Sword",
      "role_utama": "Main DPS",
      "base_hp": 12397,
      "base_atk": 350,
      "base_def": 771,
      "ascension_stat": "Pyro DMG Bonus",
      "nama_elemen": "Pyro",
      "warna_hex": "#FF4500"
    }
  }
  ```

---

#### 5. DELETE `/api/characters/<id>`
Menghapus karakter dari sistem.

- **Kasus Sukses (200 OK)**:
  Karakter berhasil dihapus jika tidak terikat di tabel inventory pemain:
  ```json
  {
    "status": "success",
    "message": "Karakter 'Navia' (ID 8) berhasil dihapus",
    "deleted_id": 8
  }
  ```

- **Kasus Pelanggaran Foreign Key (409 Conflict)**:
  Jika karakter masih terdaftar pada inventori pemain (`player_inventory_characters` dengan constraint `ON DELETE RESTRICT`):
  ```json
  {
    "status": "error",
    "message": "Tidak dapat menghapus karakter ID 1 karena masih terdaftar dalam inventori karakter pemain (Foreign Key Constraint: player_inventory_characters).",
    "error_code": "FOREIGN_KEY_VIOLATION"
  }
  ```

---

#### 6. GET `/api/teams`
Mengambil komposisi formasi tim dari PostgreSQL View `v_party_team_details`.

- **Contoh Response 200 OK**:
  ```json
  {
    "status": "success",
    "message": "Berhasil mengambil detail formasi tim",
    "total_teams": 1,
    "total_slots": 4,
    "data": [
      {
        "nama_party": "Hu Tao Darah Sekarat Asal Jangan Kena Senggol",
        "username": "izzul",
        "in_game_uid": "801992026",
        "members": [
          {
            "slot_position": 1,
            "nama_karakter": "Hu Tao",
            "nama_elemen": "Pyro",
            "character_level": 90,
            "constellation_level": 1,
            "nama_senjata": "Staff of Homa",
            "role_dalam_party": "Main DPS yang selalu sekarat"
          },
          {
            "slot_position": 2,
            "nama_karakter": "Furina",
            "nama_elemen": "Hydro",
            "character_level": 90,
            "constellation_level": 2,
            "nama_senjata": "Splendor of Tranquil Waters",
            "role_dalam_party": "Buffer air penyedot darah"
          }
        ]
      }
    ]
  }
  ```

---

## 🧪 Pengujian Otomatis (Automated Testing)

Proyek ini dilengkapi test suite komprehensif pada file `test_api.py` yang mencakup **36 skenario pengujian** menggunakan modul bawaan `unittest` dan Flask Test Client:

```bash
python test_api.py
```

### Hasil Eksekusi Test:
```text
test_01_root_endpoint (__main__.GachaApiTestCase) ... ok
test_02_health_check_endpoint (__main__.GachaApiTestCase) ... ok
test_03_get_elements (__main__.GachaApiTestCase) ... ok
test_04_get_weapons_and_filters (__main__.GachaApiTestCase) ... ok
test_05_get_teams_view (__main__.GachaApiTestCase) ... ok
test_06_get_characters_list (__main__.GachaApiTestCase) ... ok
test_07_get_characters_filter_by_element (__main__.GachaApiTestCase) ... ok
test_08_get_characters_filter_by_rarity (__main__.GachaApiTestCase) ... ok
test_09_get_character_detail_success (__main__.GachaApiTestCase) ... ok
test_10_get_character_detail_not_found (__main__.GachaApiTestCase) ... ok
test_11_create_character_success (__main__.GachaApiTestCase) ... ok
test_12_create_character_missing_fields (__main__.GachaApiTestCase) ... ok
test_13_create_character_invalid_rarity (__main__.GachaApiTestCase) ... ok
test_14_create_character_invalid_weapon_type (__main__.GachaApiTestCase) ... ok
test_15_create_character_invalid_element_fk (__main__.GachaApiTestCase) ... ok
test_16_update_character_success (__main__.GachaApiTestCase) ... ok
test_17_update_character_not_found (__main__.GachaApiTestCase) ... ok
test_18_update_character_empty_payload (__main__.GachaApiTestCase) ... ok
test_19_delete_character_not_found (__main__.GachaApiTestCase) ... ok
test_20_delete_character_fk_conflict (__main__.GachaApiTestCase) ... ok
test_21_delete_character_success (__main__.GachaApiTestCase) ... ok
test_22_unknown_route_returns_404 (__main__.GachaApiTestCase) ... ok
test_23_method_not_allowed_returns_405 (__main__.GachaApiTestCase) ... ok
test_24_sort_by_sql_injection_defense (__main__.GachaApiTestCase) ... ok
test_25_post_negative_stat_rejected (__main__.GachaApiTestCase) ... ok
test_26_post_invalid_json_format (__main__.GachaApiTestCase) ... ok
test_27_put_update_invalid_element_id (__main__.GachaApiTestCase) ... ok
test_28_put_update_invalid_role (__main__.GachaApiTestCase) ... ok
test_29_search_character_substring (__main__.GachaApiTestCase) ... ok
test_30_get_characters_filter_role_and_weapon (__main__.GachaApiTestCase) ... ok
test_31_post_rejects_null_string_fields (__main__.GachaApiTestCase) ... ok
test_32_post_and_put_rejects_boolean_stats (__main__.GachaApiTestCase) ... ok
test_33_put_rejects_null_name (__main__.GachaApiTestCase) ... ok
test_34_sorting_order_characters_and_weapons (__main__.GachaApiTestCase) ... ok
test_35_trailing_slash_normalization (__main__.GachaApiTestCase) ... ok
test_36_case_insensitive_domain_normalization (__main__.GachaApiTestCase) ... ok

----------------------------------------------------------------------
Ran 36 tests in 0.143s

OK
```

---

## 📬 Impor Postman / Thunder Client

File koleksi Postman v2.1 telah disertakan di root repositori: `postman_collection.json`.

1. Buka aplikasi **Postman** atau ekstensi **Thunder Client** di VS Code.
2. Klik tombol **Import**.
3. Pilih file `postman_collection.json`.
4. Koleksi akan otomatis terisi dengan folder:
   - `0. Root & Catalog`
   - `1. Health & System`
   - `2. Master Data (Elements & Weapons)`
   - `3. Team Builder (Joined View)`
   - `4. Characters CRUD` (Lengkap dengan skenario 200, 201, 400, 404, 409).
5. Atur variabel `{{baseUrl}}` ke `http://127.0.0.1:5000` (lokal) atau URL deployment Vercel Anda.

---

## 📋 Matriks Pemenuhan Kriteria Rubrik Tugas

| No | Kriteria Rubrik Tugas Akhir | Implementasi Teknis dalam Proyek | Status |
| :---: | :--- | :--- | :---: |
| **1** | **Minimal 5 Tabel Relasional** | Disediakan **14 Tabel** terintegrasi penuh pada `database/schema.sql`. | ✅ **Sangat Terpenuhi** (14/5 Tabel) |
| **2** | **Relasi 1 : 1** | `players (1) <-> player_profiles (1)` dengan unique foreign key constraint. | ✅ **Terpenuhi** |
| **3** | **Relasi 1 : N** | `elements (1) -> characters (N)`, `characters (1) -> skills_talents (N)`, dll. | ✅ **Terpenuhi** |
| **4** | **Relasi N : N (Junction)** | `party_teams <-> characters` via junction table `party_members` dan `player_inventory_characters`. | ✅ **Terpenuhi** |
| **5** | **Core CRUD REST API** | Operasi `GET`, `POST`, `PUT`, `DELETE` pada `/api/characters` dengan status code `200`, `201`, `400`, `404`, `409`. | ✅ **Terpenuhi** |
| **6** | **Integrity & Error Handling** | Menangkap `ForeignKeyViolation` saat DELETE dan mengembalikan pesan ramah HTTP 409 Conflict. | ✅ **Terpenuhi** |
| **7** | **Serverless Cloud Deployment** | Arsitektur WSGI `api/index.py` + `vercel.json` siap di-deploy ke Vercel Serverless. | ✅ **Terpenuhi** |
| **8** | **Dokumentasi & Testing** | Diagram ERD Mermaid, panduan setup, Postman v2.1 collection, dan 36 skenario unit testing otomatis. | ✅ **Terpenuhi** |

---

## 👨‍💻 Identitas Pengembang

- **Nama**: Muhammad Izzul Islam
- **Akun GitHub**: [@lunizura](https://github.com/lunizura)
- **Repositori**: [gacha-builder-api-learninglabs](https://github.com/lunizura/gacha-builder-api-learninglabs)
- **Topik Penugasan**: Backend Development & Cloud Database (Learning Labs)
