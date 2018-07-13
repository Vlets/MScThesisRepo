import matplotlib.pyplot as plt


def make_average_precision_graph():
    precisions = [0.37464788732394455, 0.2253521126760568, 0.16525821596244153, 0.1308098591549296, 0.10943661971830951,
                  0.09471830985915511, 0.08329979879275637, 0.07535211267605636, 0.06956181533646309,
                  0.06415492957746459, 0.060243277848911626, 0.05651408450704238, 0.05314192849404107,
                  0.05015090543259546]
    top_k = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
    plt.plot(top_k, precisions, 'bo-', label='With User Segments')
    plt.title('Average Users Item Interest Prediction')
    plt.xlabel('Top-K')
    plt.ylabel('Precision')
    plt.legend()
    plt.show()
