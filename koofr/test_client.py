import pytest
import koofr
import posixpath
import os
import time

testdir = "/koofr-python-test" + str(time.time())

@pytest.fixture()
def mount_id():
    assert "KOOFR_MOUNTID" in os.environ
    return os.environ["KOOFR_MOUNTID"]

@pytest.fixture()
def client():
    assert "KOOFR_USERNAME" in os.environ
    assert "KOOFR_PASSWORD" in os.environ

    try:
        client = koofr.client.KoofrClient(os.environ["KOOFR_API_BASE"])
    except:
        client = koofr.client.KoofrClient()

    ret = client.authenticate(os.environ["KOOFR_USERNAME"], os.environ["KOOFR_PASSWORD"])
    assert ret == True
    return client

def test_mounts(client):
    mounts = client.mounts()
    assert len(mounts) > 0

def test_new_folder(client, mount_id):
    success = client.files_new_folder(mount_id, posixpath.join(testdir))
    assert success

def test_put(client, mount_id):
    name = client.files_put(mount_id, posixpath.join(testdir, "test1234.txt"), "test")
    assert name == "test1234.txt"

def test_info(client, mount_id):
    info = client.files_info(mount_id, posixpath.join(testdir, "test1234.txt"))
    assert info["name"] == "test1234.txt"

def test_get(client, mount_id):
    content = client.files_get(mount_id, posixpath.join(testdir, "test1234.txt"))
    assert content == "test"

def test_list(client, mount_id):
    list = client.files_list(mount_id, posixpath.join(testdir))
    exist = False
    for f in list:
        if f["name"] == "test1234.txt":
            exist = True
    assert exist == True

def test_remove(client, mount_id):
    success = client.files_remove(mount_id, posixpath.join(testdir, "test1234.txt"))
    assert success == True
