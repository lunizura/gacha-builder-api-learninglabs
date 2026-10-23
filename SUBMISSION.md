# Pengumpulan Tugas Akhir: REST API Flask & PostgreSQL
**Program**: Learning Labs — Backend Development  
**Nama**: Muhammad Izzul Islam  
**Akun GitHub**: [@lunizura](https://github.com/lunizura)  
**Tema Proyek**: Gacha Character & Team Builder Platform REST API  

---

### 📌 Berkas & Tautan Pengumpulan

1. **Link Repository (GitHub)**:  
   https://github.com/lunizura/gacha-builder-api-learninglabs

2. **Link Deployment (Vercel)**:  
   https://gacha-builder-api-learninglabs.vercel.app

3. **Dokumentasi API**:  
   https://github.com/lunizura/gacha-builder-api-learninglabs#readme  
   *(Terdokumentasi lengkap di `README.md`, memuat diagram relasi database Mermaid ERD, spesifikasi lengkap parameter/header/body/response seluruh endpoint HTTP, panduan setup lokal, serta tabel evaluasi pemenuhan syarat minimum vs fitur tambahan).*

4. **Bukti Pengujian (Export Collection)**:  
   https://github.com/lunizura/gacha-builder-api-learninglabs/blob/main/postman_collection.json  
   *(File koleksi Postman v2.1 berisi 16 requests terstruktur yang dilengkapi automated test assertions `pm.test` untuk memvalidasi status code `200`, `201`, `400`, `404`, dan `409`).*

---

### 💡 Ringkasan Teknis Singkat

- **Stack**: Python (Flask 3.1), PostgreSQL di Supabase (via driver native `psycopg2` & `RealDictCursor`), Vercel Serverless WSGI.
- **Basis Data**: Arsitektur relasional komprehensif mencakup relasi 1:1, 1:N, dan N:N dengan integritas *foreign key* dan *check constraints*.
- **Endpoint Utama**:
  - `GET /` — API catalog & route index
  - `GET /api/health` — Live server uptime & PostgreSQL connection health check
  - `GET /api/characters` — List karakter dengan filter multi-parameter (`element`, `rarity`, `role`, `weapon_type`, `search`) & sorting
  - `GET /api/characters/<id>` — Detail karakter beserta relasi skill/talent
  - `POST /api/characters` — Create karakter baru dengan validasi domain ketat (`201 Created`)
  - `PUT /api/characters/<id>` — Update karakter (`200 OK`)
  - `DELETE /api/characters/<id>` — Delete dengan relational integrity protection (`409 Conflict` jika terikat data inventori pemain)
  - `GET /api/elements` — Master 7 data elemen
  - `GET /api/weapons` — Master katalog senjata
  - `GET /api/teams` — Multi-table JOIN view (`v_party_team_details`) formasi tim pemain
- **Automated Testing**: 36 skenario unit & integration test pada `test_api.py` (100% lulus / regression-free).
