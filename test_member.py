from member import Member


def test_member_creation():
    member = Member("Alice", "M001")

    assert member.name == "Alice"
    assert member.member_id == "M001"
