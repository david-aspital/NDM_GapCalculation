# Nested Demand Gap Calculation

This script calculates the demand for a nested demand model in Visum in line with the definition set out in TAG M2.1. 

The user should set the following in line with their model setup:
- `actpair_list`: A list of activity pair codes to be included in the calculation
- `modes`: A list of mode codes to be included in the calculation
- `util_mat_fil`: A string to be formatted with activity pair and mode codes to define the utility (or cost) matrix
- `demand_mat_fil`: A string to be formatted with activity pair and mode codes to define the current demand matrix
- `last_demand_mat_fil`: A string to be formatted with activity pair and mode codes to define the previous demand matrix