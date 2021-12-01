
# def sliding_window_sum(nums, size=3):
#     for i in range(size, len(nums) + 1):
#         yield sum(nums[i - size:i])

def sliding_window_sum(nums, size=3):
    total = sum(nums[:size - 1])
    for i in range(size - 1, len(nums)):
        total += nums[i]
        yield total
        total -= nums[i - size + 1]

def num_inc(nums):
    prev = None
    count = 0
    for num in nums:
        if prev is not None and num > prev:
            count += 1
        prev = num

    return count

if __name__ == "__main__":
    nums = [
        199,
        200,
        208,
        210,
        200,
        207,
        240,
        269,
        260,
        263
    ]
    print(num_inc(nums))

    print('--- Part1 ---')
    with open('input1.txt') as f:
        nums = list(map(int, f.readlines()))
    
    print(num_inc(nums))

    print('---- Part 2 -----')
    print(num_inc(sliding_window_sum(nums)))