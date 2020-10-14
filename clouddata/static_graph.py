import boto3
import matplotlib.pyplot as plt

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('IMU_Data')

#Function to return the x,y and z values as a list of float values in order to plot them
def split_axes(data):

    #Before splitting the data into x,y,z axes it must be converted to float values
    str_axes = [strlist.strip('][').replace(" ", "").split(',') for strlist in data]  #Remove the brackets, then remove space before the numbers and then split it by "," to get a list with string values inside
    #print(str_axes)
    float_axes = [[float(axis) for axis in val] for val in str_axes]   #Convert string value in the list to float values
    #print(float_axes)

    #Split into x,y,z axes respectively
    x = [item[0] for item in float_axes]
    y = [item[1] for item in float_axes]
    z = [item[2] for item in float_axes]
    # print(x,y,z)

    return x,y,z

#Plot graphs for all the data
def plotgraph():
    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize=(10, 15))

    ax1.plot(timestamp, acc_x, label='X')
    ax1.plot(timestamp, acc_y, label='Y')
    ax1.plot(timestamp, acc_z, label='Z')
    ax1.legend(frameon=False, loc='upper center', ncol=3)
    ax1.set_title('Accelerometer')

    ax2.plot(timestamp, gyro_x, label='X')
    ax2.plot(timestamp, gyro_y, label='Y')
    ax2.plot(timestamp, gyro_z, label='Z')
    ax2.legend(frameon=False, loc='upper center', ncol=3)
    ax2.set_title('Gyroscope')

    ax3.plot(timestamp, mag_x, label='X')
    ax3.plot(timestamp, mag_y, label='Y')
    ax3.plot(timestamp, mag_z, label='Z')
    ax3.legend(frameon=False, loc='upper center', ncol=3)
    ax3.set_title('Magnetometer')

    plt.xlabel('timestamp')
    plt.xticks(rotation=45)
    # lines, labels = fig.axes[-1].get_legend_handles_labels()  Shows a single legend for entire graph
    # fig.legend(lines, labels, loc = 'upper right')
    plt.show()



# Get all the data from the table
response = table.scan(Select='ALL_ATTRIBUTES')
data = (response.get('Items'))

# Store all the necessary data for plotting in corresponding variables
device_id = data[0]['device_id']
timestamp = [(item['timestamp'].split()[1])[:-4] for item in data] #Get only time value from the timestamp using split and "[1]". The -4 removes the millisecond value
accelerometer = [item['accelerometer'] for item in data]
acc_x,acc_y,acc_z = split_axes(accelerometer)
gyroscope = [item['gyroscope'] for item in data]
gyro_x,gyro_y,gyro_z = split_axes(gyroscope)
magnetometer = [item['magnetometer'] for item in data]
mag_x,mag_y,mag_z = split_axes(magnetometer)

# print(device_id)
# print(timestamp)
# print(accelerometer)
# print(gyroscope)
# print(magnetometer)

plotgraph() #Function call to plot graphs

