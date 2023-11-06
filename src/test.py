import typer

# app_test = typer.Typer()

# @app_test.command()
# def take_input():
#     user_input = typer.prompt("Enter something: ")
#     typer.echo(f"You entered {user_input}")
#
# if __name__ == '__main__':
#     app_test()

test_pri = 0

while test_pri < 1 or test_pri > 3:
    test_pri = int(input("Enter test priority:"))