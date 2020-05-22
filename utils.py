import json
import textwrap
with open("data/spells.json", "r") as spells_file:
	spells = json.load(spells_file)
	spells_file.close()



def lookup(spell_name): 
	for index in spells:
		if index.lower().strip() == spell_name.lower().strip():
			return format(index, spells[index])
	raise Exception("error", "Spell not found")

def format(index, data):
	wrapper = textwrap.TextWrapper(width=50) 
	description_array = wrapper.wrap(text=data['description'])
	description = ""
	for line in description_array:
		description = description + line + "\n\t\t"

	msg = index + "\n\tCasting Time: " + str(data['casting_time']) + "\n\tComponents: " + str(data['components']) + "\n\tDescription: " + description + "\n\tDuration: " + str(data['duration']) + "\n\tLevel: " + str(data['level']) + "\n\tRange: " + str(data['range']) + "\n\tSchool: " + str(data['school'])
	return msg