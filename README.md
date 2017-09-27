# Testing out Neural Encryption

I trained the network to swap the least significant bit and most significant bit. It is a pixel by pixel approach, so there will be a problem for images with a lot of solid colors. It will be visible and will outline the detail of the image as shown in the image below. The other problem is that neural network approach is very slow for any encryption process.

![Encrypted Image](https://user-images.githubusercontent.com/11855694/30923457-73d72c4a-a3de-11e7-943f-e91c7236bafa.png)

![Source Image](https://user-images.githubusercontent.com/11855694/30923510-9fda4a3e-a3de-11e7-8ecf-4a654cb83d08.jpg)


#### With Diffusion
So, I added the Fisher-Yates shuffling algorithm to diffuse the image.
![With Fisher-Yates algorithm](https://user-images.githubusercontent.com/11855694/30923669-17f330f8-a3df-11e7-9a69-b6d034f2bf58.png)

#### Dependencies
* Python 3.5
* Flask 0.12.2
* OpenCV 3.2
* TensorFlow 1.0.1
