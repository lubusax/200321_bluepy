from bluepy.btle import Scanner, DefaultDelegate, Peripheral,UUID

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
serviceUUID = {}
serviceUUID['Health Thermometer']= 0x1809
serviceUUID['Battery']= 0x180F
targetServiceUUID = serviceUUID['Battery']

for dev in devices:
    # print('\n################################ ***************************\n')
    # print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
    # print ("Is the Device connectable?", dev.connectable)
    scanData = dev.getScanData()
    for (adtype, desc, value) in scanData:
        # print ("  %s = %s" % (desc, value))
        if (desc == "Complete Local Name" and value == targetDeviceName):
            # print('\n\n ################################\n')
            # print('Found my baby!      #############')
            # print ('device : ', dev)
            # print ('data of device: ', dev.getScanData())
            # print ('address of device: ', dev.addr)
            # print('\n################################\n')
            targetDevice = dev
            targetDeviceDataRaw = dev.getScanData()
            break
        if targetDevice: break

scanner.stop()

if targetDevice:
    targetPeripheral = Peripheral(targetDevice.addr, targetDevice.addrType)
    # By invoking an Instance of Peripheral and passing addr AND addrType
    # a Connection is established
    print('\n\n ################################\n')
    print('CONNECTED ------ #############')
    targetServices = targetPeripheral.getServices()
    print ('\n Services: ', targetServices, '\n')
    
    targetService = targetPeripheral.getServiceByUUID(targetServiceUUID)
    
    targetCharacteristics = targetService.getCharacteristics()
    # this is a list

    targetCharacteristicProperties = targetCharacteristics[0].propertiesToString()
    # to make it work, you have to select one element of the list , hence [0]

    print ( '\n Wanted Service: ',
            targetServiceUUID,': ',
            targetService ,
            '\n')
    
    print ( '\n Wanted Characteristics for Service: ',
            targetServiceUUID,': ',
            targetCharacteristics ,
            '\n')
    
    print ( '\n Wanted Characteristic Properties: ',
            targetServiceUUID,': ',
            targetCharacteristicProperties ,
            '\n')

    print ( '\n Wanted Characteristic supports read: ',
            targetServiceUUID,': ',
            targetCharacteristics[0].supportsRead() ,
            '\n')
    
    print ( '\n Wanted Characteristic read value: ',
            targetServiceUUID,': ',
            int.from_bytes(targetCharacteristics[0].read(), byteorder='big'),
            '\n')

    input('press a key to end the script....')
    targetPeripheral.disconnect()
else:
    print('\n\n ????????????????????????????????????????????????????????\n')
    print('TARGET DEVICE NOT FOUND or NOT CONNECTABLE ------ #############')