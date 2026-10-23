drop table if exists abyss_run_records cascade;
drop table if exists party_members cascade;
drop table if exists party_teams cascade;
drop table if exists gacha_pull_history cascade;
drop table if exists gacha_banners cascade;
drop table if exists player_inventory_weapons cascade;
drop table if exists player_inventory_characters cascade;
drop table if exists artifact_sets cascade;
drop table if exists weapons cascade;
drop table if exists skills_talents cascade;
drop table if exists characters cascade;
drop table if exists elements cascade;
drop table if exists player_profiles cascade;
drop table if exists players cascade;

create table players (
    id serial primary key,
    username varchar(50) not null unique,
    email varchar(100) not null unique,
    in_game_uid varchar(20) not null unique,
    password_hash varchar(255) not null,
    created_at timestamp default current_timestamp
);

create table player_profiles (
    id serial primary key,
    id_player int not null unique,
    bio_status varchar(255) default 'ad astra abyssosque!',
    adventure_rank int default 1 check (adventure_rank between 1 and 60),
    world_level int default 0 check (world_level between 0 and 9),
    total_achievements int default 0,
    avatar_url varchar(255),
    updated_at timestamp default current_timestamp,
    constraint fk_profile_player foreign key (id_player) references players(id) on delete cascade
);

create table elements (
    id serial primary key,
    nama_elemen varchar(30) not null unique,
    warna_hex varchar(7) not null,
    reaksi_efek text not null
);

create table characters (
    id serial primary key,
    id_elemen int not null,
    nama_karakter varchar(100) not null,
    rarity int not null check (rarity in (4, 5)),
    tipe_senjata varchar(30) not null check (tipe_senjata in ('Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst')),
    role_utama varchar(30) not null check (role_utama in ('Main DPS', 'Sub DPS', 'Support', 'Healer', 'Shielder')),
    base_hp int not null,
    base_atk int not null,
    base_def int not null,
    ascension_stat varchar(50) not null,
    constraint fk_character_element foreign key (id_elemen) references elements(id) on delete restrict
);

create table skills_talents (
    id serial primary key,
    id_character int not null,
    nama_talent varchar(100) not null,
    tipe_talent varchar(50) not null,
    deskripsi text not null,
    cooldown_seconds numeric(4, 1) default 0,
    energy_cost int default 0,
    constraint fk_talent_character foreign key (id_character) references characters(id) on delete cascade
);

create table weapons (
    id serial primary key,
    nama_senjata varchar(100) not null,
    tipe_senjata varchar(30) not null,
    rarity int not null check (rarity between 3 and 5),
    base_atk int not null,
    substat_type varchar(50) not null,
    substat_value numeric(5, 2) not null,
    pasif_deskripsi text
);

create table artifact_sets (
    id serial primary key,
    nama_set varchar(100) not null unique,
    efek_2_piece text not null,
    efek_4_piece text not null
);

create table player_inventory_characters (
    id serial primary key,
    id_player int not null,
    id_character int not null,
    character_level int default 1 check (character_level between 1 and 90),
    constellation_level int default 0 check (constellation_level between 0 and 6),
    friendship_level int default 1 check (friendship_level between 1 and 10),
    obtained_at timestamp default current_timestamp,
    constraint uq_char_player unique (id_player, id_character),
    constraint fk_inv_char_player foreign key (id_player) references players(id) on delete cascade,
    constraint fk_inv_char_master foreign key (id_character) references characters(id) on delete restrict
);

create table player_inventory_weapons (
    id serial primary key,
    id_player int not null,
    id_weapon int not null,
    weapon_level int default 1 check (weapon_level between 1 and 90),
    refinement_rank int default 1 check (refinement_rank between 1 and 5),
    is_locked boolean default false,
    obtained_at timestamp default current_timestamp,
    constraint fk_inv_weap_player foreign key (id_player) references players(id) on delete cascade,
    constraint fk_inv_weap_master foreign key (id_weapon) references weapons(id) on delete restrict
);

create table gacha_banners (
    id serial primary key,
    nama_banner varchar(150) not null,
    tipe_banner varchar(50) not null,
    start_date timestamp not null,
    end_date timestamp not null,
    rate_up_5star_featured varchar(100) not null
);

create table gacha_pull_history (
    id serial primary key,
    id_player int not null,
    id_banner int not null,
    item_type varchar(20) not null,
    item_name varchar(100) not null,
    rarity_pulled int not null,
    pity_count int not null,
    is_won_50_50 boolean default true,
    pulled_at timestamp default current_timestamp,
    constraint fk_pull_player foreign key (id_player) references players(id) on delete cascade,
    constraint fk_pull_banner foreign key (id_banner) references gacha_banners(id) on delete restrict
);

