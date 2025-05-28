"""
@Author = 'Mike Stanley'

============ Change Log ============
2025-May-27 = Created.

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
import pytest
from pathlib import Path
from wmul_file_manager.AsAService import InventoryService, create_services_from_dict
from wmul_file_manager.BulkCopier import BulkCopier
from wmul_test_utils import make_namedtuple


@pytest.fixture(scope="function")
def setup_one_inventory():
    temp_1 = Path("C:\\Temp_1")
    temp_2 = Path("C:\\Temp_2")
    destination = Path("C:\\Destination")
    inventory_name = "Thing_1"

    configuration_dict_contents = { 
        inventory_name: {
            "bulkcopier": {
                "source_directories": [
                    temp_1,
                    temp_2
                ],
                "destination_directory": destination,
                "exclude_suffixes_list": [
                    ".sfk",
                    ".pk"
                ],
                "ignore_directories": [
                    Path("C:\\Temp_1\\BadDir")
                ],
                "force_copy_flag": False,
                "delete_old_files_flag": True
            }
        }
    }

    expected_source_directories = [temp_1, temp_2]

    result_services = create_services_from_dict(configuration_dict=configuration_dict_contents)

    return make_namedtuple(
        "setup_one_inventory",
        result_services=result_services,
        expected_inventory_name=inventory_name,
        expected_source_directories=expected_source_directories,
        expected_destination_directory=destination
    )

def test_one_services_is_list(setup_one_inventory):
    assert isinstance(setup_one_inventory.result_services, list)

def test_one_services_len_is_one(setup_one_inventory):
    assert len(setup_one_inventory.result_services) == 1

def test_one_thing_1_is_inventory_service(setup_one_inventory):
    thing_1 = setup_one_inventory.result_services[0]
    assert isinstance(thing_1, InventoryService)

def test_one_thing_1_has_correct_inventory_name(setup_one_inventory):
    thing_1 = setup_one_inventory.result_services[0]
    expected_inventory_name = setup_one_inventory.expected_inventory_name
    assert thing_1.inventory_name == expected_inventory_name

def test_one_thing_1_run_forever_false(setup_one_inventory):
    thing_1 = setup_one_inventory.result_services[0]
    assert not thing_1.run_forever

def test_one_thing_1_service_is_bulk_copier(setup_one_inventory):
    thing_1_service = setup_one_inventory.result_services[0].service
    assert isinstance(thing_1_service, BulkCopier)

def test_one_thing_1_service_has_source_directories(setup_one_inventory):
    thing_1_service = setup_one_inventory.result_services[0].service
    assert thing_1_service.source_directories == setup_one_inventory.expected_source_directories

def test_one_thing_1_servic_has_destination_directory(setup_one_inventory):
    thing_1_service = setup_one_inventory.result_services[0].service
    assert thing_1_service.destination_directory == setup_one_inventory.expected_destination_directory


@pytest.fixture(scope="function")
def setup_two_inventory():
    temp_1 = Path("C:\\Temp_1")
    temp_2 = Path("C:\\Temp_2")
    destination = Path("C:\\Destination")

    temp_3 = Path("C:\\Temp_3")
    temp_4 = Path("C:\\Temp_4")
    destination_2 = Path("C:\\Destination_2")

    inventory_name_1 = "Thing_1"
    inventory_name_2 = "Thing_2"

    configuration_dict_contents = { 
        inventory_name_1: {
            "bulkcopier": {
                "source_directories": [
                    temp_1,
                    temp_2
                ],
                "destination_directory": destination,
                "exclude_suffixes_list": [
                    ".sfk",
                    ".pk"
                ],
                "ignore_directories": [
                    Path("C:\\Temp_1\\BadDir")
                ],
                "force_copy_flag": False,
                "delete_old_files_flag": True
            }
        },
        inventory_name_2: {
            "bulkcopier": {
                "run_forever": True,
                "source_directories": [
                    temp_3,
                    temp_4
                ],
                "destination_directory": destination_2,
                "exclude_suffixes_list": [
                    ".sfk",
                    ".pk"
                ],
                "ignore_directories": [
                    Path("C:\\Temp_3\\NoDir")
                ],
                "force_copy_flag": False,
                "delete_old_files_flag": True
            }
        }
    }

    thing_1_expected_source_directories = [temp_1, temp_2]
    thing_2_expected_source_directories = [temp_3, temp_4]

    result_services = create_services_from_dict(configuration_dict=configuration_dict_contents)
    
    return make_namedtuple(
        "setup_one_inventory",
        result_services=result_services,
        thing_1_expected_inventory_name=inventory_name_1,
        thing_2_expected_inventory_name=inventory_name_2,
        thing_1_expected_source_directories=thing_1_expected_source_directories,
        thing_1_expected_destination_directory=destination,
        thing_2_expected_source_directories=thing_2_expected_source_directories,
        thing_2_expected_destination_directory=destination_2
    )

def test_two_services_is_list(setup_two_inventory):
    assert isinstance(setup_two_inventory.result_services, list)

def test_two_services_len_is_two(setup_two_inventory):
    assert len(setup_two_inventory.result_services) == 2

def test_two_thing_1_is_inventory_service(setup_two_inventory):
    thing_1 = setup_two_inventory.result_services[0]
    assert isinstance(thing_1, InventoryService)

def test_two_thing_1_has_correct_inventory_name(setup_two_inventory):
    thing_1 = setup_two_inventory.result_services[0]
    expected_inventory_name = setup_two_inventory.thing_1_expected_inventory_name
    assert thing_1.inventory_name == expected_inventory_name

def test_two_thing_1_run_forever_false(setup_two_inventory):
    thing_1 = setup_two_inventory.result_services[0]
    assert not thing_1.run_forever

def test_two_thing_1_service_is_bulkcopier(setup_two_inventory):
    thing_1_service = setup_two_inventory.result_services[0].service
    assert isinstance(thing_1_service, BulkCopier)

def test_two_thing_1_service_has_source_directories(setup_two_inventory):
    thing_1_service = setup_two_inventory.result_services[0].service
    assert thing_1_service.source_directories == setup_two_inventory.thing_1_expected_source_directories

def test_two_thing_1_service_has_destination_directory(setup_two_inventory):
    thing_1_service = setup_two_inventory.result_services[0].service
    assert thing_1_service.destination_directory == setup_two_inventory.thing_1_expected_destination_directory

def test_two_thing_2_is_inventory_service(setup_two_inventory):
    thing_2 = setup_two_inventory.result_services[1]
    assert isinstance(thing_2, InventoryService)

def test_two_thing_2_has_correct_inventory_name(setup_two_inventory):
    thing_2 = setup_two_inventory.result_services[1]
    expected_inventory_name = setup_two_inventory.thing_2_expected_inventory_name
    assert thing_2.inventory_name == expected_inventory_name

def test_two_thing_2_run_forever_false(setup_two_inventory):
    thing_2 = setup_two_inventory.result_services[1]
    assert thing_2.run_forever

def test_two_thing_2_service_is_bulkcopier(setup_two_inventory):
    thing_2_service = setup_two_inventory.result_services[1].service
    assert isinstance(thing_2_service, BulkCopier)

def test_two_thing_2_has_source_directories(setup_two_inventory):
    thing_2_service = setup_two_inventory.result_services[1].service
    assert thing_2_service.source_directories == setup_two_inventory.thing_2_expected_source_directories

def test_two_thing_2_has_destination_directory(setup_two_inventory):
    thing_2_service = setup_two_inventory.result_services[1].service
    assert thing_2_service.destination_directory == setup_two_inventory.thing_2_expected_destination_directory
