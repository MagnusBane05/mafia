import math
import os
from random import *

debug = False
useNameList = True

##### HELPER FUNCTIONS #####

#purpose:
#	asks the user a series of questions and gets input back
#args:
#	a list of questions
#returns:
#	the user input
def getInput(qs):
	if len(qs) == 0:
		print("error: invalid list")
		return None
	if len(qs) == 1:
		print(qs[0])
	else:
		for q in qs:
			print(q)
	a = input()
	return a
	
#purpose: 
#	convert a list to a string
#args:
#	l: the list
#returns:
#	the resulting string
def listToString(l):
	if len(l) == 0:
		print("error: invalid list")
		return None
	s = ""
	for i in range(0,len(l)-1):
		if isinstance(l[i], Player):
			s += l[i].name + ", "
		else:
			s += l[i] + ", "
	if isinstance(l[len(l)-1], Player):
		s += l[len(l)-1].name
	else:
		s += l[len(l)-1]
	return s
	
##### CLASSES #####

class Player:
	def __init__(self, name, role):
		self.name = name
		self.role = role
		self.attacked = False
		self.saved = False
		self.lastSaved = None
		self.checks = []
		
##### GAME #####

#purpose:
#	randomly assign roles to players
#args:
#	names: list of player names
#returns:
#	p: list of Player objects
def assignRoles(names):
	if len(names) < 4:
		print("Not enough players.")
		return None
	roles = []
	roles.append("Cop")
	roles.append("Medic")
	for i in range(0,int(math.sqrt(len(names)))):
		roles.append("Mafia")
	while len(roles) < len(names):
		roles.append("Town")
	p = []
	for i in range(0, len(names)):
		role = roles[randint(0,len(roles)-1)]
		p.append(Player(names[i], role))
		roles.remove(role)
	return p

#purpose:
#	get player names
#returns:
#	list of player names
def getNames():
	names = []
	if useNameList:
		#names = ["Evan", "Emma", "Angela", "Keith", "Patrick", "Isabela", "Anna", "Robin", "Matt", "Jeremy", "Amy"]
		names = ["Evan", "Emma", "Angela", "Keith", "Patrick", "Isabela", "Anna", "Robin", "Matt", "Amy", "Paige"]
		names = ["Evan", "Emma", "Angela", "Keith", "Patrick", "Isabela", "Sophia", "Robin", "Matt", "Carter"]
	else:
		while True:
			os.system("cls")
			print("Current players:", listToString(names))
			name = getInput(["Enter player names.","Enter '-1' when finished."])
			if name == "-1":
				break
			names.append(name)
	return names
	
#purpose:
# show roles to players
#args:
#	p: list of player
def showRoles(p):
	pfin = 0
	while pfin < len(p): # loop until all players have seen their role
		os.system("cls")
		inlist = False
		player = None
		while True:
			name = getInput(["Enter your name."])
			for plr in p:
				if plr.name.lower() == name.lower():
					player = plr
					break
			if player != None:
				break
			print("Unkown name.")
			
		os.system("cls")
		getInput(["Hello " + player.name, "Your role is: " + player.role, "Press enter to continue."])
		pfin += 1
	
#purpose:
#	run the night phase of the game
#args:
#	p: list of players
#returns:
#	1 if mafia wins
def night(p):
	m = 0
	t = 0
	for player in p:
		if player.role == "Mafia":
			m += 1
		else:
			t += 1
	if m == 0:  # no more mafia
		return 0
		
	# night actions
	os.system("cls")
	if not debug:
		getInput(["Set a timer give the mafia a set amount of time.", "Everybody, put your heads down and let the mafia pick their target.", 
		"Once the timer is over, everyone can raise their heads.", "Press enter once the mafia have finished."])
	pfin = 0
	while pfin < len(p): # loop until all players have finished their night action
		os.system("cls")
		inlist = False
		player = None
		while True:
			name = getInput(["Enter your name."])
			for plr in p:
				if plr.name.lower() == name.lower():
					player = plr
					break
			if player != None:
				break
			print("Unkown name.")
			
		os.system("cls")
		print("Hello", player.name)
		print("Your role is: ", player.role)
		print()
		print("Alive players:", listToString(p))
		print()
		
		if player.role == "Mafia":
			mafia(p, player)
			
		elif player.role == "Cop":
			cop(p, player)
			
		elif player.role == "Medic":
			medic(p, player)
			
		else:
			town(p, player)
			
		pfin += 1
	
	os.system("cls")
	
	# remove and display dead players
	dp = []
	for player in p:
		if player.attacked:
			if not player.saved:
				dp.append(player)
			player.attacked = False
		if player.saved:
			player.saved = False
	if len(dp) == 0:
		getInput(["Nobody has died!", "Press enter to continue..."])
	else:
		getInput(["The following players have died: " + listToString(dp), "Press enter to continue..."])
		for player in dp:
			p.remove(player)
		
	# continue to day
	return day(p)
	
