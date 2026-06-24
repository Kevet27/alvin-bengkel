import sqlite3

DB_NAME = "bengkel.db"


def get_connection():
    conn = sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_connection()
    c = conn.cursor()

    # ======================
    # USERS
    # ======================
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        username TEXT UNIQUE,
        password TEXT,
        telepon TEXT,
        role TEXT
    )
    """)

    # ======================
    # LAYANAN
    # ======================
    c.execute("""
    CREATE TABLE IF NOT EXISTS layanan(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_layanan TEXT,
        harga INTEGER,
        deskripsi TEXT
    )
    """)

    # ======================
    # CABANG BENGKEL
    # ======================
    c.execute("""
    CREATE TABLE IF NOT EXISTS cabang(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_bengkel TEXT,
        alamat TEXT,
        telepon TEXT
    )
    """)

    # ======================
    # BOOKING SERVICE
    # ======================
    c.execute("""
    CREATE TABLE IF NOT EXISTS booking(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        layanan TEXT,
        jenis_service TEXT,
        keluhan TEXT,
        tanggal TEXT,
        lokasi TEXT,
        status TEXT
    )
    """)

    # ======================
    # CUSTOMER CARE
    # ======================
    c.execute("""
    CREATE TABLE IF NOT EXISTS pengaduan(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        pesan TEXT,
        status TEXT
    )
    """)

    # ======================
    # TRANSAKSI
    # ======================
    c.execute("""
    CREATE TABLE IF NOT EXISTS transaksi(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        layanan TEXT,
        harga INTEGER,
        tanggal TEXT
    )
    """)

    conn.commit()

    # ======================
    # ADMIN DEFAULT
    # ======================
    c.execute(
        "SELECT * FROM users WHERE username=?",
        ("admin",)
    )

    admin = c.fetchone()

    if admin is None:

        c.execute("""
        INSERT INTO users(
        nama,
        username,
        password,
        telepon,
        role
        )
        VALUES(?,?,?,?,?)
        """,
        (
            "Administrator",
            "admin",
            "admin123",
            "08123456789",
            "admin"
        ))

    # ======================
    # LAYANAN DEFAULT
    # ======================
    c.execute("SELECT * FROM layanan")
    layanan = c.fetchall()

    if len(layanan) == 0:

        data_layanan = [

            (
                "Service Ringan",
                75000,
                "Pemeriksaan umum motor"
            ),

            (
                "Ganti Oli",
                60000,
                "Penggantian oli mesin"
            ),

            (
                "Tune Up",
                120000,
                "Tune up kendaraan"
            ),

            (
                "Service Lengkap",
                200000,
                "Service menyeluruh"
            ),

            (
                "Tambal Ban",
                20000,
                "Tambal ban bocor"
            )

        ]

        c.executemany("""
        INSERT INTO layanan(
        nama_layanan,
        harga,
        deskripsi
        )
        VALUES(?,?,?)
        """, data_layanan)

    conn.commit()
    conn.close()
