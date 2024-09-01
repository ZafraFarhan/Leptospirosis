import os
import requests
from bs4 import BeautifulSoup
import pdfplumber
import pandas as pd
from google.cloud import storage
from pdf2image import convert_from_path
from PIL import Image

# Define the URL of the webpage and directory to save downloaded PDFs
url = 'https://www.epid.gov.lk/weekly-epidemiological-report/weekly-epidemiological-report'
output_dir = 'pdfs'
os.makedirs(output_dir, exist_ok=True)

def download_pdfs(url, output_dir):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all accordions
    accordions = soup.find_all(class_='accordions')

    downloaded_pdfs = []

    for accordion in accordions:
        content = accordion.find(class_='content')
        if content:
            products = content.find_all('li', class_='product')
            if products:
                last_product = products[-1]
                a_tag = last_product.find('a', href=True)
                if a_tag:
                    pdf_url = a_tag['href']
                    pdf_name = os.path.basename(pdf_url)
                    pdf_path = os.path.join(output_dir, pdf_name)

                    # Download the PDF
                    pdf_response = requests.get(pdf_url)
                    with open(pdf_path, 'wb') as file:
                        file.write(pdf_response.content)

                    downloaded_pdfs.append(pdf_path)

    return downloaded_pdfs

def extract_table_from_pdf(pdf_path, table_title):
    combined_data = pd.DataFrame()
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if table_title in text:
                tables = page.extract_tables()
                print('Table found')

                for table in tables:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df = df.applymap(lambda x: ''.join(x.split())[::-1] if isinstance(x, str) else x)

                    # Check for column existence and set up the DataFrame appropriately
                    if 'DPDHS\nDivision' in df.columns:
                        df = df.iloc[1:27, 12]  # Adjust indexing as needed
                    else:
                        df = df.iloc[3:29, 12]  # Adjust indexing as needed

                    df.reset_index(drop=True, inplace=True)
                    combined_data = pd.concat([combined_data, df], ignore_index=True, sort=False)

    return combined_data if not combined_data.empty else None

def extract_table_from_pdfr(pdf_path, table_title):
    images = convert_from_path(pdf_path, first_page=1, last_page=1)
    images[0].save('page_image.png')
    rotate_image('page_image.png', 90)

    with pdfplumber.open(pdf_path) as pdf:
        combined_data = pd.DataFrame()
        for page in pdf.pages:
            text = page.extract_text()
            if table_title in text:
                tables = page.extract_tables()
                print('Table found')

                for table in tables:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df = df.applymap(lambda x: ''.join(x.split())[::-1] if isinstance(x, str) else x)

                    # Adjust indexing based on specific PDF and table structure
                    if pdf_path.endswith('en_66b1cf8a4ad9f_Vol_51_no_29-english.pdf'):
                        df = df.iloc[15, 2:28]
                    else:
                        df = df.iloc[13, 2:28]

                    df.reset_index(drop=True, inplace=True)
                    combined_data = pd.concat([combined_data, df], ignore_index=True, sort=False)

    return combined_data if not combined_data.empty else None

def rotate_image(image_path, angle):
    with Image.open(image_path) as img:
        rotated = img.rotate(angle, expand=True)
        rotated.save(image_path)  # Save rotated image back to the same file

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    client = storage.Client.from_service_account_json('path/to/your-service-account-file.json')  # Correct path
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def main():
    pdf_paths = download_pdfs(url, output_dir)
    table_title = 'Selected notifiable diseases reported by Medical Officers of Health'

    all_combined_data = pd.DataFrame()

    for index, pdf_path in enumerate(pdf_paths):
        if 1 <= index < 12:
            extracted_data = extract_table_from_pdf(pdf_path, table_title)
        else:
            extracted_data = extract_table_from_pdfr(pdf_path, table_title)
        
        if extracted_data is not None:
            all_combined_data = pd.concat([all_combined_data, extracted_data], ignore_index=True, sort=False)
            print(f"Extracted data from {pdf_path}:")
            print(extracted_data)
        else:
            print(f"No matching table found in {pdf_path}")

    all_combined_data.columns = ['Cases']
    all_combined_data.to_csv('Leptospirosis_SriLanka.csv', index=False)

    # Upload the CSV file to Google Cloud Storage
    bucket_name = 'bkt-leptospirosis-df'
    upload_to_gcs(bucket_name, 'Leptospirosis_SriLanka.csv', 'Leptospirosis_SriLanka.csv')

if __name__ == "__main__":
    main()
