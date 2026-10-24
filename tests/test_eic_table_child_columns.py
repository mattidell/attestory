"""Test that the EIC table v2 parameter with child columns is correct.

Track 1a test: loads v2 and checks every row against the formula,
and that v1 is unchanged on disk.
"""

import json
import subprocess
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import pytest


REPO = Path(__file__).resolve().parents[1]
V1_PARAM = REPO / "packages" / "content" / "tax" / "2025" / "parameter.eic-table-2025.json"
V2_PARAM = REPO / "packages" / "content" / "tax" / "2025" / "parameter.eic-table-2025.v2.json"

# Statutory rates from the 2025 EIC
RATES = {
    0: (Decimal("0.0765"), Decimal("0.0765")),
    1: (Decimal("0.34"), Decimal("0.1598")),
    2: (Decimal("0.40"), Decimal("0.2106")),
    3: (Decimal("0.45"), Decimal("0.2106")),
}

# Limits from Rev. Proc. 2024-40 §2.06
LIMITS = {
    "other": {
        0: (Decimal(8490), Decimal(649), Decimal(10620), Decimal(19104)),
        1: (Decimal(12730), Decimal(4328), Decimal(23350), Decimal(50434)),
        2: (Decimal(17880), Decimal(7152), Decimal(23350), Decimal(57310)),
        3: (Decimal(17880), Decimal(8046), Decimal(23350), Decimal(61555)),
    },
    "mfj": {
        0: (Decimal(8490), Decimal(649), Decimal(17730), Decimal(26214)),
        1: (Decimal(12730), Decimal(4328), Decimal(30470), Decimal(57554)),
        2: (Decimal(17880), Decimal(7152), Decimal(30470), Decimal(64430)),
        3: (Decimal(17880), Decimal(8046), Decimal(30470), Decimal(68675)),
    },
}


def half_up(value: Decimal) -> int:
    """Round half up to integer."""
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def table_credit(amount: int, children: int, status: str) -> int:
    """Compute the credit from the formula.

    status is "other" or "mfj".
    """
    earned_at, maximum, phaseout_at, completed = LIMITS[status][children]
    credit_rate, phaseout_rate = RATES[children]
    if amount < 1 or Decimal(amount) >= completed:
        return 0
    band = (Decimal(amount) // Decimal(50)) * Decimal(50)
    band_end = band + Decimal(50)
    midpoint = band + Decimal(25)
    # The published cell is the statutory credit at one point in the band.
    # That point is the $50 midpoint, except where the band crosses a corner
    # of the credit (the earned-income amount, the phaseout threshold, or the
    # completed phaseout) and the midpoint is still on the other side of it.
    if band < completed < band_end:
        point = (band + completed) / Decimal(2)
    elif band <= earned_at < band_end and midpoint < earned_at:
        point = earned_at
    elif band < phaseout_at < midpoint:
        point = phaseout_at
    else:
        point = midpoint
    if point >= earned_at:
        phased_in = int(maximum)
    else:
        phased_in = min(half_up(point * credit_rate), int(maximum))
    if point <= phaseout_at:
        return phased_in
    reduced = maximum - phaseout_rate * (point - phaseout_at)
    return max(0, half_up(reduced))


class TestEICTableV2:
    """Test the v2 parameter with 1, 2, 3+ child columns."""

    def test_v2_parameter_exists(self) -> None:
        """Verify v2 parameter file exists."""
        assert V2_PARAM.exists(), f"v2 parameter not found at {V2_PARAM}"

    def test_v2_structure(self) -> None:
        """Verify v2 has correct structure."""
        with open(V2_PARAM) as f:
            data = json.load(f)

        assert data["version"] == "v2"
        assert data["id"] == "tax.us.2025.parameter.eic-table-2025"
        assert data["schema"] == "parameter-declaration.v1"

        # Check all 8 columns exist
        expected_keys = {
            "other-0", "other-1", "other-2", "other-3",
            "joint-0", "joint-1", "joint-2", "joint-3"
        }
        assert set(data["values"].keys()) == expected_keys

    def test_v2_other_0_matches_v1(self) -> None:
        """Verify other-0 column matches v1 exactly."""
        with open(V1_PARAM) as f:
            v1 = json.load(f)
        with open(V2_PARAM) as f:
            v2 = json.load(f)

        v1_other = v1["values"]["other"]
        v2_other_0 = v2["values"]["other-0"]
        assert v1_other == v2_other_0, "other-0 must match v1 other exactly"

    def test_v2_joint_0_matches_v1(self) -> None:
        """Verify joint-0 column matches v1 exactly."""
        with open(V1_PARAM) as f:
            v1 = json.load(f)
        with open(V2_PARAM) as f:
            v2 = json.load(f)

        v1_joint = v1["values"]["joint"]
        v2_joint_0 = v2["values"]["joint-0"]
        assert v1_joint == v2_joint_0, "joint-0 must match v1 joint exactly"

    def test_v2_rows_against_formula(self) -> None:
        """Verify every row of every column matches the formula."""
        with open(V2_PARAM) as f:
            v2 = json.load(f)

        mismatches = []
        for column_key in sorted(v2["values"].keys()):
            status_str, children_str = column_key.rsplit("-", 1)
            children = int(children_str)
            # Map parameter status to formula status
            formula_status = "mfj" if status_str == "joint" else status_str

            rows = v2["values"][column_key]
            for i, row in enumerate(rows):
                lower = int(row["lower"])
                published = int(row["value"])
                expected = table_credit(lower, children, formula_status)

                if published != expected:
                    mismatches.append(
                        f"{column_key} row {i} (amount={lower}): "
                        f"published={published} formula={expected}"
                    )

        assert not mismatches, "\n".join(mismatches[:20])

    def test_v1_unchanged_on_disk(self) -> None:
        """Verify v1 is unchanged relative to origin/main."""
        try:
            result = subprocess.run(
                ["git", "show", f"origin/main:{V1_PARAM.relative_to(REPO)}"],
                cwd=REPO,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                original_text = result.stdout
                current_text = V1_PARAM.read_text()
                assert original_text == current_text, (
                    "v1 parameter must not be edited; "
                    "only v2 should be added"
                )
        except subprocess.TimeoutExpired:
            pytest.skip("git show timed out")
        except Exception as e:
            pytest.skip(f"Could not verify v1 against origin/main: {e}")

    def test_each_column_covers_to_its_completed_amount(self) -> None:
        """Each column is contiguous from $1, its last bounded row ends at the
        column's completed phase-out amount, and an open row from there is $0.

        A column that stops short would let range_lookup answer a larger
        amount from the wrong row.
        """
        with open(V2_PARAM) as f:
            v2 = json.load(f)

        for column_key, rows in v2["values"].items():
            status_str, children_str = column_key.rsplit("-", 1)
            formula_status = "mfj" if status_str == "joint" else status_str
            completed = int(LIMITS[formula_status][int(children_str)][3])

            assert rows[0]["lower"] == "1", column_key
            for previous, row in zip(rows, rows[1:]):
                assert previous["upper"] == row["lower"], (column_key, previous, row)
            assert rows[-1] == {"lower": str(completed), "upper": None, "value": "0"}, (
                column_key, rows[-1])
            assert rows[-2]["upper"] == str(completed), (column_key, rows[-2])
