"""Command utilities for the Aira Home library."""
# utils/commands.py
import importlib
import pkgutil


class CommandUtils:
    @staticmethod
    def camel_case_to_snake_case(name):
        """Convert CamelCase to snake_case."""
        return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")

    @staticmethod
    def snake_case_to_camel_case(name):
        """Convert snake_case to CamelCase."""
        return "".join(word.title() for word in name.split("_"))

    @staticmethod
    def find_in_modules(package_name):
        # Import the package dynamically
        package = importlib.import_module(package_name)
        
        # Get the package"s path
        package_path = package.__path__
        
        # Iterate over submodules
        commands = []
        for _, module_name, is_pkg in pkgutil.iter_modules(package_path):
            if not is_pkg and not "grpc" in module_name:
                command = CommandUtils.snake_case_to_camel_case(module_name)[:-3]  # Remove the trailing "_pb2"
                if command == "Command":
                    continue
                
                commands.append(command)

        return commands

    @staticmethod
    def get_message_field(command, package_name, raw: bool = False):
        # Convert command name to snake_case for the file name
        command_file = CommandUtils.camel_case_to_snake_case(command) + "_pb2"

        # Import the command module dynamically
        module = importlib.import_module(f"{package_name}.{command_file}")
        # Get the command class
        fields = []
        for item in dir(module):
            if not item.isupper() and "_" not in item:
                # Get command fields
                descriptor = getattr(module, item).DESCRIPTOR
                if hasattr(descriptor, "fields_by_name"):
                    for field_name, field_type in descriptor.fields_by_name.items():
                        field_data = {
                            "name": field_name,
                            "type": type(getattr(getattr(module, item)(), field_name)) if raw else type(getattr(getattr(module, item)(), field_name)).__name__,
                            "full_name": field_type.full_name,
                            "repeated": field_type.is_repeated,
                            "required": field_type.is_required,
                            "index": field_type.index,
                            "oneof": None
                        }
                        if hasattr(field_type, "containing_oneof") and field_type.containing_oneof is not None:
                            field_data["oneof"] = field_type.containing_oneof.full_name
                        fields.append(field_data)
        return fields