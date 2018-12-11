def filter_queue(q: Queue[int], minimum: int) -> None:
    """Remove all items from <q> that are less than <minimum>.
    >>> q = Queue()
    >>> q.enqueue(2)
    >>> q.enqueue(21)
    >>> q.enqueue(5)
    >>> q.enqueue(1)
    >>> filter_queue(q, 10)
    >>> q.dequeue()
    21
    >>> q.is_empty()
    True
    """
    temp_queue = Queue()
    while not q.is_empty():
        value = q.dequeue()
        if value >= minimum:
            temp_queue.enqueue(value)

    q = temp_queue
