import os
from typing import Callable, Optional
from classmods import ENVMod

class TestClass:
    @ENVMod.register(
            exclude=['service'],
            cast={'path': str},
            section_name='TestClass',
        )
    def __init__(
            self,
            name: str,
            path: os.PathLike,
            service: Callable | None = None,
        ) -> None:
        """
        Test Class.

        Args:
            name: your name.
            path: service Pathlike Object.
            service: service object.
        """
        self.name = name
        self.path = path
        self.service = service

    @ENVMod.register(section_name='connection', shared_parameters=True)
    def connect(
            self,
            host: str,
            port: int,
            timeout: float,
            password: Optional[int] = None,
        ) -> None:
        """
        Test method connect.

        Args:
            host: Connection host.
            port: connection port.
            timeout: connection timeout.
            password: connection password.
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.password = password

    @ENVMod.register(section_name='connection', shared_parameters=True)
    def db(            
        self,
        host: str,
        port: int,
        timeout: float,
        password: Optional[int] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.password = password


test_values = {
    'TESTCLASS_NAME': 'test_name',
    'TESTCLASS_PATH': '/opt/my_service',
    'CONNECTION_PORT': '123',
    'CONNECTION_HOST': '127.0.0.1',
    'CONNECTION_TIMEOUT': '1.43',
    'CONNECTION_PASSWORD': '',
}


def test_file_creations():
    if not os.path.exists('.temp'):
        os.mkdir('.temp')

    # Setting values and saving.
    os.environ.update(test_values)
    ENVMod.save_example('.temp/env_example.txt')
    ENVMod.save_file(with_values=True)

    assert os.path.exists('.temp/env_example.txt')
    assert os.path.exists('.env')

def test_env_vars():
    test_file_creations()
    ENVMod.load_dotenv()
    assert 'TESTCLASS_NAME' in os.environ
    assert 'TESTCLASS_PATH' in os.environ
    assert 'CONNECTION_PORT' in os.environ
    assert 'CONNECTION_HOST' in os.environ
    assert 'CONNECTION_TIMEOUT' in os.environ
    assert 'CONNECTION_PASSWORD' in os.environ

def test_env_values():
    test_file_creations()
    ENVMod.load_dotenv()
    assert os.environ.get('TESTCLASS_NAME') == 'test_name'
    assert os.environ.get('TESTCLASS_PATH') == '/opt/my_service'
    assert os.environ.get('CONNECTION_PORT') == '123'
    assert os.environ.get('CONNECTION_HOST') == '127.0.0.1'
    assert os.environ.get('CONNECTION_TIMEOUT') == '1.43'
    assert os.environ.get('CONNECTION_PASSWORD') == ''

def test_load_args():
    test_file_creations()
    ENVMod.load_dotenv()
    test_object = TestClass(**ENVMod.load_args(TestClass.__init__))
    test_object.connect(**ENVMod.load_args(TestClass.connect))
    assert test_object.name == 'test_name'
    assert test_object.path == '/opt/my_service'
    assert test_object.port == 123
    assert test_object.host == '127.0.0.1'
    assert test_object.timeout == 1.43
    assert test_object.password == None
