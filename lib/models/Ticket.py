
import sqlite3
import click

DATABASE = 'tickets.db'

def setup_database():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ticket_number TEXT NOT NULL,
                agent TEXT NOT NULL
            )
        ''')
        conn.commit()

@click.group()
def cli():
    """Ticket management CLI application."""
    setup_database()
    click.echo("Database setup complete.")

@click.command()
@click.argument('name')
@click.argument('ticket_number')
@click.argument('agent')
def add_ticket(name, ticket_number, agent):
    """Add a new ticket."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tickets (name, ticket_number, agent)
            VALUES (?, ?, ?)
        ''', (name, ticket_number, agent))
        conn.commit()
    click.echo(f"Ticket added: {name} ({ticket_number}) - Agent: {agent}")

@click.command()
def list_tickets():
    """List all tickets."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tickets')
        tickets = cursor.fetchall()
    if tickets:
        for ticket in tickets:
            click.echo(f"ID: {ticket[0]}, Name: {ticket[1]}, Ticket Number: {ticket[2]}, Agent: {ticket[3]}")
    else:
        click.echo("No tickets found.")

@click.command()
@click.argument('ticket_id', type=int)
@click.option('--name', help="New name for the ticket.")
@click.option('--ticket_number', help="New ticket number for the ticket.")
@click.option('--agent', help="New agent for the ticket.")
def update_ticket(ticket_id, name, ticket_number, agent):
    """Update an existing ticket."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        if name:
            cursor.execute('UPDATE tickets SET name = ? WHERE id = ?', (name, ticket_id))
        if ticket_number:
            cursor.execute('UPDATE tickets SET ticket_number = ? WHERE id = ?', (ticket_number, ticket_id))
        if agent:
            cursor.execute('UPDATE tickets SET agent = ? WHERE id = ?', (agent, ticket_id))
        conn.commit()
    click.echo(f"Ticket {ticket_id} updated.")

@click.command()
@click.argument('ticket_id', type=int)
def delete_ticket(ticket_id):
    """Delete a ticket."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tickets WHERE id = ?', (ticket_id,))
        conn.commit()
    click.echo(f"Ticket {ticket_id} deleted.")

cli.add_command(add_ticket)
cli.add_command(list_tickets)
cli.add_command(update_ticket)
cli.add_command(delete_ticket)

if __name__ == "__main__":
    cli()
