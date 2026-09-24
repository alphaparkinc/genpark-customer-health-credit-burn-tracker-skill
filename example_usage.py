import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import CustomerHealthCreditBurnTrackerClient

def main():
    client = CustomerHealthCreditBurnTrackerClient()
    res = client.track_credit_health()
    print("=== Customer Health & Credit Burn Tracker Output ===")
    print(f"Customer: {res['customer_id']} | Plan: {res['plan_name']}")
    print(f"Credits: ${res['credits_consumed_usd']:,.2f} used / ${res['total_credits_purchased_usd']:,.2f} total ({res['consumption_percentage']})")
    print(f"Credits Remaining: ${res['credits_remaining_usd']:,.2f}")
    print(f"Daily Burn Rate (weighted): ${res['weighted_daily_burn_rate_usd']:,.2f}/day")
    print(f"Runway: {res['projected_runway_days']} days | Period Remaining: {res['days_remaining_in_billing_period']} days")
    print(f"Projected Overage: ${res['projected_overage_usd']:,.2f}")
    print(f"Health Score: {res['customer_health_score']} ({res['health_status']})")
    print(f"Upsell Triggered: {res['upsell_trigger_fired']}")
    print(f"Recommended Action: {res['recommended_action']}")

if __name__ == "__main__":
    main()
