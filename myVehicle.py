from donkeycar.vehicle import Vehicle
from cvCam import CvCam
from cvCam import CvImageDisplay

V = Vehicle()

cam = CvCam()

V.add(cam, outputs = ["camera/image"], threaded=True)

disp = CvImageDisplay()

V.add(disp, inputs = ['camera/image'])
V.start()
