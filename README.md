# Goal Tracker

An all-in-one application to help achieve your goals.   Goal Tracker is tailored to your needs, sending text reminders when you need it most.  Goal Tracker acts as the best sort of planner, keeping track of the areas you excel in and focusing your energy where you need it most.

## Tech Stack

**Frontend:** HTML, CSS, Javascript, AJAX, jQuery, D3, Bootstrap, Jinja</br>
**Backend:** Python, Javascript, Flask, PosgreSQL
**API's**: Python Scheduler API, Twilio API

## Set up

Clone or fork this repo:

```
https://github.com/ElizabethLane/HB_Project.git
```

Create and activate a virtual environment inside your project directory:

```
virtualenv env
source env/bin/activate
```

Install the requirements:

```
pip install -r requirements.txt
```

Get secret keys for [twilio] (https://www.twilio.com/).  Save them to secrets.sh.

Source the variables to your evt:

```
source secrets.sh
```


Find the home page at 'localhost:5000/' and get started on your journey to self-driven success!


##Version 2.0

Goal Tracker is Elizabeth Nelson's first independent project completed in a four week time frame.  Features that are planned for v2.0 include:
* Allowing the user to visualize individual categories of goals (e.g. "let me see my percentages for my "work" goals in July").  
+ Implementing email reminders
+ Create an algorithm to keep the user on track for their various time frame (one week, one month, etc.) for their goal.



