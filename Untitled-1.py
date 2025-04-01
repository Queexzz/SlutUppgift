def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def km_to_miles(km):
    return km * 0.621371

def miles_to_km(miles):
    return miles / 0.621371

def kg_to_pounds(kg):
    return kg * 2.20462

def pounds_to_kg(pounds):
    return pounds / 2.20462

def main():
    print("Välj vad du vill konvertera:")
    print("1: Celsius till Fahrenheit")
    print("2: Fahrenheit till Celsius")
    print("3: Kilometer till Miles")
    print("4: Miles till Kilometer")
    print("5: Kilogram till Pounds")
    print("6: Pounds till Kilogram")
    
    choice = input("Ange val (1-6): ")
    value = float(input("Ange värde att konvertera: "))
    
    if choice == "1":
        print("Resultat:", celsius_to_fahrenheit(value), "°F")
    elif choice == "2":
        print("Resultat:", fahrenheit_to_celsius(value), "°C")
    elif choice == "3":
        print("Resultat:", km_to_miles(value), "miles")
    elif choice == "4":
        print("Resultat:", miles_to_km(value), "km")
    elif choice == "5":
        print("Resultat:", kg_to_pounds(value), "pounds")
    elif choice == "6":
        print("Resultat:", pounds_to_kg(value), "kg")
    else:
        print("Felaktigt val!")

if __name__ == "__main__":
    main()