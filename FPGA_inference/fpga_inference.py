import numpy as np
import time
import struct
from pynq import Overlay
from PIL import Image

# --- CONFIGURATION ---
BITSTREAM    = "lenet.bit"
IMAGE_FILE   = "test_image.jpg"  # <--- Change this to your image filename

# GTSRB Class Labels
CLASSES = {
    0: 'Speed limit (20km/h)', 1: 'Speed limit (30km/h)', 2: 'Speed limit (50km/h)',
    3: 'Speed limit (60km/h)', 4: 'Speed limit (70km/h)', 5: 'Speed limit (80km/h)',
    6: 'End of speed limit (80km/h)', 7: 'Speed limit (100km/h)', 8: 'Speed limit (120km/h)',
    9: 'No passing', 10: 'No passing for vehicles over 3.5 metric tons',
    11: 'Right-of-way at the next intersection', 12: 'Priority road', 13: 'Yield',
    14: 'Stop', 15: 'No vehicles', 16: 'Vehicles over 3.5 metric tons prohibited',
    17: 'No entry', 18: 'General caution', 19: 'Dangerous curve to the left',
    20: 'Dangerous curve to the right', 21: 'Double curve', 22: 'Bumpy road',
    23: 'Slippery road', 24: 'Road narrows on the right', 25: 'Road work',
    26: 'Traffic signals', 27: 'Pedestrians', 28: 'Children crossing',
    29: 'Bicycles crossing', 30: 'Beware of ice/snow', 31: 'Wild animals crossing',
    32: 'End of all speed and passing limits', 33: 'Turn right ahead', 34: 'Turn left ahead',
    35: 'Ahead only', 36: 'Go straight or right', 37: 'Go straight or left',
    38: 'Keep right', 39: 'Keep left', 40: 'Roundabout mandatory',
    41: 'End of no passing', 42: 'End of no passing by vehicles over 3.5 metric tons'
}

# --- 1. PREPARE DATA ---
# Load image, resize, normalize, and flatten for the FPGA
try:
    img = Image.open(IMAGE_FILE).convert('L').resize((32, 32))
    img_arr = np.array(img, dtype=np.float32)
    img_arr = (img_arr - 127.5) / 127.5 # Normalize [-1, 1]
    
    # Flat Array for Hardware (1024 floats)
    hw_input = img_arr.flatten()
    
    print(f"Loaded {IMAGE_FILE} successfully.")
except Exception as e:
    print(f"Error: {e}")
    raise

# --- 2. LOAD FPGA OVERLAY ---
print("Loading Bitstream...")
ol = Overlay(BITSTREAM)
lenet_ip = ol.lenet_predict_0
input_mem = ol.axi_bram_ctrl_0

# --- 3. RUN HARDWARE INFERENCE ---
print("\n" + "="*50)
print(f" RUNNING FPGA INFERENCE ON {IMAGE_FILE}")
print("="*50)

# Step A: Write Data to Shared Memory (BRAM)
# This is I/O, so we usually don't count it in the pure "Compute Time"
# but it is necessary for the system to work.
print("Writing data to FPGA memory...")
for i, val in enumerate(hw_input):
    # Pack float to bits and write to BRAM
    input_mem.write(i * 4, struct.unpack('<I', struct.pack('<f', val))[0])

# Step B: Run the IP
print("Starting IP Core...")
CONTROL_ADDR = 0x00
START = 0x01
DONE  = 0x02
RETURN_ADDR  = 0x10

start_hw = time.time()

# 1. Start the accelerator
lenet_ip.write(CONTROL_ADDR, START)

# 2. Wait for it to finish (Polling)
while (lenet_ip.read(CONTROL_ADDR) & DONE) == 0:
    pass

end_hw = time.time()

# 3. Read the result
hw_pred = lenet_ip.read(RETURN_ADDR)
hw_time_ms = (end_hw - start_hw) * 1000
fps = 1000.0 / hw_time_ms

# --- 4. RESULTS ---
print("\n" + "="*50)
print(f" FPGA RESULTS")
print("="*50)
print(f"Prediction Code : {hw_pred}")
print(f"Sign Label      : {CLASSES.get(hw_pred, 'Unknown')}")
print("-" * 50)
print(f"Execution Time  : {hw_time_ms:.4f} ms")
print(f"Throughput      : {fps:.2f} FPS")
print("="*50)