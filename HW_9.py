contacts = {
            'Nazar': '0931236985',
            'Max': '0669312654',
            'Ola': '0953147622',
            'Vitaliy': '0993453321',
            'Polina': '0983645963',
            'Mariya': '0974523658',
            'Daniel': '0998763201',
            'Kate': '0660632148',
            'Victoriya': '0993264152',
            'Yuriy': '0936631254'
            }


def input_error(input):
    def wrapper(*args, **kwargs):
        try:
            return input(*args, **kwargs)
        except KeyError:
            print("I don't have this contact name")
        except ValueError:
            print("Give me name and phone please'")
        except IndexError:
            print("Error, please follow the correct input format")
    return wrapper


def hello_func():
    return print("Hello, how can I help you?")


@input_error
def add_func(input):
    name = input[1].capitalize()
    phone = input[2]
    contacts[name] = phone
    return print('Phone number has been successfully added.')


@input_error
def change_func(input):
    name = input[1].capitalize()
    phone = input[2]
    if name not in contacts.keys():
        return print('Error. No contact with this name.')
    else:
        contacts[name] = phone
        return print('Phone number has been successfully changed.')


@input_error
def phone_func(input):
    name = input[1].capitalize()
    return print(contacts[name])


def all_func():
    for name, number in contacts.items():
        print(f'{name}: {number}')


def exit_func():
    return 'Good bye!'

COMMANDS = {
            'hello': hello_func,
            'add': add_func,
            'change': change_func,
            'phone': phone_func,
            'show all': all_func,
            'exit': exit_func
            }


def get_handler(command):
    return COMMANDS[command]

def main():

    stop_words = ['good bye', 'close', 'exit', '.']
    simple_command = ['hello', 'show all']
    commands_with_arg = ['add', 'change', 'phone']

    while True:

        user_input = input('Please, enter your command: ').casefold()
        split_input = user_input.split(" ")

        if user_input in stop_words:
            print(get_handler('exit')())
            break

        elif user_input in simple_command:
            get_handler(user_input)()

        elif len(split_input) <= 3 and split_input[0] in commands_with_arg:
            (get_handler(split_input[0])(split_input))

        else:
            print('Invalid command or input format. Try again.')


if __name__ == '__main__':
    main()
