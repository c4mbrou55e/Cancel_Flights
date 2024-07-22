import time
import telnetlib

# Format to cancel flight
def generate_standard_flight_plan(identifier, departure, destination):
    return f"(CNL-{identifier}-{departure}-{destination})"

# Read flight information from file
def read_flight_info(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        
    flights = []
    for line in lines:
        flights.append(line.strip().split(','))
    
    return flights

# Generate canceled flight plans from file data
def generate_canceled_flight_plans_from_file(filename):
    flight_data = read_flight_info(filename)
    
    canceled_flights = []
    for flight in flight_data:
        if len(flight) >= 3:
            identifier, departure, destination = flight[:3]
            plan = generate_standard_flight_plan(identifier, departure, destination)
            canceled_flights.append(plan)

    return canceled_flights

# Send flight plans via Telnet
def send_flight_plans_via_telnet(ip, port, plans):
    try:
        with telnetlib.Telnet(ip, port) as tn:
            for plan in plans:
                tn.write(plan.encode('ascii') + b"\n")
                time.sleep(1)  # Wait before sending the next plan
    except Exception as e:
        print(f"Failed to send message via Telnet: {e}")

if __name__ == "__main__":
    # Define the IP and port for Telnet
    telnet_ip = "127.0.0.1"  # localhost
    telnet_port = 23

    canceled_flight_plans = generate_canceled_flight_plans_from_file('flight_plans.txt')
    send_flight_plans_via_telnet(telnet_ip, telnet_port, canceled_flight_plans)
