from psycopg2 import connect
from psycopg2.errors import DivisionByZero
from dotenv import load_dotenv
import database
from models.option import Option
from models.poll import Poll
import random
from models.connections import get_connection

# MENU
MENU_PROMPT = """-- Menu --

1) Create new poll
2) List open polls
3) Vote on a poll
4) Show poll votes
5) Select a random winner from a poll option
6) Exit

Enter your choice: """
NEW_OPTION_PROMPT = "Enter new option text (or leave empty to stop adding options): "

# CREATE A POLL
def prompt_create_poll():
    # ASK TITLE AND OWNER
    poll_title = input("Enter poll title: ")
    poll_owner = input("Enter poll owner: ")
    # CREATE POLL OBJECT
    poll = Poll(poll_title, poll_owner)
    # FUNCTION TO SAVE IT ON DATABASE
    poll.save()

    # ADDING OPTIONS
    while (new_option := input(NEW_OPTION_PROMPT)):
        # ADD OPTION TO DATABASE
        poll.add_option(new_option)

# SEE POLLS
def list_open_polls():
    # GET ALL POLLS
    polls = Poll.all()

    # PRINT ALL POLLS
    for poll in polls:
        print(f"{poll.id}: {poll.title} (created by {poll.owner})")

# VOTE
def prompt_vote_poll():
    poll_id = int(input("Enter poll would you like to vote on: "))
    # GET POLL WITH ATTRIBUTE OPTIONS AND PRINT THEM
    _print_poll_options(Poll.get(poll_id).options)

    option_id = int(input("Enter option you'd like to vote for: "))
    username = input("Enter the username you'd like to vote as: ")

    #  GET THE OPTION AND INSERT THE option_id and the USERNAME in DATABASE
    Option.get(option_id).vote(username)

# PRINT OPTIONS
def _print_poll_options(options):
    for option in options:
        print(f"{option.id}: {option.text}")

# SHOWW ALL VOTES
def show_poll_votes():
    poll_id = int(input("Enter poll you would like to see votes for: "))
    # GET THE ATTRIBUTES OPTIONS WITH THE POLL ID
    options = Poll.get(poll_id).options
    # GET THE VOTES PER OPTION
    votes_per_option = [len(option.votes) for option in options]
    # TOTAL OF VOTES PER OPTION
    total_votes = sum(votes_per_option)

    # PRINT THE TOTAL OF VOTES
    try:
        for option, votes in zip(options, votes_per_option):
            percentage = votes / total_votes * 100
            print(f"{option.text} got {votes} votes ({percentage:.2f}% of total)")
    except ZeroDivisionError:
        print("No votes cast for this poll yet.")


# PICK A RANDOM WINNER
def randomize_poll_winner():
    poll_id = int(input("Enter poll you'd like to pick a winner for: "))
    _print_poll_options(Poll.get(poll_id).options)

    option_id = int(input("Enter which is the winning option, we'll pick a random winner from voters: "))
    votes = Option.get(option_id).votes
    winner = random.choice(votes)
    print(f"The randomly selected winner is {winner[0]}.")


MENU_OPTIONS = {
    "1": prompt_create_poll,
    "2": list_open_polls,
    "3": prompt_vote_poll,
    "4": show_poll_votes,
    "5": randomize_poll_winner
}



def menu():
    # GET THE CONNECTION
    with get_connection() as connection:
        database.create_tables(connection)

    # RUN PROGRAM
    while (selection := input(MENU_PROMPT)) != "6":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("Invalid input selected. Please try again.")


menu()