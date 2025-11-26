import pandas as pd
import folium
from folium import plugins
import numpy as np
from cost_calculator import OceanCleanupCostCalculator

def create_global_cost_map(csv_file='data/global_ocean_cleanup_data_with_costs.csv'):
    """
    Create an interactive global map showing ocean cleanup costs for each point
    """
    print("Loading global cleanup data with costs...")
    
    # Load the data
    try:
        df = pd.read_csv(csv_file)
        print(f"Loaded {len(df)} cleanup records with cost data")
    except FileNotFoundError:
        print(f"File {csv_file} not found. Please run generate_global_cleanup_data.py first.")
        return None
    
    # Create base map
    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles='OpenStreetMap'
    )
    
    # Define color scheme based on total cost
    def get_cost_color(cost):
        if cost < 100:
            return 'green'
        elif cost < 500:
            return 'yellow'
        elif cost < 1000:
            return 'orange'
        elif cost < 2000:
            return 'red'
        else:
            return 'darkred'
    
    # Define size based on total cost
    def get_cost_size(cost):
        if cost < 100:
            return 4
        elif cost < 500:
            return 6
        elif cost < 1000:
            return 8
        elif cost < 2000:
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
            <p><b>People:</b> {row['People']}</p>
            <p><b>Pounds:</b> {row['Pounds']:.2f}</p>
            <p><b>Miles:</b> {row['Miles']:.2f}</p>
            <hr>
            <h5><b>Cost Analysis:</b></h5>
            <p><b>Total Cost:</b> ${row['total_cost']:.2f}</p>
            <p><b>Volunteer Value:</b> ${row['volunteer_cost']:.2f}</p>
            <p><b>Direct Costs:</b> ${row['total_direct_costs']:.2f}</p>
            <p><b>Carbon Cost:</b> ${row['carbon_cost']:.2f}</p>
            <p><b>Cost per Pound:</b> ${row['cost_per_pound']:.2f}</p>
            <p><b>Cost per Person:</b> ${row['cost_per_person']:.2f}</p>
            <hr>
            <p><b>Efficiency:</b></p>
            <p>Pounds per Person: {row['pounds_per_person']:.2f}</p>
            <p>Pounds per Hour: {row['pounds_per_hour']:.2f}</p>
        </div>
        """
        
        # Add marker
        folium.CircleMarker(
            location=[lat, lon],
            radius=get_cost_size(row['total_cost']),
            popup=folium.Popup(popup_content, max_width=350),
            color='black',
            weight=1,
            fillColor=get_cost_color(row['total_cost']),
            fillOpacity=0.7,
            tooltip=f"${row['total_cost']:.2f} - {row['Country']}"
        ).add_to(m)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 120px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p><b>Total Cost Legend</b></p>
    <p><i class="fa fa-circle" style="color:green"></i> < $100</p>
    <p><i class="fa fa-circle" style="color:yellow"></i> $100-$500</p>
    <p><i class="fa fa-circle" style="color:orange"></i> $500-$1,000</p>
    <p><i class="fa fa-circle" style="color:red"></i> $1,000-$2,000</p>
    <p><i class="fa fa-circle" style="color:darkred"></i> > $2,000</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Add cost statistics layer
    add_cost_statistics_layer(m, df)
    
    # Save map
    output_file = 'maps/global_ocean_cleanup_cost_map.html'
    m.save(output_file)
    print(f"Cost map saved to: {output_file}")
    
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

def create_cost_heatmap(csv_file='data/global_ocean_cleanup_data_with_costs.csv'):
    """
    Create a heatmap showing cost density
    """
    print("Creating cost density heatmap...")
    
    # Load data
    df = pd.read_csv(csv_file)
    
    # Parse coordinates and prepare heatmap data
    heat_data = []
    for idx, row in df.iterrows():
        try:
            lat, lon = map(float, row['GPS'].split(', '))
            # Use total cost as weight for heatmap
            heat_data.append([lat, lon, row['total_cost']])
        except:
            continue
    
    # Create base map
    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles='OpenStreetMap'
    )
    
    # Add heatmap
    plugins.HeatMap(
        heat_data,
        name='Cost Density Heatmap',
        min_opacity=0.2,
        max_zoom=18,
        radius=25,
        blur=15,
        gradient={0.2: 'blue', 0.4: 'cyan', 0.6: 'lime', 0.8: 'yellow', 1.0: 'red'}
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Save heatmap
    output_file = 'maps/global_ocean_cleanup_cost_heatmap.html'
    m.save(output_file)
    print(f"Cost heatmap saved to: {output_file}")
    
    return m

def create_cost_analysis_dashboard(csv_file='data/global_ocean_cleanup_data_with_costs.csv'):
    """
    Create a comprehensive cost analysis dashboard
    """
    print("Creating cost analysis dashboard...")
    
    # Load data
    df = pd.read_csv(csv_file)
    
    # Calculate global statistics
    total_cost = df['total_cost'].sum()
    total_volunteer_cost = df['volunteer_cost'].sum()
    total_direct_costs = df['total_direct_costs'].sum()
    total_carbon_cost = df['carbon_cost'].sum()
    
    # Create dashboard HTML
    dashboard_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Global Ocean Cleanup Cost Analysis Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background-color: #2E8B57; color: white; padding: 20px; text-align: center; }}
            .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }}
            .stat-card {{ background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 5px solid #2E8B57; }}
            .stat-value {{ font-size: 2em; font-weight: bold; color: #2E8B57; }}
            .stat-label {{ color: #666; margin-top: 10px; }}
            .chart-container {{ margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Global Ocean Cleanup Cost Analysis Dashboard</h1>
            <p>Comprehensive cost analysis for {len(df):,} cleanup events across {df['Country'].nunique()} countries</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">${total_cost:,.0f}</div>
                <div class="stat-label">Total Cost</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${total_volunteer_cost:,.0f}</div>
                <div class="stat-label">Volunteer Time Value</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${total_direct_costs:,.0f}</div>
                <div class="stat-label">Direct Costs</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${total_carbon_cost:,.0f}</div>
                <div class="stat-label">Carbon Footprint Cost</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h3>Cost Breakdown</h3>
            <p>Volunteer Time Value: {total_volunteer_cost/total_cost*100:.1f}%</p>
            <p>Direct Costs: {total_direct_costs/total_cost*100:.1f}%</p>
            <p>Carbon Footprint Cost: {total_carbon_cost/total_cost*100:.1f}%</p>
        </div>
    </body>
    </html>
    """
    
    # Save dashboard
    output_file = 'maps/global_ocean_cleanup_cost_dashboard.html'
    with open(output_file, 'w') as f:
        f.write(dashboard_html)
    
    print(f"Cost dashboard saved to: {output_file}")

if __name__ == "__main__":
    print("Creating global ocean cleanup cost visualizations...")
    
    # Create cost map
    cost_map = create_global_cost_map()
    
    # Create cost heatmap
    cost_heatmap = create_cost_heatmap()
    
    # Create cost dashboard
    create_cost_analysis_dashboard()
    
    print("All cost visualizations created successfully!")
