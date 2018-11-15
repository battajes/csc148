    if left_closest is not None and item - left_closest <= self._root - item:
        return left_closest
    else:
        return self._root

else:
    if right_closest is not None and right_closest - item < item - self._root:
        return right_closest
    else:
        return self._root
