Phase 1:
1) Gather the model.py, train.py, cpu_inference.py and a test image files in a folder.
2) Create a python virtual environment so that when we download dependencies, we don't break the system.
3) Now install the requirement.txt file from prerequisite folder.
4) Now run the train.py, after successful run you will get the .pth file which is the weights.
5) Now you will be able to run the cpu_inference.py file. And get the baseline performance. (you can use it for your system / any cpu)

Phase 2:
1) Create a new folder for IP design and have all these files there.
2) run the 2 program program files export_image and export_weights programs in the vitis_hls_files folder. (should be done where your model exits and then copy to this folder).
3) add the lenet.cpp and the lenet.h files and tb_lenet.cpp. All other files image_data.h and parameters.h will generated through by the above two program.
4) Now open vitis 2024.1 and add all the necessary source files (lenet.cpp) and testbench file (tb_lenet.cpp). Select the top function in the source file. And select the part number of the board xc7z020clg400-1
5) run the simulation to check if everything works. then the synthesis then the implementation.  
6) above step will build the ip 

Vivado

7) open up a new project, select the board (dont go with the part number).
8) add our custom ip in the repo in the settings of vivado
9) create a block design with zynq7 ps and our custom ip (i have uploaded a photo for your reference of the block design).
10) run synthesis implementation and bitstream generation.

after that  
Go to your pynq's jupyter notebook create a folder and upload the .bit and .hwh files from the vivado design and also upload the .pth files and the run the final driver program.

Thatsss ittt :)