#purpose:
#	run the day phase of the game
#args:
#	p: list of player
#returns:
#	0 if town wins
def day(p):
	m = 0
	t = 0
	for player in p:
		if player.role == "Mafia":
			m += 1
		else:
			t += 1
	if t <= m:  # mafia majority
		return 1
		
	# day actions
	os.system("cls")
	print("Set a timer for the length of the day.")
	print("Once someone has been nominated and seconded, input their name.")
	print("You have a maximum of 2 votes per day.")
	nominee = None
	while True:
		innom = getInput(["Who have you nominated?"])
		for player in p:
			if innom.lower() == player.name.lower():
				nominee = player
				break
		if nominee != None:
			break
		print("Unknown name.")
		
	getInput([nominee.name + " has been nominated.", "Now, everyone except " + nominee.name + " must take turns anonymously voting.", "Press enter to continue to voting."])
	
	# voting
	votes = 0
	pfin = 0
	while pfin < len(p) - 1: # loop until all players except the nominee have voted
		os.system("cls")
		inlist = False
		player = None
		while True:
			name = getInput(["Enter your name."])
			for plr in p:
				if plr.name.lower() == name.lower() and name.lower() != nominee.name.lower():
					player = plr
					break
			if player != None:
				break
			print("Unkown name.")
		while True:
			vote = getInput(["Vote 'y' to lynch " + nominee.name + " or 'n' to let them live."])
			if vote == 'y' or vote == 'n':
				break
			print("Unkown input.")
		if vote == 'y':
			votes += 1
		else:
			votes -= 1
		pfin += 1
		
	if votes > 0: # majority have voted yes
		getInput([nominee.name + " has been lynched.", "Press enter to continue to night..."])
		nominee.attacked = True
	else:
		getInput([nominee.name + " has lived.", "Press enter to continue to night..."])
		
	
	# remove and display dead players
	dp = []
	for player in p:
		if player.attacked:
			dp.append(player)
	for player in dp:
		p.remove(player)
			
	# continue to night
	return night(p)
	
#purpose:
#	night actions for mafia
#args:
#	p: player list
#	plr: current player
def mafia(p, plr):
	teammates = []
	target = None
	for player in p:
		if player.role == "Mafia" and player != plr:
			teammates.append(player)
		if player.attacked:
			target = player
	
	if len(teammates) > 0:
		print("Your teammates:", listToString(teammates), "\n")
	if target == None: # first mafia
		while True:
			intarget = getInput(["Who did you decide to kill?. Type 'none' to kill nobody."])
			if intarget.lower() == "none":
				break
			for player in p:
				if player.name.lower() == intarget.lower():
					target = player
					break
			if target != None:
				break
		if target != None:
			target.attacked = True
	else:
		if not debug:
			getInput(["One of your teammates has already entered " + target.name + " as the target.", "Please enter a random name to make it look like you're doing something productive :)"])
					

#purpose:
#	night actions for cop
#args:
#	p: player list
#	plr: current player
def cop(p, plr):
	if len(plr.checks) == 0:
		checked = False
		while True:
			incheck = getInput(["Who would you like to check?. Type 'none' to check nobody."])
			if incheck.lower() == "none":
				break
			for player in p:
				if player.name.lower() == incheck.lower():
					plr.checks.append(player)
					checked = True
					break
			if checked:
				break
	else:
		print("You checked " + plr.checks[len(plr.checks)-1].name + " last night.")
		checked = False
		while True:
			incheck = getInput(["Who would you like to check?. Type 'none' to check nobody."])
			if incheck.lower() == "none":
				break
			for plrname in plr.checks:
				if incheck.lower() == plrname.name.lower():
					print("You have already checked", incheck + ".")
					continue
			for player in p:
				if player.name.lower() == incheck.lower():
					plr.checks.append(player)
					checked = True
					break
			if checked:
				break
		if checked:
			if plr.checks[len(plr.checks)-1].role == "Mafia" and "Mafia" == plr.checks[len(plr.checks)-2].role or plr.checks[len(plr.checks)-1].role != "Mafia" and "Mafia" != plr.checks[len(plr.checks)-2].role:
				print(plr.checks[len(plr.checks)-1].name, "and", plr.checks[len(plr.checks)-2].name, "are on the same team!")
			else:
				print(plr.checks[len(plr.checks)-1].name, "and", plr.checks[len(plr.checks)-2].name, "are on different teams!")
			getInput(["Press enter to continue..."])

#purpose:
#	night actions for medic
#args:
#	p: player list
#	plr: current player
def medic(p, plr):
	if plr.lastSaved == None:
		while True:
			insave = getInput(["Who would you like to save?. Type 'none' to save nobody."])
			if insave.lower() == "none":
				break
			for player in p:
				if player.name.lower() == insave.lower():
					plr.lastSaved = player
					break
			if plr.lastSaved != None:
				break
		if plr.lastSaved != None:
			plr.lastSaved.saved = True
	else:
		print("You saved " + plr.lastSaved.name + " last night.")
		while True:
			insave = getInput(["Who would you like to save?. Type 'none' to save nobody."])
			if insave.lower() == "none":
				break
			if insave.lower() == plr.lastSaved.name.lower():
				print("You saved", plr.lastSaved.name, "last night.")
				continue
			for player in p:
				if player.name.lower() == insave.lower():
					plr.lastSaved = player
					break
			if plr.lastSaved != None:
				break
		if plr.lastSaved != None:
			plr.lastSaved.saved = True

#purpose:
#	night actions for town
#args:
#	p: player list
#	plr: current player
def town(p, plr):
	if not debug:
		getInput(["Please enter a random name to make it look like you're doing something productive :)"])

def main():
	p = assignRoles(getNames())
	if not debug:
		showRoles(p)
	if night(p):
		print("Mafia wins!")
	else:
		print("Town wins!")
			

if __name__ == "__main__":
	main()