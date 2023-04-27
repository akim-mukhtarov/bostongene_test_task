import time
import requests as r
from pytest import fixture


@fixture
def testfile():
    with open('akim_python_cv.pdf', 'rb') as f:
        yield f


def test_retrieve_hash_with_nonexistent_task_id_responses_404():
    nonexistent_task_id = 0
    url = f"http://localhost:9000/hashes/{nonexistent_task_id}"
    response = r.get(url)
    assert response.status_code == 404


def test_compute_hash(testfile):
    url = f'http://localhost:9000/hashes/'
    response = r.post(url, files={'file': testfile})
    task_id = response.json()['task_id']

    time.sleep(15)
    url = f"http://localhost:9000/hashes/{task_id}"
    expected_response = {
        "status": "SUCCESS",
        "result": "3f3cc5790b9412cf353bfa42ed756a56"
    }
    response = r.get(url)

    assert response.status_code == 200
    assert response.json() == expected_response

