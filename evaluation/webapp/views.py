from io import BytesIO
from itertools import groupby
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import make_response, render_template, abort


from webapp import app
from webapp.evaluation import *
from webapp.ioutils import *
from webapp import config


@app.route('/')
def index():
    experiments = get_experiments_list()

    # group by date, newest first
    experiments = sorted(experiments, key=lambda r: r.timestamp.date(), reverse=True)
    experiments = [(date, list(items)) for date, items in groupby(experiments, lambda r: r.timestamp.date())]

    # for each date sort its results, best first
    experiments = [(date, sorted(items, key=lambda r: r.score, reverse=True))
                    for date, items in experiments]

    return render_template('overview.html', experiments=experiments, score_name=config.score_name)


@app.route('/<timestamp>')
def details(timestamp):
    # will fail with 404 if exp not known
    get_labels_predictions(timestamp)
    return render_template('details.html', timestamp=timestamp)


@app.route("/<timestamp>/norm_confusions")
def normalized_confusion_matrix(timestamp):
    test_labels, test_predictions = get_labels_predictions(timestamp)
    matrix_fig = plot_normalized_confusion_matrix(test_labels, test_predictions)
    return serve_matplotlib_fig(matrix_fig)

@app.route("/<timestamp>/importances")
def feature_importances(timestamp):
    features, importances = get_feature_importances(timestamp)
    importance_fig = plot_feature_importances(features, importances)

    return serve_matplotlib_fig(importance_fig)


@app.route("/<timestamp>/precision-recall")
def precision_recall(timestamp):
    test_labels, test_predictions = get_labels_predictions(timestamp)
    prec_recall_fig = plot_precision_recall_n(test_labels, test_predictions)

    return serve_matplotlib_fig(prec_recall_fig)

@app.route("/<timestamp>/precision-cutoff")
def precision_cutoff(timestamp):
    test_labels, test_predictions = get_labels_predictions(timestamp)
    prec_cutoff_fig = plot_precision_cutoff(test_labels, test_predictions)
    return serve_matplotlib_fig(prec_cutoff_fig)

@app.route("/<timestamp>/ROC")
def ROC(timestamp):
    test_labels, test_predictions = get_labels_predictions(timestamp)
    roc_fig = plot_ROC(test_labels, test_predictions)
    return serve_matplotlib_fig(roc_fig)

@app.route("/growth")
def growth():
    experiments = get_experiments_list()

    # group by date, newest first
    experiments = sorted(experiments, key=lambda r: r.timestamp.date(), reverse=True)
    experiments = [(date, list(items)) for date, items in groupby(experiments, lambda r: r.timestamp.date())]

    # only keep best result for each day
    experiments = [(date, sorted(items, key=lambda r: r.score, reverse=True)[0])
                    for date, items in experiments]
    experiments = [(date, best.score) for date, best in experiments]

    growth_fig = plot_growth(experiments)
    return serve_matplotlib_fig(growth_fig)


def serve_matplotlib_fig(fig):
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response
