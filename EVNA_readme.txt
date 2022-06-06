Keysight VNA data acquisition:

As you doubleclick the script and enter the shell window, the program will start to initialize the device with a default setting of s11 trace, 1001 points and 3MHz to 50MHz
Then the system will ask you for a command with some help info:
h -- help info, explanation of commands
f -- set the file name
clr -- clear the assigned file
s lo/s hi -- set low or high frequency sweep
w -- write trace points to csv file for 600 frames
w NumberOfFrames -- write trace points to csv file in certain number of frames
sync -- syncwrite() with the camera for 600 frames
sync NumberOfFrames -- syncwrite with camera for certain number of frames
q -- quit the script and close connections
enter command: 

The first command you need to enter is f for filename
after you set a global file name, you can start to get s11 data and write it to the designated file.

The writetrace command takes a frame number from 0 to 600, the default is 600 when you type command 'w'
If you want just 10 frames, you could try 'w 10'
The syncwrite works the same way as the writetrace while it needs Synapse open

the 's lo' or 's hi' is aimed for switching swept frequency 's lo' stands for 300kHz to 500MHz and 's hi' stnads for 500MHz to 1.5GHz

the clr command will clear the content of current file

If you want to change the workspace to the next file, type 'f' again in command to create another one

When you finish all the data acquisition, just type in q to quit the script and close connections

Feel free to email me for any problems on the program:
tzhu59@wisc.edu
wolfarm@163.com on Skype

Hai Lab
Aviad Hai
Department of Biomedical Engineering
& Grainger Institute for Engineering
University of Wisconsin-Madison