create table party_teams (
    id serial primary key,
    id_player int not null,
    nama_party varchar(100) not null,
    fokus_konten varchar(50) default 'Spiral Abyss',
    deskripsi text,
    created_at timestamp default current_timestamp,
    constraint fk_party_player foreign key (id_player) references players(id) on delete cascade
);

create table party_members (
    id serial primary key,
    id_party int not null,
    id_inventory_character int not null,
    id_inventory_weapon int,
    slot_position int not null check (slot_position between 1 and 4),
    role_dalam_party varchar(50) not null,
    constraint uq_team_slot unique (id_party, slot_position),
    constraint uq_team_char unique (id_party, id_inventory_character),
    constraint fk_pm_party foreign key (id_party) references party_teams(id) on delete cascade,
    constraint fk_pm_char foreign key (id_inventory_character) references player_inventory_characters(id) on delete cascade,
    constraint fk_pm_weap foreign key (id_inventory_weapon) references player_inventory_weapons(id) on delete set null
);

create table abyss_run_records (
    id serial primary key,
    id_party int not null,
    floor_chamber varchar(20) not null,
    clear_time_seconds int not null,
    stars_earned int not null check (stars_earned between 0 and 3),
    run_date timestamp default current_timestamp,
    constraint fk_abyss_party foreign key (id_party) references party_teams(id) on delete cascade
);

create or replace view v_party_team_details as
select 
    p.username,
    p.in_game_uid,
    pt.nama_party,
    pm.slot_position,
    c.nama_karakter,
    e.nama_elemen,
    pic.character_level,
    pic.constellation_level,
    coalesce(w.nama_senjata, 'Kosong / Belum Equip') as nama_senjata,
    pm.role_dalam_party
from party_teams pt
join players p on pt.id_player = p.id
join party_members pm on pt.id = pm.id_party
join player_inventory_characters pic on pm.id_inventory_character = pic.id
join characters c on pic.id_character = c.id
join elements e on c.id_elemen = e.id
left join player_inventory_weapons piw on pm.id_inventory_weapon = piw.id
left join weapons w on piw.id_weapon = w.id
order by pt.id, pm.slot_position asc;

insert into elements (nama_elemen, warna_hex, reaksi_efek) values
('Pyro',    '#FF4500', 'Vaporize, Melt, Overloaded, Burgeon'),
('Hydro',   '#1E90FF', 'Vaporize, Electro-Charged, Bloom, Freeze'),
('Anemo',   '#40E0D0', 'Swirl'),
('Electro', '#8A2BE2', 'Aggravate, Hyperbloom, Electro-Charged'),
('Dendro',  '#32CD32', 'Bloom, Catalyze, Spread, Hyperbloom'),
('Cryo',    '#00FFFF', 'Freeze, Melt, Superconduct'),
('Geo',     '#DAA520', 'Crystallize');

insert into characters (id_elemen, nama_karakter, rarity, tipe_senjata, role_utama, base_hp, base_atk, base_def, ascension_stat) values
(1, 'Hu Tao', 5, 'Polearm', 'Main DPS', 15552, 106, 876, 'CRIT DMG'),
(2, 'Furina', 5, 'Sword', 'Sub DPS', 15307, 244, 696, 'CRIT Rate'),
(3, 'Kaedehara Kazuha', 5, 'Sword', 'Support', 13348, 297, 807, 'Elemental Mastery'),
(7, 'Zhongli', 5, 'Polearm', 'Shielder', 14695, 251, 738, 'Geo DMG Bonus'),
(4, 'Raiden Shogun', 5, 'Polearm', 'Sub DPS', 12907, 337, 789, 'Energy Recharge'),
(6, 'Qiqi', 5, 'Sword', 'Healer', 12118, 287, 922, 'Healing Bonus'),
(1, 'Bennett', 4, 'Sword', 'Support', 12397, 191, 771, 'Energy Recharge');

insert into skills_talents (id_character, nama_talent, tipe_talent, deskripsi, cooldown_seconds, energy_cost) values
(1, 'Guide to Afterlife', 'Elemental Skill', 'Masuk mode darah sekarat tapi ATK naik drastis', 16.0, 0),
(1, 'Spirit Soother', 'Elemental Burst', 'Ngemper damage api nuklir sekalian heal tipis-tipis', 15.0, 60),
(2, 'Salon Solitaire', 'Elemental Skill', 'Mangil kroco buat gebukin musuh tapi nyedot darah satu tim', 20.0, 0),
(6, 'Adeptus Art: Preserver of Fortune', 'Elemental Burst', 'Nandain musuh pake jimat, penyelamat kalo lagi sekarat', 20.0, 80);

