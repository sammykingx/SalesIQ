from pydantic import BaseModel, Field


class MerchantLeaderboardSchema(BaseModel):
    """Schema representing a merchant's entry on a performance leaderboard.

    Attributes:
        rank (int): The merchant's numerical position on the leaderboard.
        name (str): The name of the merchant business.
        code (str): The unique identifying code for the merchant.
        owner (str): The name of the business owner or primary representative.
        biz_type (str): The category or industry type of the business.
        total_sales (int): The total count of sales or transactions completed.
        revenue_raw (float): The raw, unformatted revenue value used for sorting 
            and calculations (aliased as `revenueRaw`).
        revenue (str): The human-readable, formatted revenue string for UI display 
            (e.g., "₦2,450,000").
        growth (str): The performance growth indicator or percentage change 
            over a given period (e.g., "+12.5%").
    """
    rank: int
    name: str
    code: str
    owner: str
    biz_type: str
    total_sales: int
    revenue_raw: float
    revenue: str
    growth: str
