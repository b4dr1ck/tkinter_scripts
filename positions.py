#!/usr/bin/python3

def position_it(root,positions_array,grid_conf={}):
    """
    @param root: Tkinter root or container-object
    @param positions_array: 2D array of widgets
    @param grid_conf: dictionary of additional grid configuration options
    """
    # Configure columns to expand proportionally
    max_columns = max(len(row) for row in positions_array)
    for col in range(max_columns):
        root.grid_columnconfigure(col, weight=1)

    # Place widgets in the grid
    for row_i, row in enumerate(positions_array):
        for col_i, widget in enumerate(row):
            # If it's the last widget in the row, set columnspan to fill the remaining space
            if col_i == len(row) - 1:
                widget.grid(row=row_i, column=col_i, columnspan=max_columns - col_i, **grid_conf)
            else:
                widget.grid(row=row_i, column=col_i,**grid_conf)