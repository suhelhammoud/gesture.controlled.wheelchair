from application_configuration import Configuration
from application_roi import *
from application_commands import *
from application_arduino_bluetooth import *


"""
الموديل الرئيسي في البرنامج و من خلاله يتم استيراد جميع الموديلات البرمجية الاخرى عن طريق التعليمة
import 
from __ import 

يحتوي هذا القسم على اجرائية تشغيل البرنامج الموجودة ضمن القسم __main__
و العديد من الاجرائيات المساعدة, توثيق هذه الاجرائيات موضع بالتفصيل في الكود المصدر وباختصار هذه الاجرائيات المساعدة تقوم بـ

رسم نص على صورة الخرج من أجل اعطاء المستخدم معلومة عن التعليمة التي تم ارسالها إلى دارة الاردوينو
رسم مستطيلات و دوائر على صورة الخرج 
رسم بعض الخطوط و المستطيلات على الصورة بحيث تساعد المستخدم في تشغيل البرنامج و تحريك وجهه بشكل مناسب يسمح بدقة أكبر في التعرف على الأوامر

إن حلقة التحكم الرئيسية  في هذا البرنامج تقوم بتكرار 
استدعاء اجرائية تحديد مواضع الوجوه و العيون و الابتسامات في الصورة وهي اجرائية  process_frame
و الخوارزمية المنفذة في هذ الاجرائية هي كالتالي

1- استلام الصورة المقروءة من الكاميرا
2- الحصول على الصورة المناظرة حسب المحور الشاقولي بحيث تبدو الصورة للمستخدم كأنه ينظر إلى مرآة
3- تحويل الصورة من ملونة إلى صورة ابيض و اسود لتسريع عملية المعالجة, حيث أن معالجة الصور الرمادية في مكتبة opencvاسرع بكثير من معالجة الصورة الملونة 
3- استدعاء خوارزمية تحديد الوجه على الصورة المدروسة
4- من اجل الوجوه التي تم تحديدها يتم استدعاء خوارزميات تحديد العيون و الابتسامات داخل هذه الوجوه فقط
5- اذا تم اكتشاف هذه العيون و الابتسامات يتم ارجاع النتيجة و تسليمها إلى المرحلة التالية

المرحلة التالية:
-يتم استلام نتائج معالجة الصورة و تكون على شكل مستطيلات تمثل مواضع العيون و الابتسامات
-يتم التأكد من ان هذه النتائج صحيحة كأن تكون الابتسامات تحت العيون و أن تكون العين اليمنى إلى يمين العين اليسرى و هكذا من الاختبارات الموثقة في المصدر
-يتم تحديد الامر الذي سيرسل إلى دارة الاردوينو اعتمادا على الموضع النسبي للعينين و الابتسامة بالنسبة إلى النقطة المرجعية و عادة تكون في منتصف الصورة

-بعد تحديد الامر يتم ارساله إلى دارة الاردوينوو باستخدام الاجرائيات الموجودة في موديل الاتصال application_arduino_bluetooth و هذه الاجرائيات مشروحه في مكانها.
-يتم اظهار صورة متحركة تمثل وجه المستخدم مع رسم مواضع الوجه, العيون , الابتسامة المكتشفة بالاضافة إلى رسم معلومات عن
ناتج معالجة الصورة بحيث يرى المستخدم ما هو الامر الحالي الذي يتم ارساله إلى الاردوينو

-يتم تكرار العملية السابقة حتى يقوم المستخدم بإنهاء البرنامج عن طريق ضغط زر Q من لوحة المفاتيح

"""
def draw_text(vis, txt):
    """
    Draw text on the top left corner of provided image
    :param vis: opencv image to be drawn on
    :param txt: string, text message to be displayed on image
    """
    cv2.putText(vis, txt, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255))


def draw_center_lines(img, roi, clr):
    """
    Draw, across the whole image, one vertical line and one horizontal line which pass through roi center
    :param img: opencv image
    :param roi: RoiBounds object of "roughly" center of the image
    :param clr: tuple(g,r,b) color of the line
    """
    cv2.line(img, (roi.x0, roi.yc), (roi.x1, roi.yc), clr, 1)
    cv2.line(img, (roi.xc, roi.y0), (roi.xc, roi.y1), clr, 1)


