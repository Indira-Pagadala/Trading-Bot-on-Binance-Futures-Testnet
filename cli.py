import typer
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, FloatPrompt
from rich.panel import Panel

from bot.client import get_client
from bot.orders import create_order
from bot.logging_config import setup_logger

app = typer.Typer()
console = Console()


@app.command()
def trade():
    setup_logger()

    console.print(
        Panel.fit(
            "[bold cyan]Welcome to Binance Futures Trading Bot (Testnet)[/bold cyan]",
            border_style="cyan",
        )
    )

    client = get_client()

    symbol = Prompt.ask("Trading symbol", default="BTCUSDT").upper()
    side = Prompt.ask("Side", choices=["BUY", "SELL"], default="BUY")

    console.print("\n[bold]Select Order Type[/bold]")
    console.print("1) MARKET")
    console.print("2) LIMIT")
    console.print("3) STOP-LIMIT")

    order_choice = IntPrompt.ask("Enter choice (1-3)", default=1)

    if order_choice not in (1, 2, 3):
        console.print("[bold red]Invalid selection. Choose 1, 2, or 3.[/bold red]")
        raise typer.Exit(code=1)


    while True:
        quantity = FloatPrompt.ask("Quantity")
        if quantity > 0:
            break
        console.print("[bold red]Quantity must be greater than 0[/bold red]")


    try:
        if order_choice == 1:
            order = create_order(client, symbol, side, "MARKET", quantity)

        elif order_choice == 2:
            while True:
                price = FloatPrompt.ask("Limit price")
                if price >= 0.01:
                    break
                console.print("[bold red]Limit price must be at least 0.01[/bold red]")
            order = create_order(
                client,
                symbol,
                side,
                "LIMIT",
                quantity,
                price=price,
            )

        elif order_choice == 3:
            while True:
                stop_price = FloatPrompt.ask("Stop price")
                if stop_price >= 0.01:
                    break
                console.print("[bold red]Stop price must be at least 0.01[/bold red]")
            while True:
                limit_price = FloatPrompt.ask("Limit price")
                if limit_price >= 0.01:
                    break
                console.print("[bold red]Limit price must be at least 0.01[/bold red]")

            order = create_order(
                client,
                symbol,
                side,
                "STOP-LIMIT",
                quantity,
                price=limit_price,
                stop_price=stop_price,
            )
        console.print("\n[bold green]✅ Order placed successfully[/bold green]")
        console.print(order)

    except ValueError as e:
        console.print(f"\n[bold red]❌ Validation error:[/bold red] {e}")

    except Exception as e:
        console.print(f"\n[bold red]❌ API error:[/bold red] {e}")


if __name__ == "__main__":
    app()
