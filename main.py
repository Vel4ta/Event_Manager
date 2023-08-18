from events.events_manager import update
from os.path import dirname

def main():
    return update(dirname(__file__))

if __name__ == "__main__":
    result = main()
    print(result)
