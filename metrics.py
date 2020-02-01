from sklearn import metrics
from sklearn.preprocessing import label_binarize

def average_precision_multiclass(y_true, y_pred_proba):
    y_true_bin = label_binarize(y_true,
        classes=list(range(y_pred_proba.shape[1]))).ravel()
    return metrics.average_precision_score(y_true_bin, y_pred_proba.ravel())