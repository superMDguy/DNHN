# Notes on Deep Neural Hofstadter Networks

## Guiding Principles
* Everything must be simple and generalized.  We're solving the problem of general intelligence here, so something that works well in one specific domain isn't necessarily good enough.
* Everything can be related.  No matter what an item is (image, text, sound, etc.), it must have a relation mapping to other formats within the LTM.  This is accomplished by modeling the LTM as a vector space, and using formulas to make sure everything can relate to both things of its type, and those of other types.

## How to Represent Various types

### Numbers
In a DNHN, numbers aren't just their magnitude.  Instead, a few 'special' sequences (e.g. primes, squares) are fed into a word2vec model to create vectors of each number.  Thus, the numbers are represented subjectively as **concepts** in the brain, and not merely as a magnitude.

### Words
This is pretty much just word2vec.

### Images
Images are put through the first few layers of a VGG16 network pretrained on the ImageNet database. (Very Deep Convolutional Networks for Large-Scale Image Recognition, K. Simonyan, A. Zisserman, arXiv:1409.1556)  This is done to extract basic features, like lines, curves, and simple shapes.  Then, these features are transformed into vectors by mapping them to either words, audio, or another existing vector space.  This mapping is performed by a simple linear model that tries to optimize to make the sum of the vectors of the input are as close as possible to the vector of the image.  For example, if there is a picture of a red circle described by the phrase "this is a red circle", the model will try to make its output as close as possible to vector(this) + vector(is) + vector(a) + vector(red) + vector(circle).  I'm thinking about applying exp() to each vector, to make the more important elements (like 'red') stand out more than less important elements (what traditional NLP would call stop words).

### Audio Data
Haven't finalized this yet, but probably a fourier transform followed by something similar to word2vec.