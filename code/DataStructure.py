# Bins Settings data structure
bins_settings = {
    "variables": [
        {
            "column": "person_age",  # from Confirm Input Dataset Page
            "type": "numerical",  # from Confirm Input Dataset Page
            "info_val": 0.09,
            "bins": "none",  # either algo or custom binning (default = "none") ["none", "equal width", "equal frequency", (custom binning)]
        },
        {
            "column": "person_income",
            "type": "numerical",
            "info_val": 0.11,
            "bins": [
                {
                    "name": "0-9999, 30000-39999",
                    "cut_points": [[0, 9999], [30000, 39999]],
                },
                {
                    "name": "20000-29999",
                    "cut_points": [[20000, 29999]],
                },
            ],
        },
        {
            "column": "loan_grade",
            "type": "categorical",
            "info_val": 0.33,
            "bins": "eqaul width",
        },
        {
            "column": "person_home_ownership",
            "type": "categorical",
            "info_val": 0.07,
            "bins": [
                {
                    "name": "RENT, MORTGAGE",
                    "members": ["RENT", "MORTGAGE"],
                },
                {
                    "name": "OWN",
                    "members": ["OWN"],
                },
            ],
        },
    ]
}

# Good bad definition data structure.
good_bad_def = {
    "bad": {
        "numerical": [
            {
                "column": "person_age",
                "ranges": [[18, 22]],  # 22 is exclusive
            },
            {
                "column": "paid_past_due",
                "ranges": [[90, 121], [70, 80]],  # 121 is exclusive
            }
        ],
        "categorical": [
            {
                "column": "loan_status",
                "elements": ["1"]
            },
            {
                "column": "person_home_ownership",
                "elements": ["rent", "mortgage"]
            }
        ],
        "weight": 1.00
    },
    "indeterminate": {
        "numerical": [
            {
                "column": "person_age",
                "ranges": [[25, 30]],  # 30 is exclusive
            },
            {
                "column": "paid_past_due",
                "ranges": [[60, 90]],  # 90 is exclusive
            }
        ],
        "categorical": [
            {
                "column": "loan_grade",
                "elements": ["C", "D", "E"],
            }
        ],
    },
    "good": {
        "weight": 1.49
    }
}