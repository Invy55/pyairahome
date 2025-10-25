"""Pre-build script for pyairahome."""
from pathlib import Path
import pkgutil
import importlib
import importlib.util
import sys

def snake_case_to_camel_case(name):
        """Convert snake_case to CamelCase."""
        return "".join(word.title() for word in name.split("_"))

def generate_init_params(command_type, fields) -> str:
    if not fields:
        return ""
    params = []
    for field_name, field_type in fields.items():
        field_type = type(getattr(command_type(), field_name, ""))
        field_type_str = field_type.__name__
        if "." in field_type.__qualname__:
            field_type_str = "_" + field_type.__qualname__
        params.append(f"{field_name}: {field_type_str}" if field_type else field_name)
    return (", " if len(params) > 0 else "")+ ", ".join(params)

def generate_init_body(command_field, fields) -> str:
    body_lines = [f"        self._field = \"{command_field}\""]
    for field_name, field_type in fields.items():
        body_lines.append(f"self.{field_name} = {field_name}")
    return "\n        ".join(body_lines)

def generate_arguments(command_type, fields) -> str:
    if not fields:
        return ""
    args = []
    for field_name, field_type in fields.items():
        args.append(f"{field_name}=self.{field_name}")
    return ", ".join(args)

def generate_comment(command_type, fields) -> str:
    comment_lines = ["    \"\"\"", f"    `{command_type.__name__}` command.", ""]
    if len(fields) > 0:
        comment_lines.append("    ### Parameters:\n")
    for field_name, field_type in fields.items():
        field_type = type(getattr(command_type(), field_name, ""))
        comment_lines.append(f"    `{field_name}` : {field_type.__module__}.{field_type.__name__}\n")
    comment_lines[-1] = comment_lines[-1].rstrip()
    if comment_lines[-1] == "":
        comment_lines = comment_lines[:-1]
    comment_lines.append("    \"\"\"")
    return "\n".join(comment_lines)

root_dir = Path(__file__).parent.parent / "pyairahome"
pkg_dir = root_dir / "device" / "heat_pump" / "command" / "v1"
excluded = []

class_template = """\
class {class_name}(CommandBase):
{comment}
    def __init__(self{init_params}) -> None:
{init_body}
    
    @property
    def _message(self):
        return _{command}({arguments})

"""

# add pyairahome to sys.path[0]
#sys.path.insert(0, str(root_dir.parent))

command_module = importlib.import_module(f"pyairahome.device.heat_pump.command.v1.command_pb2")
commands = {}
for field, descriptor in command_module.Command.DESCRIPTOR.fields_by_name.items():
    #print(f"Field: {field}, Type: {type(getattr(command_module.Command(), field))}, Oneof: {getattr(getattr(descriptor, "containing_oneof", None), "name", None)}")
    if getattr(getattr(descriptor, "containing_oneof", None), "name", None) == "group0":
        commands[field] = type(getattr(command_module.Command(), field))

print(commands)
used_packages = {}
generated_classes = []
for command, command_type in commands.items():
    if "deprecated" in command.lower() or command in excluded:
        print(f"Skipping deprecated or excluded command: {command}")
        continue
    print(f"Command: {command}")#, Type: {command_type}, Fields: {command_type.DESCRIPTOR.fields_by_name.keys()}")
    # TODO GENERATE IMPORTS at the end

    import_fail = False
    for field_name, descriptor in command_type.DESCRIPTOR.fields_by_name.items():
        field_type = type(getattr(command_type(), field_name, None))
        if "ccv" in field_name.lower():
            print(f"CCV detected in field {field_name}, {field_type}. {field_type.__module__} and {field_type.__name__} and {field_type.__qualname__}")
        field_module = field_type.__module__
        # test import and add if success
        if field_module == "builtins":
            continue
        try:
            print(f"Importing {field_type.__module__}.{field_type.__name__}")
            try:
                print(f"Trying relative import for {field_type.__module__}")
                module = importlib.import_module("."+field_type.__module__, "pyairahome")
                field_module = "."+field_type.__module__
            except ImportError:
                print(f"Trying absolute import for {field_type.__module__}")
                module = importlib.import_module(field_type.__module__)
            #if hasattr(getattr(module, command, None), field_name):
            #    field_type = type(getattr(getattr(module, command, None), field_name))
            if not hasattr(module, field_type.__qualname__.split(".")[0]):
                raise ImportError(f"Module {field_type.__module__} does not have attribute {field_type.__name__}")
        except ImportError as e:
            print(e)
            import_fail = True
            continue

        if not field_module in used_packages:
            used_packages[field_module] = set()
        if "." in field_type.__qualname__:
            print(f"Adding qualified name {field_type.__qualname__.split('.')[0]} from module {field_module}")
            #used_packages[field_module].add(field_type.__qualname__.split(".")[0])
        else:
            print(f"Adding unqualified name {field_type.__name__} from module {field_module}")
            used_packages[field_module].add(field_type.__name__)

    init_params = generate_init_params(command_type, command_type.DESCRIPTOR.fields_by_name)
    init_body = generate_init_body(command, command_type.DESCRIPTOR.fields_by_name)
    arguments = generate_arguments(command_type, command_type.DESCRIPTOR.fields_by_name)
    comment = generate_comment(command_type, command_type.DESCRIPTOR.fields_by_name)

    if import_fail:
        print(f"!!! Skipping command {command_type.__name__} due to import failure.")
        continue

    if not "."+command_type.__module__ in used_packages:
        used_packages["."+command_type.__module__] = set()
    used_packages["."+command_type.__module__].add(command_type.__name__+" as _"+command_type.__name__)

    generated_classes.append(class_template.format(
        class_name=command_type.__name__,
        comment=comment,
        init_params=init_params,
        init_body=init_body,
        command=command_type.__name__,
        arguments=arguments
    ))

print(used_packages)

# TODO CHECK COLLISIONS IN FUTURE
imports = ["from google.protobuf.message import Message\n"]
for module_name, class_names in used_packages.items():
    imports.append(f"from {module_name} import {', '.join(class_names)}\n")

# remove pyairahome from sys.path[0]
#sys.path.pop(0)

output = ['"""Commands for interacting with Aira Home devices."""\n']
output.extend(sorted(imports, key=len, reverse=True))
output.append("\n")
output.append("""
class CommandBase:
    \"\"\"Base class for AiraHome commands. Do **NOT use this class** directly.\"\"\"
    @property
    def _message(self):
        raise NotImplementedError("You must use a subclass of pyairahome.commands, if you are seeing this message you did something wrong.")

    def get_field(self) -> str:
        return self._field

    def to_message(self) -> Message:
        return self._message
    
    def to_bytes(self) -> bytes:
        return self._message.SerializeToString()

""")

output.extend(generated_classes)

#print("".join(output))
print(root_dir / "commands.py")

with open(root_dir / "commands.py", "w", encoding="utf-8") as f:
    f.write("".join(output))