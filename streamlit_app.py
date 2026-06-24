import sqlite3

DB_NAME = "bengkel.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    # User
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

    # Layanan
    c.execute("""
    CREATE TABLE IF NOT EXISTS layanan(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_layanan TEXT,
        harga INTEGER,
        deskripsi TEXT
    )
    """)

    # Cabang Bengkel
    c.execute("""
    CREATE TABLE IF NOT EXISTS cabang(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_bengkel TEXT,
        alamat TEXT,
        telepon TEXT
    )
    """)

    # Booking Service
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

    # Customer Care
    c.execute("""
    CREATE TABLE IF NOT EXISTS pengaduan(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        pesan TEXT,
        status TEXT
    )
    """)

    conn.commit()

    # Admin default
    c.execute("SELECT * FROM users WHERE username='admin'")
    cek = c.fetchone()

    if not cek:
        c.execute("""
        INSERT INTO users(nama,username,password,telepon,role)
        VALUES(?,?,?,?,?)
        """,
        (
            "Administrator",
            "admin",
            "admin123",
            "08123456789",
            "admin"
        ))

    conn.commit()
    conn.close()

import streamlit as st
from database import *

init_db()

st.set_page_config(
    page_title="BengkelKu",
    layout="wide"
)

conn = get_connection()
c = conn.cursor()

if "login" not in st.session_state:
    st.session_state.login = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""


menu = st.sidebar.selectbox(
    "Menu",
    [
        "Beranda",
        "Login",
        "Register"
    ]
)

elif menu=="Register":

    st.title("Registrasi Pengguna")

    nama = st.text_input("Nama")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    telepon = st.text_input("Telepon")

    if st.button("Daftar"):

        try:

            c.execute("""
            INSERT INTO users(
            nama,username,password,telepon,role
            )
            VALUES(?,?,?,?,?)
            """,
            (
                nama,
                username,
                password,
                telepon,
                "user"
            ))

            conn.commit()

            st.success("Registrasi berhasil")

        except:
            st.error("Username sudah digunakan")

