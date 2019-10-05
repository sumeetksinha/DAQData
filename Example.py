""" 
Reading slow data and fast data files
========================================

This example shows how to read meta-data and associated sensor data from the
slow and fast data files 
"""

# import the module
import DAQData as DQ;

# Centrifuge CGM (UC Davis) data file. Can be slow as well as fast data 
Data_File = "./Binary_Data_Files/07122019@121326@154548@64.4rpm.bin";


# By default the, 'Extract_Data' parameter is set to be True. If the files are
# very large and only meta data needs to be checked, the data extraction can be
# stooped by setting 'Extract_Data' parameter false. This would increase the
# execution speed but will not read any data 
Data_DAQ = DQ.DAQ(Data_File,Extract_Data=True);


#####################################################################################################################
# Read meta data
#####################################################################################################################

# Just use the print statement to print the meta data
# print(Data_DAQ)

# Extracting meta data
FileName                      = Data_DAQ.FileName; # gets the filename
Sampling_Rate                 = Data_DAQ.Sampling_Rate; # gets Sampling_Rate
Number_of_Channels            = Data_DAQ.Number_of_Channels; # gets number of channels
Number_of_Hardware_Channels   = Data_DAQ.Number_of_Hardware_Channels; # gets number of hardware channels
Number_of_Xdcr_Serial_Numbers = Data_DAQ.Number_of_Xdcr_Serial_Numbers # gets number of Xdcr_Serial Numbers (also referred as sensors)
Channel_List                  = Data_DAQ.Channel_List; # gets the channel list
Hardware_Channel_List         = Data_DAQ.Hardware_Channel_List; # get the hardware channel list
Xdcr_Serial_Numbers_List      = Data_DAQ.Xdcr_Serial_Numbers_List; # gets the sensor list 
Number_of_Samples             = Data_DAQ.Number_of_Samples; # gets the total number of samples per sensor 
Data_Length                   = Data_DAQ.Data_Length; # gets the total data length in the binary file. Number_of_Samples*Number_of_sensors
Channel_Dictionary            = Data_DAQ.Channel_Dictionary; # returns a dictionary of channel name to the column number in data 
ExcelConfig                   = Data_DAQ.ExcelConfig; # return excel configuration file as a csv string 

#####################################################################################################################
# Extract data on demand
#####################################################################################################################

# If the 'Extract_Data' parameter is True, the whole data is already read and extracted and can be easily retrieved as
Time_Data  = Data_DAQ.Time_Data;	# 1=D array 
Sensor_Data = Data_DAQ.Sensor_Data;	# 2-D numpy array
print(Sensor_Data.shape)

# If the 'Extract_Data' parameter was initially set to False, the data can be extracted on demand by defining the start and end time
# ..... Time_Data, Sesnor_Data = Data_DAQ.Extract(Start_Time=0, End_Time=10)
# To extract the whole data, set the start time to be 0 and end time to be Number_of_Samples/Sampling_Rate
#

Data_DAQ  = DQ.DAQ(Data_File,Extract_Data=False);
Time_Data,Sensor_Data = Data_DAQ.Extract(Start_Time=0,End_Time=Number_of_Samples/Sampling_Rate);

print(Sensor_Data.shape) # would return the same length of data as above 

#####################################################################################################################
# Read a particular sensor data and make a plot
#####################################################################################################################

Channel_Index = Data_DAQ.get_Channel_Index(Channel_Name='ICP1-0');
ICP10_Data    = Sensor_Data[:,Channel_Index];
Sensor_Name   = Xdcr_Serial_Numbers_List[Channel_Index];

import matplotlib.pyplot as plt;

plt.figure(figsize=(8,3));
plt.plot(Time_Data,ICP10_Data,'k',label=Sensor_Name);
plt.legend(loc='best')
plt.grid(b=True, which='major', ls='-')
plt.grid(b=True, which='minor', ls='--', alpha=0.4)
plt.minorticks_on()
plt.xlabel('Time [s]')
plt.ylabel('Acc [g]')
plt.ylim([-10,10])
plt.tight_layout();
plt.savefig('Input_Motion.png', bbox_inches = 'tight', dpi = 800);


# ## The plot function can be alternatively used even for plotting very very large data
# Data_DAQ.Plot(Channel_Name_1='TIME', Channel_Name_2='ICP1-0',  ScaleX= 1, OffsetX = 0, ScaleY= 1, OffsetY = 0, Color = 'k');

