import json
import textwrap
import re
import random

with open("data/spells.json", "r") as spells_file:
	spells = json.load(spells_file)
	spells_file.close()


### Thanks Mako for writing this!!
def parseRoll(expression): 
	resp = 0
	components = [x.strip() for x in expression.lower().split("+")]
	rolls = components[0]
	total_modifier = sum([int(x) for x in components[1:]])
	pattern = r'([\d\.]+)?d([\d\.]+)'
	match = re.search(pattern, rolls)
	dice_num = int(float(match.group(1))) if match.group(1) else 1
	dice_type = int(float(match.group(2)))
	dice_results = [random.randint(1, dice_type) for x in range(0, dice_num)]
	
	resp += sum(dice_results)
	resp += total_modifier

	resp = str(resp) + " resulting from " + ", ".join([str(d) for d in sorted(dice_results)])

	return str(resp)


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