def draw_rect(img, roi, clr, line_width=1):
    """
    Draw on image "img" a rectangle defined by "roi" with color "clr"
    :param img: opencv image
    :param roi: RoiBounds object of the rectangle area
    :param clr: tuple(g,r,b) color of the drawing line of rectangle
    :param line_width: integer, (optional)
    """
    cv2.rectangle(img, roi.top_left(), roi.bottom_right()
                  , clr, line_width)


def draw_circles(img, command):
    """
    Depending on the command, draw array of on/off circles on the top left area of image "img"

    :param img: opencv image
    :param command: CMD
    """
    if command is None:
        return
    cmd = {
        CMD.FORWARD: [0, 1, 0, 1],
        CMD.BACKWARD: [1, 0, 1, 0],
        CMD.RIGHT: [1, 0, 0, 0],
        CMD.LEFT: [0, 0, 1, 0],
        CMD.STOP: [0, 0, 0, 0]
    }[command]
    clr = {
        0: (50, 50, 50),  # color of "off" circle
        1: (0, 0, 255)  # color of "on" circle
    }
    cv2.circle(img, (30, 100), 8, clr[cmd[0]], 20)
    cv2.circle(img, (70, 100), 8, clr[cmd[1]], 20)
    cv2.circle(img, (110, 100), 8, clr[cmd[2]], 20)
    cv2.circle(img, (150, 100), 8, clr[cmd[3]], 20)


def draw_rects(img, rois, color, line_widht=2):
    for roi in rois:
        cv2.rectangle(img, roi.top_left(), roi.bottom_right(), color, line_widht)


def draw_line(vis, center, width, height, color=(255, 0, 0)):
    cv2.line(vis, (center[0], 0), (center[0], height), color, 1)
    cv2.line(vis, (0, center[1]), (width, center[1]), color, 1)


def detect(img, cascade, min_size=(40, 40)):
    """
    Detect an object(face, eye, or smile)  using "cascade" classifier then return RoiBounds object that represents
    the area of detected object

    :param img: opencv object
    :param cascade: opencv haar classifier, for face, eye, or smile
    :param min_size: tuple(integer, integer) (optional) used to limit the search for object in areas no smaller than min_size
    :return: list of RoiBounds values for the detected objects in the image
    """
    rects = cascade.detectMultiScale(img, scaleFactor=1.3,
                                     minNeighbors=5, minSize=min_size,
                                     flags=cv2.CASCADE_SCALE_IMAGE)

    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    result = [RoiBounds(x1, y1, x2, y2) for x1, y1, x2, y2 in rects]
    return result


