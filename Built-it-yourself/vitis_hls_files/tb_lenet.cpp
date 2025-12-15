#include <iostream>
#include "lenet.h"
#include "image_data.h" // The image you just exported

int main() {
    int prediction = -1;
    
    // We need a non-const buffer to pass to the function
    float input_buf[1][32][32];
    
    // Copy data
    for(int h=0; h<32; h++)
        for(int w=0; w<32; w++)
            input_buf[0][h][w] = test_image[0][h][w];

    std::cout << "Starting LeNet-5 C-Simulation..." << std::endl;
    
    // Run the model
    lenet_predict(input_buf, &prediction);
    
    std::cout << "Prediction: " << prediction << std::endl;
    
    // Check (Adjust this ID if your bicycle sign was Class 29)
    if (prediction == 29) { 
        std::cout << "Test PASSED!" << std::endl;
        return 0;
    } else {
        std::cout << "Test FAILED!" << std::endl;
        return 1;
    }
}