# Image Recognition for Synology

## To initialize the development environment

```$ photoface\Scripts\activate.bat```

## Make the training directory.

```$ mkdir .training```

## Create the training data
This creates labelled thumbnails in .training

```$ python createTrainingData.py <photo directory>```

## Build the face model
This creates two files
.training/trainer.yml - which contains the face model
.training/names - which contains the mapping from faceID to name

```$ python createFaceModel.py```

## Test the model
This extracts faces from unlabeled pictures and writes them to .testing
Images that are recognized are labelled. Unknown images are labelled as Unknown.

```
$ mkdir .testing
$ python extractAndLabelsFaces.py <photo directory>
```


