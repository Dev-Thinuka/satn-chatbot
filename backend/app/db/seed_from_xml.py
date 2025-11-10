import xml.etree.ElementTree as ET
import psycopg2

# === Database connection ===
conn = psycopg2.connect(
    host="localhost",
    port=5433,
    dbname="satn_chatbot",
    user="satn_admin",
    password="Thinuka!@#123"
)
cur = conn.cursor()

# === XML path ===
xml_path = r"C:\Repositories\sa-thomson-chatbot\backend\app\db\sathomsonnerys.WordPress.2025-11-04.xml"


tree = ET.parse(xml_path)
root = tree.getroot()

# WordPress namespace handling
ns = {'wp': 'http://wordpress.org/export/1.2/', 'content': 'http://purl.org/rss/1.0/modules/content/'}

count = 0
for item in root.findall('./channel/item'):
    post_type = item.find('wp:post_type', ns)
    if post_type is not None and post_type.text in ('hp_listing', 'listing', 'property'):


        title = item.find('title').text or ''
        description = item.find('content:encoded', ns).text or ''
        location = ''
        price = None
        bedrooms = None
        bathrooms = None
        image_url = ''

        # Parse postmeta fields
        for meta in item.findall('wp:postmeta', ns):
            key = meta.find('wp:meta_key', ns).text
            value_elem = meta.find('wp:meta_value', ns)
            value = value_elem.text if value_elem is not None else ''

            if key in ('price', '_price'):
                try:
                    price = float(value)
                except:
                    price = None
            elif key in ('bedrooms', '_bedrooms'):
                bedrooms = int(value) if value.isdigit() else None
            elif key in ('bathrooms', '_bathrooms'):
                bathrooms = int(value) if value.isdigit() else None
            elif key in ('location', '_location'):
                location = value
            elif key in ('image_url', '_thumbnail_url', '_thumbnail_id'):
                image_url = value

        # Insert into DB
        cur.execute("""
            INSERT INTO chatbot.listings (title, description, location, price, bedrooms, bathrooms, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (title, description, location, price, bedrooms, bathrooms, image_url))

        count += 1

conn.commit()
cur.close()
conn.close()

print(f"✅ Successfully inserted {count} listings into chatbot.listings.")
