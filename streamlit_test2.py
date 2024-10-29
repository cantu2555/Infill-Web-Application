import streamlit as st

def get_float_input(prompt):
    """Utility function to convert user input to float."""
    return float(prompt.replace(",", "").replace("$", ""))

def clean_and_convert(value):
    """Clean the input value to remove non-numeric characters and convert to float."""
    return float(value.replace(",", "").replace("$", ""))

def format_as_currency(value):
    """Format the number as currency with dollar sign and commas."""
    return "${:,.2f}".format(value)

# Streamlit app starts here
st.image('https://i.imgur.com/nxRdviJ.jpeg', width=200)  # 'logo.png' with your image path or URL
st.title('Incentive Package Calculator')

# Get user inputs as text
land_value_input = st.text_input('What is your land purchase value (e.g., $200,000)?', value="$0")
tenant_improve_input = st.text_input('What is your proposed tenant improvement value (e.g., $50,000)?', value="$0")

# Clean and convert inputs
land_value = clean_and_convert(land_value_input)
tenant_improve = clean_and_convert(tenant_improve_input)

# Display formatted values
st.write(f'Land purchase value: {format_as_currency(land_value)}')
st.write(f'Tenant improvement value: {format_as_currency(tenant_improve)}')

# Calculate total investment
total_investment = land_value + tenant_improve

# Display the dropdown only if total investment is 200,000 or more
field_type = 'NO'
if total_investment >= 200000:
    field_type = st.selectbox(
        'Is the property brownfield or greyfield?',
        ['Yes', 'NO']
    )
    st.write(f'You selected: {field_type}')

# Calculate incentive package when the button is pressed
if st.button('Calculate'):
    total_investment = land_value + tenant_improve
    city_tax_rate = 0.00818875 # Can be changed 

    # Calculate additional property values for each year
    additional_property_values = [tenant_improve * 0.6]  # Initial value for year 1
    for i in range(1, 10 if field_type == 'Yes' else 5):  # Extend to 10 years if brownfield or greyfield
        additional_property_values.append(additional_property_values[-1] * 1.03)

    # Calculate city tax projections for each year
    city_tax_projections = [value * city_tax_rate for value in additional_property_values]

    # Calculate tax rebate incentives for each year loop 
    tax_rebate_incentives = []
    for i in range(len(city_tax_projections)):
        if i < 3:  # 100% rebate for years 1 to 3
            tax_rebate_incentives.append(city_tax_projections[i])
        elif i < 5:  # 75% rebate for years 4 and 5
            tax_rebate_incentives.append(city_tax_projections[i] * 0.75)
        else:  # 50% rebate for years 6 to 10 (if applicable)
            tax_rebate_incentives.append(city_tax_projections[i] * 0.5)

    # Calculate total tax rebate over the period
    total_tax_rebate = sum(tax_rebate_incentives)

    # Calculate total incentive package
    construction_tax_rebate = (tenant_improve / 2) * 0.01
    building_construction_permit_fee_rebates = 2400
    total_incentive_package = total_tax_rebate + construction_tax_rebate + building_construction_permit_fee_rebates

    # Calculate 20% less and 20% more ranges
    total_tax_rebate_range = (total_tax_rebate * 0.8, total_tax_rebate * 1.2)
    construction_tax_rebate_range = (construction_tax_rebate * 0.8, construction_tax_rebate * 1.2)
    permit_fee_rebate_range = (building_construction_permit_fee_rebates * 0.8, building_construction_permit_fee_rebates * 1.2)
    total_incentive_package_range = (total_incentive_package * 0.8, total_incentive_package * 1.2)

    # Display ranges
    st.subheader('Potential Incentive Package Range')
    st.write(f'Potential property tax rebate over {len(tax_rebate_incentives)} years: '
         f'{format_as_currency(total_tax_rebate_range[0])} - {format_as_currency(total_tax_rebate_range[1])}')
    st.write(f'Potential construction material tax rebate: '
         f'{format_as_currency(construction_tax_rebate_range[0])} - {format_as_currency(construction_tax_rebate_range[1])}')
    st.write(f'Potential construction permit fee rebate: '
         f'{format_as_currency(permit_fee_rebate_range[0])} - {format_as_currency(permit_fee_rebate_range[1])}')
    st.write(f'Total Potential Incentive Package: '
         f'{format_as_currency(total_incentive_package_range[0])} - {format_as_currency(total_incentive_package_range[1])}')

    #  original results no ranges 
    # st.subheader('Potential Incentive Package')
    # st.write(f'Potential property tax rebate over {len(tax_rebate_incentives)} years: {format_as_currency(total_tax_rebate)}')
    # st.write(f'Potential construction material tax rebate: {format_as_currency(construction_tax_rebate)}')
    # st.write(f'Potential construction permit fee rebate: {format_as_currency(building_construction_permit_fee_rebates)}')
    # st.write(f'Total Potential Incentive Package: {format_as_currency(total_incentive_package)}')


# to run
#cd "C:\Users\CantuCT\Documents\Python Scripts"
#streamlit run streamlit_test2.py