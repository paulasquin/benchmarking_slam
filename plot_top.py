#!/usr/bin/python3
# Plot RAM and CPU usage of wanted processes using the txt output of a top command
# Written by Paul Asquin paul.asquin@gmail.com for Awabot Intelligence, 2018

import os
import numpy as np 
import sys
import matplotlib.pyplot as plt

PATH='maps'

PATH_TO_TXT = os.getcwd() + "/top.txt"
SELECT_PROCESS = ["hector", "gmapping", "cartographer_no"]

class Data:
	name = ""
	les_ram = []
	les_cpu = []

	def __init__(self, name):
		self.name = name
		self.les_ram = []
		self.les_cpu = []

	def display(self):
		return "\nName : " + self.name + "\nRAM : " + str(self.les_ram) + "\nCPU : " + str(self.les_cpu)


def getCpuAndRam(path_to_txt):
	""" Read top.txt, extract informations of wanted processes and construct les_data """
	print("Creating and filling datas list", end="")
	sys.stdout.flush()
	les_data = []
	for process in SELECT_PROCESS:
		les_data.append(Data(process))

	with open(path_to_txt, 'r') as f:
		for line in f.readlines():
			for i in range(len(les_data)):
				if les_data[i].name in line:
					line_list = line.strip().replace("      ", " ").replace("     ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").split(" ")
					cpu = float(line_list[9].replace(",", "."))
					ram = float(line_list[10].replace(",", "."))
					les_data[i].les_cpu.append(cpu)
					les_data[i].les_ram.append(ram)
					continue
	print(" - Done")
	return les_data


def plotDatas(les_data):
	""" plot les_data : a list of datas constructed with ram and cpu information of listened processes """
	for i, data in enumerate(les_data):
		plt.subplot(len(les_data), 2, i*2 + 1)
		plt.plot(data.les_cpu, 'g')
		plt.title(data.name + " - CPU")
		plt.ylabel("% for 1 core")

		plt.subplot(len(les_data), 2, i*2 + 2)
		plt.plot(data.les_ram, 'r')
		plt.title(data.name + " - RAM")
		plt.ylabel("% of total RAM")
	plt.tight_layout()
	plt.show()


def main():
	print("Starting plot_top. Be sure to have a top.txt file generated with a command like")
	print("'top -b -d 1 > top.txt'")
	print("This example while save the output of top every 1 second into top.txt")
	print("Be sure to indicate which process you want to listen to, using the SELECT_PROCESS hyperparameter")
	plotDatas(getCpuAndRam(PATH_TO_TXT))


if __name__ == "__main__":
	main()
