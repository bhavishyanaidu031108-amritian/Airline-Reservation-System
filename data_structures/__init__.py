try:
    from .avl_tree import AVLTree, AVLNode
except ImportError:
    from .AVL_tree import AVLTree, AVLNode

from .graph import AirportGraph
from .hash_table import HashTable
from .priority_queue import WaitingList

__all__ = ["AVLTree", "AVLNode", "AirportGraph", "HashTable", "WaitingList"]
