# CNN

## Neural Nets Barcode Project
Files:
* data for **training** and **validation**.
* Network **models**.
* **Weights**.
* Easy classificator, builded from **Keras** tutorial.
* Script of **preprocessing** loaded images.
* Script of **sliding window**.
* Main **uniting script** for sliding and preprocessing. It makes predictions.

The main thing, on what depends **accuracy of recognition**, 
is size of target that we want to detect.
For now this is 150,150 pixels. 
Results are not so bad, but many barcodes have been lost.
    **Conclusion**: 
        Result depends on a choosen width and height of target.
        Amount of images in dataset, their shape, sliding window frame, all reshapes inside the methods, ...
        all affects the accuracy.
