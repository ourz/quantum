# quantum
This repo contains Qiskit examples, often related to statistics and probability, for use on quantum computers.

Contents
--------

estimate pi.ipynb estimates pi using an approximation of the quantum inverse Fourier transform. The approximation is iteratively improved from a start guess using the secant method.

spsa_learn_probability_dist.ipynb trains a parameterized quantum circuit to be able to sample from a user-defined probability distribution. The program attemps to minimize the entropy using SPSA gradient search.

bayesian network simulation.ipynb implements a simple v-shaped Bayesian network on a quantum circuit and samples from it.

markov.ipynb implements a circuit that simulates n steps for a simple Markov chain.
