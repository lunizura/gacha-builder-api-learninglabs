import os
import time
from contextlib import contextmanager
from decimal import Decimal
from datetime import date, datetime
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Muat environment variable dari .env jika ada
load_dotenv()

# State flag untuk pengujian mock jika DATABASE_URL tidak tersedia
USE_MOCK_DB = os.environ.get("USE_MOCK_DB", "").lower() in ("true", "1", "yes")


def serialize_data(data):
    """
    Serialisasi objek Python/PostgreSQL (Decimal, datetime, date, RealDictRow)
    menjadi format JSON-compliant native.
    """
    if isinstance(data, list):
        return [serialize_data(item) for item in data]
    elif isinstance(data, dict):
        return {key: serialize_data(value) for key, value in data.items()}
    elif isinstance(data, Decimal):
        return int(data) if data % 1 == 0 else float(data)
    elif isinstance(data, (datetime, date)):
        return data.isoformat()
    return data


def get_database_url():
    """
    Mendapatkan dan menormalisasi connection string PostgreSQL / Supabase.
    """
    url = os.environ.get("DATABASE_URL", "").strip()
    if not url:
        return None
    # Normalisasi postgres:// -> postgresql:// (kompatibilitas psycopg2)
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    return url


def get_db_connection():
    """
    Membuka koneksi ke PostgreSQL database menggunakan psycopg2.
    """
    db_url = get_database_url()
    if not db_url:
        raise ConnectionError(
            "DATABASE_URL tidak ditemukan pada environment variable (.env). "
            "Harap konfigurasikan DATABASE_URL dari Supabase / PostgreSQL."
        )

    # Tambahkan sslmode=require jika belum ada dan bukan localhost
    conn_params = {}
    if "sslmode" not in db_url.lower() and "localhost" not in db_url and "127.0.0.1" not in db_url:
        conn_params["sslmode"] = "require"
    conn_params["connect_timeout"] = 10

    conn = psycopg2.connect(db_url, **conn_params)
    return conn


@contextmanager
def get_db_cursor(commit=False):
    """
    Context manager untuk cursor database dengan RealDictCursor.
    Otomatis melakukan commit jika commit=True, rollback jika terjadi error,
    dan menutup koneksi setelah selesai.
    """
    if USE_MOCK_DB or not get_database_url():
        # Gunakan Mock Storage jika mode mock aktif atau DATABASE_URL belum ada
        yield from mock_storage.get_cursor(commit=commit)
        return

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def check_db_health():
    """
    Memeriksa status konektivitas database untuk endpoint /api/health.
    """
    if USE_MOCK_DB or not get_database_url():
        return {
            "status": "connected (mock)",
            "provider": "In-Memory Test Store",
            "latency_ms": 0.5
        }

    start_time = time.time()
    try:
        with get_db_cursor(commit=False) as cur:
            cur.execute("SELECT 1 AS ping;")
            cur.fetchone()
        latency = round((time.time() - start_time) * 1000, 2)
        return {
            "status": "connected",
            "provider": "PostgreSQL / Supabase",
            "latency_ms": latency
        }
    except Exception as e:
        return {
            "status": "disconnected",
            "provider": "PostgreSQL / Supabase",
            "error": str(e)
        }


# ==============================================================================
# IN-MEMORY MOCK STORAGE UNTUK TEST & OFFLINE VERIFICATION
# Berisi seed data persis seperti skema_database_gacha_builder_advanced.sql
# ==============================================================================

