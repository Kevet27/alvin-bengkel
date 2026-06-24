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

# ==========================
# LAYANAN
# ==========================
elif menu == "Layanan":

    st.title("Daftar Layanan Bengkel")

    c.execute("""
    SELECT * FROM layanan
    """)

    data = c.fetchall()

    for d in data:

        with st.container():

            st.subheader(
                d["nama_layanan"]
            )

            st.write(
                d["deskripsi"]
            )

            st.success(
                f"Rp {d['harga']:,}"
            )


# ==========================
# SERVICE PANGGILAN
# ==========================
elif menu == "Service Panggilan":

    st.title("Booking Service")

    c.execute("""
    SELECT *
    FROM layanan
    """)

    data_layanan = c.fetchall()

    daftar_layanan = []

    for x in data_layanan:

        daftar_layanan.append(
            x["nama_layanan"]
        )

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

    keluhan = st.text_area(
        "Keluhan Kendaraan"
    )

    tanggal = st.date_input(
        "Tanggal Service"
    )

    lokasi = st.text_area(
        "Alamat Lengkap"
    )

    if st.button(
        "Booking Sekarang"
    ):

        c.execute("""
        INSERT INTO booking(
        username,
        layanan,
        jenis_service,
        keluhan,
        tanggal,
        lokasi,
        status
        )
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
            "Booking berhasil dibuat"
        )

# ==========================
# HISTORY SERVICE
# ==========================
elif menu == "History":

    st.title("Riwayat Service")

    c.execute("""
    SELECT *
    FROM booking
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

            st.info(
                f"""
Layanan : {d['layanan']}

Jenis Service : {d['jenis_service']}

Keluhan : {d['keluhan']}

Tanggal : {d['tanggal']}

Lokasi : {d['lokasi']}

Status : {d['status']}
"""
            )


# ==========================
# CUSTOMER CARE
# ==========================
elif menu == "Customer Care":

    st.title("Customer Care")

    pesan = st.text_area(
        "Keluhan atau Pengaduan"
    )

    if st.button(
        "Kirim Pengaduan"
    ):

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

    st.subheader(
        "Riwayat Pengaduan"
    )

    c.execute("""
    SELECT *
    FROM pengaduan
    WHERE username=?
    ORDER BY id DESC
    """,
    (
        st.session_state.username,
    ))

    data = c.fetchall()

    for d in data:

        st.info(
            f"""
Pesan :
{d['pesan']}

Status :
{d['status']}
"""
        )


# ==========================
# PROFIL
# ==========================
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
        "Nomor Telepon",
        value=user["telepon"]
    )

    password_baru = st.text_input(
        "Password Baru",
        type="password"
    )

    if st.button(
        "Simpan Perubahan"
    ):

        password = user["password"]

        if password_baru != "":
            password = password_baru

        c.execute("""
        UPDATE users
        SET
        nama=?,
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

        st.success(
            "Profil berhasil diperbarui"
        )


# ==========================
# LOGOUT
# ==========================
elif menu == "Logout":

    st.session_state.login = False
    st.session_state.username = ""
    st.session_state.role = ""

    st.success(
        "Logout berhasil"
    )

    st.rerun()

# ==========================
# DASHBOARD ADMIN
# ==========================
elif menu == "Dashboard":

    st.title("Dashboard Admin")

    # =====================
    # JUMLAH USER
    # =====================
    c.execute("SELECT COUNT(*) FROM users")
    jumlah_user = c.fetchone()[0]

    # =====================
    # JUMLAH LAYANAN
    # =====================
    c.execute("SELECT COUNT(*) FROM layanan")
    jumlah_layanan = c.fetchone()[0]

    # =====================
    # JUMLAH CABANG
    # =====================
    c.execute("SELECT COUNT(*) FROM cabang")
    jumlah_cabang = c.fetchone()[0]

    # =====================
    # JUMLAH BOOKING
    # =====================
    c.execute("SELECT COUNT(*) FROM booking")
    jumlah_booking = c.fetchone()[0]

    # =====================
    # TOTAL PENGADUAN
    # =====================
    c.execute("SELECT COUNT(*) FROM pengaduan")
    jumlah_pengaduan = c.fetchone()[0]

    # =====================
    # TOTAL PENDAPATAN
    # =====================
    c.execute("""
    SELECT SUM(harga)
    FROM transaksi
    """)

    total_pendapatan = c.fetchone()[0]

    if total_pendapatan is None:
        total_pendapatan = 0

    st.subheader("Statistik Bengkel")

    col1, col2, col3 = st.columns(3)

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

    with col3:

        st.metric(
            "Jumlah Pengaduan",
            jumlah_pengaduan
        )

        st.metric(
            "Pendapatan",
            f"Rp {total_pendapatan:,}"
        )

    st.divider()

    st.subheader("Ringkasan Sistem")

    st.success(
        f"""
Jumlah User : {jumlah_user}

Jumlah Layanan : {jumlah_layanan}

Jumlah Cabang : {jumlah_cabang}

Jumlah Booking : {jumlah_booking}

Jumlah Pengaduan : {jumlah_pengaduan}

Total Pendapatan : Rp {total_pendapatan:,}
"""
    )

# ==========================
# KELOLA CABANG
# ==========================
elif menu == "Kelola Cabang":

    st.title("Kelola Cabang Bengkel")

    nama_bengkel = st.text_input(
        "Nama Bengkel"
    )

    alamat = st.text_area(
        "Alamat"
    )

    telepon = st.text_input(
        "Nomor Telepon"
    )

    if st.button(
        "Tambah Cabang"
    ):

        c.execute("""
        INSERT INTO cabang(
        nama_bengkel,
        alamat,
        telepon
        )
        VALUES(?,?,?)
        """,
        (
            nama_bengkel,
            alamat,
            telepon
        ))

        conn.commit()

        st.success(
            "Cabang berhasil ditambahkan"
        )

        st.rerun()

    st.divider()

    st.subheader(
        "Daftar Cabang"
    )

    c.execute("""
    SELECT *
    FROM cabang
    ORDER BY id DESC
    """)

    data = c.fetchall()

    for d in data:

        with st.expander(
            d["nama_bengkel"]
        ):

            alamat_baru = st.text_area(
                "Alamat",
                value=d["alamat"],
                key=f"a{d['id']}"
            )

            telepon_baru = st.text_input(
                "Telepon",
                value=d["telepon"],
                key=f"t{d['id']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Update Cabang",
                    key=f"uc{d['id']}"
                ):

                    c.execute("""
                    UPDATE cabang
                    SET alamat=?,
                    telepon=?
                    WHERE id=?
                    """,
                    (
                        alamat_baru,
                        telepon_baru,
                        d["id"]
                    ))

                    conn.commit()

                    st.success(
                        "Cabang berhasil diperbarui"
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "Hapus Cabang",
                    key=f"hc{d['id']}"
                ):

                    c.execute("""
                    DELETE FROM cabang
                    WHERE id=?
                    """,
                    (
                        d["id"],
                    ))

                    conn.commit()

                    st.rerun()
