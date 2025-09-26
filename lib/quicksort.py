def quicksort(a):
    if len(a) <= 1:
        return a
    p = a[len(a)//2]
    left  = [x for x in a if x.id <  p.id]
    mid   = [x for x in a if x.id == p.id]
    right = [x for x in a if x.id >  p.id]
    return quicksort(left) + mid + quicksort(right)