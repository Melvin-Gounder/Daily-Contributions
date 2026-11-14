"""Disk-head seek scheduler: FCFS, SSTF, and SCAN."""
def schedule(requests, head, cylinders, algorithm="fcfs", direction="up"):
    if type(cylinders) is not int or cylinders <= 0 or type(head) is not int or not 0 <= head < cylinders:
        raise ValueError("invalid disk geometry or head")
    jobs = list(requests)
    if any(type(x) is not int or not 0 <= x < cylinders for x in jobs):
        raise ValueError("request outside disk")
    if algorithm == "fcfs":
        order = jobs
    elif algorithm == "sstf":
        remaining = list(enumerate(jobs))
        order, current = [], head
        while remaining:
            index, chosen = min(remaining,key=lambda pair:(abs(pair[1]-current),pair[1],pair[0]))
            order.append(chosen)
            remaining.remove((index,chosen))
            current = chosen
    elif algorithm == "scan":
        if direction not in ("up","down"): raise ValueError("invalid direction")
        lower = sorted((x for x in jobs if x < head),reverse=True)
        upper = sorted(x for x in jobs if x >= head)
        if direction == "up":
            order = upper + ([cylinders-1] if lower and (not upper or upper[-1] != cylinders-1) else []) + lower
        else:
            order = lower + ([0] if upper and (not lower or lower[-1] != 0) else []) + upper
    else:
        raise ValueError("unknown algorithm")
    position, movement = head, 0
    for cylinder in order:
        movement += abs(cylinder-position)
        position = cylinder
    return {"order":order,"movement":movement}

if __name__ == "__main__":
    for name in ("fcfs","sstf","scan"):
        print(name,schedule([98,183,37,122,14,124,65,67],53,200,name))
