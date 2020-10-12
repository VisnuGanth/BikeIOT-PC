import boto3
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('IMU_Data')

mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, timestamp = ([] for i in range(10))
fig, ax1 = plt.subplots(figsize=(10, 15))       #This creates the figure and plot in which data is to be plotted


# Function to return the x,y and z values as a list of float values in order to plot them
def split_axes(data, x, y, z):
    # Before splitting the data into x,y,z axes it must be converted to float values
    str_axes = [strlist.strip('][').replace(" ", "").split(',') for strlist in data]  # Remove the brackets, then remove space before the numbers and then split it by "," to get a list with string values inside
    # print(str_axes)
    float_axes = [[float(axis) for axis in val] for val in str_axes]  # Convert string value in the list to float values
    # print(float_axes)

    # Split into x,y,z axes respectively and each new value is joined to the list of old values
    x.extend([item[0] for item in float_axes])
    y.extend([item[1] for item in float_axes])
    z.extend([item[2] for item in float_axes])


# Plot graphs for all the data
def animate(i):

    global response
    global lastevalkey

    data = (response.get('Items'))

    # Store all the necessary data for plotting in corresponding variables
    timestamp.extend([item['timestamp'].split()[1] for item in data])           # Get only time value from the timestamp using split and "[1]"

    magnetometer = [item['magnetometer'] for item in data]
    split_axes(magnetometer, mag_x, mag_y, mag_z)

    response = table.scan(Select='ALL_ATTRIBUTES', ExclusiveStartKey=lastevalkey)

    # Get the last set of data in order to use it as the point from which we scan
    try:
        lastitem = response.get('Items')[-1]
    except IndexError:
        print("Data Transmission stopped")
        exit()

    lastevalkey = {k: lastitem.get(k) for k in lastitem.keys() if k in ['device_id', 'timestamp']}

    ax1.clear()         #Clears the old line that was plotted
    ax1.plot(timestamp, mag_x, label='X')       #Plot only mag_x data
    ax1.legend(frameon=False, loc='upper center', ncol=1)       #Places legend at the upper center in a single line without a border box
    plt.xlabel('timestamp')
    plt.xticks(rotation=45)


# Get all the initial data from the table
response = table.scan(Select='ALL_ATTRIBUTES')

# Get the last set of data in order to use it as the point from which we scan
try:
    lastitem = response.get('Items')[-1]
except IndexError:
    print("No data!")
    exit()

lastevalkey = {k: lastitem.get(k) for k in lastitem.keys() if k in ['device_id', 'timestamp']}

time.sleep(2.1)                                 # Data is being sent at x sec intervals. After initial read, we have to wait x seconds until next data is sent to DB

ani = animation.FuncAnimation(fig, animate, interval=2200)      #Calls animate function at 2.2 sec interval repeatedly to plot the new points
plt.show()                                                      #Show plot



