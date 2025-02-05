
import math
import numpy as np


class Lognormal:
        """
        Encapsulates a lognormal distirbution
        """
        def __init__(self, mean, stdev, random_seed=None):
            """
            Params:
            -------
            mean = mean of the lognormal distribution
            stdev = standard dev of the lognormal distribution
            """
            self.rand = np.random.default_rng(seed=random_seed)
            mu, sigma = self.normal_moments_from_lognormal(mean, stdev**2)
            self.mu = mu
            self.sigma = sigma

        def normal_moments_from_lognormal(self, m, v):
            '''
            Returns mu and sigma of normal distribution
            underlying a lognormal with mean m and variance v
            source: https://blogs.sas.com/content/iml/2014/06/04/simulate-lognormal
            -data-with-specified-mean-and-variance.html

            Params:
            -------
            m = mean of lognormal distribution
            v = variance of lognormal distribution

            Returns:
            -------
            (float, float)
            '''
            phi = math.sqrt(v + m**2)
            mu = math.log(m**2/phi)
            sigma = math.sqrt(math.log(phi**2/m**2))
            return mu, sigma

        def sample(self):
            """
            Sample from the normal distribution
            """
            return self.rand.lognormal(self.mu, self.sigma)        

class Erglang_dist: 
        def __init__(self, mu, sigma, random_seed=None):
            self.mu = mu   # 52 Mean call length
            self.sigma = sigma      # 8 Standard deviation

        def ErlangRes(self, mu, sigma):
        #Generates an erlang distribution

            random_seed = np.random.default_rng(seed=random_seed)

            # Compute shape and scale parameters
            k = int(mu**2 / sigma**2)  # Shape parameter (integer)
            theta = (sigma**2) / mu  # Scale parameter
        
            e = self.erlang.rvs(self.k, self.theta,random_seed)
            return  self.e