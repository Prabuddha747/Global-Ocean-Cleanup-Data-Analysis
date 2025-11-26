#!/usr/bin/env python3
"""
Create a corrected global ocean cleanup map with accurate coordinates
"""

import os

import pandas as pd
import folium
from folium import plugins
import numpy as np

DEFAULT_COASTAL_DATA = 'data/global_ocean_cleanup_data_coastal_only.csv'
FALLBACK_DATA = 'data/global_ocean_cleanup_data_fixed_coordinates.csv'


def create_corrected_global_map(csv_file=DEFAULT_COASTAL_DATA):
    """
    Create an interactive global map with corrected coordinates
    """
    print("Loading global cleanup data with corrected coordinates...")
    
    # Load the data
    try:
        df = pd.read_csv(csv_file)
        print(f"Loaded {len(df)} cleanup records from {csv_file}")
    except FileNotFoundError:
        if csv_file != FALLBACK_DATA and os.path.exists(FALLBACK_DATA):
            print(f"File {csv_file} not found. Falling back to {FALLBACK_DATA}.")
            df = pd.read_csv(FALLBACK_DATA)
        else:
            print(f"File {csv_file} not found. Please run fix_coordinates.py first.")
            return None
    
    # Create base map
    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles='cartodbdark_matter',
        max_zoom=18,
        min_zoom=1
    )
    
    # Create marker cluster group for better performance and interactivity
    marker_cluster = plugins.MarkerCluster(
        name="Cleanup Sites",
        disableClusteringAtZoom=8,
        showCoverageOnHover=False
    )
    marker_cluster.add_to(m)
    
    # Define color scheme based on total cost
    def get_cost_color(cost):
        if cost < 1000:
            return 'green'
        elif cost < 5000:
            return 'yellow'
        elif cost < 10000:
            return 'orange'
        elif cost < 15000:
            return 'red'
        else:
            return 'darkred'
    
    # Define size based on total cost
    def get_cost_size(cost):
        if cost < 1000:
            return 4
        elif cost < 5000:
            return 6
        elif cost < 10000:
            return 8
        elif cost < 15000:
            return 10
        else:
            return 12
    
    # Add markers for each cleanup point
    for idx, row in df.iterrows():
        # Parse GPS coordinates
        try:
            lat, lon = map(float, row['GPS'].split(', '))
        except:
            continue
        
        # Create popup content with cost details
        popup_content = f"""
        <div style="width: 300px;">
            <h4><b>{row['Country']} Cleanup Site</b></h4>
            <p><b>Location:</b> {row['Zone']}</p>
            <p><b>Date:</b> {row['Cleanup Date']}</p>
            <p><b>Group:</b> {row['Group Name']}</p>
            <p><b>People:</b> {row['People']}</p>
            <p><b>Pounds:</b> {row['Pounds']:.2f}</p>
            <p><b>Total Items:</b> {row['Total Items Collected']}</p>
            <hr>
            <h5><b>Cost Analysis:</b></h5>
            <p><b>Total Cost:</b> ${row['total_cost']:.2f}</p>
            <p><b>Volunteer Value:</b> ${row['volunteer_cost']:.2f}</p>
            <p><b>Direct Costs:</b> ${row['total_direct_costs']:.2f}</p>
            <p><b>Carbon Cost:</b> ${row['carbon_cost']:.2f}</p>
            <p><b>Cost per Pound:</b> ${row['cost_per_pound']:.2f}</p>
            <p><b>Cost per Person:</b> ${row['cost_per_person']:.2f}</p>
        </div>
        """
        
        # Determine marker appearance
        marker_radius = get_cost_size(row['total_cost'])
        marker_diameter = marker_radius * 2
        marker_color = get_cost_color(row['total_cost'])

        # Create HTML for a circle marker rendered via DivIcon
        icon_html = f"""
        <div style="
            background:{marker_color};
            width:{marker_diameter}px;
            height:{marker_diameter}px;
            border-radius:50%;
            border:1px solid black;
            opacity:0.8;
        "></div>
        """

        marker = folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(
                html=icon_html,
                icon_size=(marker_diameter, marker_diameter),
                icon_anchor=(marker_radius, marker_radius)
            ),
            popup=folium.Popup(popup_content, max_width=350),
            tooltip=f"${row['total_cost']:.2f} - {row['Country']}"
        )
        marker.add_to(marker_cluster)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 120px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p><b>Total Cost Legend</b></p>
    <p><i class="fa fa-circle" style="color:green"></i> < $1,000</p>
    <p><i class="fa fa-circle" style="color:yellow"></i> $1,000-$5,000</p>
    <p><i class="fa fa-circle" style="color:orange"></i> $5,000-$10,000</p>
    <p><i class="fa fa-circle" style="color:red"></i> $10,000-$15,000</p>
    <p><i class="fa fa-circle" style="color:darkred"></i> > $15,000</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Add cost statistics layer
    add_cost_statistics_layer(m, df)
    
    # Save map
    output_file = 'maps/corrected_global_world_map.html'
    m.save(output_file)
    print(f"Corrected map saved to: {output_file}")
    
    return m

