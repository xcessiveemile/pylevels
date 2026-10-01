"""Tests the sign-in against a stand-in for the claude command."""

import sys

import pytest

import auth

# The terminal game's sign-in reads the claude command through pipes with
# select(), which Windows does not allow; the desktop app signs in another way.
pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the terminal sign-in is Mac and Linux only")
from tests.fake_claude import LINK, build


@pytest.fixture
def fake(monkeypatch):
    """Puts the fake claude command on the path and starts it logged out."""
    command, marker = build()
    monkeypatch.setattr(auth, "CLAUDE_COMMAND", str(command))
    monkeypatch.setenv("PYLEVELS_FAKE_STATE", str(marker))
    return marker.parent


def test_signed_in_follows_the_status_command(fake):
    assert auth.signed_in() is False
    (fake / "logged-in").write_text("in")
    assert auth.signed_in() is True
    assert auth.account_name() == "player@example.com"


def test_start_returns_the_link(fake):
    session = auth.LoginSession()
    try:
        assert session.start() == LINK
        assert session.url == LINK
    finally:
        session.stop()


def test_a_good_code_signs_in(fake):
    session = auth.LoginSession()
    try:
        session.start()
        session.finish("goodcode")
    finally:
        session.stop()
    assert auth.signed_in() is True


def test_a_bad_code_explains_itself(fake):
    session = auth.LoginSession()
    try:
        session.start()
        with pytest.raises(auth.LoginError) as raised:
            session.finish("nonsense")
    finally:
        session.stop()
    assert "Traceback" not in str(raised.value)
    assert str(raised.value)
    assert auth.signed_in() is False


def test_a_missing_command_says_so(monkeypatch):
    monkeypatch.setattr(auth, "CLAUDE_COMMAND", "claude-command-that-does-not-exist")
    session = auth.LoginSession()
    with pytest.raises(auth.LoginError) as raised:
        session.start()
    assert "claude" in str(raised.value)
    assert auth.signed_in() is False


def test_a_sign_in_with_no_link_is_reported(fake, monkeypatch):
    monkeypatch.setenv("PYLEVELS_FAKE_NO_LINK", "1")
    session = auth.LoginSession()
    with pytest.raises(auth.LoginError) as raised:
        session.start()
    assert "Traceback" not in str(raised.value)


def test_stop_ends_a_sign_in_the_player_walked_away_from(fake):
    session = auth.LoginSession()
    session.start()
    assert session.process.poll() is None
    session.stop()
    assert session.process.poll() is not None
    session.stop()  # stopping twice must not raise


def test_finish_without_a_start_is_reported(fake):
    session = auth.LoginSession()
    with pytest.raises(auth.LoginError):
        session.finish("goodcode")


def test_the_link_is_read_before_the_prompt_ends_the_line(fake, monkeypatch):
    """The real command leaves 'Paste code here > ' unfinished, with no newline."""
    monkeypatch.setenv("PYLEVELS_FAKE_HANG", "1")
    monkeypatch.setattr(auth, "START_SECONDS", 10)
    session = auth.LoginSession()
    try:
        assert session.start() == LINK
    finally:
        session.stop()
