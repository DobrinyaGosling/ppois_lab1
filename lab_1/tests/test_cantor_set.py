import pytest

from multitude import CantorSet


def test_parse_nested_cantor_set():
    source = "{a, b, c, {a, b}, {}, {a, {c}}}"
    cantor_set = CantorSet.from_string(source)
    assert len(cantor_set) == 6
    assert CantorSet() in cantor_set
    assert CantorSet.from_string("{a, b}") in cantor_set
    assert CantorSet.from_string("{a, {c}}") in cantor_set
    assert CantorSet.from_string(source).to_string().startswith("{")


def test_set_operations_behave_as_expected():
    first = CantorSet.from_string("{a, {b}}")
    second = CantorSet.from_string("{c, {b}}")
    union = first.union(second)
    assert "a" in union.flatten()
    assert "c" in union.flatten()
    assert first.is_subset_of(union)
    assert not first.is_subset_of(second)
    intersection = first.intersection(second)
    assert len(intersection) == 1
    assert any(isinstance(e, CantorSet) for e in intersection)
    difference = union.difference(first)
    assert "a" not in difference.flatten()


def test_invalid_sources_raise_value_error():
    with pytest.raises(ValueError):
        CantorSet.from_string("{a,,b}")
    with pytest.raises(ValueError):
        CantorSet.from_string("{a")
    with pytest.raises(TypeError):
        CantorSet((object(),))


def test_with_element_union_and_flatten():
    base = CantorSet.from_string("{a}")
    enriched = base.with_element(CantorSet.from_string("{b, c}"))
    assert len(enriched) == 2
    flattened = enriched.flatten()
    assert flattened == {"a", "b", "c"}
    other = CantorSet.from_string("{c, d}")
    difference = enriched.difference(other)
    assert "d" not in difference.flatten()
    assert enriched.union(other).flatten() == {"a", "b", "c", "d"}


def test_membership_and_repr_behaviour():
    cantor_set = CantorSet.from_string("{a, {b}}")
    assert "a" in cantor_set
    assert "  a " in cantor_set  # whitespace trimmed
    assert "" not in cantor_set
    assert object() not in cantor_set
    assert CantorSet() in CantorSet.from_string("{{}}")
    assert repr(cantor_set).startswith("{")
    matcher = CantorSet.from_string("{a}")
    assert cantor_set != matcher
    assert matcher.__eq__("not a set") is NotImplemented
    assert hash(matcher) == hash(CantorSet.from_string("{a}"))


def test_guard_clauses_raise_errors():
    base = CantorSet()
    with pytest.raises(TypeError):
        base.union("not a set")
    with pytest.raises(ValueError):
        CantorSet(("   ",))
