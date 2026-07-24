import streamlit as st
import time
import random

st.set_page_config(page_title="Experiment 1", page_icon="🔍")

st.title("Experiment 1 - Interpolation Search")

# ---------------- ALGORITHMS ----------------

def interpolation_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1

        if low == high:
            if arr[low] == target:
                return low, comparisons
            return -1, comparisons

        if arr[high] == arr[low]:
            break

        pos = low + int(
            ((target - arr[low]) * (high - low))
            / (arr[high] - arr[low])
        )

        if arr[pos] == target:
            return pos, comparisons
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1, comparisons


def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons

# ---------------- DEMO ----------------

arr = [2, 5, 10, 15, 23, 35, 48, 60, 75, 90, 105, 120]

st.write("### Sample Array")
st.write(arr)

target = st.number_input("Enter Target", value=35)

if st.button("Search"):

    idx, comps = interpolation_search(arr, target)

    if idx != -1:
        st.success(f"Element found at index {idx}")
    else:
        st.error("Element not found")

    st.write(f"Comparisons: {comps}")

# ---------------- PERFORMANCE ----------------

st.write("---")

if st.button("Run Performance Analysis"):

    st.write("### Performance Analysis")

    table = []

    sizes = [1000, 5000, 10000, 50000, 100000]

    for size in sizes:

        arr = sorted(random.sample(range(size * 10), size))
        target = arr[random.randint(0, size - 1)]

        start = time.perf_counter()
        for _ in range(100):
            _, comp_is = interpolation_search(arr, target)
        is_time = (time.perf_counter() - start) / 100 * 1000

        start = time.perf_counter()
        for _ in range(100):
            _, comp_bs = binary_search(arr, target)
        bs_time = (time.perf_counter() - start) / 100 * 1000

        table.append({
            "Array Size": size,
            "Interpolation Time (ms)": round(is_time, 5),
            "Binary Time (ms)": round(bs_time, 5),
            "Interpolation Comparisons": comp_is,
            "Binary Comparisons": comp_bs
        })

    st.table(table)
