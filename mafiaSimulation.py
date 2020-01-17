from random import *
import os

prnt = False

def day(m,t):
	if prnt:
		print()
		print("---Day---")
		print("Town remaining: ", t, "| Mafia remaning: ",m)
	if t <= m:
		if prnt:
			print("Mafia wins!")
		return 1
	if randint(0,m+t-1) < m: # town guesses correctly
		if prnt:
			print("Mafia hung...")
		return night(m-1,t)
	if prnt:
		print("Town hung...")
	return night(m,t-1)

def night(m,t):
	if prnt:
		input()
		print()
		print("---Night---")
		print("Town remaining: ", t, "| Mafia remaning: ",m)
	if m == 0:
		if prnt:
			print("Town wins!")
		return 0
	if prnt:
		print("Town killed by mafia...")
	return day(m,t-1)
	
def dayCop(m,t):
	if prnt:
		print()
		print("---Day---")
		print("Town remaining: ", t, "| Mafia remaning: ",m)
	if t <= m:
		if prnt:
			print("Mafia wins!")
		return 1
	if randint(0,m+t-1) < m: # cop finds mafia
		if prnt:
			print("Cop found mafia!")
		return nightCop(m-1,t)
	if randint(0,m+t-1) < m: # town guesses correctly
		if prnt:
			print("Mafia hung...")
		return nightCop(m-1,t)
	if prnt:
		print("Town hung...")
	return nightCop(m,t-1)
	
def nightCop(m,t):
	if prnt:
		input()
		print()
		print("---Night---")
		print("Town remaining: ", t, "| Mafia remaning: ",m)
	if m == 0:
		if prnt:
			print("Town wins!")
		return 0
	if randint(0,t-1) == 0: # mafia kills cop
		if prnt:
			print("Cop dead...")
		return day(m,t-1)
	if prnt:
		print("Town killed by mafia...")
	return dayCop(m,t-1)
	
def dayMedic(m,t,s):
	if prnt:
		print()
		print("---Day---")
		print("Town remaining: ", t, "| Mafia remaning: ",m)
	if t <= m:
		if prnt:
			print("Mafia wins!")
		return 1
	if randint(0,m+t-1) < m: # town guesses correctly
		if prnt:
			print("Mafia hung...")
		return nightMedic(m-1,t,s)
	if prnt:
		print("Town hung...")
	return nightMedic(m,t-1,s)

def nightMedic(m,t,s):
	if prnt:
		input()
		print()
		print("---Night---")
		print("Town remaining: ", t, "| Mafia remaning: ",m)
	if m == 0:
		if prnt:
			print("Town wins!")
		return 0
	if not s and randint(0,m+t-1) == 0: # medic gets a save
		if prnt:
			print("Medic saved!")
		return dayMedic(m,t,True)
	if randint(0,t-1) == 0: # mafia kills medic
		if prnt:
			print("Medic dead...")
		return day(m,t-1)
	if prnt:
		print("Town killed by mafia...")
	return dayMedic(m,t-1,False)
	
def dayCopMedic(m,t,s):
	if prnt:
		print()
		print("---Day---")
		print("Town remaining: ", t, "| Mafia remaning: ",m)
	if t <= m:
		if prnt:
			print("Mafia wins!")
		return 1
	if randint(0,m+t-1) < m: # cop finds mafia
		if prnt:
			print("Cop found mafia!")
		return nightCopMedic(m-1,t,s)
	if randint(0,m+t-1) < m: # town guesses correctly
		if prnt:
			print("Mafia hung...")
		return nightCopMedic(m-1,t,s)
	if prnt:
		print("Town hung...")
	return nightCopMedic(m,t-1,s)

