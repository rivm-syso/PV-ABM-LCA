#import
import numpy as np
from scipy.stats import lognorm, norm

def lognormal_stats(mu, sigma):
    """
    Calculate the min, max, and mode values for a lognormal distribution
    given the mean (mu) and standard deviation (sigma) of the underlying normal distribution.
    """
    # Calculate the 1st and 99th percentiles for practical min and max values
    min_value = lognorm.ppf(0.01, s=sigma, scale=np.exp(mu))
    max_value = lognorm.ppf(0.99, s=sigma, scale=np.exp(mu))
    
    # Calculate the mode value
    mode_value = np.exp(mu - sigma**2)
    return min_value, max_value, mode_value

def normal_stats(mu, sigma):
    """
    Calculate the min, max, and mode values for a normal distribution
    given the mean (mu) and standard deviation (sigma).
    """
    # Calculate the 1st and 99th percentiles for practical min and max values
    min_value = norm.ppf(0.01, loc=mu, scale=sigma)
    max_value = norm.ppf(0.99, loc=mu, scale=sigma)
    
    # Calculate the mode value
    mode_value = mu
    
    return min_value, max_value, mode_value

def normalize_value(value, min_value, max_value):
    """
    Normalize a value between min_value and max_value.
    """
    if min_value == max_value:
        raise ValueError("min_value and max_value cannot be the same")
    normalized_value = (value - min_value) / (max_value - min_value)
    return normalized_value