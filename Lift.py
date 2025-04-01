import time

def elevator_simulator():
    current_floor = 1
    
    while True:
        print(f"\nHissen är på våning {current_floor}")
        destination = input("Ange våning (1-10) eller 'q' för att avsluta: ")
        
        if destination.lower() == 'q':
            print("Hissen stannar. Hej då!")
            break
        
        if not destination.isdigit():
            print("Felaktig inmatning. Ange en siffra mellan 1 och 10.")
            continue
        
        destination = int(destination)
        
        if destination < 1 or destination > 10:
            print("Felaktigt våningsval. Ange en siffra mellan 1 och 10.")
            continue
        
        print("Hissen rör sig...")
        time.sleep(abs(destination - current_floor) * 1)
        current_floor = destination
        print(f"Hissen har nått våning {current_floor}")

if __name__ == "__main__":
    elevator_simulator()