def nightCopMedic(m,t,s):
	if prnt:
		input()
		print()
		print("---Night---")
		print("Town remaining: ", t, "| Mafia remaning: ",m)
	if m == 0:
		if prnt:
			print("Town wins!")
		return 0
	if not s and randint(0,m+t-1) == 0: # medic gets a save
		if prnt:
			print("Medic saved!")
		return dayCopMedic(m,t,True)
	if randint(0,t-1) == 0: # mafia kills cop
		if prnt:
			print("Cop dead...")
		return dayMedic(m,t-1,False)
	if randint(0,t-1) == 0: # mafia kills medic
		if prnt:
			print("Medic dead...")
		return dayCop(m,t-1)
	if prnt:
		print("Town killed by mafia...")
	return dayCopMedic(m,t-1,False)
	


def main():
	n = 10000
	t = 9
	m = 3
	os.system("cls")
	'''
	for m in range(1,5):
		for t in range(1,11):
			print("Running", n, "simulations with", t, "town and", m, "mafia.")
			mWins = 0
			for i in range(0,n):
				mWins += night(m,t)
				print("---------------------------------------------------------------------------------------------")
			print("Simulation finished.")
			print("Mafia wins: ", mWins)
			print("Town wins: ", n-mWins)
			print("Mafia winrate: ", mWins/n)
			
			print("")
			print("---------------------------------------------------------------------------------------------")
			print("")
	'''
	'''
	for t in range(5,10):
		print("Running", n, "simulations with", t, "town and", m, "mafia.")
		mWins = 0
		for i in range(0,n):
			mWins += night(m,t)
		print("Simulation finished.")
		print("Mafia wins: ", mWins)
		print("Town wins: ", n-mWins)
		print("Mafia winrate: ", mWins/n)
		
		print("---------------------------------------------------------------------------------------------")
	'''
	'''
	print("---------------------------------------------------------------------------------------------")
	
	print("Running", n, "simulations with", t, "town with a cop and", m, "mafia.")
	mWins = 0
	for i in range(0,n):
		mWins += nightCop(m,t)
	print("Simulation finished.")
	print("Mafia wins: ", mWins)
	print("Town wins: ", n-mWins)
	print("Mafia winrate: ", mWins/n)
	
	print("---------------------------------------------------------------------------------------------")
	
	print("Running", n, "simulations with", t, "town with a medic and", m, "mafia.")
	mWins = 0
	for i in range(0,n):
		mWins += nightMedic(m,t,False)
	print("Simulation finished.")
	print("Mafia wins: ", mWins)
	print("Town wins: ", n-mWins)
	print("Mafia winrate: ", mWins/n)
	
	print("---------------------------------------------------------------------------------------------")
	'''
	'''
	for t in range(5,11):
		print("Running", n, "simulations with", t, "town with a cop and a medic and", m, "mafia.")
		mWins = 0
		for i in range(0,n):
			if prnt:
				print()
				print("--------------------------------------------------")
				print("-------------------- NEW GAME --------------------")
				print("--------------------------------------------------")
				print()
			mWins += nightCopMedic(m,t,False)
			if prnt:
				input()
		print("Simulation finished.")
		print("Mafia wins: ", mWins)
		print("Town wins: ", n-mWins)
		print("Mafia winrate: ", mWins/n)
		print("---------------------------------------------------------------------------------------------")
	'''
	print(end = " ")
	print(end = " ")
	print(end = " ")
	print(end = " ")
	for i in range(0,100):
		print('|', end = " ")
	print()
	print()
	for t in range(1,51):
		mWins = 0
		for i in range(0,n):
			mWins += nightCopMedic(m,t,False)
		if t < 10:
			print("  ", t, end = " ")
		elif t < 100:
			print(" ", t, end = " ")
		else:
			print("", t, end = " ")
		for i in range(0, int(mWins/n*100)):
			print('|', end = " ")
		print()
	'''
	print(end = " ")
	print(end = " ")
	print(end = " ")
	print(end = " ")
	for i in range(0,100):
		print('|', end = " ")
	print()
	print()
	for t in range(1,501):
		if t < 10:
			print("  ", t, end = " ")
		elif t < 100:
			print(" ", t, end = " ")
		else:
			print("", t, end = " ")
		for i in range(0,n):
			if nightCopMedic(m,t,False) == 1:
				print('|', end = " ")
		print()
	'''	
		
	
if __name__ == "__main__":
	main()