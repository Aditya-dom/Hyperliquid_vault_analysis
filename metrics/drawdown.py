def calculate_max_drawdown_on_accountValue(cumulative_pnl):
    """
    Calculates the maximum drawdown from a list of cumulative daily PnL.

    :param cumulative_pnl: List of cumulative daily PnL values
    :return: The maximum drawdown in absolute value and as a percentage
    """
    # Initialize variables
    max_value = float('-inf')  # The maximum value reached at any given time
    max_drawdown = 0  # The largest recorded drop

    for pnl in cumulative_pnl:
        # Update the maximum value reached
        max_value = max(max_value, pnl)
        # Calculate the current drawdown
        drawdown = max_value - pnl
        # Update if the current drawdown is the highest
        max_drawdown = max(max_drawdown, drawdown)

    # Calculate the drawdown as a percentage (relative to the maximum peak)
    max_drawdown_pct = (max_drawdown / max_value *
                        100) if max_value != 0 else 0

    return int(max_drawdown_pct)


def calculate_sortino_ratio(daily_pnl, risk_free_rate=0.0):
    """
    Calculate the Sortino Ratio from daily returns.
    :param daily_pnl: List of daily PnL (Profit and Loss).
    :param risk_free_rate: Risk-free rate of return (default: 0%).
    :return: Sortino Ratio.
    """
    returns = [pnl / daily_pnl[i - 1] - 1 for i,
               pnl in enumerate(daily_pnl[1:], 1) if daily_pnl[i - 1] != 0]
    if len(returns) == 0:
        return 0
    avg_return = sum(returns) / len(returns)
    downside_deviation = (
        sum((min(r - risk_free_rate, 0) ** 2 for r in returns)) / len(returns)
    ) ** 0.5
    if downside_deviation == 0:
        return 0
    return avg_return / downside_deviation


def calculate_sharpe_ratio(daily_pnl, risk_free_rate=0.0):
    """
    Calculate the Sharpe Ratio from daily returns.
    :param daily_pnl: List of daily PnL (Profit and Loss).
    :param risk_free_rate: Risk-free rate of return (default: 0%).
    :return: Sharpe Ratio.
    """
    returns = [pnl / daily_pnl[i - 1] - 1 for i,
               pnl in enumerate(daily_pnl[1:], 1) if daily_pnl[i - 1] != 0]
    if len(returns) == 0:
        return 0
    avg_return = sum(returns) / len(returns)
    std_dev = (sum((r - avg_return) ** 2 for r in returns) /
               len(returns)) ** 0.5
    if std_dev == 0:
        return 0
    return avg_return / std_dev
