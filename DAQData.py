######################################################################
# Sumeet Kumar Sinha (sumeet.kumar507@gmail.com)
# PhD Student, UC Davis
# Version: 27th August, 2019
######################################################################

import os
import sys
import struct
import re
import binascii
import numpy as np
import matplotlib.pyplot as plt
import warnings
import math
import pandas as pd
warnings.filterwarnings("ignore")

class DAQ(object):
    """DAQ reads the binary data file produced by Center of Geotechnical Engineering UC Davis. 
    """

    def __init__(self, FileName, Extract_Data=True, Reading_Rate = 100000):
        
        ExcelConfig                   = '';                       
        Sampling_Rate                 = 1;
        Number_of_Channels            = 0;
        Number_of_Hardware_Channels   = 0;
        Number_of_Sensors = 0;
        Channel_List                  = [];
        Hardware_Channel_List         = [];
        Sensor_List      = [];
        Number_of_Samples             = 0;
        Data_Length                   = 0;
        Channel_Dictionary            = {};

        with open(FileName,"rb") as f:

            ##################################################
            newLine = (f.readline()).strip();
            # print newLine
            while (newLine.decode()!="[readme]"):
                newLine = (f.readline()).strip();
                # print newLine
            ## Read the readme content of the file here
            # print("Readme_Done!")
            ##################################################

            ##################################################
            newLine = (f.readline()).strip();
            while (newLine.decode()!="[Hardware channel name list]"):
                newLine = (f.readline()).strip();
            ## Read the hardware channel name list
            newLine = ((f.readline()).strip()).decode();
            Hardware_Channel_List = newLine.split(',');
            Number_of_Hardware_Channels = len(Hardware_Channel_List);
            Hardware_Channel_List = Hardware_Channel_List[0:Number_of_Hardware_Channels];
            # print Hardware_Channel_List
            # print("Hardware channel name list Done!")
            ##################################################

            ##################################################
            newLine = (f.readline()).strip();
            while (newLine.decode()!="[channel name list]"):
                newLine = ((f.readline()).strip());
            ## Read the channel name list
            newLine = ((f.readline()).strip()).decode();
            Channel_List = newLine.split(',');
            Number_of_Channels = len(Channel_List);
            Channel_List = Channel_List[0:Number_of_Channels];
            # Channel_List.append('Time');
            # print Channel_List
            ##################################################

            ##################################################
            newLine = (f.readline()).strip();
            while (newLine.decode()!="[Xdcr Serial Numbers]"):
                newLine = ((f.readline()).strip());
            ## Read the Xdcr Serial Numbers
            newLine = ((f.readline()).strip()).decode();
            Sensor_List = newLine.split(',');
            Number_of_Sensors = len(Sensor_List);
            Sensor_List = Sensor_List[0:Number_of_Channels];
            # print Sensor_List
            ##################################################

            ##################################################
            Sampling_Rate = 1;
            newLine = (f.readline()).strip();
            while (newLine.decode()!="[excelconfig]"):
                # print newLine.decode()
                newLine = (f.readline()).strip();
                if(newLine.decode()=="[sampling rate]"):
                    data = f.read(4);
                    Sampling_Rate = struct.unpack('>f',data[0: 4])[0];

            Num_of_excel_config = Number_of_Channels;
            if(Sampling_Rate==1):
                Num_of_excel_config = Num_of_excel_config-1;
            for i in range(0,Num_of_excel_config):
                newLine = (f.readline()).strip();
                ExcelConfig = ExcelConfig +newLine.decode() +'\n';
            ## Read the excelconfig of the file here
            ##################################################

            # ##################################################
            # newLine = (f.readline()).strip();
            # while (newLine.decode()!="[sampling rate]"):
            #     newLine = (f.readline()).strip();
            # ## Read the readme content of the file here
            # data = f.read(4)
            # Sampling_Rate = struct.unpack('>f',data[0: 4])[0];
            # ##################################################

            ##################################################
            newLine = (f.readline()).strip();
            while (newLine.decode()!="[data]"):
                newLine = (f.readline()).strip();

            ###################################################
            #### Reading number of samples in the binary file
            ###################################################

            old_file_position = f.tell()
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(old_file_position, os.SEEK_SET)

            Estimated_Total_Data_Length = size/4 ; # estimated data length 
            Estimated_Number_Of_Samples = Estimated_Total_Data_Length/Number_of_Channels; # estimated number of samples

            ##################################################
            #### Actual length of data 
            ##################################################

            Num_Iterations = int (Estimated_Total_Data_Length/Reading_Rate)+1;
            Data_Length    = 0;
            for i in range(0,Num_Iterations):
                data = np.fromfile(f, dtype='>f',count=Reading_Rate);
                Data_Length = Data_Length + len(data);

            data = [];
            Number_of_Samples = Data_Length/Number_of_Channels;

            ##################################################
            #### Creating Channel Dictionary
            ##################################################

            index_list = 0;
            for x in Channel_List:
                Channel_Dictionary[x]=index_list;
                index_list = index_list+1;
            if(Sampling_Rate!=1):
                Channel_Dictionary['TIME'] = -1;

            # print(Channel_Dictionary);
          
        self.FileName = FileName;
        self.Sampling_Rate                 = Sampling_Rate                ;
        self.Number_of_Channels            = Number_of_Channels           ;
        self.Number_of_Hardware_Channels   = Number_of_Hardware_Channels  ;
        self.Number_of_Sensors             = Number_of_Sensors;
        self.Channel_List                  = Channel_List                 ;
        self.Hardware_Channel_List         = Hardware_Channel_List        ;
        self.Sensor_List                   = Sensor_List     ;
        self.Number_of_Samples             = Number_of_Samples            ;
        self.Data_Length                   = Data_Length                  ;
        self.Channel_Dictionary            = Channel_Dictionary           ;
        self.ExcelConfig                   = ExcelConfig                  ;
        if(Extract_Data):
            self.Sensor_Data   = self.Extract(0,int(self.Number_of_Samples/self.Sampling_Rate),Reading_Rate=500000);
        else:
            self.Sensor_Data = [];



    def __str__(self):

        Message = "";
        Message = Message + "FileName:                        " + str(self.FileName) + "\n";
        Message = Message + "Sampling_Rate:                   " + str(self.Sampling_Rate) + "\n";
        Message = Message + "Number_of_Channels:              " + str(self.Number_of_Channels) + "\n";
        Message = Message + "Number_of_Hardware_Channels:     " + str(self.Number_of_Hardware_Channels) + "\n";
        Message = Message + "Number_of_Sensors:               " + str(self.Number_of_Sensors) + "\n";
        Message = Message + "Channel_List:                    " + str(self.Channel_List) + "\n";
        Message = Message + "Hardware_Channel_List:           " + str(self.Hardware_Channel_List) + "\n";
        Message = Message + "Sensor_List:                     " + str(self.Sensor_List) + "\n";
        Message = Message + "Number_of_Samples:               " + str(self.Number_of_Samples) + "\n";
        Message = Message + "Data_Length:                     " + str(self.Data_Length) + "\n";
        Message = Message + "Channel_Dictionary:              " + str(self.Channel_Dictionary) + "\n";
        Message = Message + "ExcelConfig:                     " + str(self.ExcelConfig) + "\n";
        return Message

    def Plot(self, Channel_Name_1, Channel_Name_2, ScaleX= 1, OffsetX = 0, ScaleY= 1, OffsetY = 0, Color = 'k', Reading_Rate = 5000000, Title=None ):
        
        plt.figure();

        with open(self.FileName,"rb") as f:


            ##################################################
            Sampling_Rate = 1;
            newLine = (f.readline()).strip();
            while (newLine.decode()!="[excelconfig]"):
                # print newLine.decode()
                newLine = (f.readline()).strip();
                if(newLine.decode()=="[sampling rate]"):
                    data = f.read(4);
                    Sampling_Rate = struct.unpack('>f',data[0: 4])[0];
                    newLine = (f.readline()).strip();
            ##################################################
            
            ##################################################
            ## Navigating the pointer to the location where 
            ## information is stored
            newLine = ((f.readline()).strip());
            while (newLine.decode()!="[data]"):
                newLine = (f.readline()).strip();
            ##################################################

            ##################################################
            ## Correct reading length based on number of channels 
            ##################################################
            Reading_Rate = int(Reading_Rate/self.Number_of_Channels)*self.Number_of_Channels;
            #################################################

            # print Channel_Name_1
            # print Channel_Name_2

            Sensor1_Index = self.Channel_Dictionary[Channel_Name_1];
            Sensor2_Index = self.Channel_Dictionary[Channel_Name_2];

