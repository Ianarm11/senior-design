# User Documentation

## Overview
Our example covert channels are made for learning purposes. To maximize knowledge learnt, the programs should be ran while also studying the code. The code is heavily commented and written with readability in mind, not performance. The programs will output statements via the command line to let the user know the current state. No user input is required.

### Network Channel

#### System Requirements
A user must be able to run a version of Python3 and be able to run with root privileges.

#### How To Run The Code
You will need two windows of your favorite command prompt open (Terminal, CMD, etc). The next directions should be followed for both windows.

 Navigate to the directory to where you have downloaded the repository. The Network Channel code lives in the library/network-channel/build/ directory. The program titled 'network-channel.py' is the driver of the program. We will run this program in each window, but with a different argument for the sender and receiver.

 In one window, we will run the receiver program. Type the following command and hit Enter.

 *sudo python3 network-channel.py --reciever*

 In the other window, we will run the sender program. Type the following command and hit Enter.

 *sudo python3 network-channel.py --sender*

 Running the above commands should prompt the user for their password because we are running it with root privileges. In the programs we are using raw sockets, which require root.

 Each program ran should output text updates on the current state of the program. The user should follow this closely to make sure of great success.

### Operating System Channel
This channel is not made for a user to run, but rather study. The Meltdown exploit is large and complex. The way it uses a side channel attack is what we are focused on. The code is well commented with explanations, along with a brief overview of what Meltdown is as a whole.

### Printer Channel

#### System Requirements
A user must be running a version of Windows as their operating system. A user must be able to run a Python 3.
A user must be able to connect to a printer via network. A user must also install the python libraries win32api and win32printing, this can be done using pip install.

example: 'pip install win32api', 'pip install win32printing'

#### How To Run The Code
You will need two windows of your favorite command prompt open (Terminal, CMD, etc). The next directions should be followed for both windows.

 Navigate to the directory to where you have downloaded the repository. The Printer Channel code lives in the library/printer-channel/build/ directory. The program titled 'printer-channel.py' is the driver of the program. We will run this program in each window, but with a different argument for the sender and receiver.

 In one window, we will run the receiver program. Type the following command and hit Enter.

 *python3 printer-channel.py --reciever*

 In the other window, we will run the sender program. Type the following command and hit Enter.

 *python3 printer-channel.py --sender*

 Each program ran should output text updates on the current state of the program. The user should follow this closely to make sure of great success.

## FAQ
* Where can I download the code?
<a href="https://github.com/Ianarm11/senior-design">Our GitHub repository here</a>
* Will the covert channels do anything evil to my computer?
No! The code in our repository is written to use resources that have no affect on your computer. In the code, we will show how to change the inputs if you are concerned.
* How can I use this for my own personal use?
In the code, you will notice what can be changed to have a more practical use. Make sure to study and read the comments!
