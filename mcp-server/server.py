from typing import Any, List
from mcp.server.fastmcp import FastMCP
import logging

from pydantic import BaseModel

# Initialize FastMCP server
mcp = FastMCP("HelloWorld")

class Order(BaseModel):
    customer_id: int
    customer_name: str
    order_date: str
    total_cost: float

@mcp.tool()
async def get_orders() -> List[Order]:
    return [
        Order(customer_id=1,  customer_name="Jeff Bezos",        order_date="2025-01-03", total_cost=189.90),
        Order(customer_id=2,  customer_name="Elon Musk",         order_date="2025-01-04", total_cost=59.99),
        Order(customer_id=3,  customer_name="Tim Cook",          order_date="2025-01-04", total_cost=324.50),
        Order(customer_id=4,  customer_name="Satya Nadella",     order_date="2025-01-05", total_cost=249.00),
        Order(customer_id=5,  customer_name="Sundar Pichai",     order_date="2025-01-06", total_cost=89.00),
        Order(customer_id=6,  customer_name="Mark Zuckerberg",   order_date="2025-01-06", total_cost=45.70),
        Order(customer_id=7,  customer_name="Jensen Huang",      order_date="2025-01-07", total_cost=129.99),
        Order(customer_id=8,  customer_name="Lisa Su",           order_date="2025-01-07", total_cost=780.00),
        Order(customer_id=9,  customer_name="Andy Jassy",        order_date="2025-01-08", total_cost=39.90),
        Order(customer_id=10, customer_name="Reed Hastings",     order_date="2025-01-08", total_cost=522.00),
        Order(customer_id=11, customer_name="Evan Spiegel",      order_date="2025-01-09", total_cost=160.00),
        Order(customer_id=12, customer_name="Dan Schulman",      order_date="2025-01-09", total_cost=99.99),
        Order(customer_id=3,  customer_name="Tim Cook",          order_date="2025-01-10", total_cost=24.50),
        Order(customer_id=8,  customer_name="Lisa Su",           order_date="2025-01-11", total_cost=1499.90),
        Order(customer_id=11, customer_name="Evan Spiegel",      order_date="2025-01-11", total_cost=77.00),
        Order(customer_id=1,  customer_name="Jeff Bezos",        order_date="2025-01-12", total_cost=289.90),
        Order(customer_id=7,  customer_name="Jensen Huang",      order_date="2025-01-12", total_cost=54.00),
        Order(customer_id=10, customer_name="Reed Hastings",     order_date="2025-01-13", total_cost=310.99),
        Order(customer_id=5,  customer_name="Sundar Pichai",     order_date="2025-01-13", total_cost=215.30),
        Order(customer_id=12, customer_name="Dan Schulman",      order_date="2025-01-14", total_cost=88.80),
    ]



@mcp.tool()
async def calc_taxes(orders: List[Order]) -> float:
    """
    Calculate taxes applying 10.5% on total cost of orders.
    """
    total = sum(order.total_cost for order in orders)
    tax = total * 0.105   # 10.5% tax
    logging.info(f"Total={total}, Tax={tax}")
    return tax



def main():
    print("Hello from mcpfun!")
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
