"""
Unused code scripts

def get_lat():
    lats = []
    for sheet in file_sheets:
        fs = file[sheet]
        fs_count_row = fs.max_row
        fs_count_column = fs.max_column

        for row in range(2, fs_count_row + 1):
            for column in range(3, 4):
                cell = fs.cell(column=column, row=row)
                cell_value = fs.cell(row, column).value
                lats.append(cell_value)

        return lats


def get_lon():
    lons = []
    for sheet in file_sheets:
        fs = file[sheet]
        fs_count_row = fs.max_row
        fs_count_column = fs.max_column

        for row in range(2, fs_count_row + 1):
            for column in range(4, 5):
                cell = fs.cell(column=column, row=row)
                cell_value = fs.cell(row, column).value
                lons.append(cell_value)

        return lons



"""

"""
def dividends_growth_graph(graph_data):
 
    data = list(graph_data.values())
    years = list(graph_data.keys())

    # Create a bar graph using Seaborn
    # "amount" assumed for y-axis
    plot = sns.barplot(x=years, y="amount", data=data)

    # Customize the graph (optional)
    plot.set_xlabel("Ano")
    plot.set_ylabel("Dividendos (€)")
    plot.set_title("Crescimento total dos dividendos YoY")

    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png')
    plt.close()  # Close the plot to avoid memory leaks
    image_buffer.seek(0)  # Reset the cursor to the beginning of the buffer
    return image_buffer
"""
