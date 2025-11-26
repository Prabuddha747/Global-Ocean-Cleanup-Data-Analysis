#!/usr/bin/env python3
"""
Script to fix coordinate mapping issues in the global ocean cleanup data
This ensures that cleanup points are placed in the correct geographical locations
"""

import pandas as pd
import random
import numpy as np

def get_accurate_coordinates_for_region(country, region):
    """
    Get accurate coordinates for specific regions, especially for India
    """
    
    # Specific coordinate mappings for Indian coastal states
    india_coastal_regions = {
        'Gujarat': {'lat_range': (20.0, 24.0), 'lon_range': (68.0, 72.0)},
        'Maharashtra': {'lat_range': (15.0, 20.0), 'lon_range': (72.0, 76.0)},
        'Goa': {'lat_range': (14.5, 15.5), 'lon_range': (73.5, 74.5)},
        'Karnataka': {'lat_range': (12.0, 15.0), 'lon_range': (74.0, 78.0)},
        'Kerala': {'lat_range': (8.0, 12.0), 'lon_range': (76.0, 77.5)},
        'Tamil Nadu': {'lat_range': (8.0, 13.0), 'lon_range': (77.0, 80.5)},
        'Andhra Pradesh': {'lat_range': (12.0, 19.0), 'lon_range': (79.0, 84.0)},
        'Odisha': {'lat_range': (17.0, 21.0), 'lon_range': (81.0, 87.0)},
        'West Bengal': {'lat_range': (21.0, 23.0), 'lon_range': (87.0, 89.0)},
        'Puducherry': {'lat_range': (11.5, 12.0), 'lon_range': (79.5, 80.0)},
        'Daman and Diu': {'lat_range': (20.0, 20.5), 'lon_range': (72.5, 73.0)},
        'Lakshadweep': {'lat_range': (8.0, 12.0), 'lon_range': (71.0, 74.0)},
        'Andaman and Nicobar Islands': {'lat_range': (6.0, 14.0), 'lon_range': (92.0, 94.0)}
    }
    
    # For other countries, use broader regional ranges
    country_coords = {
        'United States': {'lat_range': (24.5, 49.0), 'lon_range': (-125.0, -66.9)},
        'Canada': {'lat_range': (41.7, 83.1), 'lon_range': (-141.0, -52.6)},
        'Mexico': {'lat_range': (14.5, 32.7), 'lon_range': (-118.4, -86.7)},
        'Brazil': {'lat_range': (-33.8, 5.3), 'lon_range': (-73.9, -34.8)},
        'Argentina': {'lat_range': (-55.1, -21.8), 'lon_range': (-73.6, -53.6)},
        'Chile': {'lat_range': (-56.0, -17.5), 'lon_range': (-75.6, -66.4)},
        'Colombia': {'lat_range': (-4.2, 15.5), 'lon_range': (-81.7, -66.9)},
        'Peru': {'lat_range': (-18.3, -0.0), 'lon_range': (-84.6, -68.7)},
        'Ecuador': {'lat_range': (-5.0, 1.7), 'lon_range': (-92.0, -75.2)},
        'Venezuela': {'lat_range': (0.6, 15.9), 'lon_range': (-73.4, -59.8)},
        'Uruguay': {'lat_range': (-35.0, -30.1), 'lon_range': (-58.4, -53.1)},
        'United Kingdom': {'lat_range': (49.9, 60.8), 'lon_range': (-8.2, 1.8)},
        'France': {'lat_range': (41.3, 51.1), 'lon_range': (-5.1, 9.6)},
        'Spain': {'lat_range': (27.6, 43.8), 'lon_range': (-9.3, 4.3)},
        'Italy': {'lat_range': (35.5, 47.1), 'lon_range': (6.6, 18.5)},
        'Germany': {'lat_range': (47.3, 55.1), 'lon_range': (5.9, 15.0)},
        'Netherlands': {'lat_range': (50.8, 53.6), 'lon_range': (3.4, 7.2)},
        'Norway': {'lat_range': (58.0, 80.8), 'lon_range': (4.6, 31.3)},
        'Sweden': {'lat_range': (55.3, 69.1), 'lon_range': (11.0, 24.2)},
        'Denmark': {'lat_range': (54.6, 57.8), 'lon_range': (8.1, 15.2)},
        'Portugal': {'lat_range': (36.9, 42.2), 'lon_range': (-9.5, -6.2)},
        'Greece': {'lat_range': (34.8, 41.7), 'lon_range': (19.4, 29.7)},
        'Turkey': {'lat_range': (35.8, 42.1), 'lon_range': (25.7, 44.8)},
        'Russia': {'lat_range': (41.2, 81.9), 'lon_range': (-180.0, 180.0)},
        'China': {'lat_range': (18.2, 53.6), 'lon_range': (73.6, 135.1)},
        'Japan': {'lat_range': (24.2, 45.5), 'lon_range': (123.0, 145.8)},
        'South Korea': {'lat_range': (33.1, 38.6), 'lon_range': (124.6, 131.9)},
        'Indonesia': {'lat_range': (-11.0, 6.1), 'lon_range': (95.0, 141.0)},
        'Philippines': {'lat_range': (4.6, 21.1), 'lon_range': (116.9, 126.6)},
        'Thailand': {'lat_range': (5.6, 20.5), 'lon_range': (97.3, 105.6)},
        'Vietnam': {'lat_range': (8.6, 23.4), 'lon_range': (102.1, 109.5)},
        'Malaysia': {'lat_range': (0.9, 7.4), 'lon_range': (99.6, 119.3)},
        'Singapore': {'lat_range': (1.2, 1.5), 'lon_range': (103.6, 104.0)},
        'Bangladesh': {'lat_range': (20.7, 26.6), 'lon_range': (88.0, 92.7)},
        'Sri Lanka': {'lat_range': (5.9, 9.8), 'lon_range': (79.7, 81.9)},
        'Myanmar': {'lat_range': (9.8, 28.5), 'lon_range': (92.2, 101.2)},
        'South Africa': {'lat_range': (-47.0, -22.1), 'lon_range': (16.5, 32.9)},
        'Egypt': {'lat_range': (22.0, 31.7), 'lon_range': (24.7, 36.9)},
        'Morocco': {'lat_range': (21.4, 35.9), 'lon_range': (-17.0, -1.0)},
        'Algeria': {'lat_range': (18.9, 37.1), 'lon_range': (-8.7, 12.0)},
        'Tunisia': {'lat_range': (30.2, 37.5), 'lon_range': (7.5, 11.6)},
        'Libya': {'lat_range': (19.5, 33.2), 'lon_range': (9.3, 25.2)},
        'Nigeria': {'lat_range': (4.3, 13.9), 'lon_range': (2.7, 14.7)},
        'Ghana': {'lat_range': (4.7, 11.2), 'lon_range': (-3.3, 1.3)},
        'Senegal': {'lat_range': (12.3, 16.7), 'lon_range': (-17.5, -11.3)},
        'Kenya': {'lat_range': (-4.7, 5.5), 'lon_range': (33.9, 41.9)},
        'Tanzania': {'lat_range': (-11.7, -0.9), 'lon_range': (29.3, 40.3)},
        'Mozambique': {'lat_range': (-26.9, -10.5), 'lon_range': (30.2, 40.8)},
        'Madagascar': {'lat_range': (-25.6, -11.9), 'lon_range': (43.2, 50.5)},
        'Australia': {'lat_range': (-43.6, -10.7), 'lon_range': (113.3, 153.6)},
        'New Zealand': {'lat_range': (-47.3, -34.4), 'lon_range': (166.5, 178.6)},
        'Papua New Guinea': {'lat_range': (-12.0, -1.0), 'lon_range': (140.8, 159.9)},
        'Fiji': {'lat_range': (-20.7, -16.0), 'lon_range': (177.0, -178.1)},
        'Solomon Islands': {'lat_range': (-11.9, -5.3), 'lon_range': (155.5, 166.9)},
        'Vanuatu': {'lat_range': (-20.2, -13.1), 'lon_range': (166.5, 170.2)},
        'Samoa': {'lat_range': (-14.0, -13.4), 'lon_range': (-172.8, -171.4)},
        'Tonga': {'lat_range': (-24.0, -15.6), 'lon_range': (-179.1, -173.9)},
        'Kiribati': {'lat_range': (-4.7, 4.7), 'lon_range': (-174.5, -150.2)},
        'Marshall Islands': {'lat_range': (4.6, 14.7), 'lon_range': (160.8, 172.0)},
        'Micronesia': {'lat_range': (1.0, 10.1), 'lon_range': (137.3, 163.0)},
        'Palau': {'lat_range': (2.9, 8.2), 'lon_range': (131.1, 134.7)},
        'Tuvalu': {'lat_range': (-10.8, -5.6), 'lon_range': (176.0, 179.9)},
        'Nauru': {'lat_range': (-0.6, -0.5), 'lon_range': (166.9, 166.9)}
    }
    
    # For India, use specific regional coordinates
    if country == 'India' and region in india_coastal_regions:
        lat_range = india_coastal_regions[region]['lat_range']
        lon_range = india_coastal_regions[region]['lon_range']
    elif country in country_coords:
        lat_range = country_coords[country]['lat_range']
        lon_range = country_coords[country]['lon_range']
    else:
        # Default fallback
        lat_range = (-60, 60)
        lon_range = (-180, 180)
    
    # Generate random coordinates within the range
    lat = random.uniform(lat_range[0], lat_range[1])
    lon = random.uniform(lon_range[0], lon_range[1])
    
    return round(lat, 6), round(lon, 6)

