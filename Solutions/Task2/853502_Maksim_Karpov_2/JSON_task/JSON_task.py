import re

class Company:

    def __init__(self, second_name, first_name, patronymic_name):

        self.EployeeInfo = {
            "First_name": first_name,
            "Second_name": second_name,
            "Patronymic_name": patronymic_name,
            "Married": True,
            "Kids": False,
            "Kids_Name": None,
            "Company_Name": "Zhodinsky_milkdairy_plant",
            "Company_Phone": [(375, 29), 228, 14, 88],

        }

    def get_company_info(self):
        return self.EployeeInfo


class JSON:

    def __init__(self, obj):
        self.obj = obj
        self.json_string = self.encode(obj)

    def encode(self, obj):

        json_string = ''

        if isinstance(obj, int):
            if obj is True:
                return 'true'
            elif obj is False:
                return 'false'
            else:
                return str(obj)
        elif obj is None:
            return 'null'
        elif isinstance(obj, str):
            return '"{}"'.format(obj)
        elif isinstance(obj, list):
            json_string += '['
            for element in obj:
                json_string += self.encode(element)
                json_string += ', '
            json_string = json_string[0:-2]
            json_string += ']'
            return json_string
        elif isinstance(obj, dict):
            json_string += '{'
            for key, value in obj.items():
                json_string += self.encode(key)
                json_string += ': '
                json_string += self.encode(value)
                json_string += ', '
            json_string = json_string[0:-2]
            json_string += '}'
            return json_string
        elif isinstance(obj, tuple):
            json_string += '('
            for element in obj:
                json_string += self.encode(element)
                json_string += ', '

            json_string = json_string[0:-2]
            json_string += ')'
            return json_string
        else:
            return self.encode(obj.__dict__)

    def to_json(self):
        return self.json_string

    def from_json(self, json_string):
        regular_string = re.findall(r'\w+|[{\[\]]', json_string)
        iterator_json_string = iter(regular_string)
        return self.decode(iterator_json_string)

    def decode(self, iterator_string):
        next_symbol = next(iterator_string)
        if next_symbol == "{":
            python_dict = {}
            while True:
                try:
                    key = self.decode(iterator_string)
                    python_dict[key] = self.decode(iterator_string)
                except StopIteration:
                    return python_dict
        elif next_symbol == "[":
            python_list = []
            while True:
                next_list_value = self.decode(iterator_string)
                if next_list_value == ']':
                    return python_list
                else:
                    python_list.append(next_list_value)

        elif next_symbol.isdigit():
            return int(next_symbol)
        elif next_symbol == 'null':
            return None
        elif next_symbol == 'true':
            return True
        elif next_symbol == 'false':
            return False
        else:
            return next_symbol


# if __name__ == '__main__':
#     person = Company("Karpov", "Maksim", "Konstantinovich")
#     json_task = JSON(person)
#     print("Python object: ", person.__dict__)
#     print("Json string: ", json_task.to_json())
#     print("Python Object:", json_task.from_json(json_task.to_json()))