import sys
import os
import pytest
from dnt.core.service import build_service, ServiceBase


def test_build_service_non_exisiting():
    with pytest.raises(ValueError):
        build_service({"class_name": "NonExistingService"}, 'service name')


def test_build_service_dummy_service():
    sys.path.append(os.path.join(os.path.dirname(__file__), "../dummy_project"))
    _cls = build_service({"class_name": "services.dummy_services.DummyService"}, 'service name')
    assert isinstance(_cls, ServiceBase)
    sys.path.pop()
