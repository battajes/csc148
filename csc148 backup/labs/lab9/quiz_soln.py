def closest(self, item) -> Optional[int]:

    if self.is_empty():
        return None
    elif item == self._root:
        return self._root
    elif item < self._root:
        left_closest = self._left.closest(item)

        if left_closest is not None and item - left_closest <= self._root - item:
            return left_closest
        else:
            return self._root

    else:
        right_closest = self._right.closest(item)

        if right_closest is not None and right_closest - item < item - self._root:
            return right_closest
        else:
            return self._root