elif menu=="Login":

    st.title("Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Masuk"):

        c.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
        """,(username,password))

        user = c.fetchone()

        if user:

            st.session_state.login = True
            st.session_state.username = user["username"]
            st.session_state.role = user["role"]

            st.success("Login berhasil")
            st.rerun()

        else:
            st.error("Username atau password salah")

if menu=="Beranda":

    st.title("🚗 BengkelKu Online")

    st.subheader("Service Motor dan Mobil")

    st.write("""
    ✔ Service ringan

    ✔ Tune up

    ✔ Ganti oli

    ✔ Tambal ban

    ✔ Service lengkap

    ✔ Service panggilan ke lokasi
    """)

    st.image(
        "https://images.unsplash.com/photo-1487754180451-c456f719a1fc?w=1200",
        use_container_width=True
    )

if st.session_state.login:

    if st.session_state.role=="admin":

        menu = st.sidebar.selectbox(
            "Menu Admin",
            [
                "Dashboard",
                "Kelola Layanan",
                "Kelola Cabang",
                "Booking Masuk",
                "Customer Care",
                "Logout"
            ]
        )

    else:

        menu = st.sidebar.selectbox(
            "Menu User",
            [
                "Beranda",
                "Layanan",
                "Service Panggilan",
                "History",
                "Customer Care",
                "Profil",
                "Logout"
            ]
        )

# ==============================
# KELOLA LAYANAN
# ==============================

elif menu == "Kelola Layanan":

    st.title("Kelola Layanan")

    col1, col2 = st.columns(2)

    with col1:

        nama_layanan = st.text_input("Nama Layanan")
        harga = st.number_input("Harga", 0)

        deskripsi = st.text_area("Deskripsi")

        if st.button("Tambah Layanan"):

            c.execute("""
            INSERT INTO layanan(
            nama_layanan,harga,deskripsi)
            VALUES(?,?,?)
            """,
            (
                nama_layanan,
                harga,
                deskripsi
            ))

            conn.commit()

            st.success("Layanan berhasil ditambahkan")
            st.rerun()

    st.subheader("Daftar Layanan")

    c.execute("SELECT * FROM layanan")
    data = c.fetchall()

    for d in data:

        col1, col2, col3 = st.columns([3,2,1])

        with col1:
            st.write(d["nama_layanan"])

        with col2:
            st.write(f"Rp {d['harga']:,}")

        with col3:
            if st.button("Hapus", key=d["id"]):

                c.execute(
                    "DELETE FROM layanan WHERE id=?",
                    (d["id"],)
                )

                conn.commit()
                st.rerun()

# ==============================
# KELOLA CABANG
# ==============================

elif menu == "Kelola Cabang":

    st.title("Kelola Cabang Bengkel")

    nama = st.text_input("Nama Bengkel")

    alamat = st.text_area("Alamat")

    telepon = st.text_input("Nomor Telepon")

    if st.button("Tambah Cabang"):

        c.execute("""
        INSERT INTO cabang(
        nama_bengkel,
        alamat,
        telepon)
        VALUES(?,?,?)
        """,
        (
            nama,
            alamat,
            telepon
        ))

        conn.commit()

        st.success("Cabang berhasil ditambahkan")
        st.rerun()

    st.subheader("Daftar Cabang")

    c.execute("SELECT * FROM cabang")
    cabang = c.fetchall()

    for x in cabang:

        st.info(
            f"""
            {x['nama_bengkel']}

            {x['alamat']}

            {x['telepon']}
            """
        )

        if st.button(
            "Hapus Cabang",
            key=f"cabang{x['id']}"
        ):

            c.execute(
                "DELETE FROM cabang WHERE id=?",
                (x["id"],)
            )

            conn.commit()

            st.rerun()

# ==============================
# SERVICE PANGGILAN
# ==============================

elif menu == "Service Panggilan":

    st.title("Booking Service")

    c.execute("SELECT * FROM layanan")
    layanan_db = c.fetchall()

    daftar_layanan = []

    for i in layanan_db:
        daftar_layanan.append(i["nama_layanan"])

    layanan = st.selectbox(
        "Pilih Layanan",
        daftar_layanan
    )

    jenis_service = st.radio(
        "Jenis Service",
        [
            "Datang ke Bengkel",
            "Service Panggilan"
        ]
    )

    keluhan = st.text_area("Keluhan")

    tanggal = st.date_input("Tanggal")

    lokasi = st.text_area(
        "Alamat Lengkap"
    )

    if st.button("Booking Sekarang"):

        c.execute("""
        INSERT INTO booking(
        username,
        layanan,
        jenis_service,
        keluhan,
        tanggal,
        lokasi,
        status)
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            st.session_state.username,
            layanan,
            jenis_service,
            keluhan,
            str(tanggal),
            lokasi,
            "Menunggu"
        ))

        conn.commit()

        st.success(
            "Booking berhasil dilakukan"
        )

# ==============================
# HISTORY USER
# ==============================

elif menu == "History":

    st.title("Riwayat Service")

    c.execute("""
    SELECT * FROM booking
    WHERE username=?
    ORDER BY id DESC
    """,
    (
        st.session_state.username,
    ))

    data = c.fetchall()

    if len(data) == 0:

        st.warning(
            "Belum ada riwayat service"
        )

    else:

        for d in data:

            st.container()

            st.success(
                f"""
                Layanan : {d['layanan']}

                Jenis : {d['jenis_service']}

                Keluhan : {d['keluhan']}

                Tanggal : {d['tanggal']}

                Lokasi : {d['lokasi']}

                Status : {d['status']}
                """
            )

# =====================================
# BOOKING MASUK
# =====================================

