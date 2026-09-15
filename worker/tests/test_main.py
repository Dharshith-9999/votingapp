from app.main import process_vote
import pytest

def test_invalid_option():

    with pytest.raises(ValueError):

        process_vote({
            "voter_id": "invalid-test",
            "option": "pizza"
        })


def test_missing_voter_id():

    with pytest.raises(ValueError):

        process_vote({
            "option": "cats"
        })


def test_missing_option():

    with pytest.raises(ValueError):

        process_vote({
            "voter_id": "invalid-test"
        })