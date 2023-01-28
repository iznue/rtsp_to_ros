#!/usr/bin/env python
# coding: utf-8

import time
import cv2 
import rospy
import threading
import numpy as np

from sensor_msgs.msg import CompressedImage

global pub0
#pub0 = rospy.Publisher('/usb_cam/image_raw/compressed',	CompressedImage,	queue_size=1)
pub0 = rospy.Publisher('/main_camera/image_raw/compressed',	CompressedImage,	queue_size=1)

def do_read(mountpoint, stpEvent):
    
    global pub0
    url='rtsp://223.171.62.1:11112/'+mountpoint
    #url='rtsp://223.171.62.1:11112/'+mountpoint
    
    #url='rtsp://192.168.43.26/'+mountpoint
    ##url = 'rtsp://admin:admin@223.171.139.150:11112/raw'
    #url='rtsp://223.171.62.1:11111/'+mountpoint
    #url = 'rtsp://223.171.62.1:11111/raw' 
    
    print(str(url)+" rtsp steaming Start")
    cap = cv2.VideoCapture(url) 

    while not stpEvent.is_set() : 
        ret, frame = cap.read() # 윈도우 창 출력용 

        #### Create CompressedIamge ####
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', frame)[1]).tostring()
        # Publish new image
        pub0.publish(msg)
        time.sleep(0.01)
        #cv2.imshow(str(mountpoint), frame) 
        #cv2.waitKey(1)
        print('0gogoo')
    print(str(url)+" rtsp steaming Done")


if __name__ =='__main__':
    try:
        rospy.init_node('rtsp2imageCompr', anonymous=True)
        stopEvent=threading.Event()
        rawImageThread= threading.Thread(target=do_read,  args=('back', stopEvent, ))
        #rawImageThread= threading.Thread(target=do_read,  args=('raw', stopEvent, ))
        #topImageThread= threading.Thread(target=do_read2, args=('top', stopEvent, ))
        #tpfImageThread= threading.Thread(target=do_read, args=('tpf', stopEvent, ))

        rawImageThread.start()
        #topImageThread.start()
        #tpfImageThread.start()
        while not rospy.is_shutdown():
            time.sleep(1)
            rospy.spin()            
    except KeyboardInterrupt:
        print("keyboard Interrupted")
        stopEvent.set()
        pass
    finally:
        print("program done")
        stopEvent.set()
        
    


