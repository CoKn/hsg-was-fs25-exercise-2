#
# This file is based on pyperplan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

"""
Implements the A* (a-star) and weighted A* search algorithm.
"""

import heapq
import logging

from . import searchspace


def ordered_node_astar(node, h, node_tiebreaker):
    """
    Creates an ordered search node (basically, a tuple containing the node
    itself and an ordering) for A* search.

    @param node The node itself.
    @param heuristic A heuristic function to be applied.
    @param node_tiebreaker An increasing value to prefer the value first
                           inserted if the ordering is the same.
    @returns A tuple to be inserted into priority queues.
    """
    f = node.g + h
    return (f, h, node_tiebreaker, node)


def ordered_node_weighted_astar(weight):
    """
    Creates an ordered search node (basically, a tuple containing the node
    itself and an ordering) for weighted A* search (order: g+weight*h).

    @param weight The weight to be used for h
    @param node The node itself
    @param h The heuristic value
    @param node_tiebreaker An increasing value to prefer the value first
                           inserted if the ordering is the same
    @returns A tuple to be inserted into priority queues
    """
    """
    Calling ordered_node_weighted_astar(42) actually returns a function (a
    lambda expression) which is the *actual* generator for ordered nodes.
    Thus, a call like
        ordered_node_weighted_astar(42)(node, heuristic, tiebreaker)
    creates an ordered node with weighted A* ordering and a weight of 42.
    """
    return lambda node, h, node_tiebreaker: (
        node.g + weight * h,
        h,
        node_tiebreaker,
        node,
    )


def ordered_node_greedy_best_first(node, h, node_tiebreaker):
    """
    Creates an ordered search node (basically, a tuple containing the node
    itself and an ordering) for greedy best first search (the value with lowest
    heuristic value is used).

    @param node The node itself.
    @param h The heuristic value.
    @param node_tiebreaker An increasing value to prefer the value first
                           inserted if the ordering is the same.
    @returns A tuple to be inserted into priority queues.
    """
    f = h
    return (f, h, node_tiebreaker, node)


def greedy_best_first_search(task, heuristic, use_relaxed_plan=False):
    """
    Searches for a plan in the given task using greedy best first search.

    @param task The task to be solved.
    @param heuristic A heuristic callable which computes the estimated steps
                     from a search node to reach the goal.
    """
    return astar_search(
        task, heuristic, ordered_node_greedy_best_first, use_relaxed_plan
    )


def weighted_astar_search(task, heuristic, weight=5, use_relaxed_plan=False):
    """
    Searches for a plan in the given task using A* search.

    @param task The task to be solved.
    @param heuristic  A heuristic callable which computes the estimated steps.
                      from a search node to reach the goal.
    @param weight A weight to be applied to the heuristics value for each node.
    """
    return astar_search(
        task, heuristic, ordered_node_weighted_astar(weight), use_relaxed_plan
    )