insert into weapons (nama_senjata, tipe_senjata, rarity, base_atk, substat_type, substat_value, pasif_deskripsi) values
('Staff of Homa', 'Polearm', 5, 608, 'CRIT DMG', 66.20, 'Nambah HP 20% sama bonus ATK kalo darah di bawah 50%'),
('Splendor of Tranquil Waters', 'Sword', 5, 542, 'CRIT DMG', 88.20, 'Buff skill kalo HP naik turun'),
('Freedom-Sworn', 'Sword', 5, 608, 'Elemental Mastery', 198.00, 'Buff ATK buat satu tim setelah picu reaksi'),
('Black Tassel', 'Polearm', 3, 354, 'HP%', 46.90, 'Tombak slime murah meriah andalan tiang zhongli'),
('The Bell', 'Claymore', 4, 510, 'HP%', 41.30, 'Pedang terkutuk yang selalu nongol pas rate-off'),
('Debate Club', 'Claymore', 3, 401, 'ATK%', 35.20, 'Palu F2P buat gebuk hilichurl di awal game');

insert into artifact_sets (nama_set, efek_2_piece, efek_4_piece) values
('Crimson Witch of Flames', 'Pyro DMG +15%', 'Nambah damage reaksi bakar-bakaran'),
('Golden Troupe', 'Skill DMG +20%', 'Damage skill naik 25% lagi kalo karakternya lagi off-field'),
('Viridescent Venerer', 'Anemo DMG +15%', 'Nurunin resistensi elemental musuh 40% (wajib punya support anemo)');

insert into players (username, email, in_game_uid, password_hash) values
('izzul', 'izzul@genshin.id', '801992026', '$2b$12$hashpassIzzul123'),
('lunizura', 'lunizura@astral.id', '808876543', '$2b$12$hashpassLuni456'),
('izu', 'izu@teyvat.id', '804561234', '$2b$12$hashpassIzu789');

insert into player_profiles (id_player, bio_status, adventure_rank, world_level, total_achievements, avatar_url) values
(1, 'capek farming artefak berbulan-bulan dapetnya flat DEF melulu', 60, 8, 1180, 'https://api.dicebear.com/7.x/bottts/svg?seed=izzul'),
(2, 'joki abyss floor 12 murah fast respond dm telegram', 59, 8, 1020, 'https://api.dicebear.com/7.x/bottts/svg?seed=lunizura'),
(3, 'F2P murni login cuma buat komisi harian sama klaim primogem', 56, 7, 720, 'https://api.dicebear.com/7.x/bottts/svg?seed=izu');

insert into player_inventory_characters (id_player, id_character, character_level, constellation_level, friendship_level) values
(1, 1, 90, 1, 10),
(1, 2, 90, 2, 9),
(1, 3, 90, 0, 10),
(1, 4, 90, 0, 10),
(1, 6, 80, 4, 6),
(2, 5, 90, 2, 10),
(3, 7, 80, 5, 10);

insert into player_inventory_weapons (id_player, id_weapon, weapon_level, refinement_rank, is_locked) values
(1, 1, 90, 1, true),
(1, 2, 90, 1, true),
(1, 3, 90, 1, true),
(1, 4, 90, 5, true),
(1, 5, 50, 5, false);

insert into gacha_banners (nama_banner, tipe_banner, start_date, end_date, rate_up_5star_featured) values
('Banner Harapan Palsu (Hu Tao)', 'Character Event', '2026-09-01 18:00:00', '2026-09-22 15:00:00', 'Hu Tao'),
('Banner Dapur Fontaine (Furina)', 'Character Event', '2026-09-22 18:00:00', '2026-10-13 15:00:00', 'Furina');

insert into gacha_pull_history (id_player, id_banner, item_type, item_name, rarity_pulled, pity_count, is_won_50_50) values
(1, 1, 'Character', 'Qiqi', 5, 83, false),
(1, 1, 'Character', 'Hu Tao', 5, 78, true),
(1, 1, 'Character', 'Hu Tao', 5, 14, true),
(2, 2, 'Character', 'Furina', 5, 76, true);

insert into party_teams (id_player, nama_party, fokus_konten, deskripsi) values
(1, 'Hu Tao Darah Sekarat Asal Jangan Kena Senggol', 'Spiral Abyss', 'Tim andalan Izzul, damage sakit tapi jantung copot kalo shield Zhongli abis'),
(2, 'Tim Modal Nekat Bintang 36', 'Spiral Abyss', 'Spam ulti gajelas tapi musuh rata tanah');

insert into party_members (id_party, id_inventory_character, id_inventory_weapon, slot_position, role_dalam_party) values
(1, 1, 1, 1, 'Main DPS yang selalu sekarat'),
(1, 2, 2, 2, 'Buffer air penyedot darah'),
(1, 3, 3, 3, 'Tukang kumpulin musuh & shred resist'),
(1, 4, 4, 4, 'Bapak pelindung perisai anti mati');

insert into abyss_run_records (id_party, floor_chamber, clear_time_seconds, stars_earned) values
(1, '12-1', 42, 3),
(1, '12-2', 51, 3),
(1, '12-3', 59, 3);
