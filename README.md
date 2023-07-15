# Hand Gesture Detection using Raspberry Pi
This repository contains files of the Hardware Laboratory course, Spring 2023.
Although it is more convenient to use the [MediaPipe](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) library for hand keypoint detection we do it from scratch and use a pre-trained tf-lite model.

![overview](https://github.com/ckoorosh/HW-Lab-Spring23/assets/53394330/7bbb6ddc-c008-45b1-8748-0ab79f3dcd67)

## Requirements
Below is a list of the components you will need to get this system up.

- Raspberry Pi 3 Model B
- Raspberry Pi Camera Module
- Micro SD Card
- Power Supply
- Monitor (Optional - Otherwise you can use a [VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/))

### Initial Set-Up
First, you need to install the operating system on the Raspberry Pi. It is recommended to use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to install an operating system onto your SD card.
You can follow [this](https://www.raspberrypi.com/documentation/computers/getting-started.html) tutorial from the official website.
**Note:** Our code has been tested on a 64-bit OS version. 

After installing the OS, you need to install the required packages on the system.
You can use the following command to install OpenCV and TensorFlow Lite.
If you encounter an error while installing the TensorFlow Lite library check the version of python installed on the system and change the `tflite_runtime` version respectfully.

```bash
bash setup.sh
```

The client code requires Python 3.8 or later. The file [requirements.txt](requirements.txt) contains the full list of required Python modules.
```bash
pip install -r requirements.txt
```

## Running the Code
Our system will be able to receive gestures from the Raspberry device by establishing a socket connection between the two. This will enable seamless and efficient communication between the two devices. 
To begin, it is necessary to modify the IP addresses in both [`handler.py`](https://github.com/ckoorosh/HW-Lab-Spring23/blob/main/handler.py#L28) and [`client.py`](https://github.com/ckoorosh/HW-Lab-Spring23/blob/main/client.py#L78). 

In order to initiate the server on your Raspberry device, you will need to execute the `manager.py` file. 
Additionally, on your client system, you should run the `client.py` file. 
This will allow for proper communication between the server and client devices.
Finally, you can see the gestures being applied on the client side.

**Note:** Currently, only 5 gestures are supported:

- Move Mouse
- Click Mouse
- Double Click Mouse
- Right Click Mouse
- Take ScreenShot

The gestures have been defined on the `handler.py` for the server and on the `client.py` for the actions on the client.

## Report
You can find the final report (in Persian) and descriptions of various modules at [report.pdf](report/report.pdf).
The tf-lite checkpoints of our hand detection models have been put in the `checkpoints` directory.
