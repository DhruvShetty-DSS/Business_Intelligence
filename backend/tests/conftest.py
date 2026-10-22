"""Shared CSV fixtures for cleaning and upload tests."""

import pytest


@pytest.fixture
def valid_csv_bytes() -> bytes:
    return (
        b"date,description,amount,category\n"
        b"2026-01-02,Coffee,-4.50,food\n"
        b"2026-01-03,Salary,1000,Income\n"
    )


@pytest.fixture
def malformed_rows_csv_bytes() -> bytes:
    return (
        b"date,description,amount\n"
        b"not-a-date,Coffee,not-a-number\n"
    )


@pytest.fixture
def duplicate_rows_csv_bytes() -> bytes:
    return (
        b"date,description,amount,category\n"
        b"2026-01-02,Coffee,-4.50,food\n"
        b"2026-01-02,Coffee,-4.50,food\n"
    )


@pytest.fixture
def blank_rows_csv_bytes() -> bytes:
    return (
        b"date,description,amount,category\n"
        b"2026-01-02,Coffee,-4.50,food\n"
        b",,,\n"
    )


@pytest.fixture
def optional_category_csv_bytes() -> bytes:
    return b"date,description,amount\n2026-01-02,Coffee,-4.50\n"
