import csv
import os
import requests
from bs4 import BeautifulSoup

# 定义JBL.csv的表头
header = [
    "handler", "title", "sub_title", "body_html", "status", "is_use_stock", 
    "soldout_policy", "requires_shipping", "tags", "category", "optional1_name", 
    "optional1_value", "optional2_name", "optional2_value", "optional3_name", 
    "optional3_value", "price", "compare_at_price", "sku_code", "inventory_quantity", 
    "weight", "weight_unit", "barcode", "product_image", "product_image_sorted", "image"
]

def extract_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 提取数据
    handler = url.split('/products/')[-1]
    
    title_element = soup.find('input', class_='J-product-title', type='hidden')
    title = title_element['value'] if title_element else ''
    
    product_details_div = soup.find('div', class_='product-details')
    body_html = ''.join(str(content) for content in product_details_div.contents) if product_details_div else ''
    
    # 创建数据字典，未实现的属性填充空值
    data = {field: '' for field in header}
    
    # 填充已实现的属性
    data.update({
        'handler': handler,
        'title': title,
        'body_html': body_html,
        'status': 'Y',
        'is_use_stock': 0,
        'soldout_policy': 'Y',
        'requires_shipping': 0,
        'tags': '',
        'category': '',
        'optional1_name': '',
        'optional1_value': '',
        'optional2_name': '',
        'optional2_value': '',
        'optional3_name': '',
    })
    
    return data

def write_csv(data, filename='extracted_product.csv'):
    # 指定保存路径
    save_path = r'C:\Users\Administrator\Desktop'
    full_path = os.path.join(save_path, filename)
    
    with open(full_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerow(data)
    print(f'数据已保存到 {full_path}')

# 主程序
url = 'https://www.gicdas.com/products/e-xb2'
extracted_data = extract_data(url)
write_csv(extracted_data)