## Task 2:
[GitHub Repository](https://github.com/CoKn/hsg-was-fs25-exercise-2)

## Task 3:

### 1. What is the anomaly that occurs when solving the problem in the domain?
The Sussman anomaly occurs because two subgoals—**getting the hoover** and **cleaning the room**—conflict with each other. At first glance, these goals seem independent, but in reality, they interfere. If we try to clean the room first, we realize we need the hoover. However, getting the hoover requires moving to storage, which means we have to leave the room. This disrupts the goal of being in the room for cleaning, leading to a back-and-forth problem where the planner needs to interleave actions rather than solving subgoals sequentially.

---

### 2. Under what circumstances does the anomaly generally occur in classical STRIPS planning?
The **Sussman anomaly** typically happens when:
- **Subgoal Interference:** Achieving one subgoal makes another subgoal harder to reach.
- **Non-decomposability:** The problem cannot be solved by completing one subgoal first and then the other. Instead, actions must be interwoven.
- **State Disruptions:** Certain actions (like moving) remove conditions required for another subgoal, forcing the planner to re-establish them.

---

### 3. What specifically in the problem and the domain makes it susceptible?
Several aspects of the domain contribute to this issue:
- **Action Dependencies:** The `cleanRoom` action requires both being in the room and having the hoover. However, `getHoover` requires being at storage, which means leaving the room.
- **State Disruptions:** The `move` action removes the `at ?x` condition, so moving to storage makes the condition `at room1` false, preventing immediate cleaning.
- **Interleaving Requirement:** The optimal solution (as shown in the provided plan) does not complete one goal first but instead switches between them: moving to the room, then to storage, then back to the room. This is a classic symptom of the **Sussman anomaly**.

---

### 4. Why is the behavior not observable with your planner implementation from Task 2?
The planner in **Task 2** avoids the issue because it uses **state-space search** rather than a goal-decomposition approach. This leads to:
- **Holistic State Evaluation:** The planner considers entire states rather than breaking the problem into separate subgoals.
- **Interleaved Planning:** The A* search naturally finds an optimal sequence where moves and actions are interleaved, rather than trying to achieve one goal fully before the other.
- **Heuristic Guidance:** The heuristic directs the search toward feasible paths, avoiding getting stuck in a sequence where achieving one subgoal completely blocks another.

Since our planner does not follow a naive goal-by-goal approach, it does not get trapped in the anomaly.

