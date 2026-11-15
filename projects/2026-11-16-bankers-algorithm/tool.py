"""Banker's algorithm for resource-allocation safety."""
def safety(available, allocation, maximum):
    n = len(allocation)
    m = len(available)
    if len(maximum) != n or any(len(row) != m for row in allocation + maximum):
        raise ValueError("inconsistent resource dimensions")
    if any(not isinstance(x, int) or x < 0 for row in [available] + allocation + maximum for x in row):
        raise ValueError("resources must be nonnegative integers")
    if any(allocation[i][j] > maximum[i][j] for i in range(n) for j in range(m)):
        raise ValueError("allocation exceeds maximum")
    need = [[maximum[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]
    work = list(available)
    done = [False] * n
    sequence = []
    while len(sequence) < n:
        candidate = next((i for i in range(n) if not done[i] and all(need[i][j] <= work[j] for j in range(m))), None)
        if candidate is None: break
        done[candidate] = True
        sequence.append(candidate)
        work = [work[j] + allocation[candidate][j] for j in range(m)]
    return len(sequence) == n, sequence

def request(available, allocation, maximum, process, resources):
    if not 0 <= process < len(allocation) or len(resources) != len(available):
        raise ValueError("invalid request dimensions")
    if any(not isinstance(x, int) or x < 0 for x in resources):
        raise ValueError("request must be nonnegative")
    if any(resources[j] > maximum[process][j] - allocation[process][j] for j in range(len(resources))):
        raise ValueError("request exceeds declared need")
    if any(resources[j] > available[j] for j in range(len(resources))):
        return False, []
    new_available = [v-r for v,r in zip(available,resources)]
    new_allocation = [list(row) for row in allocation]
    new_allocation[process] = [v+r for v,r in zip(allocation[process],resources)]
    return safety(new_available,new_allocation,maximum)

if __name__ == "__main__":
    print(safety([3,3,2], [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]], [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]))