elif menu == "Booking Masuk":

    st.title("Booking Masuk")

    c.execute("""
    SELECT * FROM booking
    ORDER BY id DESC
    """)

    data = c.fetchall()

    if data:

        for d in data:

            st.subheader(
                f"Booking #{d['id']}"
            )

            st.write("User :", d["username"])
            st.write("Layanan :", d["layanan"])
            st.write("Jenis :", d["jenis_service"])
            st.write("Keluhan :", d["keluhan"])
            st.write("Tanggal :", d["tanggal"])
            st.write("Lokasi :", d["lokasi"])
            st.write("Status :", d["status"])

            status_baru = st.selectbox(
                "Ubah Status",
                [
                    "Menunggu",
                    "Diproses",
                    "Teknisi Menuju Lokasi",
                    "Selesai"
                ],
                key=d["id"]
            )

            if st.button(
                "Update",
                key=f"u{d['id']}"
            ):

                c.execute("""
                UPDATE booking
                SET status=?
                WHERE id=?
                """,
                (
                    status_baru,
                    d["id"]
                ))

                conn.commit()

                st.success("Status diperbarui")
                st.rerun()

# =====================================
# CUSTOMER CARE USER
# =====================================

elif menu == "Customer Care" and st.session_state.role == "user":

    st.title("Customer Care")

    pesan = st.text_area(
        "Keluhan atau Pengaduan"
    )

    if st.button("Kirim"):

        c.execute("""
        INSERT INTO pengaduan(
        username,
        pesan,
        status
        )
        VALUES(?,?,?)
        """,
        (
            st.session_state.username,
            pesan,
            "Belum Dibaca"
        ))

        conn.commit()

        st.success(
            "Pengaduan berhasil dikirim"
        )

# =====================================
# CUSTOMER CARE ADMIN
# =====================================

elif menu == "Customer Care" and st.session_state.role == "admin":

    st.title("Daftar Pengaduan")

    c.execute("""
    SELECT * FROM pengaduan
    ORDER BY id DESC
    """)

    data = c.fetchall()

    for d in data:

        st.info(
            f"""
User : {d['username']}

Pesan :
{d['pesan']}

Status :
{d['status']}
"""
        )

        if st.button(
            "Tandai Selesai",
            key=f"p{d['id']}"
        ):

            c.execute("""
            UPDATE pengaduan
            SET status='Selesai'
            WHERE id=?
            """,
            (
                d["id"],
            ))

            conn.commit()

            st.rerun()

# =====================================
# PROFIL
# =====================================

elif menu == "Profil":

    st.title("Profil Saya")

    c.execute("""
    SELECT *
    FROM users
    WHERE username=?
    """,
    (
        st.session_state.username,
    ))

    user = c.fetchone()

    nama = st.text_input(
        "Nama",
        value=user["nama"]
    )

    telepon = st.text_input(
        "Telepon",
        value=user["telepon"]
    )

    password = st.text_input(
        "Password Baru",
        type="password"
    )

    if st.button("Simpan"):

        if password == "":
            password = user["password"]

        c.execute("""
        UPDATE users
        SET nama=?,
            telepon=?,
            password=?
        WHERE username=?
        """,
        (
            nama,
            telepon,
            password,
            st.session_state.username
        ))

        conn.commit()

        st.success("Profil diperbarui")

# =====================================
# DASHBOARD ADMIN
# =====================================

elif menu == "Dashboard":

    st.title("Dashboard Admin")

    c.execute("SELECT COUNT(*) FROM users")
    jumlah_user = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM layanan")
    jumlah_layanan = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM cabang")
    jumlah_cabang = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM booking")
    jumlah_booking = c.fetchone()[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Jumlah User",
            jumlah_user
        )

        st.metric(
            "Jumlah Layanan",
            jumlah_layanan
        )

    with col2:

        st.metric(
            "Jumlah Cabang",
            jumlah_cabang
        )

        st.metric(
            "Jumlah Booking",
            jumlah_booking
        )

