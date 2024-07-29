#carter quesenberry ozone layer project 8
import pandas as pd
import matplotlib.pyplot as plt

# get state codes from files:
with open('state_codes.txt') as file:
    state_codes = dict(line.strip().split(',') for line in file)

# get state counties from files:
counties_by_state = {}
with open('counties.txt') as file:
    current_state = ""
    for line in file:
        if line.strip() and not line.startswith("\t"):
            current_state = line.strip()
            counties_by_state[current_state] = []
        elif line.startswith("\t"):
            counties_by_state[current_state].append(line.strip())

# get the AQI data:
df = pd.read_csv('daily_44201_2021.csv', low_memory=False)

# function to plot AQI
def plot_aqi(state, county, destination='Screen'):
    data = df.loc[(df['State Name'] == state) & (df['County Name'] == county), 'AQI']
    avg_aqi = data.mean()
    _, axis = plt.subplots()
    color = 'green' if avg_aqi <= 50 else 'red'
    axis.plot(data, color=color, linewidth=0.5)
    axis.set_title(f"{county} County, {state} - Average AQI: {round(avg_aqi)}")
    plt.xlabel("Days")
    plt.ylabel("AQI")

    if destination == 'Screen':
        # display to screen:
        plt.show()
    else:
        # save to files:
        plt.savefig(f'{destination}')
    plt.close()

print("Loading data...")
while True:
    state_code = input("Enter 2-letter state code (Q to quit): ").lower()
    if state_code == 'q':
        break

    state_name = state_codes.get(state_code.upper())
    if not state_name:
        print("Invalid state code!")
        continue

    repeat = 'y'
    while repeat.lower() == 'y':
        counties = counties_by_state.get(state_name, [])
        for i, county in enumerate(counties, 1):
            print(f"{i}: {county}")

        valid_county_number = False
        while not valid_county_number:
            try:
                county_number = int(input("Enter number for county: ")) - 1
                if 0 <= county_number < len(counties):
                    valid_county_number = True
                else:
                    print("Invalid county code!")
            except ValueError:
                print("Invalid county code!")

        county_name = counties[county_number]
        print("Choose destination for plot:\n     1    Screen\n     2    File")
        choice = input()

        if choice == '1':
            plot_aqi(state_name, county_name)
            print("Displayed.")
        elif choice == '2':
            filename = input("Enter file name with extension (jpg, png, pdf): ")
            plot_aqi(state_name, county_name, filename)
            print("Saved.")

        repeat = input(f"Another {state_name} county? (y/n): ")