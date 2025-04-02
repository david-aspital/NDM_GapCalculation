
# Update here with activity pair(s) to be included in the gap calculation 
actpair_list = ['HBW', 'HBEB', 'HBED', 'HBSHOPPB', 'HBRECVFR', 'NHBEB', 'NHBO']

# List of modes to be included in the gap calculation (bottom of the tree at each branch in the hierarchy)
modes = ['Car SubMode', 'Bus SubMode', 'Bus PR SubMode', 'Rail SubMode', 'Rail PR SubMode', 'Cycle', 'Walk']

# Filter text for utility, current demand and last demand matrices
util_mat_fil = 'Matrix([CODE]="GenTime {} {}")'
demand_mat_fil = 'Matrix([CODE]="{} {}" & [NAME]="{}")'
last_demand_mat_fil = 'Matrix([NAME]="Previous demand {} x {}")'


def insert_UDA_if_missing(visum_container, uda_name, value_type = None):
    # starts from end (UDAs are listed last)
    is_uda_missing = True
    for current_attr in reversed(visum_container.Attributes.GetAll):
        if str(current_attr.ID).upper() == uda_name.upper():
            is_uda_missing = False
            break

    if is_uda_missing:
        visum_container.AddUserDefinedAttribute(uda_name, uda_name, uda_name, value_type if value_type is not None else 1)


def calc_numerator(temp_mat, utility_mat, new_demand_mat, last_demand_mat):
    # Calculates the numerator term to be added with utility * | new demand - last demand | and then the matrix sum of this
    temp_mat.SetValuesToResultOfFormula(f"{utility_mat}*ABS({new_demand_mat}-{last_demand_mat})")

    return temp_mat.AttValue('Sum')

def calc_denominator(temp_mat, utility_mat, last_demand_mat):
    # Calculates the denominator term to be added with utility * last demand  and then the matrix sum of this
    temp_mat.SetValuesToResultOfFormula(f"{utility_mat}*{last_demand_mat}")

    return temp_mat.AttValue('Sum')

def update_value(att, value_add):
    # Updates the attribute value by adding something to it
    value = Visum.Net.AttValue(att)
    value += value_add
    Visum.Net.SetAttValue(att, value)


def main():

    # Create temp matrix to be used for calculations here
    temp_mat_num = 999999
    temp_mat_num_exists = temp_mat_num in [x[0] for x in Visum.Net.Matrices.GetMultipleAttributes(["NO"])]
    if temp_mat_num_exists:
        temp_mat = Visum.Net.Matrices.ItemByKey(temp_mat_num)
    else:
        temp_mat = Visum.Net.AddMatrix(temp_mat_num)

    # add UDAs if not already in Network
    insert_UDA_if_missing(Visum.Net, 'GAP_Numerator', 2)
    insert_UDA_if_missing(Visum.Net, 'GAP_Denominator', 2)


    for actpair in actpair_list:

        # Get all demand strata associated with the activity pair
        dstrata = Visum.Net.DemandStrata.GetFilteredSet(f'[DEMANDMODELCODE]="{actpair}"')
        dstrata_list = [x[0] for x in dstrata.GetMultipleAttributes(['CODE'])]

        for dstratum in dstrata_list:

            for mode in modes:

                # Get filter strings for utility, demand and last demand matrices
                util_matrix = util_mat_fil.format(mode, dstratum)
                last_demand_matrix = last_demand_mat_fil.format(dstratum, mode)
                demand_matrix = demand_mat_fil.format(actpair, mode, dstratum)

                # Calculate numerator and add to existing value
                numerator = calc_numerator(temp_mat, util_matrix, demand_matrix, last_demand_matrix)
                update_value('GAP_Numerator', numerator)

                # Calculate denominator and add to existing value
                denominator = calc_denominator(temp_mat, util_matrix, last_demand_matrix)
                update_value('GAP_Denominator', denominator)

if __name__ == 'main':
    main()
