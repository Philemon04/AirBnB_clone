#!/usr/bin/python3
"""Class that implements cmd lib"""
import cmd
import shlex

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"BaseModel": BaseModel, "Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class HBNBCommand(cmd.Cmd):
    """Console for shell."""
    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Quit command to exit the program.
        """
        print()
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program.
        """
        return True

    def do_create(self, args):
        """Create a new class instance and print its id.
        """
        arg = args.split()

        if len(arg) <= 0:
            print('** class name missing **')

        elif arg[0] in classes:
            for key, value in classes.items():
                if arg[0] == key:
                    new_instance = value()
                    print(new_instance.id)
                    new_instance.save()
        else:
            print("** class doesn't exist **")

    def do_show(self, args):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of
        a given id.
        """

        arg = args.split()
        new_dict = storage.all()
        if len(arg) == 0:
            print('** class name missing **')
        elif arg[0] not in classes:
            print("** class doesn't exist **")
        elif arg[0] in classes:
            if arg[0] + "." + arg[1] in new_dict:
                print(new_dict[arg[0] + "." + arg[1]])
            else:
                print("** no instance found **")
        else:
            print('** instance id missing **')

    def do_destroy(self, args):
        """Delete a class instance of a given id.
        """
        arg = args.split()
        new_dict = storage.all()
        if len(arg) <= 0:
            print('** class name missing **')
        elif arg[0] not in classes:
            print("** class doesn't exist **")
        elif arg[0] in classes:
            if len(arg) < 2:
                print('** instance id missing **')
            elif arg[0] + "." + arg[1] in new_dict:
                storage.all().pop(arg[0] + "." + arg[1])
                storage.save()
            else:
                print("** no instance found **")


    def do_all(self, args):
        """Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated
        objects.
        """
        arg = args.split
        new_dict = storage.all()
        all_instance = []
        if arg in classes:
            if arg[0] + "." + arg[1] in new_dict:
                print(new_dict[arg[0] + "." + arg[1]])
        elif len(args) == 0:
            for key in new_dict:
                all_instance.append(new_dict[key].__str__())
            print(all_instance)
        else:
            print("** class doesn't exist **")

    def do_update(self, args):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value
        >) or <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.
        """
        arg = args.split()
        new_dict = storage.all()
        if len(arg) <= 0:
            print('** class name missing **')
        elif arg[0] not in classes:
            print("** class doesn't exist **")
        elif len(arg) < 2:
            print("** instance id missing **")
        elif arg[0] + "." + arg[1] not in new_dict:
            print("** no instance found **")
        elif len(arg) < 3:
            print("** attribute name missing **")
        elif len(arg) < 4:
            print("** value missing **")
        else:
            k = arg[0] + "." + arg[1]
            attr = arg[2]
            v = arg[3].replace("'", "")
            v = v.replace('"', '')
            instance = new_dict[k]
            if hasattr(instance, attr) and type(getattr(instance, attr)) is int:
                if v.isnumeric():
                    v = int(v)
            elif hasattr(instance, attr) and type(getattr(instance, attr)) is float:
                idk = v.split(".")
                if idk[0].isnumeric() and idk[1].isnumeric():
                    v = float(v)
            setattr(storage.all()[k], attr, v)
            storage.all()[k].save()

    def do_count(self, args):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class.
        """
        arg = args.split()
        all_dict = storage.all()
        count = 0
        if len(arg) <= 0:
            print('** class name missing **')
        elif arg[0] not in classes:
            print("** class doesn't exist **")
        else:
            for a in all_dict:
                if all_dict[a].__class__.__name__ == args[0]:
                    count += 1
        print(count)

    def default(self, line):
        """default method to use with command()"""
        arg = line.split('.')
        if len(arg) >= 2:
            if arg[1].count('()') == 1:
                clas_name = arg[0]
                a = arg[1].replace('(', '.')
                b = a.replace(')', '.')
                c = b.split('.')
                command = c[0]
                line = str(command + ' ' + clas_name)
            elif arg[1].count('(') == 1 and arg[1].count(')') == 1:
                arguments = ""
                clas_name = arg[0]
                a = arg[1].replace('(', '.')
                b = a.replace(')', '.')
                c = b.split('.')
                command = c[0]
                args = shlex.split(c[1], '"')
                for wrd in args:
                    arguments = arguments + wrd

                d = str(command + ' ' + clas_name + ' ' + arguments)
                line = d.replace(',', ' ')
                print(line)

        return line



if __name__ == '__main__':
    HBNBCommand().cmdloop()
