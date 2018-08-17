import matplotlib.pyplot as plt
import numpy as np


def make_precision_graph_bloomreach_items():
    top_k = np.array([3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])
    precision_usg_loc = np.array([0.521, 0.349, 0.211, 0.159, 0.12, 0.103, 0.087, 0.078, 0.069, 0.066, 0.058, 0.054,
                                  0.05, 0.047, 0.046])
    errors_usg_loc = np.array([0.036, 0.032, 0.021, 0.018, 0.013, 0.012, 0.01, 0.009, 0.008, 0.008, 0.007, 0.007,
                               0.006, 0.006, 0.006])
    precision_loc = np.array([0.468, 0.333, 0.206, 0.153, 0.119, 0.101, 0.086, 0.075, 0.069, 0.063, 0.06, 0.054, 0.05,
                              0.048, 0.044])
    errors_loc = np.array([0.035, 0.031, 0.023, 0.018, 0.014, 0.012, 0.01, 0.009, 0.009, 0.008, 0.008, 0.007, 0.007,
                           0.006, 0.005])
    precision_baseline = np.array([0.23, 0.133, 0.082, 0.057, 0.048, 0.043, 0.039, 0.011, 0.028, 0.025, 0.025, 0.024,
                                   0.021, 0.021, 0.018])
    errors_baseline = np.array([0.034, 0.024, 0.014, 0.011, 0.009, 0.008, 0.007, 0.004, 0.005, 0.004, 0.005, 0.004,
                                0.004, 0.004, 0.003])
    plt.errorbar(top_k, precision_usg_loc, errors_usg_loc, linestyle='--', marker='s', label='With User Segments',
                 capsize=5, capthick=1.5)
    plt.errorbar(top_k, precision_loc, errors_loc, linestyle='--', marker='o', label='Without User Segments',
                 capsize=5, capthick=1.5, color='r')
    plt.errorbar(top_k, precision_baseline, errors_baseline, linestyle='--', marker='^', label='Random Baseline',
                 capsize=5, capthick=1.5, color='g')
    plt.title('Users Item Interest Prediction - Bloomreach Data Set')
    plt.xlabel('Top-K Items')
    plt.ylabel('Precision')
    plt.legend()
    plt.show()


def make_precision_graph_hellermanntyton_items():
    top_k = np.array([3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])
    precision_usg_loc = np.array([0.161, 0.133, 0.088, 0.076, 0.073, 0.065, 0.059, 0.05, 0.048, 0.043, 0.041, 0.033,
                                  0.034, 0.034, 0.029])
    errors_usg_loc = np.array([0.026, 0.02, 0.012, 0.012, 0.012, 0.012, 0.011, 0.009, 0.01, 0.009, 0.009, 0.007, 0.008,
                                   0.007, 0.007])
    precision_loc = np.array([0.151, 0.119, 0.081, 0.065, 0.063, 0.058, 0.048, 0.046, 0.041, 0.039, 0.034, 0.033, 0.028,
                              0.028, 0.026])
    errors_loc = np.array([0.027, 0.019, 0.013, 0.01, 0.014, 0.011, 0.009, 0.009, 0.008, 0.009, 0.008, 0.008, 0.006,
                           0.007, 0.006])
    precision_baseline = np.array([0.105, 0.09, 0.062, 0.05, 0.05, 0.037, 0.04, 0.033, 0.031, 0.026, 0.025, 0.021,
                                   0.021, 0.017, 0.018])
    errors_baseline = np.array([0.022, 0.018, 0.013, 0.012, 0.013, 0.009, 0.011, 0.01, 0.008, 0.008, 0.007, 0.006,
                                0.006, 0.006, 0.006])
    plt.errorbar(top_k, precision_usg_loc, errors_usg_loc, linestyle='--', marker='s', label='With User Segments',
                 capsize=5, capthick=1.5)
    plt.errorbar(top_k, precision_loc, errors_loc, linestyle='--', marker='o', label='Without User Segments',
                 capsize=5, capthick=1.5, color='r')
    plt.errorbar(top_k, precision_baseline, errors_baseline, linestyle='--', marker='^', label='Random Baseline',
                 capsize=5, capthick=1.5, color='g')
    plt.title('Users Item Interest Prediction - HellermannTyton Data Set')
    plt.xlabel('Top-K Items')
    plt.ylabel('Precision')
    plt.legend()
    plt.show()


