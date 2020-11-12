import json
import textwrap
import re
import random

with open("data/spells.json", "r") as spells_file:
	spells = json.load(spells_file)
	spells_file.close()

with open("data/xgtespells.json", "r") as xgf:
	xgte = json.load(xgf)
	xgf.close()

def formatXgte(data):
	wrapper = textwrap.TextWrapper(width=50) 
	description_array = wrapper.wrap(text=data['Description'])
	description = ""
	for line in description_array:
		description = description + line + "\n\t\t"

	resp = data['Name'] + "\n\tCasting Time: " + str(data['CastingTime']) + "\n\tComponents: " + str(data['Components']) + "\n\tDescription: " + description + "\n\tDuration: " + str(data['Duration']) + "\n\tLevel: " + str(data['Level']) + "\n\tRange: " + str(data['Range']) + "\n\tSchool: " + str(data['School'] + "\n\tRitual:" + str(data['Ritual']))
	return resp


def xgteLookup(spell_name):
	indicies = json.loads(xgte['ImprovedInitiative.Spells'])
	for index in indicies:
		label = "ImprovedInitiative.Spells." + index
		data = json.loads(xgte[label])
		if data['Name'].lower().strip() == spell_name.lower().strip():
			return formatXgte(data)

	raise Exception("error", "Spell not found in XGTE")

### Thanks Mako for writing this!!
def parseRoll(expression): 
	resp = 0
	components = [x.strip() for x in expression.lower().split("+")]
	rolls = components[0]
	total_modifier = sum([int(x) for x in components[1:]])
	pattern = r'([\d\.]+)?d([\d\.]+)([aA]|[dD])?'
	match = re.search(pattern, rolls)
	dice_num = int(float(match.group(1))) if match.group(1) else 1
	dice_type = int(float(match.group(2)))
	advantage = match.group(3)

	if advantage:
		dice_results = [sorted([random.randint(1, dice_type), random.randint(1, dice_type)]) for x in range(0, dice_num)]
		dice_choice = [max(x) for x in dice_results] if advantage.lower() == 'a' else [min(x) for x in dice_results]
		resp += sum(dice_choice)
		resp += total_modifier
		adv_mod = ' at advantage' if advantage.lower() == 'a' else ' at disadvantage'
		dice_results_str = ", ".join('**'+str(d)+'**' if (d[0] == 1 or d[0] == 20 or d[1] == 1 or d[1] == 20) else str(d) for d in dice_results)
		resp = str(resp) + " resulting from " + dice_results_str + adv_mod
		return str(resp)
	else:
		dice_results = [random.randint(1, dice_type) for x in range(0, dice_num)]
		resp += sum(dice_results)
		resp += total_modifier
		resp = str(resp) + " resulting from " + ", ".join([('**'+str(d)+'**' if (d == 1 or d == 20) else str(d)) for d in sorted(dice_results)])
		return str(resp)

def discordWrapper(resp, chunks):
	if len(resp) > 2000:
		excerpt = resp[0:2000]
		chunks.append(excerpt)
		return discordWrapper(resp[2000:], chunks)
	else:
		chunks.append(resp)
		return chunks

def lookup(spell_name): 
	for index in spells:
		if index.lower().strip() == spell_name.lower().strip():
			return format(index, spells[index])
	try:		
		resp = xgteLookup(spell_name)
		return resp
	except:
		raise Exception("error", "Spell not found")

def format(index, data):
	wrapper = textwrap.TextWrapper(width=50) 
	description_array = wrapper.wrap(text=data['description'])
	description = ""
	for line in description_array:
		description = description + line + "\n\t\t"

	msg = index + "\n\tCasting Time: " + str(data['casting_time']) + "\n\tComponents: " + str(data['components']) + "\n\tDescription: " + description + "\n\tDuration: " + str(data['duration']) + "\n\tLevel: " + str(data['level']) + "\n\tRange: " + str(data['range']) + "\n\tSchool: " + str(data['school'])
	return msg
