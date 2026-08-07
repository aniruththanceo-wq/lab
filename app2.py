import streamlit as st
import random
import time

st.set_page_config(page_title="Experiment 2", page_icon="🔍")

st.title("Experiment 2 - String Pattern Matching Algorithms")


def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    matches = []
    comparisons = 0

    for i in range(n - m + 1):
        j = 0

        while j < m:
            comparisons += 1

            if text[i + j] != pattern[j]:
                break

            j += 1

        if j == m:
            matches.append(i)

    return matches, comparisons


def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m

    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1

        elif length != 0:
            length = lps[length - 1]

        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)

    matches = []
    comparisons = 0

    i = 0
    j = 0

    while i < n:
        comparisons += 1

        if pattern[j] == text[i]:
            i += 1
            j += 1

            if j == m:
                matches.append(i - j)
                j = lps[j - 1]

        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches, comparisons


def rabin_karp(text, pattern, q=101):
    n, m = len(text), len(pattern)

    d = 256
    h = pow(d, m - 1, q)

    p_hash = 0
    t_hash = 0

    matches = []
    comparisons = 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for s in range(n - m + 1):

        if p_hash == t_hash:
            for k in range(m):
                comparisons += 1

                if text[s + k] != pattern[k]:
                    break

            else:
                matches.append(s)

        if s < n - m:
            t_hash = (
                d * (t_hash - ord(text[s]) * h)
                + ord(text[s + m])
            ) % q

            if t_hash < 0:
                t_hash += q

    return matches, comparisons


st.write("### Sample Text")

default_text = "AABAACAADAABAABA"
default_pattern = "AABA"

text = st.text_input("Enter Text", value=default_text)
pattern = st.text_input("Enter Pattern", value=default_pattern)

if st.button("Search"):

    naive_matches, naive_comp = naive_search(text, pattern)
    kmp_matches, kmp_comp = kmp_search(text, pattern)
    rk_matches, rk_comp = rabin_karp(text, pattern)

    st.write("### Results")

    st.table([
        {
            "Algorithm": "Naive",
            "Matches": str(naive_matches),
            "Comparisons": naive_comp
        },
        {
            "Algorithm": "KMP",
            "Matches": str(kmp_matches),
            "Comparisons": kmp_comp
        },
        {
            "Algorithm": "Rabin-Karp",
            "Matches": str(rk_matches),
            "Comparisons": rk_comp
        }
    ])

st.write("---")

if st.button("Run Performance Analysis"):

    st.write("### Performance Analysis")

    text_large = "".join(random.choices("ABCD", k=10000))

    patterns = [
        "AB",
        "ABCD",
        "ABCDAB",
        "ABCDABCD"
    ]

    table = []

    for p in patterns:

        start = time.perf_counter()
        for _ in range(100):
            _, naive_comp = naive_search(text_large, p)
        naive_time = (time.perf_counter() - start) / 100 * 1000

        start = time.perf_counter()
        for _ in range(100):
            _, kmp_comp = kmp_search(text_large, p)
        kmp_time = (time.perf_counter() - start) / 100 * 1000

        start = time.perf_counter()
        for _ in range(100):
            _, rk_comp = rabin_karp(text_large, p)
        rk_time = (time.perf_counter() - start) / 100 * 1000

        table.append({
            "Pattern": p,
            "Naive Time (ms)": round(naive_time, 5),
            "KMP Time (ms)": round(kmp_time, 5),
            "RK Time (ms)": round(rk_time, 5),
            "Naive Comparisons": naive_comp,
            "KMP Comparisons": kmp_comp,
            "RK Comparisons": rk_comp
        })

    st.table(table)