class MockStorage:
    def __init__(self):
        self.reset()

    def reset(self):
        self.elements = [
            {"id": 1, "nama_elemen": "Pyro", "warna_hex": "#FF4500", "reaksi_efek": "Vaporize, Melt, Overloaded, Burgeon"},
            {"id": 2, "nama_elemen": "Hydro", "warna_hex": "#1E90FF", "reaksi_efek": "Vaporize, Electro-Charged, Bloom, Freeze"},
            {"id": 3, "nama_elemen": "Anemo", "warna_hex": "#40E0D0", "reaksi_efek": "Swirl"},
            {"id": 4, "nama_elemen": "Electro", "warna_hex": "#8A2BE2", "reaksi_efek": "Aggravate, Hyperbloom, Electro-Charged"},
            {"id": 5, "nama_elemen": "Dendro", "warna_hex": "#32CD32", "reaksi_efek": "Bloom, Catalyze, Spread, Hyperbloom"},
            {"id": 6, "nama_elemen": "Cryo", "warna_hex": "#00FFFF", "reaksi_efek": "Freeze, Melt, Superconduct"},
            {"id": 7, "nama_elemen": "Geo", "warna_hex": "#DAA520", "reaksi_efek": "Crystallize"},
        ]
        self.characters = [
            {"id": 1, "id_elemen": 1, "nama_karakter": "Hu Tao", "rarity": 5, "tipe_senjata": "Polearm", "role_utama": "Main DPS", "base_hp": 15552, "base_atk": 106, "base_def": 876, "ascension_stat": "CRIT DMG"},
            {"id": 2, "id_elemen": 2, "nama_karakter": "Furina", "rarity": 5, "tipe_senjata": "Sword", "role_utama": "Sub DPS", "base_hp": 15307, "base_atk": 244, "base_def": 696, "ascension_stat": "CRIT Rate"},
            {"id": 3, "id_elemen": 3, "nama_karakter": "Kaedehara Kazuha", "rarity": 5, "tipe_senjata": "Sword", "role_utama": "Support", "base_hp": 13348, "base_atk": 297, "base_def": 807, "ascension_stat": "Elemental Mastery"},
            {"id": 4, "id_elemen": 7, "nama_karakter": "Zhongli", "rarity": 5, "tipe_senjata": "Polearm", "role_utama": "Shielder", "base_hp": 14695, "base_atk": 251, "base_def": 738, "ascension_stat": "Geo DMG Bonus"},
            {"id": 5, "id_elemen": 4, "nama_karakter": "Raiden Shogun", "rarity": 5, "tipe_senjata": "Polearm", "role_utama": "Sub DPS", "base_hp": 12907, "base_atk": 337, "base_def": 789, "ascension_stat": "Energy Recharge"},
            {"id": 6, "id_elemen": 6, "nama_karakter": "Qiqi", "rarity": 5, "tipe_senjata": "Sword", "role_utama": "Healer", "base_hp": 12118, "base_atk": 287, "base_def": 922, "ascension_stat": "Healing Bonus"},
            {"id": 7, "id_elemen": 1, "nama_karakter": "Bennett", "rarity": 4, "tipe_senjata": "Sword", "role_utama": "Support", "base_hp": 12397, "base_atk": 191, "base_def": 771, "ascension_stat": "Energy Recharge"},
        ]
        self.weapons = [
            {"id": 1, "nama_senjata": "Staff of Homa", "tipe_senjata": "Polearm", "rarity": 5, "base_atk": 608, "substat_type": "CRIT DMG", "substat_value": 66.20, "pasif_deskripsi": "Nambah HP 20% sama bonus ATK kalo darah di bawah 50%"},
            {"id": 2, "nama_senjata": "Splendor of Tranquil Waters", "tipe_senjata": "Sword", "rarity": 5, "base_atk": 542, "substat_type": "CRIT DMG", "substat_value": 88.20, "pasif_deskripsi": "Buff skill kalo HP naik turun"},
            {"id": 3, "nama_senjata": "Freedom-Sworn", "tipe_senjata": "Sword", "rarity": 5, "base_atk": 608, "substat_type": "Elemental Mastery", "substat_value": 198.00, "pasif_deskripsi": "Buff ATK buat satu tim setelah picu reaksi"},
            {"id": 4, "nama_senjata": "Black Tassel", "tipe_senjata": "Polearm", "rarity": 3, "base_atk": 354, "substat_type": "HP%", "substat_value": 46.90, "pasif_deskripsi": "Tombak slime murah meriah andalan tiang zhongli"},
            {"id": 5, "nama_senjata": "The Bell", "tipe_senjata": "Claymore", "rarity": 4, "base_atk": 510, "substat_type": "HP%", "substat_value": 41.30, "pasif_deskripsi": "Pedang terkutuk yang selalu nongol pas rate-off"},
            {"id": 6, "nama_senjata": "Debate Club", "tipe_senjata": "Claymore", "rarity": 3, "base_atk": 401, "substat_type": "ATK%", "substat_value": 35.20, "pasif_deskripsi": "Palu F2P buat gebuk hilichurl di awal game"},
        ]
        self.skills = [
            {"id": 1, "id_character": 1, "nama_talent": "Guide to Afterlife", "tipe_talent": "Elemental Skill", "deskripsi": "Masuk mode darah sekarat tapi ATK naik drastis", "cooldown_seconds": 16.0, "energy_cost": 0},
            {"id": 2, "id_character": 1, "nama_talent": "Spirit Soother", "tipe_talent": "Elemental Burst", "deskripsi": "Ngemper damage api nuklir sekalian heal tipis-tipis", "cooldown_seconds": 15.0, "energy_cost": 60},
            {"id": 3, "id_character": 2, "nama_talent": "Salon Solitaire", "tipe_talent": "Elemental Skill", "deskripsi": "Mangil kroco buat gebukin musuh tapi nyedot darah satu tim", "cooldown_seconds": 20.0, "energy_cost": 0},
            {"id": 4, "id_character": 6, "nama_talent": "Adeptus Art: Preserver of Fortune", "tipe_talent": "Elemental Burst", "deskripsi": "Nandain musuh pake jimat, penyelamat kalo lagi sekarat", "cooldown_seconds": 20.0, "energy_cost": 80},
        ]
        # Character IDs yang terikat di player_inventory_characters (tidak boleh didelete: FK restriction)
        self.inventory_character_ids = {1, 2, 3, 4, 5, 6, 7}
        self.teams_view = [
            {
                "username": "izzul",
                "in_game_uid": "801992026",
                "nama_party": "Hu Tao Darah Sekarat Asal Jangan Kena Senggol",
                "slot_position": 1,
                "nama_karakter": "Hu Tao",
                "nama_elemen": "Pyro",
                "character_level": 90,
                "constellation_level": 1,
                "nama_senjata": "Staff of Homa",
                "role_dalam_party": "Main DPS yang selalu sekarat"
            },
            {
                "username": "izzul",
                "in_game_uid": "801992026",
                "nama_party": "Hu Tao Darah Sekarat Asal Jangan Kena Senggol",
                "slot_position": 2,
                "nama_karakter": "Furina",
                "nama_elemen": "Hydro",
                "character_level": 90,
                "constellation_level": 2,
                "nama_senjata": "Splendor of Tranquil Waters",
                "role_dalam_party": "Buffer air penyedot darah"
            },
            {
                "username": "izzul",
                "in_game_uid": "801992026",
                "nama_party": "Hu Tao Darah Sekarat Asal Jangan Kena Senggol",
                "slot_position": 3,
                "nama_karakter": "Kaedehara Kazuha",
                "nama_elemen": "Anemo",
                "character_level": 90,
                "constellation_level": 0,
                "nama_senjata": "Freedom-Sworn",
                "role_dalam_party": "Tukang kumpulin musuh & shred resist"
            },
            {
                "username": "izzul",
                "in_game_uid": "801992026",
                "nama_party": "Hu Tao Darah Sekarat Asal Jangan Kena Senggol",
                "slot_position": 4,
                "nama_karakter": "Zhongli",
                "nama_elemen": "Geo",
                "character_level": 90,
                "constellation_level": 0,
                "nama_senjata": "Black Tassel",
                "role_dalam_party": "Bapak pelindung perisai anti mati"
            }
        ]
        self.next_char_id = 8

    def get_cursor(self, commit=False):
        yield MockCursor(self)


