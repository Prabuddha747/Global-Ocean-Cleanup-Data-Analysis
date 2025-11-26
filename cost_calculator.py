import pandas as pd
import numpy as np
from datetime import datetime

class OceanCleanupCostCalculator:
    """
    Comprehensive cost calculator for ocean cleanup activities
    Calculates various cost components for each cleanup point
    """
    
    def __init__(self):
        # Base volunteer time value (2019 rate from Independent Sector)
        self.volunteer_hourly_rate = 25.43
        
        # Additional cost factors
        self.equipment_cost_per_person = 5.00  # USD per person for gloves, bags, tools
        self.transportation_cost_per_mile = 0.50  # USD per mile
        self.administrative_cost_per_event = 25.00  # USD per cleanup event
        self.disposal_cost_per_pound = 0.15  # USD per pound of waste disposed
        
        # Carbon footprint costs (USD per ton CO2)
        self.carbon_cost_per_ton = 50.00
        
    def calculate_volunteer_time_cost(self, people, hours_per_person=None):
        """
        Calculate the economic value of volunteer time
        """
        if hours_per_person is None:
            # Default: 32.1 hours per month / 3 = ~10.7 hours per person per cleanup
            hours_per_person = 32.1 / 3
        
        total_hours = people * hours_per_person
        volunteer_cost = total_hours * self.volunteer_hourly_rate
        
        return {
            'total_hours': total_hours,
            'volunteer_cost': volunteer_cost,
            'hours_per_person': hours_per_person
        }
    
    def calculate_equipment_cost(self, people):
        """
        Calculate equipment costs (gloves, bags, tools, etc.)
        """
        return people * self.equipment_cost_per_person
    
    def calculate_transportation_cost(self, miles):
        """
        Calculate transportation costs based on distance covered
        """
        return miles * self.transportation_cost_per_mile
    
    def calculate_disposal_cost(self, pounds):
        """
        Calculate waste disposal costs
        """
        return pounds * self.disposal_cost_per_pound
    
    def calculate_carbon_footprint_cost(self, pounds, bags):
        """
        Calculate carbon footprint and associated costs
        """
        # Estimate CO2 footprint based on waste collected
        # 1 bag ≈ 5 pounds, and 1 ton of waste ≈ 0.5 tons CO2
        carbon_footprint_tons = (pounds / 2000) * 0.5  # Convert to tons and apply factor
        carbon_cost = carbon_footprint_tons * self.carbon_cost_per_ton
        
        return {
            'carbon_footprint_tons': carbon_footprint_tons,
            'carbon_cost': carbon_cost
        }
    
    def calculate_efficiency_metrics(self, people, pounds, miles, hours):
        """
        Calculate efficiency metrics for the cleanup
        """
        if people == 0 or hours == 0:
            return {
                'pounds_per_person': 0,
                'pounds_per_hour': 0,
                'miles_per_person': 0,
                'cost_per_pound': 0,
                'cost_per_person': 0
            }
        
        pounds_per_person = pounds / people
        pounds_per_hour = pounds / hours if hours > 0 else 0
        miles_per_person = miles / people
        
        return {
            'pounds_per_person': pounds_per_person,
            'pounds_per_hour': pounds_per_hour,
            'miles_per_person': miles_per_person
        }
    
    def calculate_comprehensive_costs(self, cleanup_data):
        """
        Calculate all cost components for a single cleanup event
        """
        people = cleanup_data.get('People', 0)
        pounds = cleanup_data.get('Pounds', 0)
        miles = cleanup_data.get('Miles', 0)
        bags = cleanup_data.get('# of bags', 0)
        
        # Calculate volunteer time cost
        volunteer_data = self.calculate_volunteer_time_cost(people)
        
        # Calculate other costs
        equipment_cost = self.calculate_equipment_cost(people)
        transportation_cost = self.calculate_transportation_cost(miles)
        disposal_cost = self.calculate_disposal_cost(pounds)
        administrative_cost = self.administrative_cost_per_event
        
        # Calculate carbon footprint cost
        carbon_data = self.calculate_carbon_footprint_cost(pounds, bags)
        
        # Calculate efficiency metrics
        efficiency = self.calculate_efficiency_metrics(people, pounds, miles, volunteer_data['total_hours'])
        
        # Calculate total costs
        total_direct_costs = equipment_cost + transportation_cost + disposal_cost + administrative_cost
        total_cost = volunteer_data['volunteer_cost'] + total_direct_costs + carbon_data['carbon_cost']
        
        # Calculate cost per pound
        cost_per_pound = total_cost / pounds if pounds > 0 else 0
        cost_per_person = total_cost / people if people > 0 else 0
        
        return {
            # Volunteer costs
            'volunteer_hours': volunteer_data['total_hours'],
            'volunteer_cost': volunteer_data['volunteer_cost'],
            'hours_per_person': volunteer_data['hours_per_person'],
            
            # Direct costs
            'equipment_cost': equipment_cost,
            'transportation_cost': transportation_cost,
            'disposal_cost': disposal_cost,
            'administrative_cost': administrative_cost,
            'total_direct_costs': total_direct_costs,
            
            # Environmental costs
            'carbon_footprint_tons': carbon_data['carbon_footprint_tons'],
            'carbon_cost': carbon_data['carbon_cost'],
            
            # Total costs
            'total_cost': total_cost,
            'cost_per_pound': cost_per_pound,
            'cost_per_person': cost_per_person,
            
            # Efficiency metrics
            'pounds_per_person': efficiency['pounds_per_person'],
            'pounds_per_hour': efficiency['pounds_per_hour'],
            'miles_per_person': efficiency['miles_per_person']
        }
    
    def calculate_country_level_costs(self, df):
        """
        Calculate aggregated costs by country
        """
        country_costs = df.groupby('Country').agg({
            'People': 'sum',
            'Pounds': 'sum',
            'Miles': 'sum',
            '# of bags': 'sum',
            'volunteer_cost': 'sum',
            'total_direct_costs': 'sum',
            'carbon_cost': 'sum',
            'total_cost': 'sum'
        }).reset_index()
        
        # Calculate averages and ratios
        country_costs['cost_per_person'] = country_costs['total_cost'] / country_costs['People']
        country_costs['cost_per_pound'] = country_costs['total_cost'] / country_costs['Pounds']
        country_costs['pounds_per_person'] = country_costs['Pounds'] / country_costs['People']
        
        return country_costs

def add_cost_columns_to_dataframe(df, cost_calculator=None):
    """
    Add comprehensive cost columns to an existing dataframe
    """
    if cost_calculator is None:
        cost_calculator = OceanCleanupCostCalculator()
    
    # Calculate costs for each row
    cost_data = []
    for _, row in df.iterrows():
        costs = cost_calculator.calculate_comprehensive_costs(row)
        cost_data.append(costs)
    
    # Convert to DataFrame and merge with original data
    cost_df = pd.DataFrame(cost_data)
    result_df = pd.concat([df, cost_df], axis=1)
    
    return result_df

if __name__ == "__main__":
    # Test the cost calculator
    calculator = OceanCleanupCostCalculator()
    
    # Sample cleanup data
    sample_data = {
        'People': 25,
        'Pounds': 150.5,
        'Miles': 2.3,
        '# of bags': 8
    }
    
    costs = calculator.calculate_comprehensive_costs(sample_data)
    print("Sample Cost Analysis:")
    for key, value in costs.items():
        print(f"{key}: ${value:.2f}" if isinstance(value, (int, float)) else f"{key}: {value}")
