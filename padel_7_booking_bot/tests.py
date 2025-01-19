def extract_court_number_to_dict(function_calls):
    # Initialize an empty dictionary
    court_dict = {}

    # Iterate over each AJAX call string
    for call in function_calls:
        # Split the string to extract components
        parts = call.split(",")
        # Extract and convert the court number to an integer
        court_number = int(parts[1].strip("'"))
        # Add the court number and AJAX call to the dictionary
        court_dict[court_number] = call

    return court_dict

# Example usage
function_calls = [
    "ajaxHorariosFijosBooking('18:00-19:30','0','2');",
    "ajaxHorariosFijosBooking('18:00-19:30','3','2');",
    "ajaxHorariosFijosBooking('18:00-19:30','2','2');",
    "ajaxHorariosFijosBooking('18:00-19:30','10','2');",
    "ajaxHorariosFijosBooking('18:00-19:30','11','2');"
]

court_dict = extract_court_number_to_dict(function_calls)
print(court_dict)