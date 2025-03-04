## Task 2:
https://github.com/CoKn/hsg-was-fs25-exercise-2

## Task 3:

### 1. What is the anomaly that occurs when solving the problem in the domain?
The anomaly manifests as a conflict between seemingly independent subgoals—in this case, **“obtaining the hoover”** and **“cleaning the room.”** Naively decomposing the goal *clean room1* leads to a plan that first attempts to satisfy the cleaning subgoal. However, cleaning requires the hoover, and obtaining the hoover requires leaving *room1* to go to storage. This causes an interference: achieving one subgoal (cleaning) appears to be undone by the necessary actions (moving away to get the hoover) that support the other subgoal.

---

### 2. Under what circumstances does the anomaly generally occur in classical STRIPS planning?
The **Sussman anomaly** typically occurs when:
- **Subgoal Interference:** Subgoals that seem independent actually interfere with one another.
- **Non-decomposability:** The goal cannot be solved by completely achieving one subgoal before tackling the other; instead, actions must be interleaved.
- **Irreversible Effects:** Certain actions (like moving) remove conditions (e.g., *“at room1”*) required for achieving another subgoal, forcing the planner to re-achieve these conditions later.

---

### 3. What specifically in the problem and the domain makes it susceptible?
In the provided domain:
- **Action Dependencies:** The `cleanRoom` action requires both the presence in the room and possession of the hoover. However, the `getHoover` action requires the maintenance worker to be at the storage.
- **State Disruption:** The `move` action has the effect of deleting the current location (via `(not (at ?x))`). Thus, moving to storage to get the hoover temporarily *loses* the condition of being in the room needed for cleaning.
- **Interleaving Necessity:** The optimal solution (as shown in the provided plan) interleaves moves—first moving into the room, then out to storage to get the hoover, and finally returning to the room to clean. This interleaving is the hallmark of the **Sussman anomaly**.

---

### 4. Why is the behavior not observable with your planner implementation from Task 2?
Our **Task 2 planner** uses a **state-space search** that does not decompose goals into independent subgoals. Instead, it searches over **complete states** using a heuristic that evaluates the entire state at once. This means:
- **Global Search:** The planner evaluates full states and finds interleaved plans naturally, without being misled by an incorrect sequential decomposition of goals.
- **No Subgoal Isolation:** Since the planner does not isolate subgoals (e.g., *“cleaning”* vs. *“getting the hoover”*) before planning, it does not encounter the same interference issues that arise in planners that try to solve subgoals in a strictly sequential manner.
- **Heuristic Guidance:** The heuristic used guides the search towards states that meet the overall goal, thereby circumventing the pitfalls that lead to the anomaly in classical **STRIPS** planners with separate subgoal management.

