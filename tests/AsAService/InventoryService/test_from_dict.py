"""
@Author = 'Mike Stanley'

============ Change Log ============
2025-May-28 = Created.

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
from dataclasses import dataclass
from enum import Enum
from wmul_file_manager.AsAService import InventoryService
from wmul_test_utils import make_namedtuple, generate_combination_matrix_from_dataclass


class RunForeverValue(Enum):
    NotSet = 0
    SetAsFalse = 1
    SetAsTrue = 2


@dataclass
class FromDictTestArgs:
    run_forever_value: RunForeverValue


from_dict_test_params, from_dict_test_ids = generate_combination_matrix_from_dataclass(
    input_dataclass=FromDictTestArgs
)


@pytest.fixture(scope="function", params=from_dict_test_params, ids=from_dict_test_ids)
def setup_from_dict(mocker, request):
    params = request.param
    mock_inventory_name = "mock_inventory_name"
    mock_service_arguments = {
        "mock_1": 1,
        "mock_2": True
    }

    if params.run_forever_value == RunForeverValue.SetAsFalse:
        mock_service_arguments["run_forever"] = False
    elif params.run_forever_value == RunForeverValue.SetAsTrue:
        mock_service_arguments["run_forever"] = True

    mock_service = "mock_service"

    mock_service_constructor = mocker.Mock(return_value=mock_service)

    result = InventoryService.from_dict(
        inventory_name=mock_inventory_name,
        service_arguments=mock_service_arguments,
        service_constructor=mock_service_constructor
    )

    return make_namedtuple(
        "setup_from_dict",
        params=params,
        mock_inventory_name=mock_inventory_name,
        mock_service_arguments=mock_service_arguments,
        mock_service=mock_service,
        mock_service_constructor=mock_service_constructor,
        result=result
    )


def test_isinstance_inventoryservice(setup_from_dict):
    assert isinstance(setup_from_dict.result, InventoryService)

def test_inventory_name_correct(setup_from_dict):
    assert setup_from_dict.result.inventory_name == setup_from_dict.mock_inventory_name

def test_run_forever_correct(setup_from_dict):
    run_forever_value = setup_from_dict.params.run_forever_value

    if run_forever_value == RunForeverValue.SetAsTrue:
        assert setup_from_dict.result.run_forever == True
    else:
        assert setup_from_dict.result.run_forever == False

def test_service_correct(setup_from_dict):
    assert setup_from_dict.result.service == setup_from_dict.mock_service

def test_service_constructor_called_correctly(setup_from_dict):
    mock_service_arguments = setup_from_dict.mock_service_arguments
    setup_from_dict.mock_service_constructor.assert_called_once_with(**mock_service_arguments)

def test_needs_to_run(setup_from_dict):
    assert setup_from_dict.result.needs_to_run == True
