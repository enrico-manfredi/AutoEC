import Metrohm.AUTOLAB as EC

hdw=R'C:\Program Files\Metrohm Autolab\Autolab SDK 2.1\Hardware Setup Files\PGSTAT302N\HardwareSetup.FRA32M.xml',
sdk=R"C:\Program Files\Metrohm Autolab\Autolab SDK 2.1\EcoChemie.Autolab.Sdk"
adx=R"C:\Program Files\Metrohm Autolab\Autolab SDK 2.1\Hardware Setup Files\Adk.x"

autolab = EC.AUTOLAB(sdk=sdk,adx=adx)

autolab.CMD = True

try:
    if autolab.connectToAutolab(hdw): # first we need to connect to our instrument
        print("Connecting to AUTOLAB successfully....")

except:
    print("Connecting to AUTOLAB FAIL....")

del autolab