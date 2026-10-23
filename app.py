import streamlit as st
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3

st.set_page_config(
    page_title="Sistem Klasifikasi Himpunan",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sistem Klasifikasi Data dengan Himpunan")
st.write("PJBL-2 | Operasi Himpunan dan Diagram Venn")

st.sidebar.header("Input Dataset")

contoh = st.sidebar.selectbox(
    "Pilih Dataset",
    ["Dataset 1 - Minat Pemrograman",
     "Dataset 2 - Kegiatan Mahasiswa",
     "Input Manual"]
)

if contoh == "Dataset 1 - Minat Pemrograman":
    semesta_default = "Ani, Budi, Citra, Dedi, Eka, Fajar, Gita, Hani"
    a_default = "Ani, Budi, Citra, Dedi"
    b_default = "Citra, Dedi, Eka, Fajar"
    c_default = "Budi, Dedi, Gita"

elif contoh == "Dataset 2 - Kegiatan Mahasiswa":
    semesta_default = "Andi, Bella, Candra, Dinda, Eko, Fina, Gilang, Hana, Intan"
    a_default = "Andi, Bella, Candra, Eko"
    b_default = "Bella, Dinda, Eko, Fina"
    c_default = "Candra, Eko, Gilang, Hana"

else:
    semesta_default = "Ari, Bima, Cici, Danu, Eka, Fani"
    a_default = "Ari, Bima, Cici"
    b_default = "Bima, Danu, Eka"
    c_default = "Cici, Eka, Fani"


def baca_himpunan(teks):
    return {
        x.strip()
        for x in teks.split(",")
        if x.strip()
    }


U_teks = st.sidebar.text_area(
    "Semesta U", semesta_default
)
A_teks = st.sidebar.text_area("Himpunan A", a_default)
B_teks = st.sidebar.text_area("Himpunan B", b_default)
C_teks = st.sidebar.text_area("Himpunan C", c_default)

U = baca_himpunan(U_teks)
A_input = baca_himpunan(A_teks)
B_input = baca_himpunan(B_teks)
C_input = baca_himpunan(C_teks)

if not U:
    st.error("Himpunan semesta U tidak boleh kosong.")
    st.stop()

di_luar = (A_input | B_input | C_input) - U

if di_luar:
    st.warning(
        "Anggota di luar semesta U diabaikan: "
        + ", ".join(sorted(di_luar))
    )

A = A_input & U
B = B_input & U
C = C_input & U


tab1, tab2, tab3, tab4 = st.tabs([
    "Operasi Himpunan",
    "Diagram Venn",
    "Perhitungan PIE",
    "Pengujian"
])


with tab1:
    st.header("Anggota Himpunan")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Semesta U", len(U))
    col2.metric("Himpunan A", len(A))
    col3.metric("Himpunan B", len(B))
    col4.metric("Himpunan C", len(C))

    st.write("U =", sorted(U))
    st.write("A =", sorted(A))
    st.write("B =", sorted(B))
    st.write("C =", sorted(C))

    operasi = st.selectbox(
        "Pilih Operasi",
        [
            "Union A ∪ B",
            "Intersection A ∩ B",
            "Difference A - B",
            "Difference B - A",
            "Complement A",
            "Complement B",
            "Union A ∪ B ∪ C",
            "Intersection A ∩ B ∩ C",
            "Difference A - (B ∪ C)",
            "Complement C"
        ]
    )

    hasil_operasi = {
        "Union A ∪ B": A | B,
        "Intersection A ∩ B": A & B,
        "Difference A - B": A - B,
        "Difference B - A": B - A,
        "Complement A": U - A,
        "Complement B": U - B,
        "Union A ∪ B ∪ C": A | B | C,
        "Intersection A ∩ B ∩ C": A & B & C,
        "Difference A - (B ∪ C)": A - (B | C),
        "Complement C": U - C
    }

    hasil = hasil_operasi[operasi]

    st.subheader("Hasil Operasi")
    st.write(sorted(hasil) if hasil else "Himpunan kosong (∅)")
    st.success(f"Jumlah anggota hasil: {len(hasil)}")


with tab2:
    st.header("Visualisasi Diagram Venn")

    tiga_himpunan = st.checkbox(
        "Tampilkan tiga himpunan", value=True
    )

    # Membuat objek figure gambar
    fig, ax = plt.subplots(figsize=(8, 6))

    if tiga_himpunan:
        venn3(
            [A, B, C],
            set_labels=("Himpunan A", "Himpunan B", "Himpunan C"),
            ax=ax
        )
    else:
        venn2(
            [A, B],
            set_labels=("Himpunan A", "Himpunan B"),
            ax=ax
        )

    # Tambahan baris ini untuk menghapus bingkai kotak luar agar diagram lingkaran terlihat rapi
    ax.axis('off') 
    
    ax.set_title("Diagram Venn Hubungan Antar Himpunan", fontsize=14, fontweight='bold')
    
    # Menampilkan ke UI Streamlit
    st.pyplot(fig)
    plt.close(fig)


with tab3:
    st.header("Prinsip Inklusi-Eksklusi (PIE)")

    gunakan_tiga = st.checkbox(
        "Hitung PIE untuk tiga himpunan",
        value=True
    )

    if gunakan_tiga:
        rumus = (
            len(A) + len(B) + len(C)
            - len(A & B)
            - len(A & C)
            - len(B & C)
            + len(A & B & C)
        )

        st.latex(
            r"|A\cup B\cup C|=|A|+|B|+|C|"
            r"-|A\cap B|-|A\cap C|-|B\cap C|"
            r"+|A\cap B\cap C|"
        )

        st.write(
            f"{len(A)} + {len(B)} + {len(C)} "
            f"- {len(A & B)} - {len(A & C)} "
            f"- {len(B & C)} + {len(A & B & C)}"
        )

        jumlah_langsung = len(A | B | C)

    else:
        rumus = len(A) + len(B) - len(A & B)

        st.latex(
            r"|A\cup B|=|A|+|B|-|A\cap B|"
        )

        st.write(
            f"{len(A)} + {len(B)} - {len(A & B)}"
        )

        jumlah_langsung = len(A | B)

    st.metric("Jumlah unik menurut PIE", rumus)
    st.metric("Jumlah unik hasil union", jumlah_langsung)

    if rumus == jumlah_langsung:
        st.success("Validasi PIE berhasil!")
    else:
        st.error("Hasil tidak sesuai. Periksa dataset.")


with tab4:
    st.header("Pengujian Aplikasi")

    hasil_uji = {
        "Union konsisten dengan PIE dua himpunan":
            len(A | B) == len(A) + len(B) - len(A & B),

        "Intersection merupakan bagian A dan B":
            (A & B) <= A and (A & B) <= B,

        "Difference A-B tidak beririsan dengan B":
            (A - B).isdisjoint(B),

        "Complement A berada dalam semesta U":
            (U - A) <= U,

        "PIE tiga himpunan benar":
            len(A | B | C) ==
            len(A) + len(B) + len(C)
            - len(A & B) - len(A & C)
            - len(B & C) + len(A & B & C)
    }

    for nama, status in hasil_uji.items():
        if status:
            st.success("PASS: " + nama)
        else:
            st.error("FAIL: " + nama)

    st.info(
        "Pilih Dataset 1 dan Dataset 2 melalui sidebar "
        "untuk menguji dua dataset berbeda."
    )

st.divider()
st.caption("PJBL-2 | Sistem Klasifikasi Data dengan Himpunan")