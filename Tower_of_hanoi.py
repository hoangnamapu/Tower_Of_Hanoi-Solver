import numpy as np
from numpy.core.multiarray import empty

def finding_top_position(arr, col) :
    x = np.nonzero(arr[:, col])[0]
    if x.size == 0: #empty
        return 3
    else:
        t = x[0]
        return t

def finding_top_pos_value(arr,col):
    if finding_top_position(arr, col) == 3:
        return 100
    else:
        row = finding_top_position(arr, col)
        value = arr[row,col]
        return value


def action(arr):
    #list of all valid actions:
    valid_actions = []

    #position of top disk on each tower
    t1 = finding_top_position(arr, 0)
    t2 = finding_top_position(arr, 1)
    t3 = finding_top_position(arr, 2)

    #value of top disk on each tower
    v1 = arr[t1, 0] if t1 != 3 else 100
    v2 = arr[t2, 1] if t2 != 3 else 100
    v3 = arr[t3, 2] if t3 != 3 else 100


    if t1 < t2:
        demo = np.zeros((3,3), dtype = int) #Tao ra mot 2D array 3x3 voi gia tri = 0
        demo[t1,0] = -v1
        demo[t2-1, 1] = v1
        valid_actions.append(demo.copy())

    if t1 > t2:
        demo = np.zeros((3,3), dtype = int)
        demo[t2,1] = -v2
        demo[t1-1, 0] = v2
        valid_actions.append(demo.copy())

    if t1 < t3:
        demo = np.zeros((3,3), dtype = int)
        demo[t1,0] = -v1
        demo[t3-1,2] = v1
        valid_actions.append(demo.copy())

    if t1 > t3:
        demo = np.zeros((3,3), dtype = int)
        demo[t3,2] = -v3
        demo[t1-1, 0] = v3
        valid_actions.append(demo.copy())

    if t2 < t3:
        demo = np.zeros((3,3), dtype = int)
        demo[t2,1] = -v2
        demo[t3-1,2] = v2
        valid_actions.append(demo.copy())

    if t2 > t3:
        demo = np.zeros((3,3), dtype = int)
        demo[t3,2] = -v3
        demo[t2-1, 1] = v3
        valid_actions.append(demo.copy())

    return valid_actions

def transform(curnode, act) -> dict:
    newnode = {
        "state": curnode.get("state") + act,
        "actions": act,
        "h": 0,
        "cost": curnode.get("cost") + 1
    }

    return newnode

def compare (node, othernode):
    node = node.get("state")
    othernode = othernode.get("state")
    return np.all(node == othernode)

Vcompare = np.vectorize(compare, excluded=["othernode"])

def solver(node, goal):
    explore_list = np.array([])
    funtee = np.array([node.copy()])
    while (funtee.size != 0):
        current = funtee[-1]
        x = current.get("state")
        funtee = np.delete(funtee, -1)
        explore_list = np.append(explore_list, current)
        if (np.all(x == goal)):
            return current
        else:
            pos_actions = action(x)
            for act in pos_actions:
                newNode = transform(current, act)
                if np.any(Vcompare(explore_list, newNode)): #Check neu newNode co nam trong explorelist hay k
                    continue
                else:
                    funtee = np.append(funtee, current)
    return None


if __name__ == "__main__":
    arr = np.array([
        [1,0,0],
        [2,0,0],
        [3,0,0]
    #   [100,100,100]  #1<4    #highest = none c
    ])
    goal = np.array([
        [0,0,1],
        [0,0,2],
        [0,0,3]
    ])


    node = {
        "state": arr,
        "actions": np.zeros((3,3), dtype = int),
        "h": 0,
        "cost": 0
    }


    solution = solver(node, goal)
    print(solution)