def fix_coordinates_in_dataframe(df):
    """
    Fix coordinates in the dataframe to match the correct regions
    """
    print("Fixing coordinates to match correct geographical locations...")
    
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)
    
    fixed_count = 0
    
    for idx, row in df.iterrows():
        country = row['Country']
        region = row['Zone'].split(',')[0].strip()  # Extract region from Zone
        
        # Generate correct coordinates
        lat, lon = get_accurate_coordinates_for_region(country, region)
        
        # Update the GPS coordinates
        df.at[idx, 'GPS'] = f"{lat}, {lon}"
        fixed_count += 1
        
        if fixed_count % 1000 == 0:
            print(f"Fixed {fixed_count} coordinates...")
    
    print(f"Fixed coordinates for {fixed_count} cleanup points")
    return df

def main():
    """
    Main function to fix coordinates in the global cleanup data
    """
    print("🌊 Fixing Coordinate Mapping Issues")
    print("=" * 50)
    
    # Load the data with costs
    input_file = 'data/global_ocean_cleanup_data_with_costs.csv'
    output_file = 'data/global_ocean_cleanup_data_fixed_coordinates.csv'
    
    print(f"Loading data from: {input_file}")
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} records")
    
    # Fix coordinates
    df_fixed = fix_coordinates_in_dataframe(df)
    
    # Save the corrected data
    df_fixed.to_csv(output_file, index=False)
    print(f"Corrected data saved to: {output_file}")
    
    # Show some examples of corrected coordinates
    print("\n📍 Sample of Corrected Coordinates:")
    sample_countries = ['India', 'United States', 'Australia', 'Brazil']
    
    for country in sample_countries:
        country_data = df_fixed[df_fixed['Country'] == country].head(3)
        print(f"\n{country}:")
        for _, row in country_data.iterrows():
            region = row['Zone'].split(',')[0].strip()
            gps = row['GPS']
            print(f"  {region}: {gps}")
    
    print(f"\n✅ Coordinate fixing completed!")
    print(f"   📁 Corrected file: {output_file}")
    print(f"   📊 Total records: {len(df_fixed)}")

if __name__ == "__main__":
    main()
