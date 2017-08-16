import bluetooth
import time
from application_commands import CMD

"""
موديل برمجي يحتوي مجموعة من التوابع و الاجرائيات المسؤولة عن الاتصال بدارة البلوتوث الخاصة بدارة الاردوينو

هذا ملخص عن التوابع
def discover_first_bluetooth_deivce(dr):
مسؤول عن استكشاف طرفيات البلوتوث المتوفرة و ذلك خلال فترة زمنية dr تعطى بالثانية, ثم يقوم بإرجاع اسم و عنوان أول طرفية بلوتوث مكتشفة

def discover_bluetooth_devices(duration=12):
تابع مسؤول عن استكشاف كل طرفيات البلوتوث المتوفرة و ذلك خلال فترة زمنية تعطى بالثانية
ثم يقوم بإرجاع قائمة بهذه الطرفيات على شكل معجم يحتوي اسم كل طرفية و عنوانها

class Arduino_Connection_Bluetooth:
صف يستخدم لاحتواء مجموعة من الخصائص و التوابع التي تساعد البرنامج بالاتصال بدارة الاردوينو و ارسال الاوامر لها
من الخصائص التي يحتويها مايلي

sock = bluetooth.BluetoothSocket
قابس يتم وصله بالطرف الاخر عند تاسيس اتصال بلوتوث

من الاجرائيات التي يحتويها الصف السابق مايلي
    
    def bt_connect(self, bd_add="98:D3:31:FD:11:AB", port=1):
    يستخدم للاتصال بطرفية بلوتوث بعد معرفة عنوانها bd_address
    
    def bt_send(self, data):
اجرائية تستخدم لارسال رسالة نصية عبر القابس بعد تأسيس الاتصال

    def receive(self):
اجرائية تستخدم لاستقبال رسالة عبر وصلة الاتصال 

    def bt_close(self):
اجرائية تستخدم لاغلاق القابس و تحرير الوصلة

كما ان هناك اجرائيات تستخدم لارسال رسائل تمثل اوامر محددة مسبقا إلى دارة الاردوينو مثل 

    def forward(self):
ارسال امر التقدم إلى الامام,

و هنالك اجرائيات من اجل امر التراجع, او أمر التوجه إلى اليمين أو إلى اليسار و أخير أمر التوقف
"""

def discover_first_bluetooth_deivce(dr):
    """
    Discover the first available bt device within specific time duration value.
    :param dr: int, seconds before ending up searching attempt
    :return: tuple(1st_device_name, 1st_device_bd_address), if no device were found return None
    """
    dvs = discover_bluetooth_devices(duration=dr)
    if len(dvs) > 0:
        for name in dvs:
            print 'First Device ', name, dvs[name]
            return (name, dvs[name])

    print ('No bluetooth device found')
    return None


def discover_bluetooth_devices(duration=12):
    """
    Discover bt devices with timeout duration seconds,
    :param duration: int, time out period in seconds
    :return: dictionary of devices with entries of (device_name => device BD_ADDR address)
    """
    result = {}
    print("performing bluetooth inquiry...")
    nearby_devices = bluetooth.discover_devices(
        duration=duration, lookup_names=True, flush_cache=True)
    print("found %d devices" % len(nearby_devices))
    for addr, name in nearby_devices:
        result[name] = addr
        try:
            print("  %s - %s" % (addr, name))
        except UnicodeEncodeError:
            print("  %s - %s" % (addr, name.encode('utf-8', 'replace')))
    return result


class Arduino_Connection_Bluetooth:
    """
    Use to connect the PC with HC-05 bluetooth module connected to arduino circuit
    Attributes:
        :sock: bluetooth socket
    """
    def __init__(self):
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def bt_connect(self, bd_add="98:D3:31:FD:11:AB", port=1):
        """
        Connect to bluetooth device addressed by "bd_add"
        :param bd_add: BD_ADDR address of remote bluetooth device
        :param port:
        """
        self.sock.connect((bd_add, port))
        self.sock.settimeout(1.0)
        print ('Bluetooth Connected')

    def bt_connect_first_device(self, duration=12):
        """
        If BD_ADDR address is not known, try to discover available bluetooth devices and
        connect to the first found device.
        :param duration: int, seconds to pass before ending the search
        """
        name, address = discover_first_bluetooth_deivce(duration)
        self.bt_connect(address)

    def bt_send(self, data):
        """
        Sending "data" through the bluetooth socket
        :param data: string, data to be sent
        """
        try:
            self.sock.send(data)
        except IOError:
            print "IO Error"

    def bt_close(self):
        self.sock.close() # release bluetooth socket and close it.

    def receive(self):
        """
        :return: string, data received from bt socket
        """
        return self.sock.recv(1)

    def forward(self):
        self.sock.send(CMD.FORWARD)

    def backward(self):
        self.sock.send(CMD.BACKWARD)

    def stop(self):
        self.sock.send(CMD.STOP)

    def right(self):
        self.sock.send(CMD.RIGHT)

    def left(self):
        self.sock.send(CMD.LEFT)


def example():
    # devices = discover_bluetooth_devices(4)
    # bt = discover_first_bluetooth_deivce(5)
    #
    # if bt == None:
    #     print 'no device was found'
    #     exit(0)
    # else:
    #     print bt
    #
    # bt_name , bt_address = bt
    ard = Arduino_Connection_Bluetooth()
    ard.bt_connect_first_device(3)


    # ard.bt_connect(bt_address)

    counter = 0
    while counter < 3:
        counter = counter + 1

        ard.forward()
        time.sleep(1)
        ard.backward()
        time.sleep(1)
        ard.right()
        time.sleep(1)
        ard.left()
        time.sleep(1)
        ard.stop()
        time.sleep(1)

    ard.bt_close()


if __name__ == '__main__':
    # test
    discover_bluetooth_devices(14)

