import streamlit as st
from database import *

# ==========================
# INISIALISASI DATABASE
# ==========================
init_db()

# ==========================
# KONFIGURASI HALAMAN
# ==========================
st.set_page_config(
    page_title="BengkelKu",
    page_icon="🔧",
    layout="wide"
)

# ==========================
# KONEKSI DATABASE
# ==========================
conn = get_connection()
c = conn.cursor()

# ==========================
# SESSION
# ==========================
if "login" not in st.session_state:
    st.session_state.login = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# ==========================
# MENU SEBELUM LOGIN
# ==========================
if not st.session_state.login:

    menu = st.sidebar.selectbox(
        "Menu",
        [
            "Beranda",
            "Login",
            "Register"
        ]
    )

# ==========================
# MENU SETELAH LOGIN
# ==========================
else:

    if st.session_state.role == "admin":

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

# ==========================
# BERANDA
# ==========================
if menu == "Beranda":

    st.title("🔧 BengkelKu Online")

    st.subheader(
        "Service Motor dan Mobil Profesional"
    )

    st.write("""
    ✅ Service Ringan

    ✅ Tune Up

    ✅ Ganti Oli

    ✅ Tambal Ban

    ✅ Service Lengkap

    ✅ Service Panggilan ke Lokasi
    """)

# ==========================
# REGISTER
# ==========================
elif menu == "Register":

    st.title("Registrasi Pengguna")

    nama = st.text_input("Nama")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    telepon = st.text_input(
        "Nomor Telepon"
    )

    if st.button("Daftar"):

        try:

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
                nama,
                username,
                password,
                telepon,
                "user"
            ))

            conn.commit()

            st.success(
                "Registrasi berhasil"
            )

        except:

            st.error(
                "Username sudah digunakan"
            )

# ==========================
# LOGIN
# ==========================
elif menu == "Login":

    st.title("Login")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Masuk"):

        c.execute("""
        SELECT *
        FROM users
        WHERE username=? AND password=?
        """,
        (
            username,
            password
        ))

        user = c.fetchone()

        if user:

            st.session_state.login = True
            st.session_state.username = user["username"]
            st.session_state.role = user["role"]

            st.success(
                "Login berhasil"
            )

            st.rerun()

        else:

            st.error(
                "Username atau password salah"
            )

