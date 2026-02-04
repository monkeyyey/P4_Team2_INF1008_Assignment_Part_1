import random
import timeit


def counting_sort(input):
    if not input:
        return []

    input_length = len(input)
    max_val = max(input)

    count = [0] * (max_val + 1)

    # get count of values
    for value in input:
        count[value] += 1

    # get sums of counts until idx
    for idx in range(1, max_val + 1):
        count[idx] += count[idx - 1]

    output = [0] * input_length

    for idx in range(input_length - 1, -1, -1):
        value = input[idx]
        output[count[value] - 1] = value
        count[value] -= 1

    return output


# lists for the sorted values
normal_counting_sort_correct = []
n_squared_counting_sort_correct = []


def normal_counting_sort(max_value):
    input = [random.randint(0, max_value) for _ in range(max_value)]
    print(f"Input list: {input}")
    output = counting_sort(input)
    print(f"Output list: {output}")
    normal_counting_sort_correct.append({"input": input, "output": output})


def n_squared_counting_sort(max_value):
    input = [random.randint(0, max_value * max_value)
             for _ in range(max_value)]
    print(f"Input list: {input}")
    output = counting_sort(input)
    print(f"Output list: {output}")
    n_squared_counting_sort_correct.append({"input": input, "output": output})

# test if sorted values correctly


def test_correctness(list_of_tests):
    correct = 0
    for test in list_of_tests:
        correct_sort = sorted(test["input"])
        if test["output"] == correct_sort:
            correct += 1

    return correct


if __name__ == "__main__":
    max_value = 1000
    num_rounds = 100

    normal = timeit.timeit("normal_counting_sort(1000)",
                           "from __main__ import normal_counting_sort", number=num_rounds)
    n_squared = timeit.timeit("n_squared_counting_sort(1000)",
                              "from __main__ import n_squared_counting_sort", number=num_rounds)

    print("\ncalculating...")
    normal_correctness = test_correctness(normal_counting_sort_correct)
    n_squared_correctness = test_correctness(n_squared_counting_sort_correct)

    print("\ndone calculating")
    print(f"n (average): {normal:.2f} seconds")
    print(f"n squared (average): {n_squared:.2f} seconds")
    print(
        f"n squared took around {(n_squared/normal):.2f} times longer than n")

    print(f"\nn correct: {normal_correctness}/{num_rounds}")
    print(f"n squared correct: {n_squared_correctness}/{num_rounds}")
