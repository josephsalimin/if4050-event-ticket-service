
from suds.client import Client

test_client = Client('http://localhost:8000/?wsdl')

print(test_client)
event = test_client.factory.create('ns0:Event')
event.name = "Biji"
event.location = "Jakarta"
event.partner_id = 1
event.start_at = 2
event.end_at = 3
event.description = "Festival Biji Jakarta"

section_array = test_client.factory.create('ns0:SectionArray')
section = test_client.factory.create('ns0:Section')
section.name = "Hehe"
section.capacity = 100
section.has_seat = True
print(section)

section_array.Section.append(section)

print(section_array)

results = test_client.service.CreateEvent(event, section_array)
