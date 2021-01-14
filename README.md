# BikeIOT-PC

An IoT project that receives 9-axis IMU (Inertial Measurement Unit) data from the SenseHAT emulator in the Raspberry Pi via the AWS IoT Core service and displays the retreived data by means of a dynamic graph made using Python. The data retreived from the SenseHAT emulator are: 3-axis gyroscope, 3-axis accelerometer and 3-axis magnetometer.

The relevant code to retreive the real-time data from DynamoDB and display it in the form of a graph is present inside the folder **clouddata** and the corresponding documentation explaining the code is inside the **Documentation** folder.

The Python files present in the order of increasing complexity are:
- static_graph.py - Plots a static graph of the retreived data
- realtimedata.py - Program to continuously get data from the cloud in real-time.
- realtimegraph-movingxaxis.py - Plots the x-axis magnetometer data with a moving x-axis
- realtimegraph-oneline.py - Plots a real-time moving graph of only the x-axis magnetometer data
- realtimegraph-alllines.py - Plots all the 9-axis IMU data with a moving x-axis

The documenation consists of documents for the entire project including the Raspberry Pi, AWS setup and code. Please refer them for a detailed explanation and a step-by-step guide.
