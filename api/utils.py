import xmltodict
import json

with open('tests/response_a.xml') as xml_file:
    data_dict = xmltodict.parse(xml_file.read())
    print(data_dict)
json_data = json.dumps(data_dict, indent=4,)

with open('example.json', 'w') as json_file:
    json_file.write(json_data)