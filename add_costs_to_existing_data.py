#!/usr/bin/env python3
"""
Script to add comprehensive cost analysis to existing ocean cleanup data
This can be used to add costs to any existing CSV file with ocean cleanup data
"""

import pandas as pd
import sys
import os
from cost_calculator import add_cost_columns_to_dataframe, OceanCleanupCostCalculator

def add_costs_to_existing_data(input_file, output_file=None):
    """
    Add cost analysis to existing ocean cleanup data
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file (optional)
    """
    
    print(f"Loading data from: {input_file}")
    
    # Load the data
    try:
        df = pd.read_csv(input_file)
        print(f"Loaded {len(df)} records")
    except FileNotFoundError:
        print(f"Error: File {input_file} not found")
        return None
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
    
    # Check if required columns exist
    required_columns = ['People', 'Pounds', 'Miles', '# of bags']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"Warning: Missing required columns: {missing_columns}")
        print("Adding default values for missing columns...")
        
        # Add default values for missing columns
        if 'People' not in df.columns:
            df['People'] = 1
        if 'Pounds' not in df.columns:
            df['Pounds'] = 0.1
        if 'Miles' not in df.columns:
            df['Miles'] = 0.1
        if '# of bags' not in df.columns:
            df['# of bags'] = 1
    
    # Add cost columns
    print("Calculating costs for each cleanup point...")
    df_with_costs = add_cost_columns_to_dataframe(df)
    
    # Determine output file name
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_with_costs.csv"
    
    # Save the enhanced data
    df_with_costs.to_csv(output_file, index=False)
    print(f"Enhanced data saved to: {output_file}")
    
    # Print summary
    print_cost_summary(df_with_costs)
    
    return df_with_costs

def print_cost_summary(df):
    """Print a summary of the cost analysis"""
    print("\n" + "="*60)
    print("COST ANALYSIS SUMMARY")
    print("="*60)
    
    # Basic statistics
    total_events = len(df)
    total_people = df['People'].sum()
    total_pounds = df['Pounds'].sum()
    total_miles = df['Miles'].sum()
    
    # Cost statistics
    total_volunteer_cost = df['volunteer_cost'].sum()
    total_direct_costs = df['total_direct_costs'].sum()
    total_carbon_cost = df['carbon_cost'].sum()
    total_cost = df['total_cost'].sum()
    
    print(f"Total Cleanup Events: {total_events:,}")
    print(f"Total People Involved: {total_people:,}")
    print(f"Total Pounds Collected: {total_pounds:,.2f}")
    print(f"Total Miles Covered: {total_miles:,.2f}")
    
    if 'Country' in df.columns:
        print(f"Total Countries: {df['Country'].nunique()}")
    
    print(f"\nCOST BREAKDOWN:")
    print(f"Volunteer Time Value: ${total_volunteer_cost:,.2f}")
    print(f"Direct Costs (Equipment, Transport, etc.): ${total_direct_costs:,.2f}")
    print(f"Carbon Footprint Cost: ${total_carbon_cost:,.2f}")
    print(f"TOTAL COST: ${total_cost:,.2f}")
    
    print(f"\nEFFICIENCY METRICS:")
    print(f"Average Cost per Event: ${total_cost/total_events:,.2f}")
    print(f"Average Cost per Person: ${total_cost/total_people:,.2f}")
    print(f"Average Cost per Pound: ${total_cost/total_pounds:,.2f}")
    print(f"Average Pounds per Person: {total_pounds/total_people:.2f}")
    
    # Top countries by cost (if Country column exists)
    if 'Country' in df.columns:
        country_costs = df.groupby('Country')['total_cost'].sum().sort_values(ascending=False).head(10)
        print(f"\nTOP 10 COUNTRIES BY TOTAL COST:")
        for i, (country, cost) in enumerate(country_costs.items(), 1):
            print(f"{i:2d}. {country}: ${cost:,.2f}")
    
    print("="*60)

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        print("Usage: python add_costs_to_existing_data.py <input_file> [output_file]")
        print("Example: python add_costs_to_existing_data.py data/ocean_cleanup.csv")
        print("Example: python add_costs_to_existing_data.py data/ocean_cleanup.csv data/ocean_cleanup_with_costs.csv")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist")
        return
    
    # Process the file
    result = add_costs_to_existing_data(input_file, output_file)
    
    if result is not None:
        print("\nCost analysis completed successfully!")
        print(f"Enhanced data contains {len(result)} records with {len(result.columns)} columns")
    else:
        print("Failed to process the data file")

if __name__ == "__main__":
    main()