def astar_search(
        task, heuristic, make_open_entry=ordered_node_astar, use_relaxed_plan=False
):
    """
    Searches for a plan in the given task using A* search.

    @param task The task to be solved
    @param heuristic  A heuristic callable which computes the estimated steps
                      from a search node to reach the goal.
    @param make_open_entry An optional parameter to change the bahavior of the
                           astar search. The callable should return a search
                           node, possible values are ordered_node_astar,
                           ordered_node_weighted_astar and ordered_node_greedy_best_first with obvious
                           meanings.
    """
    # For the purpose of this Task, the argument use_relaxed_plan is always
    # considered to be False
    use_relaxed_plan = False

    # Create the root node (i.e. the node that corresponds to the
    # initial state). The root node is a SearchNode instance with the following
    # attributes:
    # state: equals to the initial state of the task
    # parent (node): None
    # action (that produced the initial state): None
    # g (The path length of the root node in the count of applied operators): 0
    # See searchspace.py for more details.
    # SearchNode instances are the nodes to be visited during search.
    root = searchspace.make_root_node(task.initial_state)

    # The cost of reaching the initial state is 0
    state_cost = {task.initial_state: 0}

    # An increasing value to prefer the value first inserted in the heap of nodes
    # if the cost of two or more nodes is the same
    node_tiebreaker = 0

    # Calculate the estimated movement cost to reach the goal state
    # from the initial state (i.e. from the state in root node)
    init_h = heuristic(root)

    # The nodes to be expanded. Each node will be stored along with the
    # 1) estimated heuristic values f and h for reaching the goal state from the
    # state in node, and 2) the node_tiebreaker value
    open = []

    # Add the root node in the heap of nodes to be expanded ("open").
    # The root node is stored along along with 1) the estimated heuristic values
    # f and h for reaching the goal state from the state in node, and 2) the
    # node_tiebreaker value. f is calculated based on the callable parameter
    # make_open_entry, i.e. based on the type of the A* search algorithm.
    #
    # The node is stored in a heap so that nodes are stored based on their
    # estimated cost! See more here: https://pythontic.com/algorithms/heapq/heappush
    heapq.heappush(open, make_open_entry(root, init_h, node_tiebreaker))
    logging.info("Initial h value: %f" % init_h)

    # Initially, the best cost value is set to infinite
    besth = float("inf")

    counter = 0

    # Counter of the nodes that have been expanded
    expansions = 0

    # Iterate over the heap as long as the heap contains items to pop
    while open:

        # ---- Step 1 ----
        # Pop the next SearchNode instance (pop_node) from the heap (i.e. the next node with the lowest estimated cost)
        # pop_node is the node that will be expanded in this round!
        # HINT: Use the function heappop() of the heapq module: https://pythontic.com/algorithms/heapq/heappop
        (f, h, _tie, pop_node) = heapq.heappop(open)

        # Update the best cost value
        if h < besth:
            besth = h
            logging.info("Found new best h: %d after %d expansions" % (besth, counter))

        # ---- Step 2 ----
        # Use the node to be expanded to get its state and its cost g (i.e. the path length to the node).
        # See searchspace.py
        pop_state = pop_node.state  # state in node
        pop_g = pop_node.g  # cost g of node

        # ---- Step 3 ----
        # Only expand the node if its cost g is the lowest cost known for the node's state.
        # Otherwise, we have already found a cheaper path after creating this node and
        # hence can disregard it.
        if state_cost.get(pop_state, float("inf")) < pop_g:
            continue

        # ---- Step 4 ----
        # Increase the expansions counter and optionally print it
        expansions += 1

        # ---- Step 5 ----
        # If the goal of the task has been reach in the node's state,
        # then extract the solution and return it!
        # HINT: You can extract the solution to the task, using the SearchNode method extract_solution()
        if task.goal_reached(pop_state):
            return pop_node.extract_solution()

        # ---- Step 6 ----
        # Else create and add each neighbor node of the node to the heap if it is worth exploring
        # HINT: You can create neighbor nodes, using the SearchNode method make_child_node()
        # For every neighbor state of the node's state:
        for op, new_state in task.get_successor_states(pop_state):
            # i) Create a neighbor node
            new_g = pop_g + 1  # assuming each operator has a cost of 1
            neighbor_node = searchspace.make_child_node(pop_node, op, new_state)

            # ii) Calculate the h cost of the neighbor node using the callable parameter "heuristic"
            #     (see above how the h cost was calculated for the root node)
            h_neighbor = heuristic(neighbor_node)

            # iii) If h is equal to infinite continue to a new round (the next neighbor state)
            #      You don't need to care about states that can't reach the goal.
            if h_neighbor == float("inf"):
                continue

            # iv) Else, compare the cost g of the neighbor node's state with the lowest cost known
            #     for the neighbor's node state to see if the neighbor node is worth expanding!
            if new_state not in state_cost or new_g < state_cost[new_state]:
                state_cost[new_state] = new_g
                # ---- Step 7 ----
                # i) Increase node_tiebreaker by 1
                node_tiebreaker += 1
                # ii) Store the cost g of the neighbor node's state to the state_cost dictionary
                # iii) Add the neighbor node in the heap of nodes to be expanded ("open").
                #      The neighbor node is stored along with 1) the estimated heuristic values
                #      f and h for reaching the goal state from the state in node, and 2) the
                #      node_tiebreaker value. f is calculated based on the callable parameter
                #      make_open_entry, i.e. based on the type of the A* search algorithm.
                heapq.heappush(open, make_open_entry(neighbor_node, h_neighbor, node_tiebreaker))

        # Increase the counter by 1
        counter += 1

    # If no solution has been extracted and returned after iterating over the whole
    # heap, the function returns None, considering that the task is unsolvable
    logging.info("No operators left. Task unsolvable.")
    logging.info("%d Nodes expanded" % expansions)
    return None

