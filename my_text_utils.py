def permute(elements, n=None):
    elements = list(elements)
    if n is None:
        n = len(elements)

    perms = []
    if n == 1:
        perms.append(elements[:])
    else:
        for i in range(n-1):
            perms += permute(elements, n - 1)
            if even(n):
                swap(elements, i, n - 1)
            else:
                swap(elements, 0, n - 1)
        perms += permute(elements, n - 1)
    return perms


def combinations(elements, n=None):
    pass


def swap(A, n, m):
    A[n], A[m] = A[m], A[n]


def even(n):
    return n % 2 == 0


def test_permute():
    items = 'abc'
    print(f"permute: {items}")
    for val in permute(list(items)):
        print(f"{val}")


if __name__ == '__main__':
    test_permute()
