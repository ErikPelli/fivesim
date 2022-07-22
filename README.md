# 5sim

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