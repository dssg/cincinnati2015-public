import pickle
import glob
from os import path
import dateutil.parser
from collections import namedtuple
import sys
from threading import Lock

from flask import abort


results_folder = "results"   # should be in config todo

cache = {}
cache_lock = Lock()


from webapp.evaluation import precision_at_x_percent
from webapp import config

def timestamp_from_path(pkl_path):
    prefix = path.join(results_folder, "modelresult_")
    ts = pkl_path.replace(prefix, "")
    ts = ts.replace(".pkl", "")
    return ts


Experiment = namedtuple("Experiment", ["timestamp", "config", "score", "data"])
def experiment_summary(pkl_file):
    data = read_pickle(pkl_file)
    model_config = data["config"]
    if "parameters" not in model_config:
        model_config["parameters"] = "?"

    if "residential_only" not in model_config:
        model_config["residential_only"] = False

    if "start_date" not in model_config:
        model_config["start_date"] = "01Jan1970"

    model_config["features"] = data["features"]
    model_config["feature_summary"] = feature_summary(data["features"])
    prec_at = precision_at_x_percent(data["test_labels"], data["test_predictions"],
                                     x_percent=config.precision_at_for_overview)
    return Experiment(dateutil.parser.parse(timestamp_from_path(pkl_file)),
                      model_config,
                      prec_at,
                      data)


def update_experiments_cache():
    experiments = glob.glob(results_folder)
    experiments = glob.glob(path.join(results_folder, "*.pkl"))
    with cache_lock:
        for pkl in experiments:
            ts = timestamp_from_path(pkl)
            if ts not in cache:
                cache[ts] = experiment_summary(pkl)
    # todo delete experiments that were remove from cache

def read_pickle(pkl_file):
    with open(pkl_file, "rb") as f:
        if sys.version_info < (3, 0):
            content = pickle.load(f)
        else:
            content = pickle.load(f, encoding='latin1')
    return content

def get_labels_predictions(timestamp):
    update_experiments_cache()
    # risk of dirty reads here because outside of lock
    if timestamp not in cache:
        abort(404)
    exp = cache[timestamp]
    return exp.data["test_labels"], exp.data["test_predictions"]


def get_feature_importances(timestamp):
    update_experiments_cache()
    # risk of dirty reads here because outside of lock
    if timestamp not in cache:
        abort(404)
    exp = cache[timestamp]
    return exp.data["features"], exp.data["feature_importances"]

def get_experiments_list():
    update_experiments_cache()
    # risk of dirty reads here because outside of lock
    experiments_copy = [Experiment(e.timestamp, e.config, e.score, None) for e in cache.values()]
    return experiments_copy

def feature_summary(features):
    return ",".join(features)

# will be run when webapp first starts
print ("Initializing experiments list")
update_experiments_cache()
print ("...finished")
