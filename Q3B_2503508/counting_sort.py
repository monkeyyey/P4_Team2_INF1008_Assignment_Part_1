import random


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


if __name__ == "__main__":
    max_value = 1000
    input = [random.randint(0, max_value) for _ in range(max_value)]
    print(f"Input list: {input}")
    output = counting_sort(input)
    print(f"Output list: {output}")