def make_precision_graph_bloomreach_keywords():
    fig, ax = plt.subplots(nrows=1, sharex=True)
    mean_usg_loc = 0.074
    mean_loc = 0.065
    stdev_usg_loc = 0.006
    stdev_loc = 0.006
    ax.errorbar(mean_usg_loc, np.array([1]), xerr=stdev_usg_loc, fmt='--s', capsize=5, capthick=1.5)
    ax.errorbar(mean_loc, np.array([2]), xerr=stdev_loc, fmt='--o', color='r', capsize=5, capthick=1.5)
    ax.set_title('Bloomreach Dataset Keywords Prediction Precision')
    ax.set_yticks([1, 2])
    ax.set_yticklabels(['With User Segments', 'Without User Segments'])
    ax.margins(y=3)
    ax.set_ylabel('Input Data')
    ax.set_xlabel('Precision')
    plt.show()


def make_precision_graph_hellermanntyton_keywords():
    fig, ax = plt.subplots(nrows=1, sharex=True)
    mean_usg_usc_loc = 0.014
    mean_loc = 0.003
    stdev_usg_usc_loc = 0.013
    stdev_loc = 0.004
    ax.errorbar(mean_usg_usc_loc, np.array([1]), xerr=stdev_usg_usc_loc, fmt='--s', capsize=5, capthick=1.5)
    ax.errorbar(mean_loc, np.array([2]), xerr=stdev_loc, fmt='--o', color='r', capsize=5, capthick=1.5)
    ax.set_title('HellermannTyton Dataset Keywords Prediction Precision')
    ax.set_yticks([1, 2])
    ax.set_yticklabels(['USg\n + Loc', 'Loc'])
    ax.margins(y=3)
    ax.set_ylabel('Input Data')
    ax.set_xlabel('Precision')
    plt.show()


def make_accuracy_graph_bloomreach_keywords():
    fig, ax = plt.subplots(nrows=1, sharex=True)
    mean_usg_loc = 0.925
    mean_loc = 0.923
    stdev_usg_loc = 0.003
    stdev_loc = 0.003
    ax.errorbar(mean_usg_loc, np.array([1]), xerr=stdev_usg_loc, fmt='--s', capsize=5, capthick=1.5)
    ax.errorbar(mean_loc, np.array([2]), xerr=stdev_loc, fmt='--o', color='r', capsize=5, capthick=1.5)
    ax.set_title('Bloomreach Dataset Keywords Prediction Accuracy')
    ax.set_yticks([1, 2])
    ax.set_yticklabels(['USg\n + Loc', 'Loc'])
    ax.margins(y=3)
    ax.set_ylabel('Input Data')
    ax.set_xlabel('Precision')
    plt.show()


def make_accuracy_graph_hellermanntyton_keywords():
    fig, ax = plt.subplots(nrows=1, sharex=True)
    mean_usg_usc_loc = 0.852
    mean_loc = 0.851
    stdev_usg_usc_loc = 0.003
    stdev_loc = 0.002
    ax.errorbar(mean_usg_usc_loc, np.array([1]), xerr=stdev_usg_usc_loc, fmt='--s', capsize=5, capthick=1.5)
    ax.errorbar(mean_loc, np.array([2]), xerr=stdev_loc, fmt='--o', color='r', capsize=5, capthick=1.5)
    ax.set_title('HellermannTyton Dataset Keywords Prediction Accuracy')
    ax.set_yticks([1, 2])
    ax.set_yticklabels(['USg\n + Loc', 'Loc'])
    ax.margins(y=3)
    ax.set_ylabel('Input Data')
    ax.set_xlabel('Precision')
    plt.show()

