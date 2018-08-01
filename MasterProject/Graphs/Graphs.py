import matplotlib.pyplot as plt
import numpy as np


def make_average_precision_graph_bloomreach():
    precisions_usg_usc_loc = [0.37464788732394455, 0.2253521126760568, 0.16525821596244153, 0.1308098591549296,
                              0.10943661971830951, 0.09471830985915511, 0.08329979879275637, 0.07535211267605636,
                              0.06956181533646309, 0.06415492957746459, 0.060243277848911626, 0.05651408450704238,
                              0.05314192849404107, 0.05015090543259546]
    precisions_loc = [0.39577464788732486, 0.24859154929577482, 0.18380281690140876, 0.14507042253521124,
                      0.12126760563380239, 0.10422535211267628, 0.09235412474849072, 0.08283450704225347,
                      0.07511737089201863, 0.0694366197183096, 0.0647247119078105, 0.060739436619718444,
                      0.05758396533044409, 0.054577464788732266]
    precisions_usg_usc = [0.3746478873239445, 0.23309859154929605, 0.16666666666666693, 0.1309859154929577,
                          0.109577464788732, 0.09401408450704246, 0.08319919517102597, 0.07455985915492955,
                          0.0673708920187792, 0.06232394366197163, 0.05813060179257362, 0.05451877934272314,
                          0.05130010834236176, 0.04859154929577454]
    precisions_usg_loc = [0.37183098591549385, 0.22746478873239484, 0.1643192488262913, 0.1294014084507043,
                          0.10830985915492919, 0.09354460093896731, 0.08229376257545253, 0.07394366197183098,
                          0.0675273865414709, 0.06302816901408428, 0.05845070422535213, 0.05469483568075131,
                          0.051570964247020484, 0.04859154929577455]
    precisions_usg = [0.37746478873239525, 0.23345070422535236, 0.16713615023474201, 0.13186619718309855,
                      0.10971830985915453, 0.09460093896713635, 0.08329979879275635, 0.07455985915492955,
                      0.0673708920187792, 0.06246478873239416, 0.05819462227912931, 0.054636150234741915,
                      0.051625135427952225, 0.04864185110663973]
    top_k = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
    plt.plot(top_k, precisions_usg_usc_loc, 'bo--', label='USg + USc + Loc')
    plt.plot(top_k, precisions_usg_loc, 'cs--', label='USg + Loc')
    plt.plot(top_k, precisions_usg_usc, 'rx--', label='USg + USc')
    plt.plot(top_k, precisions_loc, 'g^--', label='Loc')
    plt.plot(top_k, precisions_usg, 'mp--', label='USg')
    plt.title('Average Users Item Interest Prediction - Bloomreach Data Set')
    plt.xlabel('Top-K')
    plt.ylabel('Precision')
    plt.legend()
    plt.show()


def make_average_precision_graph_hellermanntyton():
    precisions_usg_usc_loc = [0.15833333333333327, 0.09999999999999994, 0.07962962962962965, 0.07291666666666664,
                              0.06333333333333335, 0.0574074074074074, 0.05119047619047616, 0.04826388888888886,
                              0.04660493827160492, 0.044166666666666674, 0.040656565656565634, 0.03680555555555554,
                              0.0346153846153846, 0.03214285714285712]
    precisions_loc = [0.17222222222222214, 0.1194444444444444, 0.09629629629629628, 0.08888888888888885,
                      0.0766666666666667, 0.06805555555555556, 0.06150793650793646, 0.05590277777777776,
                      0.054320987654320974, 0.0513888888888889, 0.046717171717171685, 0.04328703703703703,
                      0.03995726495726494, 0.037103174603174575]
    top_k = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
    plt.plot(top_k, precisions_usg_usc_loc, 'bo--', label='USg + USc + Loc')
    plt.plot(top_k, precisions_loc, 'g^--', label='Loc')
    plt.title('Average Users Item Interest Prediction - HellermannTyton Data Set')
    plt.xlabel('Top-K')
    plt.ylabel('Precision')
    plt.legend()
    plt.show()