class MockCursor:
    def __init__(self, storage: MockStorage):
        self.storage = storage
        self._result = []
        self._rowcount = 0

    def execute(self, query, params=None):
        q = " ".join(query.strip().split())
        params = list(params) if params else []
        q_upper = q.upper()

        # ----------------------------------------------------------------------
        # 1. SELECT STATEMENTS
        # ----------------------------------------------------------------------
        if q_upper.startswith("SELECT"):
            # A. PING / HEALTH CHECK
            if "SELECT 1" in q_upper:
                self._result = [{"ping": 1}]
                self._rowcount = 1
                return

            # B. ELEMENTS TABLE
            if "FROM ELEMENTS" in q_upper:
                if "WHERE ID = %S" in q_upper or "WHERE ID = ?" in q_upper:
                    el_id = int(params[0])
                    found = [e for e in self.storage.elements if e["id"] == el_id]
                    self._result = found
                    self._rowcount = len(found)
                else:
                    self._result = list(self.storage.elements)
                    self._rowcount = len(self._result)
                return

            # C. WEAPONS TABLE
            if "FROM WEAPONS" in q_upper:
                res = list(self.storage.weapons)
                param_idx = 0
                if "RARITY = %S" in q_upper or "RARITY = ?" in q_upper:
                    rarity_val = int(params[param_idx])
                    param_idx += 1
                    res = [w for w in res if w["rarity"] == rarity_val]

                if "LOWER(TIPE_SENJATA) = LOWER(%S)" in q_upper or "TIPE_SENJATA = %S" in q_upper:
                    wt_val = str(params[param_idx]).lower()
                    param_idx += 1
                    res = [w for w in res if w["tipe_senjata"].lower() == wt_val]

                if "LOWER(NAMA_SENJATA) LIKE LOWER(%S)" in q_upper:
                    search_val = str(params[param_idx]).replace("%", "").lower()
                    param_idx += 1
                    res = [w for w in res if search_val in w["nama_senjata"].lower()]

                if "ORDER BY" in q_upper:
                    res.sort(key=lambda w: (-w.get("rarity", 0), -w.get("base_atk", 0), w.get("id", 0)))

                self._result = res
                self._rowcount = len(res)
                return

            # D. TEAMS VIEW (V_PARTY_TEAM_DETAILS)
            if "V_PARTY_TEAM_DETAILS" in q_upper:
                self._result = list(self.storage.teams_view)
                self._rowcount = len(self._result)
                return

            # E. TALENTS TABLE
            if "FROM SKILLS_TALENTS" in q_upper:
                if "WHERE ID_CHARACTER = %S" in q_upper or "WHERE ID_CHARACTER = ?" in q_upper:
                    char_id = int(params[0])
                    self._result = [s for s in self.storage.skills if s["id_character"] == char_id]
                    self._rowcount = len(self._result)
                else:
                    self._result = list(self.storage.skills)
                    self._rowcount = len(self._result)
                return

            # F. SINGLE CHARACTER QUERY (DETAIL ATAU CHECK EXISTENCE)
            if ("FROM CHARACTERS C" in q_upper or "FROM CHARACTERS" in q_upper) and (
                "WHERE C.ID = %S" in q_upper or "WHERE ID = %S" in q_upper
            ):
                char_id = int(params[0])
                found = None
                for c in self.storage.characters:
                    if c["id"] == char_id:
                        el = next((e for e in self.storage.elements if e["id"] == c["id_elemen"]), None)
                        item = dict(c)
                        if el:
                            item["nama_elemen"] = el["nama_elemen"]
                            item["warna_hex"] = el["warna_hex"]
                            item["reaksi_efek"] = el["reaksi_efek"]
                        found = item
                        break
                self._result = [found] if found else []
                self._rowcount = 1 if found else 0
                return

            # G. LIST ALL CHARACTERS (WITH JOINS AND FILTERS)
            if "FROM CHARACTERS" in q_upper:
                rows = []
                for c in self.storage.characters:
                    el = next((e for e in self.storage.elements if e["id"] == c["id_elemen"]), None)
                    item = dict(c)
                    if el:
                        item["nama_elemen"] = el["nama_elemen"]
                        item["warna_hex"] = el["warna_hex"]
                        item["reaksi_efek"] = el["reaksi_efek"]
                    rows.append(item)

                param_idx = 0
                if "C.ID_ELEMEN = %S" in q_upper:
                    el_val = int(params[param_idx])
                    param_idx += 1
                    rows = [r for r in rows if r["id_elemen"] == el_val]
                elif "LOWER(E.NAMA_ELEMEN) = LOWER(%S)" in q_upper:
                    el_name = str(params[param_idx]).lower()
                    param_idx += 1
                    rows = [r for r in rows if r.get("nama_elemen", "").lower() == el_name]

                if "C.RARITY = %S" in q_upper:
                    r_val = int(params[param_idx])
                    param_idx += 1
                    rows = [r for r in rows if r["rarity"] == r_val]

                if "LOWER(C.TIPE_SENJATA) = LOWER(%S)" in q_upper:
                    wt_val = str(params[param_idx]).lower()
                    param_idx += 1
                    rows = [r for r in rows if r["tipe_senjata"].lower() == wt_val]

                if "LOWER(C.ROLE_UTAMA) = LOWER(%S)" in q_upper:
                    role_val = str(params[param_idx]).lower()
                    param_idx += 1
                    rows = [r for r in rows if r["role_utama"].lower() == role_val]

                if "LOWER(C.NAMA_KARAKTER) LIKE LOWER(%S)" in q_upper:
                    s_val = str(params[param_idx]).replace("%", "").lower()
                    param_idx += 1
                    rows = [r for r in rows if s_val in r["nama_karakter"].lower()]

                if "ORDER BY" in q_upper:
                    order_part = q_upper.split("ORDER BY")[1].strip().rstrip(";").strip()
                    tokens = order_part.split()
                    if tokens:
                        col_token = tokens[0].replace("C.", "").lower()
                        is_desc = len(tokens) > 1 and tokens[1] == "DESC"
                        rows.sort(key=lambda r: (r.get(col_token) is None, r.get(col_token, 0)), reverse=is_desc)

                self._result = rows
                self._rowcount = len(rows)
                return

        # ----------------------------------------------------------------------
        # 2. INSERT STATEMENTS
        # ----------------------------------------------------------------------
        if q_upper.startswith("INSERT INTO CHARACTERS"):
            new_id = self.storage.next_char_id
            self.storage.next_char_id += 1
            new_char = {
                "id": new_id,
                "id_elemen": int(params[0]),
                "nama_karakter": str(params[1]),
                "rarity": int(params[2]),
                "tipe_senjata": str(params[3]),
                "role_utama": str(params[4]),
                "base_hp": int(params[5]),
                "base_atk": int(params[6]),
                "base_def": int(params[7]),
                "ascension_stat": str(params[8]),
            }
            self.storage.characters.append(new_char)
            self._result = [new_char]
            self._rowcount = 1
            return

        # ----------------------------------------------------------------------
        # 3. UPDATE STATEMENTS
        # ----------------------------------------------------------------------
        if q_upper.startswith("UPDATE CHARACTERS"):
            char_id = int(params[-1])
            found = next((c for c in self.storage.characters if c["id"] == char_id), None)
            if found:
                set_part = q_upper.split("SET")[1].split("WHERE")[0]
                cols = [item.strip().split("=")[0].strip().lower() for item in set_part.split(",")]
                for i, col in enumerate(cols):
                    found[col] = params[i]
                self._result = [dict(found)]
                self._rowcount = 1
            else:
                self._result = []
                self._rowcount = 0
            return

        # ----------------------------------------------------------------------
        # 4. DELETE STATEMENTS
        # ----------------------------------------------------------------------
        if q_upper.startswith("DELETE FROM CHARACTERS"):
            char_id = int(params[0])
            if char_id in self.storage.inventory_character_ids:
                raise psycopg2.IntegrityError(
                    f'update or delete on table "characters" violates foreign key constraint '
                    f'"fk_inv_char_master" on table "player_inventory_characters". '
                    f'Key (id)=({char_id}) is still referenced from table "player_inventory_characters".'
                )
            initial_count = len(self.storage.characters)
            self.storage.characters = [c for c in self.storage.characters if c["id"] != char_id]
            self.storage.skills = [s for s in self.storage.skills if s.get("id_character") != char_id]
            self._rowcount = initial_count - len(self.storage.characters)
            self._result = []
            return

        # Fallback default
        self._result = []
        self._rowcount = 0

    def fetchone(self):
        if self._result:
            return self._result[0]
        return None

    def fetchall(self):
        return list(self._result)

    @property
    def rowcount(self):
        return self._rowcount

    def close(self):
        pass


mock_storage = MockStorage()
