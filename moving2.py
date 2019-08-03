import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt


def calculate_amortization_amount(principal, interest_rate, period):
    x = (1 + interest_rate) ** period
    return principal * (interest_rate * x) / (x - 1)


def amortization_schedule(principal, interest_rate, period):
    amortization_amount = calculate_amortization_amount(principal, interest_rate, period)
    number = 1
    balance = principal
    total_interest = 0
    total_principal = 0
    while number <= period:
        interest = balance * interest_rate
        principal = amortization_amount - interest
        balance = balance - principal
        total_interest = total_interest + interest
        total_principal = total_principal + principal
        yield number, amortization_amount, interest, principal, total_interest, total_principal, balance \
            if balance > 0 else 0
        number += 1


def stamp_duty(purchase_price):
    if purchase_price <= 125000:
        return "No stamp Duty"
    elif 125000 < purchase_price <= 250000:
        return "Didn't code for this"
    elif 250000 < purchase_price <= 850000:
        duty1 = 125000 * 0.02
        duty2 = (purchase_price - 250000) * 0.05
        duty = int(duty1 + duty2)
        return duty
    elif 850000 < purchase_price:
        return "Didn't code for this"


def equity_calc(selling_price, mortgage):
    if selling_price > mortgage:
        equity = int(selling_price - mortgage)
        return equity
    else:
        return ArithmeticError


def diff_month(start_date, end_date):
    d1 = end_date
    d2 = start_date
    return (d1.year - d2.year) * 12 + (d1.month - d2.month)


def mortgage_data(data, principal, interest_rate, period, months1):
    amortization = list(amortization_schedule(principal, interest_rate/100/12, period*12))
    amortization_df = pd.DataFrame(amortization)
    amortization_df.columns = ["number", "amortization_amount", "interest", "principal", 'total_interest',
                               'total_principal', "balance"]
    amortization_row = amortization_df[amortization_df.number == months1]
    column_of_interest = data
    result = amortization_row[column_of_interest].values[0]
    return result


start = dt(2018, 11, 10)
# end = dt(2020, 12, 31)
end = dt.today()
principal1 = 271999
interest_rate1 = 2.09
period1 = 25
months = (diff_month(start, end))
selling1 = 320000
buying1 = 575000
savings1 = 7000
savings_rate = 1000
desired_deposit_p = 0.1
moving_costs = int(5000)
solicitor = int(1200)


def savings_projection(end1, savings_rate1):
    end = end1
    savings_rate = savings_rate1
    if diff_month(end, dt.today()) == 0:
        savings = savings1
        return savings
    else:
        month_in_future = diff_month(dt.today(), end)
        future_savings = month_in_future * savings_rate
        savings = savings1 + future_savings
        return savings


savings = int(savings_projection(end, savings_rate))
deposit = int(desired_deposit_p * buying1)
mortgage = (mortgage_data("balance", principal1, interest_rate1, period1, months))
equity = (equity_calc(selling1, mortgage))
duty = int(stamp_duty(buying1))
total_cash = equity + savings
total_expenses = deposit + moving_costs + solicitor + duty





# print(amortization_df, sep='\n')

# df_obj.plot(x='number', y=['amortization_amount', 'total_principal'], figsize=(10, 5), grid=True)
#plt.show()



# Print section #

print(f'----- Input Data -----')
print(f'Selling price £{selling1:,}')
print(f'New house price £{buying1:,}')
print(f'Assumed date for calculation {end}')

print(f'---- Equity ------')
print(f'Equity in the house = £{equity:,} (mortgage of £{int(mortgage):,})')
print(f'Savings = £{savings:,}')
print(f'===========> Total Cash = £{total_cash:,}')

print(f'----- Expenses -----')
print(f'Money needed for deposit of {int(desired_deposit_p * 100):,}% = £{deposit:,}')
print(f'Stamp Duty = £{duty:,}')
print(f'Solicitor & Moving costs = £{moving_costs + solicitor:,}')
print(f'===========> Total expenses = £{total_expenses:,}')

if total_cash < total_expenses:
    left = total_expenses - total_cash
    print(f'You have to save = £{left:,}')
else:
    left = total_cash - total_expenses
    print(f'You have more than required = £{left:,}')


year = 2019
month = 8  # TODO Find out today's month
df1 = pd.DataFrame({"date": [end], "total_cash": [total_cash]})
cols = ["date", "equity", "savings", "total_cash", "left_to_save", "deposit", "stamp_duty", "total_expenses"]
lst = []
# Try and work out the break even point
while total_cash < total_expenses:
    end = dt(year, month, 28)
    months = diff_month(start, end)
    mortgage = (mortgage_data("balance", principal1, interest_rate1, period1, months))
    equity = (equity_calc(selling1, mortgage))
    savings = int(savings_projection(end, savings_rate))
    total_cash = equity + savings
    left = total_expenses - total_cash
    lst.append([end, equity, savings, total_cash, left, deposit, duty, total_expenses])
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1

df1 = pd.DataFrame(lst, columns=cols)
print(df1, sep='\n')

df1.plot(x='date', y=['total_cash', 'total_expenses'], figsize=(10, 5), grid=True)
plt.show()