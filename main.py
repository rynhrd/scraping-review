import requests
from datetime import datetime
import json
import csv
import os

def load_cookie(cookies_json) -> dict:
    # Function ini bertanggung jawab untuk memuat cookie json
    cookies_data = None
    with open(cookies_json) as f:
        cookies_data = json.load(f)

    cookies_string = ""
    for index, data in enumerate(cookies_data):
        temp = f"{str(data['name'])}={data['value']}"

        if index < len(cookies_data) - 1:
            temp += ";"

        cookies_string += temp

    return cookies_string


def shopee(url, cookies_json, save_format):
    # Setup ID toko dan ID pengguna dari URL
    shop_url = url.split("/")
    cookies = load_cookie(cookies_json)

    if not cookies:
        print("Cookies not valid")
        return

    headers = {"content-type": "application/json", "cookie": cookies}

    user_id = shop_url[4]
    shop_id = shop_url[5].replace("rating?shop_id=", "")
    count = 0  # Mulai dari 0
    reviews = []

    while True:
        try:
            # Menggunakan count sebagai offset
            url = f"https://shopee.co.id/api/v4/seller_operation/get_shop_ratings_new?limit=6&offset={count}&replied=false&shopid={shop_id}&userid={user_id}"
            req = requests.request("GET", url, headers=headers, data={})
            data_req = req.json()
            data_review = []
            try:
                data_review = data_req["data"]["items"]
            except:
                break

            for value in data_review:
                data_result = {
                    "code_id": f"{value['itemid']}_{value['ctime']}_{value['userid']}",
                    "orderid": value["orderid"],
                    "itemid": value["itemid"],
                    "nama_pengguna": value["author_username"],
                    "produk": value["product_items"][0]["name"],
                    "review": value["comment"],
                    "rating": value["rating_star"],
                    "waktu_transaksi": datetime.fromtimestamp(value["ctime"]).strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                }
                reviews.append(data_result)

            # Tampilkan progress "Fetching reviews: (count)"
            count += 6  # Tambahkan 6 setelah setiap pengambilan data
            print(f"Fetching reviews: {count} reviews", end='\r')  # Tampilkan di baris yang sama

        except KeyError:        
            break

    # Membuat folder output jika belum ada
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Nama file dengan format product_name_timestamp
    if reviews:
        product_name = shop_id
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Simpan data sesuai pilihan format
        if save_format == "json":
            file_name = os.path.join(output_folder, f"{product_name}_{timestamp}.json")

            # Menyimpan data ke file JSON di folder output dengan id_shop di luar reviews
            output_data = {
                "id_shop": shop_id,
                "reviews": reviews
            }

            with open(file_name, "w", encoding="utf-8") as output_file:
                json.dump(output_data, output_file, ensure_ascii=False, indent=4)

            print(f"\nData saved as JSON at {file_name}")
        
        elif save_format == "csv":
            file_name = os.path.join(output_folder, f"{product_name}_{timestamp}.csv")

            # Menyimpan data ke file CSV di folder output
            keys = reviews[0].keys()
            with open(file_name, "w", newline='', encoding="utf-8") as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(reviews)

            print(f"\nData saved as CSV at {file_name}")
        
        else:
            print("\nInvalid format selected.")
    else:
        print("\nNo reviews found.")


if __name__ == '__main__':    
    # Input URL
    url_shop = input("Please enter the Shopee shop URL: ")
    cookies_json = "cookies.json"

    # Memilih format penyimpanan dengan pilihan angka
    print("Select save format:")
    print("1. JSON")
    print("2. CSV")
    
    while True:
        save_format_choice = input("Enter your choice (1/2): ")

        if save_format_choice == "1":
            save_format = "json"
            break
        elif save_format_choice == "2":
            save_format = "csv"
            break
        else:
            print("Invalid choice, please select 1 or 2.")

    # Panggil fungsi dengan format yang dipilih
    shopee(url_shop, cookies_json, save_format)

