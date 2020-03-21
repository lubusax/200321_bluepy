from bluepy.btle import Scanner, DefaultDelegate, Peripheral,UUID
import time

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

class MyDelegate(DefaultDelegate):
    def __init__(self, params):
        DefaultDelegate.__init__(self)
        # ... initialise here
        self.handle = params
        #self.time = 

    def handleNotification(self, cHandle, data):
        #data come as one byte
        if cHandle ==self.handle:
            dataInteger = int.from_bytes(targetCharacteristic.read(), byteorder='big')
            print(time.strftime("%H:%M:%S", time.localtime()), " Battery Status: ", dataInteger,"%")
        else:
            print("Notification for another Characteristic")
        # ... perhaps check cHandle
        # ... process 'data'

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(scanTimeout)

targetDevice = False
targetDeviceName = "Things"

serviceUUID = {}
serviceUUID['Health Thermometer']= 0x1809
serviceUUID['Battery']= 0x180F


# serviceUUIDBattery = serviceUUID['Battery']

targetServiceUUIDs = [ serviceUUID['Battery'],serviceUUID['Health Thermometer'] ]

print('target Service UUIDs : ', targetServiceUUIDs)

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

if targetDevice:
    targetPeripheral = Peripheral(targetDevice.addr, targetDevice.addrType)
    # By invoking an Instance of Peripheral and passing addr AND addrType
    # a Connection is established
    print('\n\n ################################\n')
    print('CONNECTED ------ #############')
    targetServices = targetPeripheral.getServices()
    print ('\n Services: ', targetServices, '\n')
    
    targetServiceList = [targetPeripheral.getServiceByUUID(s) for s in targetServiceUUIDs]

    
    targetCharacteristicList = [s.getCharacteristics()[0] for s in targetServiceList]
    # this is the first element of a list

    targetHandleList = [c.getHandle() for c in targetCharacteristicList]

    targetDelegateList = [targetPeripheral.setDelegate( MyDelegate(h) for h in targetHandleList]
    # This is needed to Handle Notifications.
    # By passing the Handle with each instantiation
    # you always know which characteristic(handle) sent the Notification
    
    for h in targetHandleList:
        ConfigHandle = h.valHandle + 1
        targetPeripheral.writeCharacteristic(ConfigHandle , (1).to_bytes(2, byteorder='little'))
    # enable notifications

    print ( '\n Wanted Service: ',
            serviceUUIDBattery,': ',
            targetService ,
            '\n')
    
    print ( '\n Wanted Characteristic for Service: ',
            serviceUUIDBattery,': ',
            targetCharacteristic ,
            '\n')
    
    print ( '\n Wanted Characteristic Properties: ',
            serviceUUIDBattery,': ',
            targetCharacteristic.propertiesToString() ,
            '\n')

    print ( '\n Wanted Characteristic supports read: ',
            serviceUUIDBattery,': ',
            targetCharacteristic.supportsRead() ,
            '\n')
    
    print ( '\n Wanted Characteristic read value: ',
            serviceUUIDBattery,': ',
            int.from_bytes(targetCharacteristic.read(), byteorder='big'),
            '\n')
    while True:
        if targetPeripheral.waitForNotifications(1.0):
            # handleNotification() was called
            continue
        time.sleep(3)
        print ("Waiting...")
        # Perhaps do something else here

    input('press a key to end the script....')
    targetPeripheral.disconnect()
else:
    print('\n\n ????????????????????????????????????????????????????????\n')
    print('TARGET DEVICE NOT FOUND or NOT CONNECTABLE ------ #############')
