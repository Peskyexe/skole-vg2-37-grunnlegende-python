import math

# Earth's average radius in meters
earth_radius = 6371000
rope_radius = earth_radius + 1

# Calculate Circumference: 2 * pi * radius
def calculate_circumference(radius):
    return 2 * math.pi * radius

earth_circumference = calculate_circumference(earth_radius)
rope_circumference = calculate_circumference(rope_radius)

print(f"The earth's circumference is {earth_circumference:.2f} meters.")
print(f"The length of the rope is {rope_circumference:.2f} meters.")

# Calculate and display how much longer the rope is
earth_rope_difference = rope_circumference - earth_circumference
print(f"The rope is {earth_rope_difference:.2f} meters longer than the earth's circumference.")