import os
import time
from datetime import datetime, timezone
from flask import Flask, request, jsonify
import psycopg2

try:
    from api.db import get_db_cursor, serialize_data, check_db_health, USE_MOCK_DB
except ImportError:
    from db import get_db_cursor, serialize_data, check_db_health, USE_MOCK_DB

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.url_map.strict_slashes = False

from urllib.parse import parse_qs

class VercelPathMiddleware:
    """
    Middleware untuk merekonstruksi PATH_INFO asli saat request
    di-rewrite oleh Vercel Serverless Function menggunakan parameter __path.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        qs = parse_qs(environ.get("QUERY_STRING", ""))
        if "__path" in qs:
            p = qs["__path"][0]
            if not p.startswith("/"):
                p = "/" + p
            environ["PATH_INFO"] = p
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

# Timestamp awal server start untuk metrik uptime
START_TIME = time.time()

# Validasi Domain Data Gacha
VALID_WEAPON_TYPES = {"Sword", "Claymore", "Polearm", "Bow", "Catalyst"}
VALID_ROLES = {"Main DPS", "Sub DPS", "Support", "Healer", "Shielder"}
WEAPON_MAP = {w.lower(): w for w in VALID_WEAPON_TYPES}
ROLE_MAP = {r.lower(): r for r in VALID_ROLES}
VALID_RARITIES = {4, 5}
ALLOWED_SORT_FIELDS = {"id", "nama_karakter", "rarity", "base_hp", "base_atk", "base_def"}
ALLOWED_SORT_ORDERS = {"asc", "desc"}


# ==============================================================================
# GLOBAL ERROR HANDLERS (Standard JSON Responses)
# ==============================================================================

@app.errorhandler(400)
def handle_bad_request(e):
    return jsonify({
        "status": "error",
        "message": getattr(e, "description", "Bad Request: Permintaan tidak valid"),
        "error_code": "BAD_REQUEST"
    }), 400


@app.errorhandler(404)
def handle_not_found(e):
    return jsonify({
        "status": "error",
        "message": getattr(e, "description", "Resource endpoint atau data tidak ditemukan"),
        "error_code": "NOT_FOUND",
        "received_path": request.path
    }), 404


@app.errorhandler(405)
def handle_method_not_allowed(e):
    return jsonify({
        "status": "error",
        "message": f"Metode HTTP {request.method} tidak diizinkan pada endpoint ini",
        "error_code": "METHOD_NOT_ALLOWED"
    }), 405


@app.errorhandler(500)
def handle_internal_server_error(e):
    return jsonify({
        "status": "error",
        "message": "Terjadi kesalahan internal pada server database",
        "error_code": "INTERNAL_SERVER_ERROR"
    }), 500


# ==============================================================================
# 1. ROOT & HEALTH CHECK ENDPOINTS
# ==============================================================================

@app.route("/", methods=["GET"])
@app.route("/api", methods=["GET"])
@app.route("/api/index", methods=["GET"])
def root():
    """
    Katalog root informasi REST API & navigasi endpoint.
    """
    return jsonify({
        "project": "Gacha Character & Team Builder REST API",
        "course": "Tugas Akhir Learning Labs: Backend Development",
        "author": "lunizura (Muhammad Izzul Islam)",
        "version": "1.0.0",
        "status": "operational",
        "documentation": {
            "github": "https://github.com/lunizura/gacha-builder-api-learninglabs",
            "endpoints": {
                "health": "GET /api/health",
                "elements": "GET /api/elements",
                "weapons": "GET /api/weapons",
                "teams": "GET /api/teams",
                "characters": {
                    "list": "GET /api/characters?element=Pyro&rarity=5",
                    "detail": "GET /api/characters/<int:id>",
                    "create": "POST /api/characters",
                    "update": "PUT /api/characters/<int:id>",
                    "delete": "DELETE /api/characters/<int:id>"
                }
            }
        }
    }), 200


@app.route("/api/health", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    """
    Pemeriksaan status uptime server dan konektivitas live database PostgreSQL.
    """
    db_status = check_db_health()
    uptime_seconds = round(time.time() - START_TIME, 2)
    is_healthy = db_status.get("status") in ("connected", "connected (mock)")

    payload = {
        "status": "healthy" if is_healthy else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": uptime_seconds,
        "environment": os.environ.get("FLASK_ENV", "production"),
        "database": db_status
    }
    status_code = 200 if is_healthy else 503
    return jsonify(payload), status_code


# ==============================================================================
# 2. MASTER DATA ENDPOINTS: ELEMENTS & WEAPONS & TEAMS
# ==============================================================================

@app.route("/api/elements", methods=["GET"])
@app.route("/elements", methods=["GET"])
def get_elements():
    """
    Mengambil seluruh daftar elemen master (Pyro, Hydro, Anemo, Electro, Dendro, Cryo, Geo).
    """
    query = "SELECT id, nama_elemen, warna_hex, reaksi_efek FROM elements ORDER BY id ASC;"
    try:
        with get_db_cursor(commit=False) as cur:
            cur.execute(query)
            elements = cur.fetchall()
        return jsonify({
            "status": "success",
            "message": "Berhasil mengambil data elemen",
            "total": len(elements),
            "data": serialize_data(elements)
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Gagal membaca data elemen: {str(e)}"
        }), 500


@app.route("/api/weapons", methods=["GET"])
@app.route("/weapons", methods=["GET"])
def get_weapons():
    """
    Mengambil katalog senjata dengan filter opsional (?rarity=5, ?weapon_type=Sword, ?search=Staff).
    """
    rarity = request.args.get("rarity")
    weapon_type = request.args.get("weapon_type") or request.args.get("tipe_senjata")
    search = request.args.get("search")

    query = "SELECT id, nama_senjata, tipe_senjata, rarity, base_atk, substat_type, substat_value, pasif_deskripsi FROM weapons"
    conditions = []
    params = []

    if rarity:
        try:
            rarity_int = int(rarity)
            conditions.append("rarity = %s")
            params.append(rarity_int)
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Parameter 'rarity' harus berupa angka (3, 4, atau 5)"
            }), 400

    if weapon_type:
        conditions.append("LOWER(tipe_senjata) = LOWER(%s)")
        params.append(weapon_type.strip())

    if search:
        conditions.append("LOWER(nama_senjata) LIKE LOWER(%s)")
        params.append(f"%{search.strip()}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY rarity DESC, base_atk DESC, id ASC;"

    try:
        with get_db_cursor(commit=False) as cur:
            cur.execute(query, tuple(params))
            weapons = cur.fetchall()
        return jsonify({
            "status": "success",
            "message": "Berhasil mengambil data senjata",
            "filters": {
                "rarity": rarity,
                "weapon_type": weapon_type,
                "search": search
            },
            "total": len(weapons),
            "data": serialize_data(weapons)
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Gagal membaca data senjata: {str(e)}"
        }), 500


@app.route("/api/teams", methods=["GET"])
@app.route("/teams", methods=["GET"])
def get_teams():
    """
    Mengambil daftar komposisi party/tim lengkap dengan join karakter, elemen, senjata,
    dan statistik inventory menggunakan view PostgreSQL 'v_party_team_details'.
    """
    query = """
    SELECT 
        username,
        in_game_uid,
        nama_party,
        slot_position,
        nama_karakter,
        nama_elemen,
        character_level,
        constellation_level,
        nama_senjata,
        role_dalam_party
    FROM v_party_team_details;
    """
    try:
        with get_db_cursor(commit=False) as cur:
            cur.execute(query)
            rows = cur.fetchall()

        # Mengelompokkan data berdasarkan tim
        teams_map = {}
        for row in rows:
            party_key = (row["nama_party"], row["username"], row["in_game_uid"])
            if party_key not in teams_map:
                teams_map[party_key] = {
                    "nama_party": row["nama_party"],
                    "username": row["username"],
                    "in_game_uid": row["in_game_uid"],
                    "members": []
                }
            teams_map[party_key]["members"].append({
                "slot_position": row["slot_position"],
                "nama_karakter": row["nama_karakter"],
                "nama_elemen": row["nama_elemen"],
                "character_level": row["character_level"],
                "constellation_level": row["constellation_level"],
                "nama_senjata": row["nama_senjata"],
                "role_dalam_party": row["role_dalam_party"]
            })

        grouped_teams = list(teams_map.values())
        return jsonify({
            "status": "success",
            "message": "Berhasil mengambil detail formasi tim",
            "total_teams": len(grouped_teams),
            "total_slots": len(rows),
            "data": serialize_data(grouped_teams)
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Gagal membaca data formasi tim: {str(e)}"
        }), 500


# ==============================================================================
# 3. CORE CRUD ENDPOINTS: CHARACTERS
# ==============================================================================

@app.route("/api/characters", methods=["GET"])
@app.route("/characters", methods=["GET"])
def get_characters():
    """
    GET /api/characters
    Mengambil daftar semua karakter dengan relasi elemen dan mendukung query filter:
    ?element=Pyro | ?element=1
    ?rarity=5
    ?weapon_type=Polearm
    ?role=Main DPS
    ?search=Hu
    ?sort_by=base_atk&order=desc
    """
    element = request.args.get("element")
    rarity = request.args.get("rarity")
    weapon_type = request.args.get("weapon_type") or request.args.get("tipe_senjata")
    role = request.args.get("role") or request.args.get("role_utama")
    search = request.args.get("search")
    sort_by = (request.args.get("sort_by") or "id").lower()
    order = (request.args.get("order") or "asc").lower()

    if sort_by not in ALLOWED_SORT_FIELDS:
        sort_by = "id"
    if order not in ALLOWED_SORT_ORDERS:
        order = "asc"

    query = """
    SELECT 
        c.id,
        c.nama_karakter,
        c.rarity,
        c.tipe_senjata,
        c.role_utama,
        c.base_hp,
        c.base_atk,
        c.base_def,
        c.ascension_stat,
        c.id_elemen,
        e.nama_elemen,
        e.warna_hex
    FROM characters c
    JOIN elements e ON c.id_elemen = e.id
    """
    conditions = []
    params = []

    if element:
        element_clean = element.strip()
        if element_clean.isdigit():
            conditions.append("c.id_elemen = %s")
            params.append(int(element_clean))
        else:
            conditions.append("LOWER(e.nama_elemen) = LOWER(%s)")
            params.append(element_clean)

    if rarity:
        try:
            rarity_int = int(rarity)
            if rarity_int not in VALID_RARITIES:
                return jsonify({
                    "status": "error",
                    "message": "Filter 'rarity' hanya mendukung angka 4 atau 5"
                }), 400
            conditions.append("c.rarity = %s")
            params.append(rarity_int)
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Filter 'rarity' harus berupa angka bulat"
            }), 400

    if weapon_type:
        conditions.append("LOWER(c.tipe_senjata) = LOWER(%s)")
        params.append(weapon_type.strip())

    if role:
        conditions.append("LOWER(c.role_utama) = LOWER(%s)")
        params.append(role.strip())

    if search:
        conditions.append("LOWER(c.nama_karakter) LIKE LOWER(%s)")
        params.append(f"%{search.strip()}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += f" ORDER BY c.{sort_by} {order.upper()};"

    try:
        with get_db_cursor(commit=False) as cur:
            cur.execute(query, tuple(params))
            characters = cur.fetchall()

        return jsonify({
            "status": "success",
            "message": "Berhasil mengambil data karakter",
            "filters": {
                "element": element,
                "rarity": rarity,
                "weapon_type": weapon_type,
                "role": role,
                "search": search,
                "sort_by": sort_by,
                "order": order
            },
            "total": len(characters),
            "data": serialize_data(characters)
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Gagal membaca data karakter: {str(e)}"
        }), 500


@app.route("/api/characters/<int:id>", methods=["GET"])
@app.route("/characters/<int:id>", methods=["GET"])
def get_character_detail(id):
    """
    GET /api/characters/<id>
    Mengambil data spesifik karakter lengkap beserta talent/skill pasif dan aktifnya.
    """
    char_query = """
    SELECT 
        c.id,
        c.nama_karakter,
        c.rarity,
        c.tipe_senjata,
        c.role_utama,
        c.base_hp,
        c.base_atk,
        c.base_def,
        c.ascension_stat,
        c.id_elemen,
        e.nama_elemen,
        e.warna_hex,
        e.reaksi_efek
    FROM characters c
    JOIN elements e ON c.id_elemen = e.id
    WHERE c.id = %s;
    """
    skill_query = """
    SELECT id, nama_talent, tipe_talent, deskripsi, cooldown_seconds, energy_cost
    FROM skills_talents
    WHERE id_character = %s
    ORDER BY id ASC;
    """
    try:
        with get_db_cursor(commit=False) as cur:
            cur.execute(char_query, (id,))
            character = cur.fetchone()
            if not character:
                return jsonify({
                    "status": "error",
                    "message": f"Karakter dengan ID {id} tidak ditemukan"
                }), 404

            cur.execute(skill_query, (id,))
            skills = cur.fetchall()

        character_data = dict(character)
        character_data["skills"] = list(skills) if skills else []

        return jsonify({
            "status": "success",
            "message": "Detail karakter berhasil ditemukan",
            "data": serialize_data(character_data)
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Gagal mengambil detail karakter: {str(e)}"
        }), 500


@app.route("/api/characters", methods=["POST"])
@app.route("/characters", methods=["POST"])
def create_character():
    """
    POST /api/characters
    Menambahkan karakter baru dengan validasi ketat sesuai constraint skema database.
    Required fields:
    - nama_karakter (str, non-empty, max 100)
    - id_elemen (int, fk to elements)
    - rarity (int, 4 or 5)
    - tipe_senjata (str, in Sword, Claymore, Polearm, Bow, Catalyst)
    - role_utama (str, in Main DPS, Sub DPS, Support, Healer, Shielder)
    - base_hp (int, > 0)
    - base_atk (int, > 0)
    - base_def (int, > 0)
    - ascension_stat (str, non-empty, max 50)
    """
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Request body harus berupa JSON object yang valid"
        }), 400

    errors = []

    # Validasi nama_karakter
    nama_karakter_raw = data.get("nama_karakter")
    if not isinstance(nama_karakter_raw, str) or not nama_karakter_raw.strip():
        errors.append("Field 'nama_karakter' wajib diisi (string non-empty)")
    elif len(nama_karakter_raw.strip()) > 100:
        errors.append("Field 'nama_karakter' maksimal 100 karakter")
    nama_karakter = nama_karakter_raw.strip() if isinstance(nama_karakter_raw, str) else ""

    # Validasi id_elemen
    id_elemen = data.get("id_elemen")
    if not isinstance(id_elemen, int) or isinstance(id_elemen, bool) or id_elemen <= 0:
        errors.append("Field 'id_elemen' wajib diisi berupa integer positif yang valid")

    # Validasi rarity
    rarity = data.get("rarity")
    if not isinstance(rarity, int) or isinstance(rarity, bool) or rarity not in VALID_RARITIES:
        errors.append("Field 'rarity' wajib bernilai 4 atau 5")

    # Validasi tipe_senjata
    tipe_senjata_raw = data.get("tipe_senjata")
    tipe_senjata = ""
    if not isinstance(tipe_senjata_raw, str) or not tipe_senjata_raw.strip():
        errors.append(f"Field 'tipe_senjata' harus salah satu dari: {', '.join(sorted(VALID_WEAPON_TYPES))}")
    else:
        norm_w = WEAPON_MAP.get(tipe_senjata_raw.strip().lower())
        if not norm_w:
            errors.append(f"Field 'tipe_senjata' harus salah satu dari: {', '.join(sorted(VALID_WEAPON_TYPES))}")
        else:
            tipe_senjata = norm_w

    # Validasi role_utama
    role_utama_raw = data.get("role_utama")
    role_utama = ""
    if not isinstance(role_utama_raw, str) or not role_utama_raw.strip():
        errors.append(f"Field 'role_utama' harus salah satu dari: {', '.join(sorted(VALID_ROLES))}")
    else:
        norm_r = ROLE_MAP.get(role_utama_raw.strip().lower())
        if not norm_r:
            errors.append(f"Field 'role_utama' harus salah satu dari: {', '.join(sorted(VALID_ROLES))}")
        else:
            role_utama = norm_r

    # Validasi base_hp, base_atk, base_def
    for stat_field in ("base_hp", "base_atk", "base_def"):
        val = data.get(stat_field)
        if not isinstance(val, int) or isinstance(val, bool) or val <= 0:
            errors.append(f"Field '{stat_field}' wajib berupa integer positif (> 0)")

    # Validasi ascension_stat
    ascension_stat_raw = data.get("ascension_stat")
    if not isinstance(ascension_stat_raw, str) or not ascension_stat_raw.strip():
        errors.append("Field 'ascension_stat' wajib diisi (contoh: 'CRIT DMG', 'Elemental Mastery')")
    elif len(ascension_stat_raw.strip()) > 50:
        errors.append("Field 'ascension_stat' maksimal 50 karakter")
    ascension_stat = ascension_stat_raw.strip() if isinstance(ascension_stat_raw, str) else ""

    if errors:
        return jsonify({
            "status": "error",
            "message": "Validasi input gagal",
            "errors": errors
        }), 400

    # Pastikan id_elemen terdaftar pada tabel elements
    check_el_query = "SELECT id, nama_elemen, warna_hex FROM elements WHERE id = %s;"
    insert_query = """
    INSERT INTO characters (
        id_elemen, nama_karakter, rarity, tipe_senjata, role_utama,
        base_hp, base_atk, base_def, ascension_stat
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id, id_elemen, nama_karakter, rarity, tipe_senjata, role_utama, base_hp, base_atk, base_def, ascension_stat;
    """

    try:
        with get_db_cursor(commit=True) as cur:
            cur.execute(check_el_query, (id_elemen,))
            element_row = cur.fetchone()
            if not element_row:
                return jsonify({
                    "status": "error",
                    "message": f"id_elemen {id_elemen} tidak ditemukan pada tabel master elements"
                }), 400

            cur.execute(insert_query, (
                id_elemen, nama_karakter, rarity, tipe_senjata, role_utama,
                data["base_hp"], data["base_atk"], data["base_def"], ascension_stat
            ))
            new_char = cur.fetchone()

        result_payload = dict(new_char)
        result_payload["nama_elemen"] = element_row["nama_elemen"]
        result_payload["warna_hex"] = element_row["warna_hex"]

        return jsonify({
            "status": "success",
            "message": f"Karakter '{nama_karakter}' berhasil dibuat",
            "data": serialize_data(result_payload)
        }), 201
    except psycopg2.IntegrityError as ie:
        return jsonify({
            "status": "error",
            "message": f"Integritas database gagal: {str(ie)}"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Gagal menambahkan karakter: {str(e)}"
        }), 500


@app.route("/api/characters/<int:id>", methods=["PUT"])
@app.route("/characters/<int:id>", methods=["PUT"])
def update_character(id):
    """
    PUT /api/characters/<id>
    Memperbarui satu atau beberapa atribut data karakter.
    """
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Request body harus berupa JSON object yang valid"
        }), 400

    # Filter dan validasi field yang diizinkan untuk diubah
    updatable_fields = {
        "nama_karakter", "id_elemen", "rarity", "tipe_senjata",
        "role_utama", "base_hp", "base_atk", "base_def", "ascension_stat"
    }
    updates = {}
    errors = []

    for key, value in data.items():
        if key not in updatable_fields:
            continue

        if key == "nama_karakter":
            if not isinstance(value, str) or not value.strip() or len(value.strip()) > 100:
                errors.append("nama_karakter harus berupa string 1-100 karakter non-kosong")
            else:
                updates[key] = value.strip()

        elif key == "id_elemen":
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                errors.append("id_elemen harus berupa integer positif")
            else:
                updates[key] = value

        elif key == "rarity":
            if not isinstance(value, int) or isinstance(value, bool) or value not in VALID_RARITIES:
                errors.append("rarity harus bernilai 4 atau 5")
            else:
                updates[key] = value

        elif key == "tipe_senjata":
            if not isinstance(value, str) or not value.strip():
                errors.append(f"tipe_senjata harus salah satu dari: {', '.join(sorted(VALID_WEAPON_TYPES))}")
            else:
                norm_w = WEAPON_MAP.get(value.strip().lower())
                if not norm_w:
                    errors.append(f"tipe_senjata harus salah satu dari: {', '.join(sorted(VALID_WEAPON_TYPES))}")
                else:
                    updates[key] = norm_w

        elif key == "role_utama":
            if not isinstance(value, str) or not value.strip():
                errors.append(f"role_utama harus salah satu dari: {', '.join(sorted(VALID_ROLES))}")
            else:
                norm_r = ROLE_MAP.get(value.strip().lower())
                if not norm_r:
                    errors.append(f"role_utama harus salah satu dari: {', '.join(sorted(VALID_ROLES))}")
                else:
                    updates[key] = norm_r

        elif key in ("base_hp", "base_atk", "base_def"):
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                errors.append(f"{key} harus berupa integer positif")
            else:
                updates[key] = value

        elif key == "ascension_stat":
            if not isinstance(value, str) or not value.strip() or len(value.strip()) > 50:
                errors.append("ascension_stat harus berupa string 1-50 karakter non-kosong")
            else:
                updates[key] = value.strip()

    if errors:
        return jsonify({
            "status": "error",
            "message": "Validasi input pembaruan gagal",
            "errors": errors
        }), 400

    if not updates:
        return jsonify({
            "status": "error",
            "message": "Tidak ada field valid yang dikirim untuk diupdate"
        }), 400

    check_query = "SELECT id, nama_karakter FROM characters WHERE id = %s;"
    set_clauses = [f"{col} = %s" for col in updates.keys()]
    params = list(updates.values())
    params.append(id)

    update_query = f"""
    UPDATE characters 
    SET {', '.join(set_clauses)}
    WHERE id = %s
    RETURNING id, id_elemen, nama_karakter, rarity, tipe_senjata, role_utama, base_hp, base_atk, base_def, ascension_stat;
    """

    try:
        with get_db_cursor(commit=True) as cur:
            cur.execute(check_query, (id,))
            existing = cur.fetchone()
            if not existing:
                return jsonify({
                    "status": "error",
                    "message": f"Karakter dengan ID {id} tidak ditemukan"
                }), 404

            # Jika id_elemen diupdate, pastikan elemen valid dalam sesi yang sama
            if "id_elemen" in updates:
                cur.execute("SELECT id FROM elements WHERE id = %s;", (updates["id_elemen"],))
                if not cur.fetchone():
                    return jsonify({
                        "status": "error",
                        "message": f"id_elemen {updates['id_elemen']} tidak ditemukan pada tabel elements"
                    }), 400

            cur.execute(update_query, tuple(params))
            updated_char = cur.fetchone()

            # Ambil relasi elemen
            cur.execute("SELECT nama_elemen, warna_hex FROM elements WHERE id = %s;", (updated_char["id_elemen"],))
            el = cur.fetchone()

        result_payload = dict(updated_char)
        if el:
            result_payload["nama_elemen"] = el["nama_elemen"]
            result_payload["warna_hex"] = el["warna_hex"]

        return jsonify({
            "status": "success",
            "message": f"Data karakter ID {id} berhasil diperbarui",
            "data": serialize_data(result_payload)
        }), 200
    except psycopg2.IntegrityError as ie:
        return jsonify({
            "status": "error",
            "message": f"Integritas database gagal: {str(ie)}"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Gagal memperbarui karakter: {str(e)}"
        }), 500


@app.route("/api/characters/<int:id>", methods=["DELETE"])
@app.route("/characters/<int:id>", methods=["DELETE"])
def delete_character(id):
    """
    DELETE /api/characters/<id>
    Menghapus data karakter dari database.
    - Menghasilkan 404 jika ID tidak ditemukan.
    - Menangkap ForeignKeyViolation jika karakter terikat di player_inventory_characters
      dan mengembalikan 409 Conflict dengan pesan ramah.
    """
    check_query = "SELECT id, nama_karakter FROM characters WHERE id = %s;"
    delete_query = "DELETE FROM characters WHERE id = %s;"

    try:
        with get_db_cursor(commit=True) as cur:
            cur.execute(check_query, (id,))
            character = cur.fetchone()
            if not character:
                return jsonify({
                    "status": "error",
                    "message": f"Karakter dengan ID {id} tidak ditemukan"
                }), 404

            char_name = character["nama_karakter"]
            cur.execute(delete_query, (id,))

        return jsonify({
            "status": "success",
            "message": f"Karakter '{char_name}' (ID {id}) berhasil dihapus",
            "deleted_id": id
        }), 200

    except psycopg2.IntegrityError as ie:
        err_msg = str(ie).lower()
        if "foreign key" in err_msg or "violates foreign key" in err_msg or "fk_inv_char_master" in err_msg:
            return jsonify({
                "status": "error",
                "message": (
                    f"Tidak dapat menghapus karakter ID {id} karena masih terdaftar "
                    "dalam inventori karakter pemain (Foreign Key Constraint: player_inventory_characters)."
                ),
                "error_code": "FOREIGN_KEY_VIOLATION"
            }), 409
        return jsonify({
            "status": "error",
            "message": f"Pelanggaran integritas database: {str(ie)}",
            "error_code": "INTEGRITY_ERROR"
        }), 409

    except Exception as e:
        err_str = str(e)
        if "foreign key" in err_str.lower():
            return jsonify({
                "status": "error",
                "message": (
                    f"Tidak dapat menghapus karakter ID {id} karena masih terdaftar "
                    "dalam inventori karakter pemain (Foreign Key Constraint: player_inventory_characters)."
                ),
                "error_code": "FOREIGN_KEY_VIOLATION"
            }), 409
        return jsonify({
            "status": "error",
            "message": f"Gagal menghapus karakter: {err_str}"
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
