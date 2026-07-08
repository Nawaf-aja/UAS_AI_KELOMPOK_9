from typing import Dict


DEFAULT_RECOMMENDATION = {
    "summary": "Keluhan perlu ditinjau oleh customer support untuk validasi detail kasus.",
    "priority": "Medium",
    "target_unit": "Customer Support",
    "sla": "1-3 hari kerja",
    "actions": [
        "Verifikasi identitas nasabah dan nomor laporan.",
        "Minta bukti pendukung seperti tanggal transaksi, nominal, dan kanal transaksi.",
        "Buat tiket pengaduan dan informasikan nomor tiket kepada nasabah.",
    ],
}


RECOMMENDATIONS: Dict[str, Dict] = {
    "account_management": {
        "summary": "Masalah terkait pengelolaan akun, akses rekening, PIN, login, ATM, atau data nasabah.",
        "priority": "Medium",
        "target_unit": "Account Support / Customer Service",
        "sla": "1-2 hari kerja",
        "actions": [
            "Verifikasi identitas nasabah melalui kanal resmi sebelum membuka detail akun.",
            "Jika terkait PIN, login, atau ATM, arahkan reset akses melalui aplikasi resmi, call center, atau cabang.",
            "Jika ada indikasi akses tidak sah, blokir sementara kanal digital sampai validasi selesai.",
        ],
    },
    "account_closure": {
        "summary": "Masalah terkait penutupan rekening, pembatalan layanan, atau akun yang belum selesai ditutup.",
        "priority": "Medium",
        "target_unit": "Branch Operation / Account Closure Team",
        "sla": "2-5 hari kerja",
        "actions": [
            "Cek saldo, hold dana, tagihan, dispute, atau produk tertaut yang menghambat penutupan.",
            "Berikan daftar syarat penutupan rekening secara tertulis kepada nasabah.",
            "Jika syarat lengkap, eskalasi ke unit operasional untuk penyelesaian dan bukti penutupan.",
        ],
    },
    "card_dispute": {
        "summary": "Masalah terkait kartu debit/kredit, transaksi kartu, statement, atau transaksi yang diperselisihkan.",
        "priority": "High",
        "target_unit": "Card Operation / Dispute / Chargeback Team",
        "sla": "3-14 hari kerja",
        "actions": [
            "Minta detail transaksi: tanggal, nominal, merchant, kanal, dan bukti statement.",
            "Pastikan transaksi bukan pending, subscription, cicilan, atau transaksi sah anggota keluarga.",
            "Jika transaksi tidak dikenali, ajukan dispute atau chargeback sesuai aturan kartu.",
        ],
    },
    "credit_reporting": {
        "summary": "Keluhan terkait informasi laporan kredit, skor, data tunggakan, atau pelaporan yang dianggap salah.",
        "priority": "Medium",
        "target_unit": "Credit Bureau Dispute / Data Correction Team",
        "sla": "5-14 hari kerja",
        "actions": [
            "Minta bukti data yang benar, identitas, dan laporan kredit yang dipermasalahkan.",
            "Bandingkan data internal bank dengan informasi yang dilaporkan ke biro kredit.",
            "Jika kesalahan tervalidasi, ajukan koreksi data dan informasikan estimasi pembaruan laporan.",
        ],
    },
    "fees_interest": {
        "summary": "Keluhan terkait biaya, bunga, penalti, denda, overdraft, atau tagihan yang dianggap tidak sesuai.",
        "priority": "Medium",
        "target_unit": "Billing / Fee Dispute Team",
        "sla": "3-7 hari kerja",
        "actions": [
            "Cocokkan biaya atau bunga dengan kontrak produk, tabel tarif, dan riwayat transaksi.",
            "Minta detail tanggal, nominal, dan bukti mutasi yang dipermasalahkan.",
            "Jika terjadi salah tagih, ajukan koreksi, waiver, atau refund sesuai kebijakan bank.",
        ],
    },
    "fraud_scam": {
        "summary": "Indikasi penipuan, scam, phishing, transaksi tidak sah, atau penyalahgunaan identitas.",
        "priority": "Critical",
        "target_unit": "Fraud Investigation / Security Team",
        "sla": "Segera, maksimal 1 hari kerja",
        "actions": [
            "Blokir sementara kartu, rekening, atau akses digital yang berisiko.",
            "Ingatkan nasabah untuk tidak membagikan OTP, PIN, password, atau data rahasia apa pun.",
            "Kumpulkan kronologi, bukti transaksi, nomor pelaku, tautan, dan waktu kejadian untuk investigasi.",
        ],
    },
    "loan_mortgage": {
        "summary": "Keluhan terkait pinjaman, mortgage, lender, cicilan, penagihan, atau servicing kredit.",
        "priority": "Medium",
        "target_unit": "Loan Servicing / Collection Support",
        "sla": "3-10 hari kerja",
        "actions": [
            "Cek status pinjaman, jadwal cicilan, bunga, denda, dan riwayat pembayaran.",
            "Minta dokumen kontrak, bukti pembayaran, dan komunikasi terakhir dengan lender atau servicer.",
            "Jika ada salah catat pembayaran atau penagihan, eskalasi ke loan servicing untuk koreksi.",
        ],
    },
    "payment_transfer": {
        "summary": "Masalah saat pembayaran, transfer, deposit, withdrawal, autodebet, atau transaksi gagal.",
        "priority": "High",
        "target_unit": "Payment Operation / Transaction Support",
        "sla": "1-3 hari kerja",
        "actions": [
            "Cek status transaksi melalui reference number, tanggal, nominal, dan rekening atau merchant tujuan.",
            "Jika saldo terdebit tetapi transaksi gagal, lakukan rekonsiliasi dan pantau proses reversal.",
            "Informasikan estimasi pengembalian dana dan minta nasabah menyimpan bukti transaksi.",
        ],
    },
    "managing_an_account": {
        "summary": "Masalah terkait pengelolaan akun, akses rekening, PIN, login, atau perubahan data.",
        "priority": "Medium",
        "target_unit": "Account Support / Customer Service",
        "sla": "1-2 hari kerja",
        "actions": [
            "Verifikasi identitas nasabah melalui data resmi dan kanal aman.",
            "Jika terkait PIN atau akses akun, arahkan nasabah ke reset PIN/password melalui aplikasi atau cabang.",
            "Jika ada indikasi akses tidak sah, blokir sementara akses digital sampai validasi selesai.",
        ],
    },
    "closing_an_account": {
        "summary": "Masalah terkait penutupan rekening atau layanan yang belum selesai.",
        "priority": "Medium",
        "target_unit": "Branch Operation / Account Closure Team",
        "sla": "2-5 hari kerja",
        "actions": [
            "Cek apakah masih ada saldo, tagihan, hold dana, atau produk aktif yang menghambat penutupan.",
            "Berikan daftar syarat penutupan rekening secara tertulis kepada nasabah.",
            "Jika syarat lengkap, eskalasi ke unit operasional cabang untuk penyelesaian.",
        ],
    },
    "fees_or_interest": {
        "summary": "Keluhan terkait biaya, bunga, denda, atau tagihan yang dianggap tidak sesuai.",
        "priority": "Medium",
        "target_unit": "Billing / Fee Dispute Team",
        "sla": "3-7 hari kerja",
        "actions": [
            "Cocokkan biaya atau bunga dengan tabel tarif dan kontrak produk.",
            "Minta detail tanggal, nominal, dan bukti mutasi yang dipermasalahkan.",
            "Jika terbukti salah tagih, ajukan koreksi atau refund sesuai prosedur bank.",
        ],
    },
    "fraud_or_scam": {
        "summary": "Indikasi penipuan, scam, phishing, transaksi tidak sah, atau penyalahgunaan akun.",
        "priority": "High",
        "target_unit": "Fraud Investigation / Security Team",
        "sla": "Segera, maksimal 1 hari kerja",
        "actions": [
            "Blokir sementara kartu, akun digital, atau kanal transaksi yang berisiko.",
            "Minta nasabah tidak membagikan OTP, PIN, password, atau data rahasia apa pun.",
            "Kumpulkan kronologi, bukti transaksi, nomor pelaku, tautan, dan waktu kejadian untuk investigasi.",
        ],
    },
    "getting_a_credit_card": {
        "summary": "Masalah pengajuan, aktivasi, pengiriman, atau verifikasi kartu kredit.",
        "priority": "Low",
        "target_unit": "Credit Card Acquisition / Card Operation",
        "sla": "3-7 hari kerja",
        "actions": [
            "Cek status aplikasi kartu kredit dan kelengkapan dokumen.",
            "Verifikasi alamat pengiriman dan status kurir jika kartu belum diterima.",
            "Jika aktivasi gagal, arahkan ke kanal aktivasi resmi atau cabang terdekat.",
        ],
    },
    "incorrect_information_on_your_report": {
        "summary": "Keluhan terkait data laporan kredit atau informasi nasabah yang dianggap salah.",
        "priority": "Medium",
        "target_unit": "Data Correction / Credit Bureau Dispute",
        "sla": "5-14 hari kerja",
        "actions": [
            "Minta bukti data yang benar dan dokumen identitas pendukung.",
            "Bandingkan data internal bank dengan laporan yang dipermasalahkan.",
            "Ajukan koreksi data ke unit pelaporan atau biro kredit jika kesalahan tervalidasi.",
        ],
    },
    "other_features_terms_or_problems": {
        "summary": "Keluhan umum tentang fitur, syarat layanan, atau masalah produk yang belum spesifik.",
        "priority": "Low",
        "target_unit": "Product Support",
        "sla": "2-5 hari kerja",
        "actions": [
            "Klarifikasi produk, kanal, dan fitur yang digunakan nasabah.",
            "Berikan penjelasan syarat dan ketentuan produk secara ringkas.",
            "Jika masalah teknis berulang, eskalasi ke tim produk atau IT support.",
        ],
    },
    "problem_with_a_lender_or_other_company_charging_your_account": {
        "summary": "Masalah debit oleh pemberi pinjaman, merchant, atau pihak ketiga.",
        "priority": "High",
        "target_unit": "Dispute / Third Party Debit Team",
        "sla": "1-5 hari kerja",
        "actions": [
            "Identifikasi merchant atau pihak ketiga yang melakukan pendebitan.",
            "Cek mandat autodebet, subscription, atau perjanjian pembayaran yang aktif.",
            "Jika transaksi tidak sah, buat dispute dan pertimbangkan blokir debit berikutnya.",
        ],
    },
    "problem_with_a_purchase_shown_on_your_statement": {
        "summary": "Transaksi pembelian muncul di statement tetapi tidak dikenali atau diperselisihkan.",
        "priority": "High",
        "target_unit": "Card Dispute / Chargeback Team",
        "sla": "3-14 hari kerja",
        "actions": [
            "Minta detail transaksi: tanggal, nominal, merchant, dan bukti statement.",
            "Pastikan transaksi bukan pending, subscription, atau transaksi keluarga yang sah.",
            "Jika tidak dikenali, ajukan dispute atau chargeback sesuai aturan kartu.",
        ],
    },
    "trouble_during_payment_process": {
        "summary": "Masalah saat pembayaran, transfer, autodebet, atau transaksi yang gagal.",
        "priority": "Medium",
        "target_unit": "Payment Operation / Transaction Support",
        "sla": "1-3 hari kerja",
        "actions": [
            "Cek status transaksi melalui reference number, tanggal, nominal, dan rekening tujuan.",
            "Jika saldo terdebit tetapi transaksi gagal, lakukan rekonsiliasi dan pantau proses reversal.",
            "Informasikan estimasi pengembalian dana dan minta nasabah menyimpan bukti transaksi.",
        ],
    },
}


def get_recommendation(label: str, confidence: float) -> Dict:
    recommendation = dict(RECOMMENDATIONS.get(label, DEFAULT_RECOMMENDATION))
    recommendation["actions"] = list(recommendation["actions"])
    if confidence < 0.45:
        recommendation["needs_human_review"] = True
        recommendation["confidence_note"] = (
            "Confidence model rendah, sehingga hasil perlu diverifikasi oleh petugas sebelum keputusan final."
        )
    else:
        recommendation["needs_human_review"] = False
        recommendation["confidence_note"] = "Confidence cukup untuk rekomendasi awal, tetapi tetap perlu validasi operasional."
    return recommendation
