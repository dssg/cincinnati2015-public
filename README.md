# Blight Risk Prediction

This readme describes how to run experiments for models. 

Download the code to a directory, edit `default.yaml` as necessary and then do the following at your Python interpreter:


```
from blight_risk_prediction import model
model.main()
```

Look at the IPython notebook in this directory to see example output. 

## Automatic output

Each model run produces a pickle file which contains:

* the full list of parcels predicted to have violations
* the configuration file used to generate that model
* standard evaluation metrics, e.g. precision, recall, F1 score

In addition to the pickle file, a plot of the confusion matrix is generated and saved as a PNG file. 

These output files include a timestamp in their filename such that they will not be accidentally overwritten. 

## Featurebot

To generate a new table of features, e.g. for a new  testing inspection date, run `featurebot.main()`. 

## Writing a new feature

Add features in `featurebot.py`:

*  Define a new feature to generate in `featurebot.features_to_generate()`. This function will generate a new table in the database by pairs of inspection and date, for a list of parcels.
*  Add feature generation code in a seperete file `<feature_name>.py`
*  Add feature to list of features to load when creating training and testing in `dataset.feature_loaders()` --> list all columns in feature table!
*  Add a function to load feature in class `FeatureLoader().def load_<feature_name>_feature()`
*  Add a string corresponding to the feature in the default YAML configuration file: list all column names!
*  Start `featurebot` to populate the database with features.
