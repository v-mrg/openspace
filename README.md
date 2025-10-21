# OpenSpace Simulation
This is a simulation setup for OpenSpace, an architectural roadmap for a more open and heterogeneous satellite Internet paradigm.
In the branch simple-sim, we simulate the total coverage per number of satellites, and the minimum latency via n-hop ISLs per a randomized number of satellites.
We run a simplified simulation, fixing the user and groundstation coordinates and randomly distributing satellites orbital paths. 
We then compute the shortest path between the satellite that picks up the user’s signal, and the satellite that will relay that signal to the ground station, and use this path length to estimate latency. 
To get a realistic coverage estimate, we assume that if there is any overlap between a pair of satellite ranges, their effective coverage will be reduced to that of a single satellite.
That is, we take the worst case where two satellites have completely overlapping ground coverage.

HotNet 2024 conference paper: https://conferences.sigcomm.org/hotnets/2024/papers/hotnets24-75.pdf 