def add_cost_statistics_layer(m, df):
    """
    Add a statistics layer showing cost summaries by country
    """
    # Calculate country-level statistics
    country_stats = df.groupby('Country').agg({
        'total_cost': ['sum', 'mean', 'count'],
        'volunteer_cost': 'sum',
        'total_direct_costs': 'sum',
        'carbon_cost': 'sum',
        'People': 'sum',
        'Pounds': 'sum'
    }).round(2)
    
    # Flatten column names
    country_stats.columns = ['_'.join(col).strip() for col in country_stats.columns]
    country_stats = country_stats.reset_index()
    
    # Add text layer with top countries
    top_countries = country_stats.nlargest(10, 'total_cost_sum')
    
    stats_html = f"""
    <div style="position: fixed; 
                top: 50px; right: 50px; width: 300px; height: 400px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:12px; padding: 10px; overflow-y: auto;">
    <h4><b>Top 10 Countries by Total Cost</b></h4>
    """
    
    for i, (_, country) in enumerate(top_countries.iterrows(), 1):
        stats_html += f"""
        <p><b>{i}.</b> {country['Country']}</p>
        <p style="margin-left: 20px;">
            Total: ${country['total_cost_sum']:,.0f}<br>
            Events: {country['total_cost_count']:.0f}<br>
            Avg/Event: ${country['total_cost_mean']:.0f}<br>
            People: {country['People_sum']:,.0f}<br>
            Pounds: {country['Pounds_sum']:,.0f}
        </p>
        """
    
    stats_html += "</div>"
    m.get_root().html.add_child(folium.Element(stats_html))

def create_india_focused_map(csv_file=DEFAULT_COASTAL_DATA):
    """
    Create a focused map on India to verify coordinate corrections
    """
    print("Creating India-focused map to verify coordinate corrections...")
    
    # Load the data
    if not os.path.exists(csv_file) and csv_file != FALLBACK_DATA:
        print(f"India map csv {csv_file} not found. Falling back to {FALLBACK_DATA}.")
        csv_file = FALLBACK_DATA

    df = pd.read_csv(csv_file)
    
    # Filter for India only
    india_df = df[df['Country'] == 'India']
    print(f"Found {len(india_df)} cleanup points in India")
    
    # Create base map centered on India
    m = folium.Map(
        location=[20.5, 78.0],  # Center on India
        zoom_start=5,
        tiles='OpenStreetMap'
    )
    
    # Create marker cluster group for better performance and interactivity
    marker_cluster = folium.plugins.MarkerCluster().add_to(m)
    
    # Add markers for Indian cleanup points
    for idx, row in india_df.iterrows():
        try:
            lat, lon = map(float, row['GPS'].split(', '))
        except:
            continue
        
        # Create popup content
        popup_content = f"""
        <div style="width: 250px;">
            <h4><b>India Cleanup Site</b></h4>
            <p><b>Location:</b> {row['Zone']}</p>
            <p><b>Date:</b> {row['Cleanup Date']}</p>
            <p><b>Group:</b> {row['Group Name']}</p>
            <p><b>People:</b> {row['People']}</p>
            <p><b>Pounds:</b> {row['Pounds']:.2f}</p>
            <p><b>Total Items:</b> {row['Total Items Collected']}</p>
            <hr>
            <p><b>Total Cost:</b> ${row['total_cost']:.2f}</p>
            <p><b>Cost per Pound:</b> ${row['cost_per_pound']:.2f}</p>
        </div>
        """
        
        # Add marker to cluster group
        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            popup=folium.Popup(popup_content, max_width=300),
            color='red',
            weight=2,
            fillColor='lightblue',
            fillOpacity=0.7,
            tooltip=f"{row['Zone']} - ${row['total_cost']:.2f}"
        ).add_to(marker_cluster)
    
    # Save India-focused map
    output_file = 'maps/india_corrected_map.html'
    m.save(output_file)
    print(f"India-focused map saved to: {output_file}")
    
    return m

def main():
    """
    Main function to create corrected maps
    """
    print("🌊 Creating Corrected Global Ocean Cleanup Maps")
    print("=" * 60)
    
    # Create the main corrected global map
    data_source = DEFAULT_COASTAL_DATA if os.path.exists(DEFAULT_COASTAL_DATA) else FALLBACK_DATA
    global_map = create_corrected_global_map(data_source)
    
    # Create India-focused map for verification
    india_map = create_india_focused_map(data_source)
    
    print("\n✅ Corrected maps created successfully!")
    print("   📁 Global map: maps/corrected_global_world_map.html")
    print("   📁 India map: maps/india_corrected_map.html")
    print("\n📍 The coordinates should now be correctly positioned!")

if __name__ == "__main__":
    main()