#             print(Sensor1_Index);
#             print(Sensor2_Index);

            #################################################
            ### Reading Data
            #################################################
            Num_Iterations = int (self.Data_Length/Reading_Rate)+1;
            time = 0;Time = []; HaveLabel=True; Iter = 0;
            for i in range(0,Num_Iterations):

                Sensor1_Data = []; Sensor2_Data = [];

                data = np.fromfile(f, dtype='>f',count=Reading_Rate);

                ######################################################################################
                correct_datalength = int(len(data)/self.Number_of_Channels)*self.Number_of_Channels;
                data = data[0:correct_datalength];
                Reading_Sampling_Rate = int(correct_datalength/self.Number_of_Channels);
                data = data.reshape(Reading_Sampling_Rate,self.Number_of_Channels);
                ######################################################################################

                if(Sensor1_Index==-1):
                    Time = np.linspace(time, time+(Reading_Sampling_Rate-1)*1.0/self.Sampling_Rate, num=Reading_Sampling_Rate);
                    if(len(Time)==0):
                        time =0;
                    else:
                        time = Time[-1];
                    Sensor1_Data = Time;
                else:
                    Sensor1_Data = (data[:,Sensor1_Index]).copy();

                if(Sensor2_Index==-1 and Sensor1_Index!=-1):
                    Time = np.linspace(time, time+(Reading_Sampling_Rate-1)*1.0/self.Sampling_Rate, num=Reading_Sampling_Rate);
                    if(len(Time)==0):
                        time =0;
                    else:
                        time = Time[-1];
                    Sensor2_Data = Time;
                elif(Sensor2_Index==-1 and Sensor1_Index==-1):
                    Sensor2_Data = Time;
                else:
                    Sensor2_Data = (data[:,Sensor2_Index]).copy();

                ################################################################
                ## Filtering the data
                ################################################################
                # N  = 2    # Filter order
                # Wn = 0.002 # Cutoff frequency
                # B, A = signal.butter(N, Wn, output='ba')
                # data = [];
                # Sensor1_Data    = signal.filtfilt(B,A, Sensor1_Data)
                # Sensor2_Data    = signal.filtfilt(B,A, Sensor2_Data)
                # # Iter = Iter +1;
                # # print ("Figure " + str(Iter) + "completed")
                # # return
                ################################################################
                ## Filtering the data ends
                ################################################################

                plt.plot(Sensor1_Data[:]*ScaleX+OffsetX, Sensor2_Data[:]*ScaleY+OffsetY,color=Color);
                Sensor1_Data = []; Sensor2_Data = [];

            plt.xlabel(Channel_Name_1)
            plt.ylabel(Channel_Name_2)
            plt.grid(b=True, which='major', color='k', linestyle='-')
            plt.grid(b=True, which='minor', color='k', linestyle='-', alpha=0.2)
            plt.legend()
            plt.minorticks_on()
            plt.grid(True)
