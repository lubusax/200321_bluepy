from bluepy.btle import Scanner, DefaultDelegate, Peripheral

scanTimeout = 1.0
# timeout in seconds. During this period,
# callbacks to the delegate object will be called.
# When the timeout ends, scanning will stop and 
# the method will return a list (or a view on Python 3.x)
# of ScanEntry objects for all devices
# discovered during that time.

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(scanTimeout)

targetDevice = False
targetDeviceName = "Things"

for dev in devices:
    print('\n################################ ***************************\n')
    print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
    print ("Is the Device connectable?", dev.connectable)
    for (adtype, desc, value) in dev.getScanData():
        print ("  %s = %s" % (desc, value))
        if (desc == "Complete Local Name" and value == targetDeviceName):
            print('\n\n ################################\n')
            print('Found my baby!      #############')
            print ('device : ', dev)
            print ('data of device: ', dev.getScanData())
            print ('address of device: ', dev.addr)
            print('\n################################\n')
            targetDevice = dev
            targetDeviceDataRaw = dev.getScanData()
            break
        if targetDevice: break

if targetDevice:
    targetPeripheralConnection = Peripheral(targetDevice.addr, targetDevice.addrType)
    print('\n\n ################################\n')
    print('CONNECTED ------ #############')
    input('press a key to end the script....')
    targetPeripheralConnection.disconnect()