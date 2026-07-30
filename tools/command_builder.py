"""Pre-build script for pyairahome."""
from google.protobuf.descriptor import FieldDescriptor
from pathlib import Path
import importlib

def snake_case_to_camel_case(name):
        """Convert snake_case to CamelCase."""
        return "".join(word.title() for word in name.split("_"))

def is_repeated_message_field(command_type, field_name) -> bool:
    """True for repeated composite (message) fields (e.g. google._upb._message.RepeatedCompositeContainer)"""
    descriptor = command_type.DESCRIPTOR.fields_by_name[field_name]
    return descriptor.label == FieldDescriptor.LABEL_REPEATED and descriptor.type == FieldDescriptor.TYPE_MESSAGE

def get_oneof_groups(command_type) -> dict:
    # map oneof with at least 2 members
    groups = {}
    for field_name, descriptor in command_type.DESCRIPTOR.fields_by_name.items():
        oneof = getattr(descriptor, "containing_oneof", None)
        if oneof is not None:
            groups.setdefault(oneof.name, []).append(field_name)
    return {name: members for name, members in groups.items() if len(members) > 1}

def generate_init_params(command_type, fields, oneof_groups) -> str:
    if not fields:
        return ""
    oneof_fields = {f for members in oneof_groups.values() for f in members}
    required_params = []
    optional_params = []
    for field_name, field_type in fields.items():
        if is_repeated_message_field(command_type, field_name):
            field_type_str = "Iterable[Message]"
        else:
            field_type = type(getattr(command_type(), field_name, ""))
            field_type_str = field_type.__name__
            if "." in field_type.__qualname__:
                field_type_str = "_" + field_type.__qualname__
        if field_name in oneof_fields:
            optional_params.append(f"{field_name}: {field_type_str} | None = None" if field_type else f"{field_name}=None")
        else:
            required_params.append(f"{field_name}: {field_type_str}" if field_type else field_name)
    params = required_params + optional_params
    return (", " if len(params) > 0 else "")+ ", ".join(params)

def generate_init_body(command_field, fields) -> str:
    body_lines = [f"        self._field = \"{command_field}\""]
    for field_name, field_type in fields.items():
        body_lines.append(f"self.{field_name} = {field_name}")
    return "\n        ".join(body_lines)

def generate_message_body(command_type, fields, oneof_groups) -> str:
    # check that at least one argument is passed since now oneof fields are not required, but at least one of them must be provided
    oneof_fields = {f for members in oneof_groups.values() for f in members}
    kwargs_parts = [f"{f}=self.{f}" for f in fields if f not in oneof_fields]
    lines = []
    for oneof_name, members in oneof_groups.items():
        var_name = f"_{oneof_name}_args"
        members_dict = ", ".join(f"\"{m}\": self.{m}" for m in members)
        lines.append(f"        {var_name} = {{k: v for k, v in {{{members_dict}}}.items() if v is not None}}")
        lines.append(f"        if len({var_name}) != 1:")
        names = ", ".join(repr(m) for m in members)
        lines.append(f"            raise ValueError(\"Exactly one of {names} must be provided for {command_type.__name__}.\")")
        kwargs_parts.append(f"**{var_name}")
    lines.append(f"        return _{command_type.__name__}({', '.join(kwargs_parts)})")
    return "\n".join(lines)

def generate_comment(command_type, fields) -> str:
    comment_lines = ["    \"\"\"", f"    `{command_type.__name__}` command.", ""]
    if len(fields) > 0:
        comment_lines.append("    ### Parameters:\n")
    for field_name, field_type in fields.items():
        if is_repeated_message_field(command_type, field_name):
            comment_lines.append(f"    `{field_name}` : Iterable[Message]\n")
            continue
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
{message_body}

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
uses_iterable = False
for command, command_type in commands.items():
    if "deprecated" in command.lower() or command in excluded:
        print(f"Skipping deprecated or excluded command: {command}")
        continue
    print(f"Command: {command}")#, Type: {command_type}, Fields: {command_type.DESCRIPTOR.fields_by_name.keys()}")
    # TODO GENERATE IMPORTS at the end

    import_fail = False
    for field_name, descriptor in command_type.DESCRIPTOR.fields_by_name.items():
        if is_repeated_message_field(command_type, field_name):
            uses_iterable = True
            continue
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

    oneof_groups = get_oneof_groups(command_type)
    init_params = generate_init_params(command_type, command_type.DESCRIPTOR.fields_by_name, oneof_groups)
    init_body = generate_init_body(command, command_type.DESCRIPTOR.fields_by_name)
    message_body = generate_message_body(command_type, command_type.DESCRIPTOR.fields_by_name, oneof_groups)
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
        message_body=message_body
    ))

print(used_packages)

# TODO CHECK COLLISIONS IN FUTURE
imports = ["from google.protobuf.message import Message\n"]
if uses_iterable:
    imports.append("from typing import Iterable\n")
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