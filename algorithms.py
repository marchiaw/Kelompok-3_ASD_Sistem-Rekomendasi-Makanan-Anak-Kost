def binary_search_warung(arr, target_nama):
    low = 0
    high = len(arr) - 1
    target = target_nama.lower()

    while low <= high:
        mid = (low + high) // 2
        if target == arr[mid].nama_warung.lower():
            return mid
        elif arr[mid].nama_warung.lower() < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
