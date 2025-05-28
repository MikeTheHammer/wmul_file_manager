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
from wmul_file_manager.AsAService import InventoryService


def test_needs_to_run_and_run_forever(mocker):
    mock_inventory_name = "mock_inventory_name"
    run_forever = True

    mock_run_script = mocker.Mock()
    mock_service = mocker.Mock(run_script=mock_run_script)

    inventory_service = InventoryService(
        inventory_name=mock_inventory_name,
        run_forever=run_forever,
        service=mock_service
    )

    inventory_service.run_script()

    assert inventory_service.needs_to_run
    mock_run_script.assert_called_once_with()


def test_needs_to_run_and_dont_run_forever(mocker):
    mock_inventory_name = "mock_inventory_name"
    run_forever = False

    mock_run_script = mocker.Mock()
    mock_service = mocker.Mock(run_script=mock_run_script)

    inventory_service = InventoryService(
        inventory_name=mock_inventory_name,
        run_forever=run_forever,
        service=mock_service
    )

    mock_run_script.assert_not_called()

    inventory_service.run_script()   
    assert not inventory_service.needs_to_run
    mock_run_script.assert_called_once_with()

    inventory_service.run_script()
    assert not inventory_service.needs_to_run
    mock_run_script.assert_called_once_with()


def test_doesnt_need_to_run(mocker):
    mock_inventory_name = "mock_inventory_name"
    run_forever = False

    mock_run_script = mocker.Mock()
    mock_service = mocker.Mock(run_script=mock_run_script)

    inventory_service = InventoryService(
        inventory_name=mock_inventory_name,
        run_forever=run_forever,
        service=mock_service
    )

    inventory_service.needs_to_run = False

    mock_run_script.assert_not_called()
    inventory_service.run_script()

    assert not inventory_service.needs_to_run
    mock_run_script.assert_not_called()
