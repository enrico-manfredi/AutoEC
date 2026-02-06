import time
import math
from rzdt import *
from rzbase import *
from pyvium import Core
import os

class PumpSystem:
	def __init__(self, com_port):
		'''Specify the system COM port as str. Opens the serial port and initialises all pumps
		by cycling through addresses sequentially. Saves a pump list and dict attribute for later use. Designed for a
		4 pump system operating in 2 pairs per MEA side. Pumps 1 and 2 should be connected to the cathode while
		pumps 3 and 4 should be connected to the anode. All pumps should have valve position 1 connected to the wash 
		bottle, position 2 should be connected to the catholyte/anolyte chambers, position 5 should be connected to
		the MEA and posiiton 6 should be connected to the waste.'''

		self.pump_list = [1,2,3,4]
		self.pump_pairs = [[1,2],[3,4]]

		serialPort = com_port        # Windows only
		serialBaudrate = 9600       # Default baudrate of RzController
		self.logger = RzLogger.get_instance()
		self.default_speed = 440 # in steps/s - comes out to 183 ul/s with 5ml syringe
		self.full_stroke = 11900 # in steps
		self.max_speed = 3000 # in steps/s
		self.pump_dict = {}

		try:
			self.logger.info("---------- Open Serial Port ----------")
			self.conn = RzdtConn(serialPort, serialBaudrate)
			self.logger.info("---------- Initialising all pumps ----------")
			for pump in self.pump_list:
				self.pump_dict[pump] = RzdtDeviceUtil(self.conn, pump)
				self.pump_dict[pump].controller.initialize_system()
				self.pump_dict[pump].wait_and_check_system_ready() #this is needed after every cmd to prevent overflow
				self.pump_dict[pump].controller.set_top_speed_of_plunger(self.max_speed) #set pump to top speed
				self.pump_dict[pump].wait_and_check_system_ready()
				self.pump_dict[pump].controller.query()

		#error handling block included in every function, reports problems to logger and stops machine
		except RzException as e:
			error_code = str(e.error_code)
			self.logger.error(f"RzException: {e} error_code: {error_code}")
			print(error_code)
			self.logger.info("---------- Disconnecting System ----------")
			self.conn.close()

		except Exception as e:
			self.logger.error(f"Exception: {e}")
			print(e)
			self.logger.info("---------- Disconnecting System ----------")
			self.conn.close()

	def close(self):
		self.logger.info("---------- Disconnecting System ----------")
		self.conn.close()

	def move(self, pump_list, pos, speed, valve):
		'''moves the syringe plunger for pumps specified in pump list (list of addresses as ints) to the specified position in
		steps (int) at the specified speed in steps per second (int) at the specified valve address (int)'''
		try:
			for pump in pump_list:
				self.pump_dict[pump].wait_and_check_system_ready()
			for pump in pump_list:
				self.pump_dict[pump].controller.set_top_speed_of_plunger(speed) #set pump to speed
			for pump in pump_list:
				self.pump_dict[pump].wait_and_check_system_ready()
			for pump in pump_list:
				self.pump_dict[pump].controller.move_valve(valve, RzDef.AUTO) #move valve to pos
			for pump in pump_list:
				self.pump_dict[pump].wait_and_check_system_ready()
			for pump in pump_list:
				self.pump_dict[pump].controller.move_plunger(pos) #move plunger
			time.sleep(self.full_stroke/speed-1) #needed to avoid timeout, assuming full strokes
			for pump in pump_list:
				self.pump_dict[pump].wait_and_check_system_ready()

		except RzException as e:
			error_code = str(e.error_code)
			self.logger.error(f"RzException: {e} error_code: {error_code}")
			print([e, error_code])
			self.close()

		except Exception as e:
			self.logger.error(f"Exception: {e}")
			print(e)
			self.close()


	def flush_syringes(self, pump_list):
		'''flushes specified syringes (specify as list containing desired numerical pump addresses) with a full stroke of wash solution
		and dispenses to waste'''
		
		print("Flushing syringes")
		self.logger.info("---------- Flushing pumps "+str(pump_list)+"----------")
		self.move(pump_list, self.full_stroke, self.max_speed, 1) #draw wash solution
		self.move(pump_list, 0, self.max_speed, 6) #fully dispense to waste
		print("Flush finished")


	def clean_system(self, side = "both"):
		'''flushes the MEA with water and then flushes the chamber to remove contaminants. By default cleans both sides 
		but can be told to do one side by specifying side = "cathode" or side = "anode"'''
		
		print("Cleaning system")

		if side == "both":
			self.logger.info("---------- Cleaning Whole System ----------")
			
			#rinse the MEA
			self.move(self.pump_list, self.full_stroke, self.max_speed, 1) #draw wash solution
			self.move(self.pump_list, 0, int(self.default_speed/2), 5) #dispense both pumps at half default speed into MEA
			self.move(self.pump_list, self.full_stroke, int(self.default_speed/2), 5) #draw dirty solution out of MEA
			self.move(self.pump_list, 0, self.max_speed, 2) #dump into chamber
			for i in range(2): #twice to ensure we remove residue from the primed MEA
				self.move(self.pump_list, self.full_stroke, self.max_speed, 2) #draw dirty MEA solution from chamber
				self.move(self.pump_list, 0, self.max_speed, 6) #fully dispense to waste

			#rinse the chamber
			for i in range(3):
				self.move(self.pump_list, self.full_stroke, self.max_speed, 1) #draw wash solution
				self.move(self.pump_list, 0, self.max_speed, 2) #dispense both pumps into chamber
			for i in range(3):
				self.move(self.pump_list, self.full_stroke, self.max_speed, 2) #draw dirty solution from chamber
				self.move(self.pump_list, 0, self.max_speed, 6) #fully dispense to waste

			#rinse the syringes
			self.flush_syringes(self.pump_pairs[0])

		else:
			self.logger.info("Exception in clean_system: User did not specify a side when cleaning")
			raise Exception("Exception in clean_system: \
				please specify either anode or cathode (all lower case) or leave blank to clean both sides")

		print("Cleaning finished")


	def run_MEA(self, runtime, samples, flowrate = None, settling_time = 10, pre_clean = False):
		'''Runs the MEA in experimental mode with a user defined flowrate in ul/s (float, defaults to 183 ul/s
		if not specified) for a given time in s (float) and for a given sample lane (tuple of 2 values each 1-4, int).'''

		test_file = "C:\\IviumStat\\test.imf"
		Core.IV_open()
		
		#if precleaning selected cleans whole system before experiment
		if pre_clean:
			self.clean_system()

		self.logger.info("---------- Preparing MEA ----------")

		#convert ul/s to steps/s for the 5ml syringe, change for different syringe sizes
		if flowrate:
			speed = int(flowrate/.4167)
		else:
			speed = self.default_speed

		#calculate dispensation wait time, minus a second for check call
		#assuming full strokes
		disp_time = self.full_stroke/speed - 1

		#work out which pumps are needed to pull the specified sample
		#cathode side
		pumps_dict = {}
		if samples[0] == 1 or samples[0] == 2:
			pumps_dict[1] = samples[0]+2
		elif samples[0] == 3 or samples[0] == 4:
			pumps_dict[2] = samples[0]
		else:
			self.logger.info("Exception in run_MEA: cathode pump sample lane out of range")
			raise Exception("Exception in run_MEA: please specify a sample lane between 1 and 4")
		
		#anode side
		if samples[1] == 1 or samples[1] == 2:
			pumps_dict[3] = samples[1]+2
		elif samples[1] == 3 or samples[1] == 4:
			pumps_dict[4] = samples[1]
		else:
			self.logger.info("Exception in run_MEA: cathode pump sample lane out of range")
			raise Exception("Exception in run_MEA: please specify a sample lane between 1 and 4")

		# #fill chambers
		for pump in pumps_dict:
			for i in range(2): #once to prime, twice to fill
				self.move([pump], self.full_stroke, self.max_speed, pumps_dict[pump]) #draw from sample bottle
				self.move([pump], 0, self.max_speed, 2) #dispense into chamber
			self.move([pump], self.full_stroke, self.max_speed, pumps_dict[pump]) #draw extra sample

		#fill the other pumps from chamber
		other_pumps = []
		for pump in self.pump_list:
			if pump not in pumps_dict:
				other_pumps.append(pump)
				self.move([pump], self.full_stroke, self.max_speed, 2)

		#prime and flush MEA with all pumps
		self.move(self.pump_list, 0, int(self.default_speed/2), 5)

		#fill active pumps from chamber
		self.move(self.pump_list, self.full_stroke, self.max_speed, 2)

		#experiment start - simultaneous movement
		self.logger.info("---------- Experiment Start ----------")
		pump_order = [list(pumps_dict), other_pumps] #0 is active pumps, 1 is standby pumps
		print(pump_order)
		
		#2 pump continous flow
		for pump in self.pump_list:
			self.pump_dict[pump].controller.set_top_speed_of_plunger(speed) #set pump to speed
		for pump in self.pump_list:
			self.pump_dict[pump].wait_and_check_system_ready()
		for pump in self.pump_list:
			self.pump_dict[pump].controller.move_valve(5, RzDef.AUTO) #move pump 1 to MEA
		for pump in self.pump_list:
			self.pump_dict[pump].wait_and_check_system_ready()

		for pump in pump_order[0]:
			self.pump_dict[pump].controller.move_plunger(0) #dispense sample
		start_time = time.time()
		Core.IV_startmethod(test_file)
		time.sleep(disp_time)

		while (time.time() - start_time) < (runtime + settling_time):
			loop_time = time.time()

			for pump in pump_order[1]:
				self.pump_dict[pump].controller.move_plunger(0) #dispense sample
			for pump in pump_order[0]:
				self.pump_dict[pump].wait_and_check_system_ready()
			for pump in pump_order[0]:
				self.pump_dict[pump].controller.move_valve(2, RzDef.AUTO) #move pump 2 to chamber
			for pump in pump_order[0]:
				self.pump_dict[pump].wait_and_check_system_ready()
			for pump in pump_order[0]:
				self.pump_dict[pump].controller.set_top_speed_of_plunger(self.max_speed) #set pump to speed
			for pump in pump_order[0]:
				self.pump_dict[pump].wait_and_check_system_ready()
			for pump in pump_order[0]:
				self.pump_dict[pump].controller.move_plunger(self.full_stroke)
			for pump in pump_order[0]:
				self.pump_dict[pump].wait_and_check_system_ready()
			for pump in pump_order[0]:
				self.pump_dict[pump].controller.set_top_speed_of_plunger(speed) #set pump to speed
			for pump in pump_order[0]:
				self.pump_dict[pump].wait_and_check_system_ready()
			for pump in pump_order[0]:
				self.pump_dict[pump].controller.move_valve(5, RzDef.AUTO) #move pump 2 to chamber
			for pump in pump_order[0]:
				self.pump_dict[pump].wait_and_check_system_ready()
			time.sleep(disp_time - (time.time()-loop_time))
			pump_order = list(reversed(pump_order))
			for pump in pump_order[0]:
				self.pump_dict[pump].wait_and_check_system_ready()

		self.end_time = time.time()-start_time
		Core.IV_savedata(os.path.splitext(test_file)[0]+str(samples)+".csv")

		#dump any remaining solution into the chamber
		self.move(self.pump_list, 0, self.max_speed, 2)

		#evacuate MEA into chamber
		self.move(self.pump_list, self.full_stroke, int(self.default_speed/2), 5)
		self.move(self.pump_list, 0, self.max_speed, 2)

		#return chamber liquid to appropriate sample bay
		for i in range(3):
			for pump in pumps_dict:
				self.move([pump], self.full_stroke, self.max_speed, 2)
				self.move([pump], 0, self.max_speed, pumps_dict[pump])

		self.clean_system()

if __name__ == "__main__":
	system = PumpSystem("COM4")
	
	#syringe flush test
	# system.flush_syringes(pumps.pump_list)

	#dump stuff that gets stuck in the chamber
	for i in range(3):
		system.move(system.pump_list, system.full_stroke, system.max_speed, 2)
		system.move(system.pump_list, 0, system.max_speed, 6)

	#test cleaning both sides of MEA simultaneously
	# system.clean_system()

	#test cleaning the anode only
	# system.clean_system(side = "anode")

	#test cleaning on the cathode only
	# system.clean_system(side = "cathode")

	system.run_MEA(100, [1,1])
	system.run_MEA(100, [2,2])
	system.run_MEA(100, [3,3])
	system.run_MEA(100, [4,4])

	system.close()