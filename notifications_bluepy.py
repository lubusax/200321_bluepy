from bluepy.btle import Scanner, DefaultDelegate, Peripheral,UUID, AssignedNumbers
import time
import struct

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
    def __init__(self, handle):
        DefaultDelegate.__init__(self)
        # ... initialise here
        self.handle = handle

        #self.time = 

    def handleNotification(self, cHandle, data):
        #data come as one byte
        dataInteger = int.from_bytes(data, byteorder='big')
        
        print ('cHandle : ', cHandle )
        print ('self.handle : ', self.handle )
        print ("data", data," - length ", len(data))
        
        number = int.from_bytes(data[1:4], byteorder='little')

        print ("data", data[1:4]," - converted ", number)

        print ("data ", data[4],' - exponent - ', -(256-int(data[4])))

        
        # print (' handle 12 - unpacked :) ', struct.unpack('f', valueHandle12))
        # if cHandle ==self.handle:
        #     print(time.strftime("%H:%M:%S", time.localtime()), " Battery Status: ", dataInteger,"%")
        # else:
        #     print("Notification for another Characteristic")
        # ... perhaps check cHandle
        # ... process 'data'

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(scanTimeout)

targetDevice = False
targetDeviceName = "Things"

print(AssignedNumbers.healthThermometer)
print(AssignedNumbers.batteryService)

targetServiceUUIDs = [ AssignedNumbers.healthThermometer ]

print('target Service UUIDs : ', targetServiceUUIDs)

for dev in devices:
    scanData = dev.getScanData()
    for (adtype, desc, value) in scanData:
        if (desc == "Complete Local Name" and value == targetDeviceName):
            targetDevice = dev
            #targetDeviceDataRaw = dev.getScanData()
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

    print ( 'targetHandleList: ', targetHandleList[0])


    targetHandles = {}

    # Enabling Indications and Notifications of Health Thermometer Service
    handle = 14 # handle for the CCCD of Health Thermometer Service
    value = int(3).to_bytes(2, 'little')    # enable Notifications and Indications 
                                            # two bytes are required
    targetPeripheral.writeCharacteristic(   14, 
                                            value , 
                                            withResponse=False)

    # i = 0
    # for s in targetServices:
    #     print ('\n')
    #     targetHandles ["service"+str(i)] = {}
    #     try:
    #         hndStart = s.hndStart
    #         hndEnd   = s.hndEnd
    #         maxNumberHandlesAllowed = 8
    #         if (hndEnd>hndStart+maxNumberHandlesAllowed):
    #             hndEnd = hndStart+maxNumberHandlesAllowed
    #         targetHandles ["service"+str(i)] ['Handle Start']= hndStart
    #         targetHandles ["service"+str(i)] ['Handle End']= hndEnd
    #         targetHandles ["service"+str(i)] ['uuid']= str(s.uuid)
    #         targetHandles ["service"+str(i)] ['Common Name']= s.uuid.getCommonName()
    #         print (s.uuid.getCommonName(), ' - ',  hndStart, ' - ',  hndEnd)
            
    #         for h in range(hndStart, hndEnd+1):
    #             print ('_____________________________________________________________\n')
    #             print ('                                                              \n')
    #             try:
    #                 print (h, ' - value - ', targetPeripheral.readCharacteristic(h))
    #             except:
    #                 print (h , ' handle value not readable')
    #             try:
    #                 print ( h, ' - UUID -' ,
    #                 targetPeripheral.getCharacteristics(startHnd=h, endHnd=h)[0].uuid)
    #             except:
    #                 print (h , ' handle UUID not readable')
    #             try: 
    #                 print (h, 'UUID Common Name',
    #                 targetPeripheral.getCharacteristics(startHnd=h, endHnd=h)[0].uuid.getCommonName() )
    #             except:
    #                 print(h, 'no common name for the uuid found')
    #         print ('\n')
    #         print (targetHandles ["service"+str(i)])
    #     except:
    #         print('service :', s, "doesn't have Descriptors")
    #     finally:
    #         i += 1



    # targetDelegateList = [targetPeripheral.setDelegate( MyDelegate(h) ) for h in targetHandleList]
    # 13 is the handle for the Thermometer measurements
    targetPeripheral.setDelegate( MyDelegate(13))
    # This is needed to Handle Notifications.
    # By passing the Handle with each instantiation
    # you always know which characteristic(handle) sent the Notification
    
    # for h in targetHandleList:
    #     ConfigHandle = h + 1
    #     targetPeripheral.writeCharacteristic(ConfigHandle , (1).to_bytes(2, byteorder='little'))
    # enable notifications

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