class ProcessVideo:
    """

    Attributes
        :cam stream: to read the video frames, it is either from local file or from web camera
        :face_classifier: Classifer to detect and to locate faces in images
        :eye_classifier: Classifier to detect and to locate eyes in images
        :smile_classifier: Classifer to detect and to locate smile in images
    """

    def __init__(self, file_path=None):
        if file_path is None:
            file_path = 0
        self.cam = cv2.VideoCapture(file_path)
        self.face_classifier = cv2.CascadeClassifier(Configuration.face_file)
        self.eye_classifier = cv2.CascadeClassifier(Configuration.eye_file)
        self.left_eyes_classifier = cv2.CascadeClassifier(Configuration.left_eye_file)
        self.right_eyes_classifier = cv2.CascadeClassifier(Configuration.right_eye_file)
        self.smile_classifier = cv2.CascadeClassifier(Configuration.nested_smile_file)

    def get_one_frame(self):
        """
        Read one frame from video source

        :return: numpy.array(), opencv image
        """
        ret, img = self.cam.read()
        return img

    def process_frame(self, img):
        """
        Process one image frame , locate faces in image, choose only one face,
        then locate eyes in the face, and locate possible smile
        :param img: numpy.array(), opencv image
        :return:      vis: numpy.array, copy of "img" image to be shown with drawing on it
            roibound_eyes: list of RoiBounds objects representing the detected eyes
           roibound_smile: list of RoiBounds objects represeting the detected smiles

        """
        # TODO: resize image to fixed size defined in Configurations class
        # img = cv2.resize(img, (600, 800))
        img = cv2.flip(img, 1)  # flip image horizontally to be shown as the mirror

        # TODO: Try Skip number of frames defined in Configurations class
        # get gray image from the colored "img" for faster processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # TODO: adjust the equalized Histogram
        # gray = cv2.equalizeHist(gray)

        # TODO: use clock time measures

        # TODO: check weather defensive copy "vis = img.copy()" is necessary here
        vis = img
        roibound_face = detect(gray, self.face_classifier, Configuration.min_face_size)
        # Draw rectangles around the detected faces, border color = Configuration.color_face
        draw_rects(vis, roibound_face, Configuration.color_face)

        # continue only if one face were detected in image, otherwise exit this method
        if len(roibound_face) != 1:
            return (vis, None, None)  # Only one face is allowed in image

        # keep the top left coordinates of the face area
        dx, dy = roibound_face[0].top_left()

        for area in roibound_face:
            eyes_roi = RoiBounds.get_roi(gray, area)
            vis_roi = RoiBounds.get_roi(vis, area)

            # Locate eyes in the face area using eye classifier
            roibound_eyes = detect(eyes_roi, self.eye_classifier, Configuration.min_eye_size)

            # Locate smile in the face area using smile classifier
            roibound_smile = detect(eyes_roi, self.smile_classifier,
                                    Configuration.min_smile_size)
            # Draw rectangles around eyes and smile areas using colors defined in Configuration class
            draw_rects(vis_roi, roibound_eyes, Configuration.color_eye)
            draw_rects(vis_roi, roibound_smile, Configuration.color_smile)
            return (vis, [r.translate(dx, dy) for r in roibound_eyes],
                    [r.translate(dx, dy) for r in roibound_smile])

    def image_process_loop(self):
        ard = Arduino_Connection_Bluetooth()
        try:
            ard.bt_connect("98:D3:31:FD:11:AB")
        except IOError:
            print "IO error with arduino"

        init_img = self.get_one_frame()
        height, width = RoiBounds.height_width(init_img)

        # Define boxes to be drawn on the vis image
        roibound_ref = RoiBounds.center_roibound(init_img, [2])
        roibound_face = RoiBounds.center_roibound(init_img, [100, 110, 100, 120])

        if self.left_eyes_classifier.empty() \
                or self.right_eyes_classifier.empty() \
                or self.smile_classifier.empty():
            print 'one of the cascade xml files is not there, check your path'
            return  # early exit the method if an error were discovered

        command_queue = CommandQueue(8, 2)  # initialize the command_queue buffer with capacity and threshold
        result_command = CMD.STOP

        while self.cam.isOpened():  # while web camera stream is there do the following
            # take one frame from the video stream
            img = self.get_one_frame()
            # decide where are the areas of eyes and smile in the image
            vis, roibound_eyes, roibound_smile = self.process_frame(img)

            # Draw lines and rectangles to help the user align his face in the center of image
            draw_line(vis, roibound_ref.center(), width, height, (255, 0, 0))
            draw_rects(vis, [roibound_ref], color=(0, 255, 255))
            draw_rects(vis, [roibound_face], color=(255, 0, 0))

            # pass this areas for further processing to deduce the command to be sent to the arduino device
            command = RoiBounds.process_roibounds(roibound_eyes, roibound_smile, roibound_ref)
            if command is not CMD.NONE:
                # if command is valid, add it the command buffer and get the current most common command
                result_command = command_queue.add_and_get(command)

            # Now we have a result_command, print it on vis image and draw on/off circles of it

            draw_text(vis, CMD.st(result_command))
            draw_circles(vis, result_command)
            # TODO : uncommenct next line when bluetooth device is there

            # send this command to arduino device through bluetooth connection
            if result_command is not None:
                ard.bt_send(result_command)


            cv2.imshow('facedetect', vis)
            if cv2.waitKey(1) & 0xFF == ord('q') & ord('Q'):
                #  press q/Q key to quit the main loop and hence the application
                break

        # clear and free resources
        cv2.destroyAllWindows()
        ard.bt_close()


if __name__ == '__main__':
    print ("start")

    vid = ProcessVideo()
    vid.image_process_loop()
