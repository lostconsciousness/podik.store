import xmltodict
import json

data = json.load(open("data.json", "r", encoding="UTF-8"))
pods = data["yml_catalog"]["shop"]["offers"]["offer"]
print(pods[0]["@id"])

# with open('media/final.xml', 'r', encoding='utf-8') as f:
#     xml_data = f.read()

# xml_dict = xmltodict.parse(xml_data.replace("&", "&amp;"))

# json_data = json.dumps(xml_dict, indent=4, ensure_ascii=False)

# with open('data.json', 'w', encoding='utf-8') as f:
#     f.write(json_data)

# import xmltodict
# from xml.dom.minidom import parseString
# import json

# with open('offer.xml', 'r') as f:
#     xml_data = f.read()

# dom = parseString(xml_data.replace("&", "&amp;"))
# xmlStringSerialized = dom.toxml()

# allDone = ""

# parser = xmltodict.parse(xmlStringSerialized)

# allDone = json.dumps(parser, indent=4, ensure_ascii=False)

# with open('data.json', 'w', encoding='utf-8') as f:
#     f.write(allDone)