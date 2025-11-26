#!/usr/bin/env python3
"""
Simple cost analysis script that creates cost summaries and basic visualizations
without requiring additional mapping libraries
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from cost_calculator import OceanCleanupCostCalculator

def create_cost_analysis_report(csv_file='data/global_ocean_cleanup_data_with_costs.csv'):
    """
    Create a comprehensive cost analysis report
    """
    print("Loading global cleanup data with costs...")
    
    # Load the data
    try:
        df = pd.read_csv(csv_file)
        print(f"Loaded {len(df)} cleanup records with cost data")
    except FileNotFoundError:
        print(f"File {csv_file} not found. Please run add_costs_to_existing_data.py first.")
        return None
    
    # Create comprehensive analysis
    print("\n" + "="*80)
    print("GLOBAL OCEAN CLEANUP COST ANALYSIS REPORT")
    print("="*80)
    
    # Basic statistics
    total_events = len(df)
    total_people = df['People'].sum()
    total_pounds = df['Pounds'].sum()
    total_miles = df['Miles'].sum()
    total_countries = df['Country'].nunique()
    
    # Cost statistics
    total_volunteer_cost = df['volunteer_cost'].sum()
    total_direct_costs = df['total_direct_costs'].sum()
    total_carbon_cost = df['carbon_cost'].sum()
    total_cost = df['total_cost'].sum()
    
    print(f"OVERVIEW:")
    print(f"   Total Cleanup Events: {total_events:,}")
    print(f"   Total People Involved: {total_people:,}")
    print(f"   Total Pounds Collected: {total_pounds:,.2f}")
    print(f"   Total Miles Covered: {total_miles:,.2f}")
    print(f"   Total Countries: {total_countries}")
    
    print(f"\n COST BREAKDOWN:")
    print(f"   Volunteer Time Value: ${total_volunteer_cost:,.2f} ({total_volunteer_cost/total_cost*100:.1f}%)")
    print(f"   Direct Costs: ${total_direct_costs:,.2f} ({total_direct_costs/total_cost*100:.1f}%)")
    print(f"   Carbon Footprint Cost: ${total_carbon_cost:,.2f} ({total_carbon_cost/total_cost*100:.1f}%)")
    print(f"   TOTAL COST: ${total_cost:,.2f}")
    
    print(f"\n EFFICIENCY METRICS:")
    print(f"   Average Cost per Event: ${total_cost/total_events:,.2f}")
    print(f"   Average Cost per Person: ${total_cost/total_people:,.2f}")
    print(f"   Average Cost per Pound: ${total_cost/total_pounds:,.2f}")
    print(f"   Average Pounds per Person: {total_pounds/total_people:.2f}")
    print(f"   Average Pounds per Hour: {total_pounds/(df['volunteer_hours'].sum()):.2f}")
    
    # Country analysis
    print(f"\nTOP 15 COUNTRIES BY TOTAL COST:")
    country_costs = df.groupby('Country').agg({
        'total_cost': 'sum',
        'volunteer_cost': 'sum',
        'total_direct_costs': 'sum',
        'carbon_cost': 'sum',
        'People': 'sum',
        'Pounds': 'sum',
        'Cleanup ID': 'count'
    }).round(2)
    
    country_costs = country_costs.sort_values('total_cost', ascending=False).head(15)
    
    for i, (country, data) in enumerate(country_costs.iterrows(), 1):
        print(f"   {i:2d}. {country}:")
        print(f"       Total Cost: ${data['total_cost']:,.2f}")
        print(f"       Events: {data['Cleanup ID']}")
        print(f"       People: {data['People']:,}")
        print(f"       Pounds: {data['Pounds']:,.2f}")
        print(f"       Cost per Event: ${data['total_cost']/data['Cleanup ID']:,.2f}")
        print()
    
    # Cost distribution analysis
    print(f"\n COST DISTRIBUTION ANALYSIS:")
    cost_ranges = [
        (0, 100, "Very Low"),
        (100, 500, "Low"),
        (500, 1000, "Medium"),
        (1000, 2000, "High"),
        (2000, float('inf'), "Very High")
    ]
    
    for min_cost, max_cost, label in cost_ranges:
        if max_cost == float('inf'):
            count = len(df[df['total_cost'] >= min_cost])
        else:
            count = len(df[(df['total_cost'] >= min_cost) & (df['total_cost'] < max_cost)])
        percentage = count / total_events * 100
        print(f"   {label} Cost (${min_cost}-{max_cost if max_cost != float('inf') else '∞'}): {count} events ({percentage:.1f}%)")
    
    # Most efficient countries
    print(f"\n MOST EFFICIENT COUNTRIES (by cost per pound):")
    efficiency = df.groupby('Country').agg({
        'total_cost': 'sum',
        'Pounds': 'sum',
        'People': 'sum'
    })
    efficiency['cost_per_pound'] = efficiency['total_cost'] / efficiency['Pounds']
    efficiency['pounds_per_person'] = efficiency['Pounds'] / efficiency['People']
    efficiency = efficiency[efficiency['Pounds'] > 100]  # Only countries with significant cleanup
    efficiency = efficiency.sort_values('cost_per_pound').head(10)
    
    for i, (country, data) in enumerate(efficiency.iterrows(), 1):
        print(f"   {i:2d}. {country}: ${data['cost_per_pound']:.2f}/pound, {data['pounds_per_person']:.2f} lbs/person")
    
    # Save detailed country analysis
    country_analysis_file = 'data/country_cost_analysis.csv'
    country_costs.to_csv(country_analysis_file)
    print(f"\nDetailed country analysis saved to: {country_analysis_file}")
    
    return df

def create_cost_visualizations(df):
    """
    Create basic cost visualizations using matplotlib
    """
    print("\n📊 Creating cost visualizations...")
    
    # Set up the plotting style
    plt.style.use('default')
    
    # 1. Cost breakdown pie chart
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Cost breakdown
    cost_breakdown = {
        'Volunteer Time': df['volunteer_cost'].sum(),
        'Direct Costs': df['total_direct_costs'].sum(),
        'Carbon Cost': df['carbon_cost'].sum()
    }
    
    ax1.pie(cost_breakdown.values(), labels=cost_breakdown.keys(), autopct='%1.1f%%', startangle=90)
    ax1.set_title('Total Cost Breakdown')
    
    # Top 10 countries by cost
    top_countries = df.groupby('Country')['total_cost'].sum().sort_values(ascending=False).head(10)
    ax2.barh(range(len(top_countries)), top_countries.values)
    ax2.set_yticks(range(len(top_countries)))
    ax2.set_yticklabels(top_countries.index, fontsize=8)
    ax2.set_xlabel('Total Cost ($)')
    ax2.set_title('Top 10 Countries by Total Cost')
    
    # Cost distribution histogram
    ax3.hist(df['total_cost'], bins=50, alpha=0.7, edgecolor='black')
    ax3.set_xlabel('Total Cost per Event ($)')
    ax3.set_ylabel('Number of Events')
    ax3.set_title('Distribution of Event Costs')
    ax3.set_yscale('log')
    
    # Efficiency scatter plot
    ax4.scatter(df['Pounds'], df['total_cost'], alpha=0.5, s=20)
    ax4.set_xlabel('Pounds Collected')
    ax4.set_ylabel('Total Cost ($)')
    ax4.set_title('Cost vs Pounds Collected')
    
    plt.tight_layout()
    plt.savefig('plots/global_cost_analysis.png', dpi=300, bbox_inches='tight')
    print("   Cost analysis plots saved to: plots/global_cost_analysis.png")
    
    # 2. Country efficiency analysis
    plt.figure(figsize=(12, 8))
    
    country_stats = df.groupby('Country').agg({
        'total_cost': 'sum',
        'Pounds': 'sum',
        'People': 'sum',
        'Cleanup ID': 'count'
    })
    
    # Filter countries with significant activity
    country_stats = country_stats[country_stats['Pounds'] > 100]
    country_stats['cost_per_pound'] = country_stats['total_cost'] / country_stats['Pounds']
    country_stats['pounds_per_person'] = country_stats['Pounds'] / country_stats['People']
    
    # Create scatter plot
    plt.scatter(country_stats['pounds_per_person'], country_stats['cost_per_pound'], 
               s=country_stats['Cleanup ID']*10, alpha=0.6)
    
    # Add country labels for top countries
    top_countries_by_events = country_stats.nlargest(10, 'Cleanup ID')
    for country, data in top_countries_by_events.iterrows():
        plt.annotate(country, (data['pounds_per_person'], data['cost_per_pound']), 
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.xlabel('Pounds per Person')
    plt.ylabel('Cost per Pound ($)')
    plt.title('Country Efficiency Analysis\n(Bubble size = Number of Events)')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/country_efficiency_analysis.png', dpi=300, bbox_inches='tight')
    print("   Country efficiency analysis saved to: plots/country_efficiency_analysis.png")
    
    plt.close('all')

def main():
    """
    Main function to run the cost analysis
    """
    print(" Global Ocean Cleanup Cost Analysis")
    print("=" * 50)
    
    # Create the analysis report
    df = create_cost_analysis_report()
    
    if df is not None:
        # Create visualizations
        create_cost_visualizations(df)
        
        print("\n Cost analysis completed successfully!")
        print(f"    Data file: data/global_ocean_cleanup_data_with_costs.csv")
        print(f"    Country analysis: data/country_cost_analysis.csv")
        print(f"    Plots: plots/global_cost_analysis.png, plots/country_efficiency_analysis.png")
    else:
        print(" Failed to complete cost analysis")

if __name__ == "__main__":
    main()
