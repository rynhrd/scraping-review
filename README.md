# scraping-review

Adalah tools untuk mendapatkan informasi data review pada suatu toko yang ada di Shopee.
Ada beberapa pilihan output yaitu (Json & CSV).

## Dataset

| Atribut         | Penjelasan                               |
| --------------- | -----------------------------------------|
| cod_id          | gabungan beberapa atribut menjadi unique |
| orderid         | oderan yang dibuat                       |
| itemid          | barang yang direview pelanggan           |
| nama_pengguna   | nama user yang memberikan review         |
| produk          | nama produk dari toko                    |
| review          | isi text review                          |
| rating          | rating yang diberikan pada produk        |
| waktu transaksi | waktu user transaksi                     |


## Persyaratan

Sebelum memulai, pastikan Anda telah memenuhi persyaratan berikut:

1. Anda telah menginstal Python 3.x.
2. Anda memiliki akses ke terminal atau antarmuka baris perintah.
3. Anda telah menginstal Git (opsional, untuk cloning repository).

## Cara Mendapatkan URL Page Review

1. Buka toko mana yang ingin diambil review nya, kemudian klik bagian penilaian
   ![alt text](https://github.com/rynhrd/scraping-review/blob/main/assets/get_id_shop.jpg?raw=true)
2. Copy urlnya, Contoh `https://shopee.co.id/buyer/#########/rating?shop_id=#########`

## Setup main.py

- Git Clone -> git clone https://github.com/rynhrd/scraping-review.git
- Masuk ke direktori - > cd Scraping-Shopee-Produk
- Buat virtual environment -> python -m venv env
- Activate environment -> .\env\Scripts\activate (windows)
- Install requirement.txt -> pip install -r requirements.txt
- Cara mendapatkan cookies.json [Refrensi](https://fajrulfalah18.medium.com/melewati-sistem-auth-website-di-selenium-emang-bisa-8d88a8a177e8)
  taruh cookies hasil dari referensi ke cookies.json
- Jalankan -> python main.py