#             ax.tick_params(axis='x',which='minor',bottom='off')
            # plt.title(Title)
            plt.show() 
    
    
    ###################################################################################################
    ### Extracts Data in the given time interval
    ###################################################################################################
    def Extract(self,Start_Time, End_Time,Reading_Rate=100000):

        # Reading_Rate = self.Number_of_Channels*100+5;
        
        UserStartIndex = int(Start_Time*(self.Sampling_Rate)); 
        UserEndIndex = int(End_Time*(self.Sampling_Rate))+1; 
        Sensor_Data = np.empty([0, self.Number_of_Channels])
        time = Start_Time; Time=[];
                
        # print(UserStartIndex)
        # print(UserEndIndex)
        
        with open(self.FileName,"rb") as f:

            ##################################################
            Sampling_Rate = 1;
            newLine = (f.readline()).strip();
            while (newLine.decode()!="[excelconfig]"):
                # print newLine.decode()
                newLine = (f.readline()).strip();
                if(newLine.decode()=="[sampling rate]"):
                    data = f.read(4);
                    Sampling_Rate = struct.unpack('>f',data[0: 4])[0];
                    newLine = (f.readline()).strip();
            ##################################################
            
            ##################################################
            ## Navigating the pointer to the location where 
            ## information is stored
            newLine = ((f.readline()).strip());
            while (newLine.decode()!="[data]"):
                newLine = (f.readline()).strip();
            ##################################################

            ##################################################
            ## Correct reading length based on number of channels 
            ##################################################
            Reading_Rate = int(Reading_Rate/self.Number_of_Channels)*self.Number_of_Channels;
            # print Reading_Rate
            #################################################

            #################################################
            ### Reading Data
            #################################################
            Num_Iterations = int (self.Data_Length/Reading_Rate)+1;
            # print Num_Iterations
            # print Num_Iterations
            # print Reading_Rate
            DataStartIndex = 0;
            DataEndIndex   = 0;
            for i in range(0,Num_Iterations):

                data = np.fromfile(f, dtype='>f',count=Reading_Rate);

                ######################################################################################
                correct_datalength = int(len(data)/self.Number_of_Channels)*self.Number_of_Channels;
                data = data[0:correct_datalength];
                Reading_Sampling_Rate = int(correct_datalength/self.Number_of_Channels);
                data = data.reshape(Reading_Sampling_Rate,self.Number_of_Channels);
                ######################################################################################

                # print Reading_Sampling_Rate
                
                DataStartIndex = DataEndIndex;                
                DataEndIndex = DataStartIndex + Reading_Sampling_Rate;
                # print ('DataEndIndex '+str(DataEndIndex));
                # print ('DataStartIndex '+str(DataStartIndex));
                # print ('UserStartIndex '+str(UserStartIndex));
                # print ('UserEndIndex '+str(UserEndIndex));
