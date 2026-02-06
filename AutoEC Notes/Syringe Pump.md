A integrated syringe pump and 6-way selector valve. Usage instructions are provided in the manual below:
[[sy-01b-ascii-code-instruction-manuall-v1-1.pdf]]
## General
- The stepper motor controlling the syringe stroke has 12,000 steps total 
- stroke length of 30mm
- Can take syringes from 25uL to 5mL
- All numbers sent via serial (for example for number of steps) must be sent in hexadecimal
- Recommends using RS232/485 comm protocol as it will send back more checksum and status data than raw terminal commands
- Requires 24V power with minimum 1.5A specification and a maximum operating current of 31A (and limit of 35A)
- Must always be run with liquid else the sealing surfaces can be damaged
- Have a self test mode if address switch is set to position F
## Addressing
![[Pasted image 20240330162039.png]]

## Comm Protocol
![[Pasted image 20240330161352.png]]
For sending data:
- STX is the start string
- Pump address is according to the table in [[Syringe Pump#Addressing]]
- Sequence number -  a number from 0-7 and a bit flag for repetition. Only read if the bit flag is high - used to check whether it is currently repeating the same command as previous or whether (acknowledge only) it is receiving a new command to repeat (acknowledge and execute).
- Data block - the data or command to be sent as an ascii string (see [[Syringe Pump#Commands]])
- ETX is the end of the string
- Checksum is used to check for communication errors or corruptions

For receiving data:
- Master address - the address of the host computer - always set to 30h (0 in ascii)
- Status code - a code that will either indicate pump status (ready/busy) or [[Syringe Pump#Error Codes]]

## Manual Control
Using SerialCommV1.0 provided by Runze it is possible to operate a single pump directly from the terminal by sending and receiving serial commands. This software only works with windows.
Other settings:
- Only 9600 Brate supported (other params same as [[Syringe Pump#Comm Protocol]])
- Pump address switch must be set to 0.
## Commands
### General
Commands are stored in a 255 char buffer. A single R at the end of the command string indicates that the command is to be run immediately, otherwise it will enter the buffer and be kept there until a new command is received where the buffer will be overwritten. The pump will not accept further commands unless the current command has been completed (hence don't send until confirmation of complete command from the pump - can maybe also place in buffer?). If the command receives an incorrect command it will send an error code back to the host computer.

#### Backlash Config
Kn where n is between 0-800 for full steps and 0-1600 in microstepping mode (fine positioning which does halg steps)

#### Pump Config
Un where n can take the following values:
![[Pasted image 20240330174535.png]]
The pump must be restarted for these to take effect.

The U200 commands are presumably in the form of U201 for a 1A stall current and U231 for a 31A stall current (to be tested)
- Stall current must be set to be below the maximum rated current of the power supply being used

#### Initialisation
The plunger and valve drive can be initialised seperately or together and going counter clockwise Y(n1, n2, n3) or clockwise Z(n1, n2, n3) - presumably the sub blocks use commas as separators

For combined plunger and valve initialisation, the table of values is shown below:
![[Pasted image 20240330175514.png]]
## Error Codes


