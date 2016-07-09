import numpy as np
import datautils


def L_i(x, y, W):
  """
  unvectorized version. Compute the multiclass svm loss for a single example (x,y)
  - x is a column vector representing an image (e.g. 3073 x 1 in CIFAR-10)
    with an appended bias dimension in the 3073-rd position (i.e. bias trick)
  - y is an integer giving index of correct class (e.g. between 0 and 9 in CIFAR-10)
  - W is the weight matrix (e.g. 10 x 3073 in CIFAR-10)
  """
  delta = 1.0 # see notes about delta later in this section
  scores = W.dot(x) # scores becomes of size 10 x 1, the scores for each class
  correct_class_score = scores[y]
  D = W.shape[0] # number of classes, e.g. 10
  loss_i = 0.0
  for j in xrange(D): # iterate over all wrong classes
    if j == y:
      # skip for the true class to only loop over incorrect classes
      continue
    # accumulate loss for the i-th example
    loss_i += max(0, scores[j] - correct_class_score + delta)
  return loss_i


def L_i_vectorized(x, y, W):
  """
  A faster half-vectorized implementation. half-vectorized
  refers to the fact that for a single example the implementation contains
  no for loops, but there is still one loop over the examples (outside this function)
  """
  delta = 1.0
  scores = W.dot(x)
  # compute the margins for all classes in one vector operation
  margins = np.maximum(0, scores - scores[y] + delta)
  # on y-th position scores[y] - scores[y] canceled and gave delta. We want
  # to ignore the y-th position and only consider margin on max wrong class
  margins[y] = 0
  loss_i = np.sum(margins)
  return loss_i


def L(X, y, W, lam=0.1):
  """
  fully-vectorized implementation :
  - X holds all the training examples as columns (e.g. 3073 x 50,000 in CIFAR-10)
  - y is array of integers specifying correct class (e.g. 50,000-D array)
  - W are weights (e.g. 10 x 3073)
  """
  # evaluate loss over all examples in X without using any for loops
  # left as exercise to reader in the assignment
  delta = 1.0
  # W = np.zeros([category, X.shape[1]])

  scores = X.dot(W.T)
  # print scores
  ind = range(scores.shape[0])
  y_list = y.tolist()
  yi = scores[ind, y_list]
  yi = yi[:, np.newaxis]
  margin = np.maximum(0, scores - yi + delta)
  loss_i = np.sum(margin, axis=1)
  total_loss = np.sum(loss_i) + lam*regulariztion(W)
  return total_loss


def regulariztion(W):
  regular = W**2
  result = np.sum(regular, axis=0)
  result = np.sum(result, axis=0)
  return result


Xtr, Ytr, Xte, Yte = datautils.load_CIFAR10('/home/auroua/workspace/cifar-10-batches-py/') # a magic function we provide
    # flatten out all images to be one-dimensional
Xtr_rows = Xtr.reshape(Xtr.shape[0], 32 * 32 * 3) # Xtr_rows becomes 50000 x 3072
Xtr_means = np.mean(Xtr_rows, axis=0)

Xtr_rows -= Xtr_means
Xtr_rows /= 127.0
# print Xtr_rows
Xte_rows = Xte.reshape(Xte.shape[0], 32 * 32 * 3) # Xte_rows becomes 10000 x 3072
Xtr_totals = np.ones((Xtr_rows.shape[0], Xtr_rows.shape[1] + 1))
Xtr_totals[:, :Xtr_totals.shape[1]-1] = Xtr_rows

def CIFAR10_loss_fun(W):
      # data pre_process
    return L(Xtr_totals, Ytr, W)