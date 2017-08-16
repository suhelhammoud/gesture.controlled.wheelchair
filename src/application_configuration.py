"""
صف يحتوي مجموعة من الثوابت المستخدمة في اماكن مختلفة من البرنامج
 بعض هذه الثوابت يشير إلى مواضع ملفات بارمترات خوارزميات تحديد الوجوه و العيون و الابتسامات

 بعض هذه الثوابت يحدد الابعاد الصغرى لحجوم الوجوه و العين و الابتسامة الممكن اكتشافها في الصورة المدروسة

  و أخيرا هنالك عدة ثوابت تقوم بتعريف قيم لونية تستخدم من اجل رسم مستطيلات محيطة بالوجه أو العين أو الابتسامة المكتشفة
"""
class Configuration:
    """
    All project configurations are grouped here in one place
    """
    face_file = "../data/haarcascades/haarcascade_frontalface_default.xml"
    eye_file = "../data/haarcascades/haarcascade_eye.xml"
    left_eye_file = "../data/haarcascades/haarcascade_lefteye_2splits.xml"
    right_eye_file = "../data/haarcascades/haarcascade_righteye_2splits.xml"
    nested_smile_file = "../data/haarcascades/haarcascade_smile.xml"

    # Minimum Sizes for face, eye, and smile areas
    min_face_size = (140, 140)
    min_eye_size = (30, 30)
    min_smile_size = (130, 60)  # TODO: adjust values

    # Colors for rectangles, lines, and circles to be drawn on output image
    color_face = (0, 255, 0)
    color_eye = (0, 0, 255)
    color_eye_left = (255, 0, 0)
    color_eye_right = (0, 0, 255)
    color_smile = (0, 255, 255)
