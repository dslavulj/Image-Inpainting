"""
Author: Danijel Slavulj
"""

import torch

def ex6(logits, activation_function, threshold, targets):
    #raise a TypeError exception if logits is not a torch.Tensor of floating point datatype (as determined by torch.is_floating_point)
    if not torch.is_floating_point(logits):
        raise TypeError("logits is not floating point tensor")

    #raise a TypeError exception if threshold is not a torch.Tensor
    if not isinstance(threshold, torch.Tensor):
        raise TypeError("threshold is not a torch.Tensor")

    #raise a TypeError exception if targets is not a torch.Tensor of datatype torch.bool.
    if targets.dtype is not torch.bool:
        raise TypeError("targets is not a torch.Tensor of datatype torch.bool")

    #raise a ValueError exception if the shape of logits or targets is not (n_samples,)
    if logits.ndim != 1 or targets.ndim != 1:
        raise ValueError("shape of logits or targets is not (n_samples,)")

    #raise a ValueError exception if n_samples is not equal for logits and targets.
    if len(logits) != len(targets):
        raise ValueError("n_samples is not equal for logits and targets.")

    #raise a ValueError exception if targets does not contain at least one entry with value False and at least one entry with value True
    if not True in targets or not False in targets:
        raise ValueError("targets does not contain at least one entry with value False and at least one entry with value True")

    predictions = activation_function(logits)
    predictions = torch.ge(predictions, threshold)

    TP = torch.sum(predictions & targets).double().item()
    FP = torch.sum(predictions & ~targets).double().item()
    TN = torch.sum(~predictions & ~targets).double().item()
    FN = torch.sum(~predictions & targets).double().item()

    return [[TP, FN], [FP, TN]], ((2*TP)/(2*TP+FP+FN)), ((TP+TN)/(TP+TN+FP+FN)), (((TP/(TP+FN))+(TN/(TN+FP)))/2)
