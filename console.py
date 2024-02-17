#!/usr/bin/python3

"""This module is the entry point for Command Line Intepreter"""

import json
from pydoc import classname
import re
from cmd import Cmd
from models.base_model import BaseModel
from models import storage


class HBNBCommand(Cmd):
    """Class for the Command Line Interpreter (CLI)"""

    prompt = "(hbnb) "

    def _precmd(self, line):
        """Tests class.syntax() commands """
        it = re.search(r"^(\w*)\.(w+)(?:\(([^]*)\))$", line)
        if not it:
            return line
        classname = it.group(1)
        mthd = it.group(2)
        args = it.group(3)
        uid_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if uid_args:
            u = uid_args.group(1)
            a_d = uid_args.group(2)
        else:
            u = args
            a_d = False

        a_d = ""
        if mthd is "update" and a_d:
            b = re.search('^({.*})$', a_d)
            if b:
                self.updict(classname, u, b.group(1))
                return ""
            c = re.search('^(?:"([^"]*)")?(?:, (.*))?$', a_d)
            if c:
                a_val = (c.group(1) or "") + " " + (c.group(2) or "")
            com = mthd + " " + classname + " " + u + " " + a_val
            self.onecmd(com)

            return com

    def default(self, line):
        """Once nothing matches, this method catchs it"""
        self._precmd(line)

    def do_all(self, line):
        """Prints all __str__"""
        if line is not "":
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class does not exist **")
            else:
                nil = [str(a) for key, a in storage.all().items()
                       if type(a).__name__ == words[0]]
                print(nil)
        else:
            b_list = [str(a) for key, a in storage.all().items()]
            print(b_list)

    def do_count(self, line):
        """Counts the instances of a class"""
        count = line.split(' ')
        if not count[0]:
            print("** class name missing **")
        elif count[0] not in storage.classes():
            print("** class does not exist **")
        else:
            does = [
                b for b in storage.all() if b.startswith(
                    count[0] + '.')
            ]
            print(len(count))

    def do_create(self, line):
        """Creates the instance"""
        if line is "" or line is None:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class does not exist **")
        else:
            y = storage.classes()[line]()
            y.save()
            print(y.id)

    def do_destroy(self, line):
        """Deletes instance based on id and class name"""
        if line is "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class does not exist **")
            elif len(words) > 2:
                print("** instance id missing **")
            else:
                ki = "{}.{}".format(words[0], words[1])
                if ki not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[ki]
                    storage.save()

    def do_EOF(self, line):
        """End of File handler"""
        print()
        return True

    def do_quit(self, line):
        """Exits program"""
        return True

    def do_show(self, line):
        """Prints __str__"""
        if line is "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** instance id missing **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                ki = "{}.{}".format(words[0], words[1])
                if ki not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[ki])

    def do_update(self, line):
        """Updates instance attributes"""
        if line is "" or line is None:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        a = re.search(rex, line)
        clsname = a.group(1)
        u = a.group(2)
        attr = a.group(3)
        val = a.group(4)
        if not a:
            print("** class name missing **")
        elif clsname not in storage.classes():
            print("** class does not exist **")
        elif u is None:
            print("** instance is missing **")
        else:
            ki = "{}.{}".format(clsname, u)
            if ki not in storage.all():
                print("** no instance found **")
            elif not attr:
                print("** attribute name missing **")
            elif not val:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', val):
                    if '.' in val:
                        cast = float
                    else:
                        cast = int
                else:
                    val = val.replace('"', '')
                atts = storage.attributes()[clsname]
                if attr in atts:
                    val = atts[attr](val)
                elif cast:
                    try:
                        val = cast(val)
                    except ValueError:
                        pass
                    setattr(storage.all()[ki], attr, val)
                    storage.all()[ki].save()

    def emptyline(self):
        """Does not do anything when ENTER key pressed"""
        pass

    def updict(self, clsname, u, st):
        """Updates dictionary, which helps update() method"""
        a = st.replace("'", '"')
        b = json.loads(a)
        if not clsname:
            print("** class name missing **")
        elif clsname not in storage.classes():
            print("** class does not exist **")
        elif u is None:
            print("** instance id missing **")
        else:
            ki = "{}.{}".format(clsname, u)
            if ki not in storage.all():
                print("** no instance found **")
            else:
                atts = storage.attributes()[clsname]
                for attr, val in b.items():
                    if attr in atts:
                        val = atts[attr](val)
                    setattr(storage.all()[ki], attr, val)
                storage.all()[ki].save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()