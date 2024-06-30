import pandas as pd
import numpy as np
import random
import math
import sys
import matplotlib.pyplot as plt
import statistics
from itertools import combinations



# distance using haversine formula from https://gist.github.com/rochacbruno/2883505
def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 * 10**3 # km to m

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

# adapted from stack overflow https://gis.stackexchange.com/questions/59339/generate-random-world-point-geometries 
def newpoint():
   return random.uniform(-90, 90), random.uniform(-180,180)

# Python program for Dijkstra's single
# source shortest path algorithm. The program is
# for adjacency matrix representation of the graph

class Graph():

    def __init__(self, input_graph):
        self.V = len(input_graph[0])
        # print("V:", self.V)
        # self.graph = [[0 for column in range(vertices)]
        #               for row in range(vertices)]
        self.graph = input_graph
        # print("graph:")
        # print(self.graph)

    # def printSolution(self, dist):
        # print("Vertex \tDistance from Source")
        # for node in range(self.V):
            # print(node, "\t", dist[node])

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):

        # Initialize minimum distance for next node
        min = sys.maxsize

        # Search not nearest vertex not in the
        # shortest path tree
        for u in range(self.V):
            if dist[u] < min and sptSet[u] == False:
                min = dist[u]
                min_index = u

        return min_index

    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):

        dist = [sys.maxsize] * self.V
        # print("dist initialized to: ", dist)
        dist[src] = 0
        sptSet = [False] * self.V

        for cout in range(self.V):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # x is always equal to src in first iteration
            x = self.minDistance(dist, sptSet)

            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[x] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for y in range(self.V):
                if self.graph[x][y] > 0 and sptSet[y] == False and \
                        dist[y] > dist[x] + self.graph[x][y]:
                    dist[y] = dist[x] + self.graph[x][y]

        # self.printSolution(dist)
        return dist


class Satellite:
    def __init__(self, id, position, in_orbit_with_user, in_orbit_with_gs):
        self.id = id
        self.pos = position
        self.in_orbit_with_user = in_orbit_with_user
        self.in_orbit_with_gs = in_orbit_with_gs


# create adjacency matrix
def create_adj_matrix(sats):
    i_arr = []
    for i in range(len(sats)):
        j_arr = []
        for j in range(len(sats)):
            # euclidian distance
            dist = distance(sats[i].pos, sats[j].pos)
            # dist = abs(np.array(sats[i].pos) - np.array(sats[j].pos))
            # print("distance in adj matrix:", dist)
            # instead of this, chck if the total path is longer than (MAX_LINK_LENGTH * (NUM_SATELLITES-1))
            # if dist > MAX_ISL_LENGTH:
            #     dist = np.inf
            j_arr.append(dist)
        i_arr.append(j_arr)
    return i_arr

def get_random_sats(sats, num_sats):
    returned_sats = []
    for _ in range(num_sats):
        selectedsat = sats[random.randint(0, TOTAL_SATELLITES - 1)]	
        returned_sats.append(selectedsat)
    return returned_sats

# important constants
user_pos = (40.4438068, -79.9470891)
gs_pos = (1.2850432, 36.8216259)
# SATELLITE_RANGE  = 25 * 10**3 # diameter of starlink cell in m
SATELLITE_RANGE  = 2209 # foorprint radius of iridium in km
TOTAL_SATELLITES = 66
SATELLITE_SPEED = 7.5 * 10**3  # speed in m/sec
SAT_TO_GROUND_TRAVEL_TIME = 0.0026 # travel time for signals in sec assuming satellite altitude of 780km
MAX_ISL_LENGTH = 4000 * 10**3 # in km
TRIAL_LENGTH = 50
LIGHT_SPEED = 3 * 10**8
EARTH_CIRC = 40000 * 10^3
TOTAL_EARTH_AREA = 510 * 10**6 # total area in km2

def determine_coverage(sats):
    coverage = 0
    pairs = list(combinations(sats, 2))
    counted_sats = set()
    for i, j in pairs:
        d = distance(i.pos, j.pos) * 10**-3 # convert to km
        if d < 2*SATELLITE_RANGE: # some overlap
            # print("overlap detected with ", len(sats), "satellites")
            if i.id not in counted_sats and j.id not in counted_sats:
                # coverage += ((math.pi * SATELLITE_RANGE) / 2.0) * d + (math.pi * SATELLITE_RANGE**2)
                counted_sats.add(i)
                counted_sats.add(j)
            elif i.id in counted_sats and j.id not in counted_sats:
                # coverage += ((math.pi * SATELLITE_RANGE) / 2.0) * d 
                counted_sats.add(j)
            elif j.id in counted_sats and i.id not in counted_sats:
                # coverage += ((math.pi * SATELLITE_RANGE) / 2.0) * d 
                counted_sats.add(i)

    # print(len(counted_sats))
    coverage += math.pi * SATELLITE_RANGE**2 * (len(sats) - len(counted_sats))
    coverage += math.pi * SATELLITE_RANGE**2 * int(len(counted_sats)/2)

    # fix area overflow
    coverage = TOTAL_EARTH_AREA if coverage > TOTAL_EARTH_AREA else coverage
    return coverage

