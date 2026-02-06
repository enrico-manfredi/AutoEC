![[Pasted image 20240330184920.png]]
## Modules
- Mains power is an extension chord with enough plugs for other the [[Power Supplies]] of connected devices (5) and is connected to a [[Kill Switch]] that allows for the system to be switched off automatically (int22) for safety and sustainability reasons.
- The Control PC is a windows machine that centrally controls the movement and operation of all devices in the system, and is also responsible for monitoring errors or failure conditions. Should be accessible remotely.
- [[Syringe Pump]] is the fluid driving element that retrieves both sample and wash solution and pumps them through the electrochemical cell
- Test solutions are solutions of [[Catholyte]] and [[Anolyte]] that need to be tested, and will be in a [[Sample Rack]] which is easily accessible and interchangeable to the user
- [[Wash Solution]] will be used to purge all elements of the fluid system from any traces of test solutions
- [[Potentiostat]] is the device that controls cell potential and current between the electrodes as well as responsible for taking measurements from the cell and reporting those measurements to the control PC.
- [[Booster]] is a device controlled by the potentiostat via proprietary interface (int13) that increases the amount of current that can be delivered to the cell.
- The [[Cell]] is [[Membrane]] [[Electrode]] assembly (MEA) in which the test solutions travel through a [[Fluid Path]] during electrochemical measurement by the potentiostat.
- Test solution [[Reservoirs]] are chambers where the current test solution will drain into after being pumped through the cell and where the syringe filters will fill from during operation and dispense to when setting up for a new test solution run.
- [[Thermal Control]] is the thermostat system that will heat up the cell and/or syringe pumps and reservoirs to maintain a constant temperature for the liquids being run through the system.

## Interfaces
1. Fluid transfer link between wash solution reservoir and the syringe pump valve selector
2. Fluid transfer link from the syringe pump to a waste container for spent wash solution and/or excess test solutions
3. Fluid transfer link from the test solution reservoir to the syringe pump such that the syringe pump can be loaded with test solution
4. Fluid transfer link from the syringe pump to the test solution reservoir such that the syringe pump can be dispensed into the test solution reservoir (in implementation this would be on the same fluid line as 3 as the syringe pump is bidirectional)
5. A fluid transfer link between the syringe pump and the cell fluid inlet such that the syringe pump can dispense test solution into the cell
6. A fluid transfer link between the cell and the test solution reservoir such that fluid moving through the cell can be drained into the reservoir
7. An electrical communication link from the syringe pump to the control PC shows the control PC the pump status and any errors that the pump has encountered, such as overheating, stalling or blockage
8. An electrical communication link from the control PC to the syringe pump that allows the control PC to send actuation commands to the syringe pump (in implementation this will be a single bidirectional RS-485 connection using the protocol set out in [[Syringe Pump]])
9. A fluid transfer link from a particular test solution in the test solution rack to the syringe pump that allows for test solution to be drawn into the syringe pump
10. A fluid transfer link from the syringe pump to a particular test solution in the test solution rack that allows for the dispensation of test solution from the syringe pump into the appropriate sample container 