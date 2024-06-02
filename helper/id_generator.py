import uuid

def generate_fitness_centre_id():
    fitness_centre_id  = f"gym_{str(uuid.uuid4().hex)[:6]}"  # Adjust the length as needed
    return fitness_centre_id

def generate_membership_id():
    membership_id  = f"mbs_{str(uuid.uuid4().hex)[:6]}"  # Adjust the length as needed
    return membership_id

print(generate_fitness_centre_id())