import xml.etree.ElementTree as ET
ns = {'wp': 'http://wordpress.org/export/1.2/', 'content': 'http://purl.org/rss/1.0/modules/content/'}
tree = ET.parse("app/db/sathomsonnerys.WordPress.2025-11-04.xml")
root = tree.getroot()
for item in root.findall('./channel/item'):
    post_type = item.find('wp:post_type', ns)
    title = item.find('title').text
    print(post_type.text, "=>", title)
