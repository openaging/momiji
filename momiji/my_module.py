# reference: https://github.com/biopackathon/python-packaging-exercise/tree/main/poetry/mypackageabc/mypackageabc
import numpy as np

# Creates a NumPy array from the given string elements
my_array = np.array(["1", "2", "3"])

def my_func(x):
    """Converts a Numpy array with string elements into an integer Numpy array.

    Args:
        A Numpy array with string elements (e.g., my_array)

    Returns:
        A Numpy array with int64 elements

    Example:
        >>> import mypackageabc as my
        >>> my.my_func(my.my_array)

    Note:
        This is very simple function only for the demonstration

    """
    return x.astype(np.int64)




import torch
import torch.nn as nn


class MyModel(nn.Module):
    def __init__(self, in_dim, out_dim, clock_name, features):
        """
        Parameters
        ----------
        input_dim : int
            Number of input features.
        """
        super(MyModel, self).__init__()

        self.linear = nn.Linear(in_dim, out_dim)
        self.features = features
        self.metadata = {"clock_name": clock_name}

    def forward(self, x):
        return self.linear(x)



__all__ = ["my_array", "my_func", "MyModel"]