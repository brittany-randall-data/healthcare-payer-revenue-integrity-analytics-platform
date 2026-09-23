from pathlib import Path
import pandas as pd

# ---------------------------------------------------------
# Healthcare Payer Revenue Integrity Analytics Platform
# Raw Data Validation
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATASETS = {
    "providers": DATA_DIR / "providers.csv",
    "provider_locations": DATA_DIR / "provider_locations.csv",
    "payer_enrollment": DATA_DIR / "payer_enrollment.csv",
    "claims": DATA_DIR / "claims.csv",
}

REQUIRED_COLUMNS = {
    "providers": [
        "provider_id",
        "npi",
        "provider_name",
        "specialty",
        "taxonomy_code",
        "provider_type",
        "active_status",
    ],
    "provider_locations": [
        "provider_id",
        "location_id",
        "location_name",
        "city",
        "state",
        "zip_code",
        "location_status",
    ],
    "payer_enrollment": [
        "enrollment_id",
        "provider_id",
        "payer_name",
        "line_of_business",
        "enrollment_status",
        "effective_date",
        "termination_date",
        "panel_status",
        "payer_specialty",
        "payer_location_id",
    ],
    "claims": [
        "claim_id",
        "provider_id",
        "payer_name",
        "line_of_business",
        "service_date",
        "billed_amount",
        "paid_amount",
        "claim_status",
        "denial_reason",
    ],
}


def load_dataset(name, path):
    """Load a CSV dataset and confirm that the file exists."""

    if not path.exists():
        raise FileNotFoundError(f"Missing dataset: {path}")

    df = pd.read_csv(path)

    print(f"\n{name.upper()}")
    print("-" * 50)
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    return df


def validate_required_columns(name, df):
    """Check whether all required columns are present."""

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS[name]
        if column not in df.columns
    ]

    if missing_columns:
        print(f"FAIL - Missing columns: {missing_columns}")
        return False

    print("PASS - All required columns are present.")
    return True


def validate_duplicate_ids(name, df):
    """Check duplicate primary identifiers."""

    id_columns = {
        "providers": "provider_id",
        "provider_locations": ["provider_id", "location_id"],
        "payer_enrollment": "enrollment_id",
        "claims": "claim_id",
    }

    key = id_columns[name]
    duplicate_count = df.duplicated(subset=key).sum()

    if duplicate_count > 0:
        print(f"FAIL - Duplicate key records: {duplicate_count}")
        return False

    print("PASS - No duplicate key records detected.")
    return True


def validate_provider_references(datasets):
    """Confirm that related datasets reference known providers."""

    valid_provider_ids = set(datasets["providers"]["provider_id"])

    for name in ["provider_locations", "payer_enrollment", "claims"]:
        unknown_ids = set(datasets[name]["provider_id"]) - valid_provider_ids

        if unknown_ids:
            print(
                f"FAIL - {name} contains unknown provider IDs: "
                f"{sorted(unknown_ids)}"
            )
        else:
            print(
                f"PASS - {name} references valid provider IDs."
            )


def validate_claim_amounts(claims):
    """Validate claim financial fields."""

    invalid_billed = claims[claims["billed_amount"] < 0]
    invalid_paid = claims[claims["paid_amount"] < 0]
    paid_over_billed = claims[
        claims["paid_amount"] > claims["billed_amount"]
    ]

    if invalid_billed.empty:
        print("PASS - No negative billed amounts.")
    else:
        print(
            f"FAIL - Negative billed amounts: {len(invalid_billed)}"
        )

    if invalid_paid.empty:
        print("PASS - No negative paid amounts.")
    else:
        print(
            f"FAIL - Negative paid amounts: {len(invalid_paid)}"
        )

    if paid_over_billed.empty:
        print("PASS - No paid amounts exceed billed amounts.")
    else:
        print(
            f"FAIL - Paid amount exceeds billed amount: "
            f"{len(paid_over_billed)}"
        )


def main():
    print("=" * 60)
    print("HEALTHCARE PAYER REVENUE INTEGRITY - DATA VALIDATION")
    print("=" * 60)

    datasets = {}

    for name, path in DATASETS.items():
        df = load_dataset(name, path)
        datasets[name] = df

        validate_required_columns(name, df)
        validate_duplicate_ids(name, df)

    print("\nREFERENTIAL INTEGRITY")
    print("-" * 50)
    validate_provider_references(datasets)

    print("\nCLAIM FINANCIAL VALIDATION")
    print("-" * 50)
    validate_claim_amounts(datasets["claims"])

    print("\n" + "=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()