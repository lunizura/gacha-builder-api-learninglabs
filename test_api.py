"""
Automated Test Suite for Gacha Character & Team Builder REST API.
Menjalankan pengujian komprehensif untuk seluruh endpoint REST API:
- Root & Health Check
- Master Data (Elements, Weapons, Teams)
- Character CRUD (Create, Read, Update, Delete)
- Validasi Input & Constraint Domain
- Foreign Key Violation & Error Handling (400, 404, 405, 409)
"""

import os
import unittest
import json

# Pastikan menggunakan mock database jika DATABASE_URL tidak disediakan
if not os.environ.get("DATABASE_URL"):
    os.environ["USE_MOCK_DB"] = "true"

from api.index import app
from api.db import mock_storage


class GachaApiTestCase(unittest.TestCase):
    def setUp(self):
        """
        Setup Flask test client dan reset state mock storage sebelum tiap pengujian.
        """
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        mock_storage.reset()

    # ==========================================================================
    # 1. PENGUJIAN ROOT & HEALTH CHECK
    # ==========================================================================

    def test_01_root_endpoint(self):
        """Memastikan endpoint GET / mengembalikan metadata dan navigasi API."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "operational")
        self.assertIn("documentation", data)
        self.assertIn("endpoints", data["documentation"])

    def test_02_health_check_endpoint(self):
        """Memastikan endpoint GET /api/health mengembalikan status database dan uptime."""
        response = self.client.get("/api/health")
        self.assertIn(response.status_code, [200, 503])
        data = response.get_json()
        self.assertIn("status", data)
        self.assertIn("database", data)
        self.assertIn("uptime_seconds", data)

    # ==========================================================================
    # 2. PENGUJIAN MASTER DATA (ELEMENTS, WEAPONS, TEAMS)
    # ==========================================================================

    def test_03_get_elements(self):
        """Memastikan GET /api/elements mengembalikan seluruh 7 master element."""
        response = self.client.get("/api/elements")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(data["total"], 7)
        element_names = [e["nama_elemen"] for e in data["data"]]
        self.assertIn("Pyro", element_names)
        self.assertIn("Hydro", element_names)
        self.assertIn("Geo", element_names)

    def test_04_get_weapons_and_filters(self):
        """Memastikan GET /api/weapons dapat mengambil senjata dan menerapkan query filters."""
        # Ambil semua senjata
        response = self.client.get("/api/weapons")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(data["total"], 6)

        # Filter berdasarkan rarity
        resp_r5 = self.client.get("/api/weapons?rarity=5")
        self.assertEqual(resp_r5.status_code, 200)
        for w in resp_r5.get_json()["data"]:
            self.assertEqual(w["rarity"], 5)

        # Filter berdasarkan weapon_type
        resp_sword = self.client.get("/api/weapons?weapon_type=Sword")
        self.assertEqual(resp_sword.status_code, 200)
        for w in resp_sword.get_json()["data"]:
            self.assertEqual(w["tipe_senjata"].lower(), "sword")

        # Invalid rarity
        resp_bad = self.client.get("/api/weapons?rarity=invalid")
        self.assertEqual(resp_bad.status_code, 400)

    def test_05_get_teams_view(self):
        """Memastikan GET /api/teams mengembalikan formasi tim dari view v_party_team_details."""
        response = self.client.get("/api/teams")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(data["total_teams"], 1)
        first_team = data["data"][0]
        self.assertIn("nama_party", first_team)
        self.assertIn("members", first_team)
        self.assertGreater(len(first_team["members"]), 0)

    # ==========================================================================
    # 3. PENGUJIAN READ CHARACTERS & QUERY PARAMS
    # ==========================================================================

    def test_06_get_characters_list(self):
        """Memastikan GET /api/characters mengembalikan daftar karakter default."""
        response = self.client.get("/api/characters")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(data["total"], 7)

    def test_07_get_characters_filter_by_element(self):
        """Memastikan filter karakter berdasarkan elemen (?element=Pyro atau ?element=1)."""
        # Filter by element name
        resp_pyro = self.client.get("/api/characters?element=Pyro")
        self.assertEqual(resp_pyro.status_code, 200)
        for c in resp_pyro.get_json()["data"]:
            self.assertEqual(c["nama_elemen"], "Pyro")

        # Filter by element ID
        resp_el1 = self.client.get("/api/characters?element=1")
        self.assertEqual(resp_el1.status_code, 200)
        for c in resp_el1.get_json()["data"]:
            self.assertEqual(c["id_elemen"], 1)

    def test_08_get_characters_filter_by_rarity(self):
        """Memastikan filter karakter berdasarkan rarity (?rarity=4 atau 5)."""
        resp_r4 = self.client.get("/api/characters?rarity=4")
        self.assertEqual(resp_r4.status_code, 200)
        for c in resp_r4.get_json()["data"]:
            self.assertEqual(c["rarity"], 4)

        # Invalid rarity (e.g. 3) -> 400 Bad Request
        resp_bad = self.client.get("/api/characters?rarity=3")
        self.assertEqual(resp_bad.status_code, 400)

    def test_09_get_character_detail_success(self):
        """Memastikan GET /api/characters/<id> mengembalikan relasi elemen dan skill."""
        response = self.client.get("/api/characters/1")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        char = data["data"]
        self.assertEqual(char["id"], 1)
        self.assertEqual(char["nama_karakter"], "Hu Tao")
        self.assertEqual(char["nama_elemen"], "Pyro")
        self.assertIn("skills", char)
        self.assertGreater(len(char["skills"]), 0)

    def test_10_get_character_detail_not_found(self):
        """Memastikan GET /api/characters/9999 mengembalikan 404 Not Found."""
        response = self.client.get("/api/characters/9999")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["status"], "error")
        self.assertIn("tidak ditemukan", data["message"])

    # ==========================================================================
    # 4. PENGUJIAN CREATE CHARACTER (POST) & VALIDATION
    # ==========================================================================

    def test_11_create_character_success(self):
        """Memastikan POST /api/characters berhasil menambahkan karakter baru (201 Created)."""
        payload = {
            "nama_karakter": "Navia",
            "id_elemen": 7,  # Geo
            "rarity": 5,
            "tipe_senjata": "Claymore",
            "role_utama": "Main DPS",
            "base_hp": 12650,
            "base_atk": 352,
            "base_def": 793,
            "ascension_stat": "CRIT DMG"
        }
        response = self.client.post(
            "/api/characters",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["nama_karakter"], "Navia")
        self.assertEqual(data["data"]["nama_elemen"], "Geo")
        self.assertIn("id", data["data"])

    def test_12_create_character_missing_fields(self):
        """Memastikan POST dengan field tidak lengkap mengembalikan 400 Bad Request."""
        payload = {
            "nama_karakter": "Incomplete Char"
            # Missing id_elemen, rarity, stats, dll
        }
        response = self.client.post(
            "/api/characters",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["status"], "error")
        self.assertIn("errors", data)
        self.assertGreater(len(data["errors"]), 0)

    def test_13_create_character_invalid_rarity(self):
        """Memastikan POST dengan rarity tidak valid (misal 3 atau 6) mengembalikan 400."""
        payload = {
            "nama_karakter": "Test Char",
            "id_elemen": 1,
            "rarity": 3,  # Invalid, harus 4 atau 5
            "tipe_senjata": "Sword",
            "role_utama": "Main DPS",
            "base_hp": 10000,
            "base_atk": 200,
            "base_def": 500,
            "ascension_stat": "ATK%"
        }
        response = self.client.post(
            "/api/characters",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_14_create_character_invalid_weapon_type(self):
        """Memastikan POST dengan tipe_senjata tidak valid mengembalikan 400."""
        payload = {
            "nama_karakter": "Gunner Char",
            "id_elemen": 1,
            "rarity": 5,
            "tipe_senjata": "Gun",  # Invalid, bukan tipe senjata Genshin
            "role_utama": "Main DPS",
            "base_hp": 10000,
            "base_atk": 200,
            "base_def": 500,
            "ascension_stat": "ATK%"
        }
        response = self.client.post(
            "/api/characters",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_15_create_character_invalid_element_fk(self):
        """Memastikan POST dengan id_elemen yang tidak ada di master elements mengembalikan 400."""
        payload = {
            "nama_karakter": "Alien Char",
            "id_elemen": 999,  # Elemen tidak ada
            "rarity": 5,
            "tipe_senjata": "Sword",
            "role_utama": "Main DPS",
            "base_hp": 10000,
            "base_atk": 200,
            "base_def": 500,
            "ascension_stat": "ATK%"
        }
        response = self.client.post(
            "/api/characters",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    # ==========================================================================
    # 5. PENGUJIAN UPDATE CHARACTER (PUT)
    # ==========================================================================

    def test_16_update_character_success(self):
        """Memastikan PUT /api/characters/<id> berhasil memperbarui data (200 OK)."""
        update_payload = {
            "base_atk": 350,
            "role_utama": "Main DPS",
            "ascension_stat": "Pyro DMG Bonus"
        }
        response = self.client.put(
            "/api/characters/7",  # Bennett
            data=json.dumps(update_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["base_atk"], 350)
        self.assertEqual(data["data"]["role_utama"], "Main DPS")

    def test_17_update_character_not_found(self):
        """Memastikan PUT ke ID yang tidak ada mengembalikan 404 Not Found."""
        response = self.client.put(
            "/api/characters/9999",
            data=json.dumps({"base_atk": 300}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_18_update_character_empty_payload(self):
        """Memastikan PUT dengan payload kosong mengembalikan 400 Bad Request."""
        response = self.client.put(
            "/api/characters/1",
            data=json.dumps({}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    # ==========================================================================
    # 6. PENGUJIAN DELETE CHARACTER & FOREIGN KEY INTEGRITY
    # ==========================================================================

    def test_19_delete_character_not_found(self):
        """Memastikan DELETE ke ID tidak terdaftar mengembalikan 404 Not Found."""
        response = self.client.delete("/api/characters/9999")
        self.assertEqual(response.status_code, 404)

    def test_20_delete_character_fk_conflict(self):
        """
        Memastikan DELETE karakter yang terikat dalam player inventory menghasilkan
        409 Conflict dengan penjelasan constraint yang ramah.
        """
        # ID 1 (Hu Tao) digunakan dalam player_inventory_characters
        response = self.client.delete("/api/characters/1")
        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertEqual(data["status"], "error")
        self.assertIn("FOREIGN_KEY_VIOLATION", data.get("error_code", ""))

    def test_21_delete_character_success(self):
        """
        Memastikan DELETE karakter yang tidak terikat inventori berhasil dihapus (200 OK).
        """
        # Buat karakter sementara terlebih dahulu
        payload = {
            "nama_karakter": "Temporary Test Char",
            "id_elemen": 1,
            "rarity": 4,
            "tipe_senjata": "Bow",
            "role_utama": "Support",
            "base_hp": 9000,
            "base_atk": 150,
            "base_def": 400,
            "ascension_stat": "Energy Recharge"
        }
        create_resp = self.client.post(
            "/api/characters",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(create_resp.status_code, 201)
        created_id = create_resp.get_json()["data"]["id"]

        # Hapus karakter tersebut
        del_resp = self.client.delete(f"/api/characters/{created_id}")
        self.assertEqual(del_resp.status_code, 200)
        self.assertEqual(del_resp.get_json()["status"], "success")

        # Pastikan sudah tidak ada lagi
        get_resp = self.client.get(f"/api/characters/{created_id}")
        self.assertEqual(get_resp.status_code, 404)

    # ==========================================================================
    # 7. PENGUJIAN ERROR HANDLERS (404 & 405)
    # ==========================================================================

    def test_22_unknown_route_returns_404(self):
        """Memastikan rute antah berantah menghasilkan 404 JSON standard."""
        response = self.client.get("/api/unknown_resource")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["error_code"], "NOT_FOUND")

    def test_23_method_not_allowed_returns_405(self):
        """Memastikan request method yang tidak didukung mengembalikan 405 JSON."""
        response = self.client.delete("/api/elements")
        self.assertEqual(response.status_code, 405)
        data = response.get_json()
        self.assertEqual(data["error_code"], "METHOD_NOT_ALLOWED")

    # ==========================================================================
    # 8. PENGUJIAN BOUNDARY, SECURITY & EDGE CASES
    # ==========================================================================

    def test_24_sort_by_sql_injection_defense(self):
        """Memastikan parameter sort_by aman dari SQL Injection dan hanya menerima whitelist."""
        response = self.client.get("/api/characters?sort_by=id;+DROP+TABLE+characters;--&order=desc")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # Harus fallback ke 'id' yang aman
        self.assertEqual(data["filters"]["sort_by"], "id")

    def test_25_post_negative_stat_rejected(self):
        """Memastikan base_hp, base_atk, base_def <= 0 ditolak dengan 400 Bad Request."""
        payload = {
            "nama_karakter": "Zero HP Character",
            "id_elemen": 1,
            "rarity": 4,
            "tipe_senjata": "Bow",
            "role_utama": "Support",
            "base_hp": 0,  # Invalid
            "base_atk": -50,  # Invalid
            "base_def": 100,
            "ascension_stat": "ATK%"
        }
        response = self.client.post("/api/characters", json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("errors", data)

    def test_26_post_invalid_json_format(self):
        """Memastikan request body non-json atau format list ditolak dengan 400."""
        response = self.client.post("/api/characters", data="plain text data", content_type="text/plain")
        self.assertEqual(response.status_code, 400)

        response_list = self.client.post("/api/characters", json=[{"id": 1}])
        self.assertEqual(response_list.status_code, 400)

    def test_27_put_update_invalid_element_id(self):
        """Memastikan PUT dengan id_elemen yang tidak ada mengembalikan 400."""
        response = self.client.put("/api/characters/1", json={"id_elemen": 9999})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("tidak ditemukan", data["message"])

    def test_28_put_update_invalid_role(self):
        """Memastikan PUT dengan role_utama yang tidak valid mengembalikan 400."""
        response = self.client.put("/api/characters/1", json={"role_utama": "Sniper"})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("errors", data)

    def test_29_search_character_substring(self):
        """Memastikan filter search case-insensitive dan mencocokkan substring nama karakter."""
        response = self.client.get("/api/characters?search=tao")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["data"][0]["nama_karakter"], "Hu Tao")

    def test_30_get_characters_filter_role_and_weapon(self):
        """Memastikan kombinasi filter role dan weapon_type berfungsi bersamaan."""
        response = self.client.get("/api/characters?role=Main+DPS&weapon_type=Polearm")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        for c in data["data"]:
            self.assertEqual(c["role_utama"], "Main DPS")
            self.assertEqual(c["tipe_senjata"], "Polearm")

    def test_31_post_rejects_null_string_fields(self):
        """Memastikan field string bernilai null (JSON) ditolak dengan 400 Bad Request."""
        payload = {
            "nama_karakter": None,
            "id_elemen": 1,
            "rarity": 5,
            "tipe_senjata": "Sword",
            "role_utama": "Main DPS",
            "base_hp": 10000,
            "base_atk": 250,
            "base_def": 700,
            "ascension_stat": None
        }
        resp = self.client.post("/api/characters", json=payload)
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("errors", data)
        errors_str = " ".join(data["errors"])
        self.assertIn("nama_karakter", errors_str)
        self.assertIn("ascension_stat", errors_str)

    def test_32_post_and_put_rejects_boolean_stats(self):
        """Memastikan passing tipe boolean true/false untuk stat numerik ditolak (400)."""
        # Test pada POST
        post_payload = {
            "nama_karakter": "Bool Test",
            "id_elemen": True,
            "rarity": 5,
            "tipe_senjata": "Sword",
            "role_utama": "Main DPS",
            "base_hp": True,
            "base_atk": True,
            "base_def": True,
            "ascension_stat": "ATK"
        }
        post_resp = self.client.post("/api/characters", json=post_payload)
        self.assertEqual(post_resp.status_code, 400)

        # Test pada PUT
        put_resp = self.client.put("/api/characters/1", json={"base_hp": True})
        self.assertEqual(put_resp.status_code, 400)

    def test_33_put_rejects_null_name(self):
        """Memastikan PUT dengan nama_karakter null ditolak (400 Bad Request)."""
        resp = self.client.put("/api/characters/1", json={"nama_karakter": None})
        self.assertEqual(resp.status_code, 400)

    def test_34_sorting_order_characters_and_weapons(self):
        """Memastikan sorting data karakter dan senjata berjalan dengan urutan yang benar."""
        # Sorting characters by base_atk descending
        resp_c = self.client.get("/api/characters?sort_by=base_atk&order=desc")
        self.assertEqual(resp_c.status_code, 200)
        atks = [c["base_atk"] for c in resp_c.get_json()["data"]]
        self.assertEqual(atks, sorted(atks, reverse=True))

        # Sorting weapons (default by rarity DESC, base_atk DESC, id ASC)
        resp_w = self.client.get("/api/weapons")
        self.assertEqual(resp_w.status_code, 200)
        w_data = resp_w.get_json()["data"]
        rarities = [w["rarity"] for w in w_data]
        self.assertEqual(rarities, sorted(rarities, reverse=True))

    def test_35_trailing_slash_normalization(self):
        """Memastikan request dengan trailing slash (/api/characters/) dilayani tanpa error 308/404."""
        resp = self.client.get("/api/characters/")
        self.assertEqual(resp.status_code, 200)

        resp_el = self.client.get("/api/elements/")
        self.assertEqual(resp_el.status_code, 200)

    def test_36_case_insensitive_domain_normalization(self):
        """Memastikan tipe senjata dan role dengan variasi huruf kecil dinormalisasi secara otomatis."""
        payload = {
            "nama_karakter": "Chevreuse",
            "id_elemen": 1,
            "rarity": 4,
            "tipe_senjata": "polearm",  # Huruf kecil
            "role_utama": "healer",     # Huruf kecil
            "base_hp": 11980,
            "base_atk": 193,
            "base_def": 605,
            "ascension_stat": "HP%"
        }
        resp = self.client.post("/api/characters", json=payload)
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()["data"]
        self.assertEqual(data["tipe_senjata"], "Polearm")
        self.assertEqual(data["role_utama"], "Healer")


if __name__ == "__main__":
    unittest.main(verbosity=2)
