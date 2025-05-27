"""
@Author = 'Mike Stanley'

Allows wmul_file_manager to be run as a service. 


============ Change Log ============
2025-May-22 = Created.

============ License ============
The MIT License (MIT)

Copyright (c) 2025 Michael Stanley

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader
import yaml
from dataclasses import dataclass
from wmul_file_manager.ArgumentBase import ArgumentBase
from wmul_file_manager.BulkCopier import BulkCopier as BulkCopier

_services_available: dict[str, type[ArgumentBase]] = {
    "bulkcopier": BulkCopier 
}


def create_services_from_dict(configuration_dict: dict[str, dict]):
    services: dict[str, ArgumentBase] = {}
    for inventory_name, service_configuration_dict in configuration_dict.items():
        try:
            _validate_service_configuration_dict(service_configuration_dict)
            for service_type, service_arguments in service_configuration_dict.items():
                service_constructor = _get_service_constructor(service_type)
                services[inventory_name] = service_constructor(**service_arguments)
        except ValueError as ve:
            raise ValueError(f"Service: {inventory_name} has an incorrect configuration.") from ve
    return services


def _validate_service_configuration_dict(service_configuration_dict) -> bool:
    if not isinstance(service_configuration_dict, dict):
        raise ValueError(
                f"The configuration for the service requires a dictionary type. Instead, it received Type: "
                f"'{type(service_configuration_dict)}', {service_configuration_dict} ."
            )
    if (count_of_function_names := len(service_configuration_dict)) != 1:
        raise ValueError(
                f"The configuration for the service does not have the correct number of function names. There "
                f"must be exactly one function name per service. This entry has {count_of_function_names}: "
                f"{list(service_configuration_dict.keys())} ."
            )
    return True


def _get_service_constructor(service_type: str) -> type[ArgumentBase]:
    try:
        return _services_available[service_type.casefold()]
    except KeyError:
        raise ValueError(
            f"The service wants service type '{service_type}', but there is no service available "
            f"with that type. The available services are: {list(_services_available.keys())}"
        )

        



@dataclass
class FileManagerService:
    config_filename: str

    def _load_config_from_file(self) -> dict[str, dict]:
        with open(self.config_filename) as config_file:
            return yaml.load(config_file.read(), SafeLoader)

    def service_loop(self):
        configuration_dict = self._load_config_from_file()
        services = create_services_from_dict(configuration_dict=configuration_dict)
        for inventory_name, service in services.items():
            pass

        