def main():
    # initialize satellites using positions
    sat_positions = (newpoint() for x in range(66))
    sat_positions = [x for x in sat_positions]
    # print(sat_positions)
    sats = []
    for i in range(len(sat_positions)):
        # there are 6 orbits; 
        # make it a 1/6 chance that the user is in the same orbit as the satellite, 
        # and a 1/6 chance that the ground station is in the same orbit as the satellite
        new_sat = Satellite(i, sat_positions[i], random.random() < 1/6, random.random() < 1/6)
        sats.append(new_sat)
    
    # for plotting
    x_axis = [] # number of satellites
    y_axis = [] # latency
    failed_links_y = []
    stdev = []
    stdev_coverage = []
    covered_area = []

    for i in range(TOTAL_SATELLITES):
        average_time = []
        # sat_area = i * math.pi * ((SATELLITE_RANGE * 10**(-3)) ** 2)
        average_coverage = []
        failed_links = 0 # due to user/gs not in orbit with any satellite, isl links too long, etc

        for _ in range(TRIAL_LENGTH):
            selected_sats = get_random_sats(sats, i)

            # compute coverage
            average_coverage.append(determine_coverage(selected_sats))

            # is there a sat in same orbit as user, and a sat in same orbit as GS?
            user_contact, gs_contact = None, None
            for ix in range(len(selected_sats)):
                if selected_sats[ix].in_orbit_with_user == True:
                    user_contact = selected_sats[ix]
                    user_contact.id = ix
                if selected_sats[ix].in_orbit_with_gs == True:
                    gs_contact = selected_sats[ix] 
                    gs_contact.id = ix
            if user_contact == None or gs_contact == None:
                # there is no satellite in the same orbit as either the user or ground station, so an e2e connection is not possible
                failed_links += 1
                # penalty for this link is the best case where a satellite "ubers" from the user to the ground station to deliver a message
                t = distance(user_pos, gs_pos) / SATELLITE_SPEED
                average_time.append(t)
                continue

            # which sats are close to each other and can form ISLs?
            # use dijkstra's
            # first create adjacency matrix
            adj_matrix = create_adj_matrix(selected_sats)
            g = Graph(adj_matrix)
            # use dijkstra's to get shortest path from defined start node to all other nodes
            dikstra = g.dijkstra(user_contact.id)
            # get shortest path from user node to gs node
            length_to_gs = dikstra[gs_contact.id]

            # if the length of the shortest path is longer than the number of ISLs possible in the system, ignore
            if length_to_gs > (MAX_ISL_LENGTH * (i-1)):
                failed_links += 1
                # penalty
                t = distance(user_contact.pos, user_pos) / SATELLITE_SPEED
                average_time.append(t)
                continue

            t = 0
            t += (length_to_gs / LIGHT_SPEED * 1.0)

            # how far away from the user is the sat in the same orbit as the user?
            d_user = distance(user_contact.pos, user_pos)
            # d_user = random.choice([d_user, EARTH_CIRC - d_user]) -- was doing this to insert randomness about the direction of orbit

            # calculate time to user if out of range of satellite
            if d_user > SATELLITE_RANGE:
                time_to_user = d_user / SATELLITE_SPEED * 1.0
                # t += time_to_user 

            # is the sat in gs orbit in range of the user?
            d_gs = distance(gs_contact.pos, gs_pos)
            d_gs = random.choice([d_gs, EARTH_CIRC - d_gs])
            if d_gs > SATELLITE_RANGE:
                time_to_gs = d_gs / SATELLITE_SPEED * 1.0
                # t += time_to_gs
            average_time.append(t)

        if failed_links == TRIAL_LENGTH:
            average_time_val= np.inf
            stdev_val  = 0
        else:
            average_time_val = np.sum(average_time) / len(average_time)
            stdev_val = np.std(average_time)

        x_axis.append(i)
        y_axis.append(average_time_val)
        failed_links_y.append(failed_links)
        stdev.append(stdev_val)
        stdev_coverage.append(np.std(average_coverage))
        # print(average_coverage)
        covered_area.append(np.sum(average_coverage) / len(average_coverage))

    y_axis = np.array(y_axis)
    # stdev = np.std(y_axis[np.isfinite(y_axis)])
    # print("latency:", y_axis)

    # plot coverage
    # plt.plot(covered_area, label = 'area covered')
    plt.errorbar(x_axis, covered_area, stdev_coverage, fmt = 'o', label = 'satellite coverage area with std deviation')
    print("TOTAL_EARTH_AREA", TOTAL_EARTH_AREA)
    plt.plot([TOTAL_EARTH_AREA] * len(covered_area), label = 'total earth area')
    plt.legend()
    plt.xlabel('number of satellites')
    plt.ylabel('coverage (km2)')
    plt.title("Coverage vs. number of satellites")
    plt.savefig('coverage.png')
    plt.clf() 

    # plot latency
    # plt.plot(x_axis, y_axis)
    plt.errorbar(x_axis, y_axis, stdev, fmt = 'o')
    plt.xlabel('number of satellites')
    plt.ylabel('one-way propagation latency (seconds)')
    plt.title("Propagation latency vs. number of satellites")
    plt.savefig('latency.png')
    plt.clf() 

main()

# print(t)


# sat_positions_df = pd.read_csv('/Users/wairimu/Desktop/cmu/research/openspace-main/sat_positions.csv', header = None)
# print(sat_positions_df.shape)
# # print(sat_positions_df)

# sat_positions = sat_positions_df.values
# print(sat_positions.shape)
# print(sat_positions[:, 1])