import time
from rzdt import *
from rzbase import *

serialPort = 'COM4'        # Windows
serialBaudrate = 9600       # Default baudrate of RzController
logger = RzLogger.get_instance()

try:
	logger.info("---------- Open Serial Port ----------")
	conn = RzdtConn(serialPort, serialBaudrate)
	pump1 = RzdtDeviceUtil(conn, 1)
	pump2 = RzdtDeviceUtil(conn, 2)
	pump3 = RzdtDeviceUtil(conn, 3)
	pump4 = RzdtDeviceUtil(conn, 4)

	logger.info("---------- Initialize systems ----------")
	pump1.controller.initialize_system()
	pump1.wait_and_check_system_ready()
	pump1.controller.set_top_speed_of_plunger(2800) #set pump to top speed
	pump1.wait_and_check_system_ready()
	pump2.controller.initialize_system()
	pump2.wait_and_check_system_ready()
	pump2.controller.set_top_speed_of_plunger(2800) #set pump to top speed
	pump2.wait_and_check_system_ready()
	pump3.controller.initialize_system()
	pump3.wait_and_check_system_ready()
	pump4.controller.initialize_system()
	pump4.wait_and_check_system_ready()

	logger.info("---------- Flush Syringes ----------")
	#pump1
	pump1.controller.move_valve(1, RzDef.AUTO) #move valve to wash pos
	pump1.wait_and_check_system_ready()
	pump1.controller.move_plunger(11900) #fully extend the plunger
	pump1.wait_and_check_system_ready()
	pump1.controller.move_valve(6, RzDef.AUTO) #move valve to waste pos
	pump1.wait_and_check_system_ready()
	pump1.controller.move_plunger(0) #fully collapse to evacuate syringe
	pump1.wait_and_check_system_ready()

	#pump2
	pump2.controller.move_valve(1, RzDef.AUTO) #move valve to wash pos
	pump2.wait_and_check_system_ready()
	pump2.controller.move_plunger(11900) #fully extend the plunger
	pump2.wait_and_check_system_ready()
	pump2.controller.move_valve(6, RzDef.AUTO) #move valve to waste pos
	pump2.wait_and_check_system_ready()
	pump2.controller.move_plunger(0) #fully collapse to evacuate syringe
	pump2.wait_and_check_system_ready()

	#pump3
	pump3.controller.move_valve(1, RzDef.AUTO) #move valve to wash pos
	pump3.wait_and_check_system_ready()
	pump3.controller.move_plunger(11900) #fully extend the plunger
	pump3.wait_and_check_system_ready()
	pump3.controller.move_valve(6, RzDef.AUTO) #move valve to waste pos
	pump3.wait_and_check_system_ready()
	pump3.controller.move_plunger(0) #fully collapse to evacuate syringe
	pump3.wait_and_check_system_ready()

	#pump4
	pump4.controller.move_valve(1, RzDef.AUTO) #move valve to wash pos
	pump4.wait_and_check_system_ready()
	pump4.controller.move_plunger(11900) #fully extend the plunger
	pump4.wait_and_check_system_ready()
	pump4.controller.move_valve(6, RzDef.AUTO) #move valve to waste pos
	pump4.wait_and_check_system_ready()
	pump4.controller.move_plunger(0) #fully collapse to evacuate syringe
	pump4.wait_and_check_system_ready()

	logger.info("---------- Cleaning MEA ----------")
	#pump1 wash MEA
	pump1.controller.move_valve(1, RzDef.AUTO) #move valve to wash pos
	pump1.wait_and_check_system_ready()
	pump1.controller.move_plunger(11900) #fully extend the plunger
	pump1.wait_and_check_system_ready()
	pump1.controller.move_valve(5, RzDef.AUTO) #move valve to MEA pos
	pump1.wait_and_check_system_ready()
	pump1.controller.set_top_speed_of_plunger(440) #set pump to 183ul/s
	pump1.wait_and_check_system_ready()
	pump1.controller.move_plunger(0) #push plunger
	pump1.wait_and_check_system_ready()
	pump1.controller.move_valve(2, RzDef.AUTO) #move valve to chamber
	pump1.wait_and_check_system_ready()
	pump1.controller.set_top_speed_of_plunger(2800) #set pump to top speed
	pump1.wait_and_check_system_ready()
	pump1.controller.move_plunger(11900) #fully extend the plunger
	pump1.wait_and_check_system_ready()
	pump1.controller.move_valve(6, RzDef.AUTO) #move valve to waste
	pump1.wait_and_check_system_ready()
	pump1.controller.move_plunger(0) #push plunger
	pump1.wait_and_check_system_ready()

	logger.info("---------- Running MEA ----------")
	#remember to put an MEA cleaning cycle in here

	#prime chamber
	pump1.controller.move_valve(3, RzDef.AUTO) #move valve to sample 1
	pump1.wait_and_check_system_ready()
	pump1.controller.move_plunger(11900) #draw sample
	pump1.wait_and_check_system_ready()
	pump1.controller.move_valve(2, RzDef.AUTO) #move valve to chamber
	pump1.wait_and_check_system_ready()
	pump1.controller.move_plunger(0) #dispense sample
	pump1.wait_and_check_system_ready()

	#fill the chamber
	pump1.controller.move_valve(3, RzDef.AUTO) #move valve to sample 1
	pump1.wait_and_check_system_ready()
	pump1.controller.move_plunger(11900) #draw sample
	pump1.wait_and_check_system_ready()
	pump1.controller.move_valve(2, RzDef.AUTO) #move valve to chamber
	pump1.wait_and_check_system_ready()
	pump1.controller.move_plunger(0) #dispense sample
	pump1.wait_and_check_system_ready()

	#fill the pumps
	pump1.controller.move_valve(3, RzDef.AUTO) #move valve to sample 1
	pump2.controller.move_valve(2, RzDef.AUTO) #move pump 2 to chamber
	pump1.wait_and_check_system_ready()
	pump2.wait_and_check_system_ready()
	pump1.controller.move_plunger(11900) #draw sample
	pump2.controller.move_plunger(11900) #draw from chamber
	pump1.wait_and_check_system_ready()
	pump2.wait_and_check_system_ready()

	#prime MEA fluid paths by dispensing at half speed simultaneously
	pump1.controller.move_valve(5, RzDef.AUTO) #move pump 1 to MEA
	pump2.controller.move_valve(5, RzDef.AUTO) #move pump 2 to MEA
	pump1.wait_and_check_system_ready()
	pump2.wait_and_check_system_ready()
	pump1.controller.set_top_speed_of_plunger(220) #set pump to 183ul/s
	pump2.controller.set_top_speed_of_plunger(220) #set pump to 183ul/s
	pump1.wait_and_check_system_ready()
	pump2.wait_and_check_system_ready()
	pump1.controller.move_plunger(0) #dispense sample
	pump2.controller.move_plunger(0) #dispense sample
	time.sleep(54)
	pump1.wait_and_check_system_ready()
	pump2.wait_and_check_system_ready()

	#fill both pumps from chamber after MEA priming
	pump1.controller.move_valve(2, RzDef.AUTO) #move pump 1 to chamber
	pump2.controller.move_valve(2, RzDef.AUTO) #move pump 2 to chamber
	pump1.wait_and_check_system_ready()
	pump2.wait_and_check_system_ready()
	pump1.controller.set_top_speed_of_plunger(2800) #set pump to top speed
	pump2.controller.set_top_speed_of_plunger(2800) #set pump to top speed
	pump1.wait_and_check_system_ready()
	pump2.wait_and_check_system_ready()
	pump1.controller.move_plunger(11900) #draw sample
	pump2.controller.move_plunger(11900) #draw sample
	pump1.wait_and_check_system_ready()
	pump2.wait_and_check_system_ready()

	#2 pump continous flow
	pump1.controller.set_top_speed_of_plunger(440) #set pump to top speed
	pump2.controller.set_top_speed_of_plunger(440) #set pump to top speed
	pump1.wait_and_check_system_ready()
	pump2.wait_and_check_system_ready()
	pump1.controller.move_valve(5, RzDef.AUTO) #move pump 1 to MEA
	pump2.controller.move_valve(5, RzDef.AUTO) #move pump 2 to MEA
	pump1.wait_and_check_system_ready()
	pump2.wait_and_check_system_ready()
	pump2.controller.move_plunger(0) #dispense sample
	pump2.wait_and_check_system_ready()
	
	for i in range(4):
		pump1.controller.move_plunger(0) #dispense sample when other is finished
		pump2.controller.move_valve(2, RzDef.AUTO) #move pump 2 to chamber
		pump2.wait_and_check_system_ready()
		pump2.controller.set_top_speed_of_plunger(2800) #set pump to top speed
		pump2.wait_and_check_system_ready()
		pump2.controller.move_plunger(11900) #draw sample
		pump2.wait_and_check_system_ready()
		pump2.controller.set_top_speed_of_plunger(440) #set pump to top speed
		pump2.wait_and_check_system_ready()
		pump2.controller.move_valve(5, RzDef.AUTO) #move pump 1 to MEA
		pump2.wait_and_check_system_ready()
		pump1.wait_and_check_system_ready()
		pump2.controller.move_plunger(0) #dispense sample
		pump1.controller.set_top_speed_of_plunger(2800) #set pump to top speed
		pump1.wait_and_check_system_ready()
		pump1.controller.move_valve(2, RzDef.AUTO) #move pump 1 to chamber
		pump1.wait_and_check_system_ready()
		pump1.controller.move_plunger(11900) #draw sample
		pump1.wait_and_check_system_ready()
		pump1.controller.set_top_speed_of_plunger(440) #set pump to top speed
		pump1.wait_and_check_system_ready()
		pump1.controller.move_valve(5, RzDef.AUTO) #move pump 1 to MEA
		pump1.wait_and_check_system_ready()
		pump2.wait_and_check_system_ready()

	#empty syringes if they're still full
	pump1.controller.set_top_speed_of_plunger(2800) #set pump to top speed
	pump2.controller.set_top_speed_of_plunger(2800) #set pump to top speed
	pump1.wait_and_check_system_ready()
	pump2.wait_and_check_system_ready()
	pump1.controller.move_valve(2, RzDef.AUTO) #move pump 1 to chamber
	pump2.controller.move_valve(2, RzDef.AUTO) #move pump 2 to chamber
	pump1.wait_and_check_system_ready()
	pump2.wait_and_check_system_ready()
	pump1.controller.move_plunger(0) #dispense sample
	pump2.controller.move_plunger(0) #dispense sample
	pump1.wait_and_check_system_ready()
	pump2.wait_and_check_system_ready()

	#Returns sample to original location
	pump1.wait_and_check_system_ready()
	pump1.controller.set_top_speed_of_plunger(2800) #set pump to top speed
	pump1.wait_and_check_system_ready()
	for i in range(3):
		pump1.controller.move_valve(2, RzDef.AUTO) #move pump 1 to chamber
		pump1.wait_and_check_system_ready()
		pump1.controller.move_plunger(11900) #draw sample
		pump1.wait_and_check_system_ready()
		pump1.controller.move_valve(3, RzDef.AUTO) #move pump 1 to chamber
		pump1.wait_and_check_system_ready()
		pump1.controller.move_plunger(0) #dispense sample
		pump1.wait_and_check_system_ready()


	logger.info("---------- Close Serial Port ----------")
	conn.close()
	print("test complete")

except RzException as e:
        error_code = str(e.error_code)
        logger.error(f"RzException: {e} error_code: {error_code}")
        print(error_code)

except Exception as e:
    logger.error(f"Exception: {e}")
    print(e)
finally:
    conn.close()