def make_precision_graph_bloomreach_items():
    top_k = np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])
    precision_usg_loc = np.array([0.379, 0.24, 0.173, 0.137, 0.116, 0.101, 0.087, 0.078, 0.072, 0.066, 0.061, 0.058,
                                      0.056, 0.052])
    errors_usg_loc = np.array([0.031, 0.024, 0.019, 0.015, 0.013, 0.012, 0.01, 0.009, 0.009, 0.008, 0.007, 0.007,
                                   0.007, 0.007])
    precision_loc = np.array([0.383, 0.246, 0.179, 0.139, 0.119, 0.102, 0.093, 0.082, 0.073, 0.068, 0.064, 0.06, 0.057,
                              0.054])
    errors_loc = np.array([0.032, 0.024, 0.02, 0.015, 0.013, 0.012, 0.011, 0.01, 0.008, 0.008, 0.008, 0.007, 0.007,
                           0.007])
    plt.errorbar(top_k, precision_usg_loc, errors_usg_loc, linestyle='--', marker='s', label='USg + Loc',
                 capsize=5, capthick=1.5)
    plt.errorbar(top_k, precision_loc, errors_loc, linestyle='--', marker='o', label='Loc',
                 capsize=5, capthick=1.5, color='r')
    plt.title('Users Item Interest Prediction - Bloomreach Data Set')
    plt.xlabel('Top-K')
    plt.ylabel('Precision')
    plt.legend()
    plt.show()


def make_precision_graph_hellermanntyton_items():
    top_k = np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])
    precision_usg_loc = np.array([0.172, 0.119, 0.086, 0.091, 0.076, 0.057, 0.055, 0.052, 0.047, 0.048, 0.045, 0.04,
                                      0.038, 0.036])
    errors_usg_loc = np.array([0.043, 0.037, 0.029, 0.032, 0.025, 0.02, 0.018, 0.021, 0.021, 0.023, 0.02, 0.019,
                                   0.017, 0.016])
    precision_loc = np.array([0.181, 0.117, 0.097, 0.088, 0.076, 0.068, 0.061, 0.057, 0.054, 0.052, 0.044, 0.043, 0.04,
                              0.037])
    errors_loc = np.array([0.045, 0.028, 0.029, 0.029, 0.025, 0.023, 0.022, 0.021, 0.022, 0.022, 0.018, 0.019, 0.017,
                           0.016])
    plt.errorbar(top_k, precision_usg_loc, errors_usg_loc, linestyle='--', marker='s', label='USg + Loc',
                 capsize=5, capthick=1.5)
    plt.errorbar(top_k, precision_loc, errors_loc, linestyle='--', marker='o', label='Loc',
                 capsize=5, capthick=1.5, color='r')
    plt.title('Users Item Interest Prediction - HellermannTyton Data Set')
    plt.xlabel('Top-K')
    plt.ylabel('Precision')
    plt.legend()
    plt.show()


def make_precision_graph_bloomreach_keywords():
    fig, ax = plt.subplots(nrows=1, sharex=True)
    mean_usg_loc = 0.037
    mean_loc = 0.034
    stdev_usg_loc = 0.004
    stdev_loc = 0.004
    ax.errorbar(mean_usg_loc, np.array([1]), xerr=stdev_usg_loc, fmt='--s', capsize=5, capthick=1.5)
    ax.errorbar(mean_loc, np.array([2]), xerr=stdev_loc, fmt='--o', color='r', capsize=5, capthick=1.5)
    ax.set_title('Bloomreach Dataset Keywords Prediction Precision')
    ax.set_yticks([1, 2])
    ax.set_yticklabels(['USg\n + Loc', 'Loc'])
    ax.margins(y=3)
    ax.set_ylabel('Input Data')
    ax.set_xlabel('Precision')
    plt.show()


def make_precision_graph_hellermanntyton_keywords():
    fig, ax = plt.subplots(nrows=1, sharex=True)
    mean_usg_usc_loc = 0.011
    mean_loc = 0.01
    stdev_usg_usc_loc = 0.007
    stdev_loc = 0.006
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
    mean_usg_loc = 0.706
    mean_loc = 0.531
    stdev_usg_loc = 0.01
    stdev_loc = 0.015
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
    mean_usg_usc_loc = 0.471
    mean_loc = 0.042
    stdev_usg_usc_loc = 0.223
    stdev_loc = 0.037
    ax.errorbar(mean_usg_usc_loc, np.array([1]), xerr=stdev_usg_usc_loc, fmt='--s', capsize=5, capthick=1.5)
    ax.errorbar(mean_loc, np.array([2]), xerr=stdev_loc, fmt='--o', color='r', capsize=5, capthick=1.5)
    ax.set_title('HellermannTyton Dataset Keywords Prediction Accuracy')
    ax.set_yticks([1, 2])
    ax.set_yticklabels(['USg\n + Loc', 'Loc'])
    ax.margins(y=3)
    ax.set_ylabel('Input Data')
    ax.set_xlabel('Precision')
    plt.show()

