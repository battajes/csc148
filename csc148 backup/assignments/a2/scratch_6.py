from __future__ import annotations
import csv
from typing import Any, Dict, List, Optional, Tuple

from melody import Melody
from prefix_tree import SimplePrefixTree, CompressedPrefixTree

with open('data/lotr.txt', encoding='utf8') as f:

    clean_words = []
    # for line in f:
    for i in range(10):
        raw = f.readline()
        chars = [c for c in raw if c.isalnum() or c == ' ']
        clean = ''.join(chars).lower()
        # in letter autocomplete engine do split, not in sentence autocomplete.
        # text = text.split()
        if len(clean) >= 1:
            autocompleter.insert(clean, weight, prefix(clean))
