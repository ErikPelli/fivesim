# 5sim

## Introduction
5SIM is a service for receiving SMS and activating accounts on any site that require SMS verification, without using your personal number to avoid spam in future.

When registering on social networks, messengers and on other sites, an SMS verification of account is required. 5SIM provides the opportunity to bypass SMS verification procedure with the help of a temporary virtual phone number without using the personal one. By purchasing virtual numbers for SMS receiving and for activating any site or app, you will register many profiles on websites by receiving a confirmation code online.

## 5SIM Features
- You can get SMS online 24/7. This is a fully automated service: the receipt of a text message with a verification code happens instantaneously.
- Receive an unlimited quantity of messages from the selected site or app. Herewith, the cost of one SMS number starts from 0,014$, and you’ll not have to pay monthly rates of mobile operators.
- Use foreign virtual numbers from more than 180 countries all over the world. Practically you can find mobile numbers for registration of almost any country, including the UK, Russia, Sweden, Germany, Ukraine, France, India, Indonesia, Malaysia, Cambodia, Mongolia, Nicaragua, Canada, the USA, Thailand, the Philippines, Ethiopia and others.
- Top up the balance with a minimum commission on the website (Visa/MasterCard/MIR, Alipay, Apple Pay, Google Play, Samsung Pay and others).
- Register accounts automatically via the API.

## Rating System
Actual rating is displayed in account settings, tab "General".

Number of points rating equals number of orders that you can create simultaneously.

Initial rating for new users is 8 points.

Highest possible rating is 96 points.

| Action                                          | Rating (points) |
| ----------------------------------------------- | --------------- |
| Receive sms and finish the order before timeout | +0.5            |
| Receive sms and order finished after timeout    | +0.25           |
| Cancel                                          | -0.125          |
| Ban number                                      | -0.125          |
| Timeout                                         | -0.35           |

If rating drops to zero, you will not be able order within 24 hours. After 24 hours, rating will return to initial value of 8 points.

## Library
This library is unofficial and is not directly linked to the website in question.

It was created out of need to use their API easily, without having to handle all possible cases in the application.

At the time of its creation, there were no such libraries.

## Examples

### Buy a number
```python
from fivesim import FiveSim, Country, Operator, FiveSimError

if __name__ == "__main__":
    client = FiveSim(api_key="YOUR_5SIM_API_KEY")
    try:
        result = client.user.buy_number(
            country=Country.ARMENIA,
            operator=Operator.ANY_OPERATOR,
            product=ActivationProduct.EBAY
        )
        code = result.sms[0].activation_code
        print(code)
    except FiveSimError as e:
        print(e)
```