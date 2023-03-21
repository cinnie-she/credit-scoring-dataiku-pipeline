"""
Good/Bad Definition:
Change categorical multi-value dropdown based on changes in column choice for
indeterminate categorical definitions
"""
@app.callback(
    Output("indeterminate_categoric_def_list", "children"),
    Input({"index": ALL, "type": "indeterminate_categorical_column"}, "value"),
    [
        State("categorical_columns", "data"),
        State({"index": ALL, "type": "indeterminate_categorical_element"}, "value"),
        State({"index": ALL, "type": "indeterminate_categorical_checkbox"}, "value"),
    ],
)
def update_multi_value_dropdown_bad_categorical(column_list, categoric_col_data, elements_list, checkbox_list):
    new_spec = [
        (column, elements, selected) for column, elements, selected in zip(column_list, elements_list, checkbox_list)
        if not (removing and selected)
    ]
    new_list = [
        html.Div([
            html.P(str(idx+1) + ".",
                   style={"float": "left", "marginRight": 5}),
            dcc.Dropdown(
                options=convert_column_list_to_dropdown_options(
                    json.loads(categoric_col_data)),
                value=column,
                clearable=False,
                searchable=False,
                style={"width": 180},
                id={"index": idx, "type": "indeterminate_categorical_column"},
            ),
            html.P(
                " :", style={"float": "left", "marginLeft": 5, "fontWeight": "bold", "marginRight": 10}
            ),
            dcc.Dropdown(
                options=convert_column_list_to_dropdown_options(df[column].unique()),
                value=elements,
                multi=True,
                style={"width": 500},
                id={"index": idx, "type": "indeterminate_categorical_element"},
            ),
            dcc.Checklist(
                id={"index": idx, "type": "indeterminate_categorical_checkbox"},
                options=[{"label": "", "value": "selected"}],
                value=selected,
                style={"display": "inline", "marginLeft": 15},
            )
        ], style={"display": "flex", "alignItems": "flex-end", "marginTop": 10})
        for idx, (column, elements, selected) in enumerate(new_spec)
    ]
    return new_list