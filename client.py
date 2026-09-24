import json
import math
from typing import Dict, Any, List, Optional

class CustomerHealthCreditBurnTrackerClient:
    """
    Production-grade customer health and prepaid credit burn rate tracker.
    Inspired by Metronome (metronome.com) — monitoring credit usage and driving upsells at the right time.
    Calculates real-time burn velocity, runway days, and upsell trigger thresholds.
    """
    def __init__(self, upsell_trigger_pct: float = 0.75):
        self.upsell_trigger_pct = upsell_trigger_pct

    def track_credit_health(
        self,
        customer_id: str = "cust_fly_io_prod_007",
        plan_name: str = "Compute Startup Bundle",
        total_credits_purchased_usd: float = 10000.0,
        credits_consumed_to_date_usd: float = 7820.0,
        days_elapsed_in_period: int = 22,
        total_billing_period_days: int = 30,
        daily_burn_history_usd: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        if not daily_burn_history_usd:
            daily_burn_history_usd = [
                310.5, 298.0, 325.8, 341.2, 290.0, 315.7, 388.4,
                402.1, 378.9, 350.0, 362.5, 371.0, 395.3, 410.0,
                388.0, 401.5, 422.3, 399.7, 415.0, 430.1, 418.8, 445.2
            ]

        credits_remaining = total_credits_purchased_usd - credits_consumed_to_date_usd
        consumption_pct = round(credits_consumed_to_date_usd / max(1.0, total_credits_purchased_usd), 4)

        # Weighted burn velocity (recent 7 days weighted 60%, older 40%)
        recent_burns = daily_burn_history_usd[-7:]  if len(daily_burn_history_usd) >= 7 else daily_burn_history_usd
        older_burns  = daily_burn_history_usd[:-7]  if len(daily_burn_history_usd) >  7 else []
        recent_avg = sum(recent_burns) / max(1, len(recent_burns))
        older_avg  = sum(older_burns)  / max(1, len(older_burns)) if older_burns else recent_avg
        weighted_daily_burn = round(recent_avg * 0.60 + older_avg * 0.40, 2)

        runway_days = round(credits_remaining / max(0.01, weighted_daily_burn), 1)
        days_remaining_in_period = total_billing_period_days - days_elapsed_in_period
        projected_overage_usd = max(0.0, round((weighted_daily_burn * days_remaining_in_period) - credits_remaining, 2))

        upsell_triggered = consumption_pct >= self.upsell_trigger_pct
        health_score = round(max(0.0, 1.0 - (consumption_pct * (days_elapsed_in_period / total_billing_period_days))), 2)

        if health_score >= 0.6:
            health_status = "HEALTHY"
        elif health_score >= 0.3:
            health_status = "AT_RISK"
        else:
            health_status = "CRITICAL_BURN_RATE"

        return {
            "tracking_id": "hlth_crdt_mtr_3319",
            "customer_id": customer_id,
            "plan_name": plan_name,
            "total_credits_purchased_usd": total_credits_purchased_usd,
            "credits_consumed_usd": credits_consumed_to_date_usd,
            "credits_remaining_usd": round(credits_remaining, 2),
            "consumption_percentage": f"{round(consumption_pct * 100, 1)}%",
            "weighted_daily_burn_rate_usd": weighted_daily_burn,
            "projected_runway_days": runway_days,
            "days_remaining_in_billing_period": days_remaining_in_period,
            "projected_overage_usd": projected_overage_usd,
            "customer_health_score": health_score,
            "health_status": health_status,
            "upsell_trigger_fired": upsell_triggered,
            "recommended_action": (
                "TRIGGER_UPSELL_EMAIL_AND_IN_APP_UPGRADE_NUDGE" if upsell_triggered and projected_overage_usd > 0
                else "TRIGGER_UPSELL_EMAIL" if upsell_triggered
                else "MONITOR_PASSIVELY"
            ),
            "powered_by": "metronome.com customer health tracking engine"
        }
