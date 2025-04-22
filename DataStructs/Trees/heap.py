from typing import Any, Callable
from DataStructs.List import arlt
from Utils.error import error_handler as err


def dflt_heap_elm_cmp(id1: Any, id2: Any) -> int:
    if id1 > id2:
        return 1
    elif id1 < id2:
        return -1
    return 0


def new_heap(cmp_function: Callable[[Any, Any], int] = None) -> dict:
    try:
        _new_heap = {
            "elements": arlt.new_list(cmp_function),
            "size": 0,
            "cmp_function": cmp_function or dflt_heap_elm_cmp
        }
        return _new_heap
    except Exception as exp:
        err("heap", "new_heap()", exp)


def size(heap: dict) -> int:
    try:
        return heap["size"]
    except Exception as exp:
        err("heap", "size()", exp)


def is_empty(heap: dict) -> bool:
    try:
        return heap["size"] == 0
    except Exception as exp:
        err("heap", "is_empty()", exp)


def get_min(heap: dict) -> Any:
    try:
        if is_empty(heap):
            return None
        return arlt.get_element(heap["elements"], 0)
    except Exception as exp:
        err("heap", "get_min()", exp)


def insert(heap: dict, elm: Any) -> None:
    try:
        arlt.add_last(heap["elements"], elm)  # Inserta correctamente al final
        heap["size"] = arlt.size(heap["elements"])
        _swim(heap, heap["size"] - 1)
    except Exception as exp:
        err("heap", "insert()", exp)


def delete_min(heap: dict) -> Any:
    try:
        if is_empty(heap):
            return None
        _min = arlt.get_element(heap["elements"], 0)
        _last = arlt.get_element(heap["elements"], heap["size"] - 1)
        arlt.update(heap["elements"], 0, _last)
        arlt.remove_last(heap["elements"])
        heap["size"] = arlt.size(heap["elements"])
        _sink(heap, 0)
        return _min
    except Exception as exp:
        err("heap", "delete_min()", exp)


def _swim(heap: dict, idx: int) -> None:
    try:
        while idx > 0:
            parent_idx = (idx - 1) // 2
            parent = arlt.get_element(heap["elements"], parent_idx)
            current = arlt.get_element(heap["elements"], idx)
            if _greater(heap, parent, current):
                _exchange(heap, idx, parent_idx)
                idx = parent_idx
            else:
                break
    except Exception as exp:
        err("heap", "_swim()", exp)


def _sink(heap: dict, idx: int) -> None:
    try:
        _size = heap["size"]
        while 2 * idx + 1 < _size:
            j = 2 * idx + 1
            if j + 1 < _size:
                left = arlt.get_element(heap["elements"], j)
                right = arlt.get_element(heap["elements"], j + 1)
                if _greater(heap, left, right):
                    j += 1
            current = arlt.get_element(heap["elements"], idx)
            child = arlt.get_element(heap["elements"], j)
            if not _greater(heap, current, child):
                break
            _exchange(heap, idx, j)
            idx = j
    except Exception as exp:
        err("heap", "_sink()", exp)


def _greater(heap: dict, elm1: Any, elm2: Any) -> bool:
    try:
        return heap["cmp_function"](elm1, elm2) > 0
    except Exception as exp:
        err("heap", "_greater()", exp)


def _exchange(heap: dict, idx1: int, idx2: int) -> None:
    try:
        arlt.exchange(heap["elements"], idx1, idx2)
    except Exception as exp:
        err("heap", "_exchange()", exp)
