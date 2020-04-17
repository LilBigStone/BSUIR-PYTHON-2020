import os
import tempfile
import random


class ExternalSort:

    def __init__(self, count_of_number, count_of_digits, input_file, output_file):
        self.chunk = []
        self.file = input_file
        self.count_of_number = count_of_number
        self.numbers_count = count_of_digits
        self.ext_sort(output_file)

    def split_files(self, size):
        with open(self.file, 'r') as file:
            temp_array = []
            i = 1
            for digit in file:
                temp_array.append(int(digit))
                i += 1
                if i > size:
                    i = 1
                    self.merge(temp_array)
                    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_f:
                        temp_f.writelines(f'{i}\n' for i in temp_array)
                        self.chunk.append(temp_f.name)
                    temp_array = []

    def merge_file(self):
        while len(self.chunk) > 1:
            with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_f:
                with open(self.chunk[0], 'r') as first, open(self.chunk[1], 'r') as second:
                    digits_from_first = first.readline()
                    digits_from_second = second.readline()
                    while digits_from_first and digits_from_second:
                        if int(digits_from_first) <= int(digits_from_second):
                            temp_f.writelines(digits_from_first)
                            digits_from_first = first.readline()
                        else:
                            temp_f.writelines(digits_from_second)
                            digits_from_second = second.readline()

                    while digits_from_first:
                        temp_f.writelines(digits_from_first)
                        digits_from_first = first.readline()
                    while digits_from_second:
                        temp_f.writelines(digits_from_second)
                        digits_from_second = second.readline()

                    self.chunk.append(temp_f.name)

            if os.path.exists(first.name):
                self.chunk.pop(0)
                os.remove(first.name)

            if os.path.exists(second.name):
                self.chunk.pop(0)
                os.remove(second.name)

    def merge(self, array):
        if len(array) > 1:
            mid = len(array) // 2
            left_half = array[:mid]
            right_half = array[mid:]

            self.merge(left_half)
            self.merge(right_half)

            i = 0
            j = 0
            k = 0
            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    array[k] = left_half[i]
                    i = i + 1
                else:
                    array[k] = right_half[j]
                    j = j + 1
                k = k + 1

            while i < len(left_half):
                array[k] = left_half[i]
                i = i + 1
                k = k + 1

            while j < len(right_half):
                array[k] = right_half[j]
                j = j + 1
                k = k + 1

    def ext_sort(self, output_file):
        with open(self.file, 'w') as random_file:
            random_file.writelines('{}\n'.format(random.randint(-1000000, 1000000)) for _ in range(self.numbers_count))
        self.split_files(self.count_of_number)
        self.merge_file()
        with open(self.chunk[0], 'r') as temp_file:
            with open(output_file, 'w') as sorted_f:
                for line_i in temp_file:
                    sorted_f.writelines(line_i)


if __name__ == "__main__":

    main_test = ExternalSort(10, 100000, "random_digits.txt", "sorted_numbers.txt")





