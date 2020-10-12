import boto3
import time


# Function to return the x,y and z values as a list of float values
def split_axes(data, x, y, z):
    # Before splitting the data into x,y,z axes it must be converted to float values
    str_axes = [strlist.strip('][').replace(" ", "").split(',') for strlist in
                data]  # Remove the brackets, then remove space before the numbers and then split it by "," to get a list with string values inside
    # print(str_axes)
    float_axes = [[float(axis) for axis in val] for val in str_axes]  # Convert string value in the list to float values
    # print(float_axes)

    # Split into x,y,z axes respectively and each new value is joined to the list of old values
    x.extend([item[0] for item in float_axes])
    y.extend([item[1] for item in float_axes])
    z.extend([item[2] for item in float_axes])


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('IMU_Data')

mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, timestamp = ([] for i in range(10))

# Get all the data from the table
response = table.scan(Select='ALL_ATTRIBUTES')

# Get the last set of data in order to use it as the point from which we scan in the next iteration
try:
    lastitem = response.get('Items')[-1]
except IndexError:
    print("No data!")
    exit()

lastevalkey = {k: lastitem.get(k) for k in lastitem.keys() if k in ['device_id', 'timestamp']}

#Loop that keeps getting data from cloud until there is a lastevalkey
while lastevalkey:
    data = (response.get('Items'))

    # Store all the necessary data for plotting in corresponding variables
    device_id = data[0]['device_id']
    timestamp.extend([item['timestamp'].split()[1] for item in data])  # Get only time value from the timestamp using split and "[1]"
    accelerometer = [item['accelerometer'] for item in data]
    split_axes(accelerometer, acc_x, acc_y, acc_z)
    print(acc_x)
    gyroscope = [item['gyroscope'] for item in data]
    split_axes(gyroscope, gyro_x, gyro_y, gyro_z)
    magnetometer = [item['magnetometer'] for item in data]
    split_axes(magnetometer, mag_x, mag_y, mag_z)

    time.sleep(2.2)                                                     # Data is being sent at x second intervals, so the program has to wait x sec before reading the next data

    response = table.scan(Select='ALL_ATTRIBUTES', ExclusiveStartKey=lastevalkey)       #Read next set of data starting from the last read data

    # Get the last set of data in order to use it as the point from which we scan
    try:
        lastitem = response.get('Items')[-1]
    except IndexError:
        print("Data Transmission stopped")
        break

    lastevalkey = {k: lastitem.get(k) for k in lastitem.keys() if k in ['device_id', 'timestamp']}
    # print(device_id)
    # print(timestamp)
    # print(accelerometer)
    # print(gyroscope)
    # print(magnetometer)