#                 print ('Reading_Sampling_Rate '+str(Reading_Sampling_Rate));

                if(DataStartIndex >=UserStartIndex and DataEndIndex< UserEndIndex):
                    Sensor_Data = np.append(Sensor_Data,(data[:,:]).copy());
                    dTime = np.linspace(time, time+(Reading_Sampling_Rate-1)*1.0/self.Sampling_Rate, num=Reading_Sampling_Rate);
                    Time = np.append(Time,dTime);
                    time = Time[-1]+1/self.Sampling_Rate;
                    # print ('Condition 1');
                    # print Sensor_Data.shape
                elif(DataStartIndex >=UserStartIndex and DataEndIndex>=UserEndIndex):
                    # print('Condition 2');
                    # print UserEndIndex
                    # print DataEndIndex
                    # print data
                    Sensor_Data = np.append(Sensor_Data,(data[: UserEndIndex-DataStartIndex,:]).copy());
#                     print(data[: UserEndIndex-DataEndIndex,:]);
                    dTime = np.linspace(time, time+(Reading_Sampling_Rate+(UserEndIndex-DataEndIndex)-1)*1.0/self.Sampling_Rate, num=Reading_Sampling_Rate+(UserEndIndex-DataEndIndex));
                    Time = np.append(Time,dTime);
                    time = Time[-1]+1/self.Sampling_Rate;
                    break ;
                elif(DataStartIndex < UserStartIndex and DataEndIndex< UserEndIndex):
                    # print ('Condition 3' + str (Reading_Sampling_Rate-(UserStartIndex-DataStartIndex)));
                    if(Reading_Sampling_Rate-(UserStartIndex-DataStartIndex)>=0):
                        Sensor_Data = np.append(Sensor_Data,(data[UserStartIndex-DataStartIndex:,:]).copy());
                        dTime = np.linspace(time, time+(Reading_Sampling_Rate-(UserStartIndex-DataStartIndex)-1)*1.0/self.Sampling_Rate, num=Reading_Sampling_Rate-(UserStartIndex-DataStartIndex));
                        Time = np.append(Time,dTime);
                        time = Time[-1]+1/self.Sampling_Rate;
                elif(DataStartIndex < UserStartIndex and DataEndIndex>=UserEndIndex):
                    # print ('Condition 4');
                    Sensor_Data = np.append(Sensor_Data,(data[UserStartIndex-DataStartIndex:UserEndIndex-DataEndIndex,:]).copy());
                    dTime = np.linspace(time, time+((UserEndIndex-UserStartIndex)-1)*1.0/self.Sampling_Rate, num=(UserEndIndex-UserStartIndex));
                    # print Reading_Sampling_Rate
                    # print UserStartIndex
                    # print UserEndIndex
                    # print DataStartIndex
                    # print DataEndIndex
                    # print dTime
                    Time = np.append(Time,dTime);
                    time = Time[-1]+1/self.Sampling_Rate;
                    break ;
                   
        Sensor_Data = Sensor_Data.reshape(int(len(Sensor_Data)/self.Number_of_Channels),self.Number_of_Channels); 
        Sensor_Data_dF         = pd.DataFrame(Sensor_Data)
        Sensor_Data_dF.columns = self.Channel_List

        
        if(self.Sampling_Rate!=1):
            Sensor_Data_dF['TIME'] = Time;
            Sensor_Data_dF = Sensor_Data_dF.reindex_axis(['TIME'] + list(Sensor_Data_dF.columns.drop(['TIME'])), axis=1)

        return Sensor_Data_dF


    def get_Channel_Index(self, Channel_Name):

        if Channel_Name in self.Channel_Dictionary.keys():
            return self.Channel_Dictionary[Channel_Name];
        else:
            print(Channel_Name + 'Does not exist');
            return -1;
