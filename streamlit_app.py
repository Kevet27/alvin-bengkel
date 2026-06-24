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

