import census_debug as cd
import pandas as pd

CENSUS_DATA = 'data/BulkdatadetailedcharacteristicsmergedwardspluslaandregE&Wandinfo3.3'
f = None


def read_index():
    global f
    excel_file = CENSUS_DATA+'/Cell Numbered DC Tables 3.3.xlsx'
    cd.start_timer()
    f = pd.ExcelFile(excel_file)
    cd.print_timer('Read data Excel')       # 0.6s
    index = f.parse(sheet_name='Index')
    cd.print_timer('Read data Index')       # 0.02s
    return index


def read_table(table_name):
    cd.start_timer()
    if f == None:
        exit("Call read_index() to open table list")
    table = f.parse(sheet_name=table_name, header=None)
    # Column headings start at row 6, upto row that has data in column 0
    ALL_CATEGORIES = "All categories: "
    COL_HEAD_ROW = 6
    row = COL_HEAD_ROW
    while pd.isna(table.iloc[row, 0]):
        row += 1
    # Previous row has column names, earlier rows (if any) have hierarchy
    col_levels = row - COL_HEAD_ROW
    col_level_names = []
    col_level_values = [[] for _ in range(col_levels)]
    col = 1
    row = COL_HEAD_ROW
    while col < len(table.columns):
        for r in range(col_levels):
            if pd.isna(table.iloc[row+r, col]):
                col_level_values[r].append(col_level_values[r][-1])
            else:
                value = table.iloc[row+r, col]
                if value.startswith(ALL_CATEGORIES):
                    category = value[len(ALL_CATEGORIES):]
                    value = 'All'
                    if len(col_level_names) <= r:
                        col_level_names.append(category)
                col_level_values[r].append(value)
        col += 1

    # Row headings start after column headings, last level has data in column 1
    ROW_HEAD_ROW = COL_HEAD_ROW+col_levels
    row = ROW_HEAD_ROW
    while pd.isna(table.iloc[row, 1]):
        row += 1
    # This row has row name, earlier rows (if any) have hierarchy
    row_levels = row + 1 - ROW_HEAD_ROW
    row_level_names = []
    row_level_values = [[] for _ in range(row_levels)]
    row = ROW_HEAD_ROW
    level = -1
    wasLevel = True
    data_row_indexes = []
    while row < len(table.index) and not pd.isna(table.iloc[row, 0]):
        if wasLevel or pd.isna(table.iloc[row, 1]):
            level += 1
            if level >= row_levels:
                level = 0
            if pd.isna(table.iloc[row, 1]):
                wasLevel = True
            else:
                wasLevel = False
        value = table.iloc[row, 0]
        if value.startswith(ALL_CATEGORIES):
            category = value[len(ALL_CATEGORIES):]
            value = 'All'
            if len(row_level_names) < row_levels:
                row_level_names.append(category)
        row_level_values[level].append(value)
        if level+1 == row_levels:
            for l in range(level):
                if len(row_level_values[l]) < len(row_level_values[level]):
                    row_level_values[l].append(row_level_values[l][-1])
            data_row_indexes.append(row)
        row += 1
    # print('tableName='+table_name)
    # print(col_level_names)
    # print(col_level_values)
    # print(row_level_names)
    # print(row_level_values)

    # Construct DataFrame
    num_cols = len(col_level_values[0])
    num_rows = len(row_level_values[0])
    for l in range(row_levels):
        # Repeat row values in order
        row_level_values[l] = [x for x in row_level_values[l]
                               for n in range(num_cols)]
    for l in range(col_levels):
        # Repeat col values in turn
        col_level_values[l] = col_level_values[l] * num_rows
    values = []
    for r in range(0, num_rows):
        row = data_row_indexes[r]
        values.extend(table.iloc[row, 1:])
    values = [str(int).zfill(4) for int in values]
    data = [row_level_values[l] for l in range(row_levels)] + \
           [col_level_values[l] for l in range(col_levels)] + \
        [values]
    index = row_level_names+col_level_names+['Dataset']
    df = pd.DataFrame(
        data=data,
        index=index
    )
    df = df.transpose()
    cd.print_timer(f'Load table {table_name}')  # 0.06s
    return df


def read_data(table_name):
    datafile = CENSUS_DATA + '/' + table_name + 'DATA.CSV'
    # DC1104EW0001	All categories: Age, All categories: Residence type, All categories: Sex
    cd.start_timer()
    df = pd.read_csv(datafile)
    cd.print_timer(f'Load data {table_name}')  # 0.03s
    return df


def read_data_item(table_name, item_name):
    datafile = CENSUS_DATA + '/' + table_name + 'DATA.CSV'
    # DC1104EW0001	All categories: Age, All categories: Residence type, All categories: Sex
    datacol = table_name+item_name
    locationcol = "GeographyCode"
    columns = [locationcol, datacol]
    cd.start_timer()
    df = pd.read_csv(datafile, usecols=columns)
    cd.print_timer(f'Load table {table_name} data {item_name}')     # 0.01s
    return df


def read_geography():
    # Get Census Merged Ward and Local Authority Data
    cd.start_timer()
    lookupfile = 'data/Ward_to_Census_Merged_Ward_to_Local_Authority_District_(December_2011)_Lookup_in_England_and_Wales.csv'
    cmwd = pd.read_csv(lookupfile, usecols=[
        'CMWD11CD', 'CMWD11NM', 'LAD11CD', 'LAD11NM'])
    cmwd.drop_duplicates(inplace=True)
    locationcol = "GeographyCode"
    cmwd[locationcol] = cmwd['CMWD11CD']
    namecol = 'Name'
    cmwd[namecol] = cmwd['CMWD11NM']
    lad = pd.read_csv(lookupfile, usecols=['LAD11CD', 'LAD11NM'])
    lad = lad.drop_duplicates()
    lad[locationcol] = lad['LAD11CD']
    lad[namecol] = lad['LAD11NM']
    lad['CMWD11CD'] = ''
    lad['CMWD11NM'] = ''
    geography = pd.concat([cmwd, lad])
    cd.print_timer('Load geography')
    return geography


def get_table_names(index):
    names = [(index.loc[i, 'Table Number'], index.loc[i, 'Table Title'])
             for i in range(index.shape[0])]
    return names


def get_table_columns(tdf):
    return list(tdf.columns[:-1].values)


def get_table_column_values(tdf):
    return [tdf[col].unique().tolist() for col in get_table_columns(tdf)]


def get_table_column_names_and_values(tdf):
    return [(col, tdf[col].unique().tolist()) for col in get_table_columns(tdf)]


if __name__ == '__main__':
    index = read_index()
    print(index.head())
    print(get_table_names(index))
    table_name = index['Table Number'][6]
    tdf = read_table(table_name)
    print(get_table_columns(tdf))
    print(get_table_column_values(tdf))
    print(get_table_column_names_and_values(tdf))
    print(tdf.head())
    data_name = tdf['Dataset'][0]
    # df = read_data_item(table_name, data_name)
    # print(df.head())
    df = read_data(table_name)
    print(df.head())
