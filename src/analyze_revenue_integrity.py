from pathlib import Path
import pandas as pd

# ---------------------------------------------------------
# Healthcare Payer Revenue Integrity Analytics Platform
# Revenue Integrity Exception Analysis
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


def load_data():
    """Load validated source datasets."""

    providers = pd.read_csv(DATA_DIR / "providers.csv")
    locations = pd.read_csv(DATA_DIR / "provider_locations.csv")
    enrollment = pd.read_csv(DATA_DIR / "payer_enrollment.csv")
    claims = pd.read_csv(DATA_DIR / "claims.csv")

    return providers, locations, enrollment, claims


def build_provider_configuration(providers, locations, enrollment):
    """Combine provider master, location, and payer enrollment records."""

    configuration = enrollment.merge(
        providers,
        on="provider_id",
        how="left"
    )

    configuration = configuration.merge(
        locations,
        left_on=["provider_id", "payer_location_id"],
        right_on=["provider_id", "location_id"],
        how="left"
    )

    return configuration


def detect_configuration_issues(configuration):
    """Identify payer and provider configuration discrepancies."""

    configuration["specialty_mismatch"] = (
        configuration["specialty"].str.strip().str.lower()
        != configuration["payer_specialty"].str.strip().str.lower()
    )

    configuration["pending_enrollment"] = (
        configuration["enrollment_status"].str.lower() == "pending"
    )

    configuration["terminated_enrollment"] = (
        configuration["enrollment_status"].str.lower() == "terminated"
    )

    configuration["closed_panel"] = (
        configuration["panel_status"].str.lower() == "closed"
    )

    configuration["inactive_location"] = (
        configuration["location_status"].str.lower() == "inactive"
    )

    configuration["inactive_provider_active_enrollment"] = (
        (configuration["active_status"].str.lower() == "inactive")
        & (configuration["enrollment_status"].str.lower() == "active")
    )

    issue_columns = [
        "specialty_mismatch",
        "pending_enrollment",
        "terminated_enrollment",
        "closed_panel",
        "inactive_location",
        "inactive_provider_active_enrollment",
    ]

    configuration["issue_count"] = configuration[issue_columns].sum(axis=1)

    configuration["has_configuration_issue"] = (
        configuration["issue_count"] > 0
    )

    return configuration


def classify_issue(row):
    """Create a readable list of detected configuration issues."""

    issues = []

    if row["specialty_mismatch"]:
        issues.append("SPECIALTY_MISMATCH")

    if row["pending_enrollment"]:
        issues.append("PENDING_ENROLLMENT")

    if row["terminated_enrollment"]:
        issues.append("TERMINATED_ENROLLMENT")

    if row["closed_panel"]:
        issues.append("CLOSED_PANEL")

    if row["inactive_location"]:
        issues.append("INACTIVE_LOCATION")

    if row["inactive_provider_active_enrollment"]:
        issues.append("INACTIVE_PROVIDER_ACTIVE_ENROLLMENT")

    if not issues:
        return "NO_EXCEPTION"

    return " | ".join(issues)


def summarize_claims(claims):
    """Aggregate claim outcomes by provider, payer, and line of business."""

    claims["is_denied"] = (
        claims["claim_status"].str.lower() == "denied"
    )

    claims["denied_billed_amount"] = claims["billed_amount"].where(
        claims["is_denied"],
        0
    )

    summary = (
        claims.groupby(
            ["provider_id", "payer_name", "line_of_business"],
            as_index=False
        )
        .agg(
            total_claim_count=("claim_id", "count"),
            denied_claim_count=("is_denied", "sum"),
            total_billed_amount=("billed_amount", "sum"),
            total_paid_amount=("paid_amount", "sum"),
            denied_billed_amount=("denied_billed_amount", "sum"),
        )
    )

    return summary


def build_exception_report(configuration, claim_summary):
    """Combine configuration findings with reimbursement outcomes."""

    report = configuration.merge(
        claim_summary,
        on=["provider_id", "payer_name", "line_of_business"],
        how="left"
    )

    report["exception_type"] = report.apply(classify_issue, axis=1)

    financial_columns = [
        "total_claim_count",
        "denied_claim_count",
        "total_billed_amount",
        "total_paid_amount",
        "denied_billed_amount",
    ]

    report[financial_columns] = report[financial_columns].fillna(0)

    report["potential_revenue_at_risk"] = report["denied_billed_amount"]

    exceptions = report[
        report["has_configuration_issue"]
    ].copy()

    exceptions = exceptions.sort_values(
        by=["potential_revenue_at_risk", "issue_count"],
        ascending=[False, False]
    )

    return exceptions


def main():

    print("=" * 70)
    print("HEALTHCARE PAYER REVENUE INTEGRITY - EXCEPTION ANALYSIS")
    print("=" * 70)

    providers, locations, enrollment, claims = load_data()

    configuration = build_provider_configuration(
        providers,
        locations,
        enrollment
    )

    configuration = detect_configuration_issues(configuration)

    claim_summary = summarize_claims(claims)

    exceptions = build_exception_report(
        configuration,
        claim_summary
    )

    output_columns = [
        "provider_id",
        "provider_name",
        "payer_name",
        "line_of_business",
        "specialty",
        "payer_specialty",
        "active_status",
        "location_status",
        "enrollment_status",
        "panel_status",
        "exception_type",
        "issue_count",
        "denied_claim_count",
        "denied_billed_amount",
        "potential_revenue_at_risk",
    ]

    exception_report = exceptions[output_columns]

    output_path = OUTPUT_DIR / "revenue_integrity_exceptions.csv"
    exception_report.to_csv(output_path, index=False)

    total_risk = exception_report[
        "potential_revenue_at_risk"
    ].sum()

    total_denied_claims = exception_report[
        "denied_claim_count"
    ].sum()

    print(f"\nConfiguration exceptions detected: {len(exception_report)}")
    print(f"Denied claims associated with exceptions: {int(total_denied_claims)}")
    print(f"Potential revenue at risk: ${total_risk:,.2f}")

    print("\nTOP EXCEPTIONS")
    print("-" * 70)

    print(
        exception_report[
            [
                "provider_id",
                "provider_name",
                "exception_type",
                "denied_claim_count",
                "potential_revenue_at_risk",
            ]
        ].to_string(index=False)
    )

    print(f"\nException report created: {output_path}")

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()