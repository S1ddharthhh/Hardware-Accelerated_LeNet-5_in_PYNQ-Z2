# Hardware-Accelerated_LeNet-5_in_PYNQ-Z2
Hi everyone !! Here i have modified the vanila LeNet-5 model slightly and trained with the german traffic sign benchmark dataset. So by analysing the computation heavy layers i have designed an IP using Vitis HLS 2024.1 and implemented it in the PYNQ Z2 Platform.

Hardware Used:
PYNQ Z2.

Software Used:
Pynqv3.1 (image file),
Vivado 2024.1,
Vitis 2024.1.

I was able to beat the raw processign which is the computational part when compared it to my laptop processor (Ultra 5 125H) but it comes to the overall end to end performance the python over-head takes much longer in the dual-core arm processor which slows up the entire process. This project clealy shows the raw performance potential of FPGA in parallel processing with much less power draw.

                 /\____/\
                > •   • <
