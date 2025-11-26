#!/usr/bin/env python3
"""
Script to display cost information for individual cleanup points
"""

import pandas as pd
import sys

def show_point_costs(csv_file='data/global_ocean_cleanup_data_with_costs.csv', limit=10):
    """
    Display cost information for individual cleanup points
    """
    print("Loading global cleanup data with costs...")
    
    try:
        df = pd.read_csv(csv_file)
        print(f"Loaded {len(df)} cleanup records with cost data")
    except FileNotFoundError:
        print(f"File {csv_file} not found. Please run add_costs_to_existing_data.py first.")
        return
    
    print(f"\n{'='*100}")
    print("INDIVIDUAL CLEANUP POINT COST ANALYSIS")
    print(f"{'='*100}")
    
    # Show sample of points with their costs
    sample_df = df.head(limit)
    
    for idx, row in sample_df.iterrows():
        print(f"\n📍 CLEANUP POINT #{idx+1}")
        print(f"   Location: {row['Zone']}, {row['Country']}")
        print(f"   GPS: {row['GPS']}")
        print(f"   Date: {row['Cleanup Date']}")
        print(f"   Type: {row['Cleanup Type']}")
        print(f"   Group: {row['Group Name']}")
        
        print(f"\n   📊 ACTIVITY METRICS:")
        print(f"   People: {row['People']}")
        print(f"   Pounds Collected: {row['Pounds']:.2f}")
        print(f"   Miles Covered: {row['Miles']:.2f}")
        print(f"   Bags Used: {row['# of bags']}")
        
        print(f"\n   💰 COST BREAKDOWN:")
        print(f"   Volunteer Hours: {row['volunteer_hours']:.2f}")
        print(f"   Volunteer Cost: ${row['volunteer_cost']:.2f}")
        print(f"   Equipment Cost: ${row['equipment_cost']:.2f}")
        print(f"   Transportation Cost: ${row['transportation_cost']:.2f}")
        print(f"   Disposal Cost: ${row['disposal_cost']:.2f}")
        print(f"   Administrative Cost: ${row['administrative_cost']:.2f}")
        print(f"   Carbon Cost: ${row['carbon_cost']:.2f}")
        print(f"   TOTAL COST: ${row['total_cost']:.2f}")
        
        print(f"\n   📈 EFFICIENCY METRICS:")
        print(f"   Cost per Person: ${row['cost_per_person']:.2f}")
        print(f"   Cost per Pound: ${row['cost_per_pound']:.2f}")
        print(f"   Pounds per Person: {row['pounds_per_person']:.2f}")
        print(f"   Pounds per Hour: {row['pounds_per_hour']:.2f}")
        print(f"   Miles per Person: {row['miles_per_person']:.2f}")
        
        print("-" * 100)
    
    # Show cost statistics
    print(f"\n📊 COST STATISTICS SUMMARY:")
    print(f"   Average Cost per Point: ${df['total_cost'].mean():.2f}")
    print(f"   Median Cost per Point: ${df['total_cost'].median():.2f}")
    print(f"   Min Cost per Point: ${df['total_cost'].min():.2f}")
    print(f"   Max Cost per Point: ${df['total_cost'].max():.2f}")
    print(f"   Standard Deviation: ${df['total_cost'].std():.2f}")
    
    # Show most expensive points
    print(f"\n💸 TOP 10 MOST EXPENSIVE CLEANUP POINTS:")
    expensive_points = df.nlargest(10, 'total_cost')
    for i, (idx, row) in enumerate(expensive_points.iterrows(), 1):
        print(f"   {i:2d}. {row['Country']} - ${row['total_cost']:.2f} ({row['People']} people, {row['Pounds']:.1f} lbs)")
    
    # Show most efficient points (lowest cost per pound)
    print(f"\n🏆 TOP 10 MOST EFFICIENT CLEANUP POINTS (lowest cost per pound):")
    efficient_points = df[df['Pounds'] > 0].nsmallest(10, 'cost_per_pound')
    for i, (idx, row) in enumerate(efficient_points.iterrows(), 1):
        print(f"   {i:2d}. {row['Country']} - ${row['cost_per_pound']:.2f}/lb ({row['People']} people, {row['Pounds']:.1f} lbs)")

def search_points_by_country(country, csv_file='data/global_ocean_cleanup_data_with_costs.csv'):
    """
    Search and display points for a specific country
    """
    try:
        df = pd.read_csv(csv_file)
        country_data = df[df['Country'].str.contains(country, case=False, na=False)]
        
        if len(country_data) == 0:
            print(f"No cleanup points found for country: {country}")
            return
        
        print(f"\n🌍 CLEANUP POINTS IN {country.upper()}")
        print(f"Found {len(country_data)} cleanup points")
        
        total_cost = country_data['total_cost'].sum()
        total_people = country_data['People'].sum()
        total_pounds = country_data['Pounds'].sum()
        
        print(f"\nCountry Summary:")
        print(f"   Total Cost: ${total_cost:,.2f}")
        print(f"   Total People: {total_people:,}")
        print(f"   Total Pounds: {total_pounds:,.2f}")
        print(f"   Average Cost per Point: ${total_cost/len(country_data):,.2f}")
        
        # Show individual points
        for idx, row in country_data.iterrows():
            print(f"\n   📍 {row['Zone']} - ${row['total_cost']:.2f}")
            print(f"      Date: {row['Cleanup Date']}, People: {row['People']}, Pounds: {row['Pounds']:.1f}")
    
    except FileNotFoundError:
        print(f"File {csv_file} not found.")

def main():
    """
    Main function
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == "search":
            if len(sys.argv) > 2:
                search_points_by_country(sys.argv[2])
            else:
                print("Usage: python show_point_costs.py search <country_name>")
        else:
            try:
                limit = int(sys.argv[1])
                show_point_costs(limit=limit)
            except ValueError:
                print("Usage: python show_point_costs.py [number_of_points] or python show_point_costs.py search <country>")
    else:
        show_point_costs()

if __name__ == "__main__":
    main()
