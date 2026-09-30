import tutor

LEVEL = {
    "id": "1-3", "title": "Rectangle",
    "brief": "Print the area of a rectangle with this width and height.",
    "starter": "width = 7\nheight = 3\n", "expected": "21\n", "hidden": "",
    "hint": "print(width * height)", "concepts": ["print"],
}


def test_situation_has_task_numbered_code_verdict_and_theory():
    text = tutor.situation(LEVEL, "width = 7\nheight = 3\nprint(width)", "7\n", 'line 1: expected "21" but got "7"')
    assert "Print the area" in text
    assert "  3  print(width)" in text
    assert "never reveal" in text
    assert 'expected "21"' in text
    assert "World 1" in text          # the theory section came along
    assert "World: Basics" in text


def test_chat_prompt_keeps_the_conversation():
    history = [("you", "what is a variable?"), ("tutor", "a name for a value")]
    original = tutor.run_claude
    seen = {}
    tutor.run_claude = lambda rules, prompt: seen.update(rules=rules, prompt=prompt) or "reply"
    try:
        answer = tutor.chat(LEVEL, "", "", "", history, "and how do I print it?")
    finally:
        tutor.run_claude = original
    assert answer == "reply"
    assert "what is a variable?" in seen["prompt"]
    assert seen["prompt"].rstrip().endswith("tutor:")
    assert "Never write the full" in seen["rules"]


def test_theory_for_picks_the_right_world():
    assert "Printing" in tutor.theory_for(LEVEL)
    assert "Classes" not in tutor.theory_for(LEVEL)[:200]


def test_missing_command_gives_friendly_message():
    original = tutor.CLAUDE_COMMAND
    tutor.CLAUDE_COMMAND = "claude-command-that-does-not-exist"
    try:
        text = tutor.ask_for_hint(LEVEL, "", "", "", [])
    finally:
        tutor.CLAUDE_COMMAND = original
    assert "claude" in text
    assert "Traceback" not in text


def test_rules_ask_for_the_exact_spot_and_forbid_the_answer():
    assert "line number" in tutor.TUTOR_RULES
    assert "never write the full solution" in tutor.TUTOR_RULES


def test_status_reads_the_json():
    assert tutor.read_status('{"loggedIn": true, "authMethod": "claude.ai"}') == (True, "signed in (claude.ai)")
    assert tutor.read_status('{"loggedIn": false}') == (False, "not signed in")
    assert tutor.read_status("garbage")[0] is False


def test_status_with_missing_command_is_friendly():
    original = tutor.CLAUDE_COMMAND
    tutor.CLAUDE_COMMAND = "claude-command-that-does-not-exist"
    try:
        ok, message = tutor.status()
    finally:
        tutor.CLAUDE_COMMAND = original
    assert ok is False and "not installed" in message
