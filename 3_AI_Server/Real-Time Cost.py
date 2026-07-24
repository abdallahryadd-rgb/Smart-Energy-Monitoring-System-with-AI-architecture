# =====================================================================
# REAL-TIME DETAILED BILLING SYSTEM (Egyptian Residential Electricity Tariff)
# =====================================================================

def calculate_device_tariff(kwh_consumed):
    """
    Applies the official Egyptian residential electricity tariff tiers 
    to compute the exact cost and find the current tier for a given kWh consumption.
    """
    if kwh_consumed <= 50:
        tier_label = "Tier 1 (0-50 kWh)"
        cost = kwh_consumed * 0.68
    elif kwh_consumed <= 100:
        tier_label = "Tier 2 (51-100 kWh)"
        cost = (50 * 0.68) + ((kwh_consumed - 50) * 0.78)
    elif kwh_consumed <= 200:
        tier_label = "Tier 3 (101-200 kWh)"
        cost = (50 * 0.68) + (50 * 0.78) + ((kwh_consumed - 100) * 0.95)
    else:
        tier_label = "Tier 4 (201-350 kWh)"
        cost = (50 * 0.68) + (50 * 0.78) + (100 * 0.95) + ((kwh_consumed - 200) * 1.55)
        
    return tier_label, cost


def generate_billing_report(dataframe):
    """
    Processes the raw wattage data (sampled every 5 seconds) from the dataframe, 
    converts it to cumulative kWh, and calculates separate bills for p1, p2, and p3.
    """
    # Time factor for 5-second sampling interval (5 seconds / 3600 seconds in an hour)
    time_hours_factor = 5 / 3600
    
    # Calculate cumulative kWh consumption for each device channel (divided by 1000 to convert W to kW)
    p1_kwh = (dataframe['p1'].sum() / 1000) * time_hours_factor
    p2_kwh = (dataframe['p2'].sum() / 1000) * time_hours_factor
    p3_kwh = (dataframe['p3'].sum() / 1000) * time_hours_factor
    
    # Get exact tier and cost details for each device channel separately
    p1_tier, p1_cost = calculate_device_tariff(p1_kwh)
    p2_tier, p2_cost = calculate_device_tariff(p2_kwh)
    p3_tier, p3_cost = calculate_device_tariff(p3_kwh)
    
    # Structure billing insights into a structured response dictionary
    billing_report = {
        "P1_Device": {"kwh": p1_kwh, "tier": p1_tier, "cost": p1_cost},
        "P2_Device": {"kwh": p2_kwh, "tier": p2_tier, "cost": p2_cost},
        "P3_Device": {"kwh": p3_kwh, "tier": p3_tier, "cost": p3_cost},
        "Cumulative_System_Cost": p1_cost + p2_cost + p3_cost
    }
    
    # Print console confirmation example
    print("\n=== Real-Time Billing Estimation Summary ===")
    print(f"Device P1 Cost: {p1_cost:.2f} EGP ({p1_tier})")
    print(f"Device P2 Cost: {p2_cost:.2f} EGP ({p2_tier})")
    print(f"Device P3 Cost: {p3_cost:.2f} EGP ({p3_tier})")
    print(f"Total System Cost: {billing_report['Cumulative_System_Cost']:.2f} EGP")
    
    return billing_report
