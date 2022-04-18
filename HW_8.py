from datetime import datetime, timedelta


def get_birthdays_per_week(birthday_list):

    week_days = {
                'Monday': [],
                'Tuesday': [],
                'Wednesday': [],
                'Thursday': [],
                'Friday': []
                }

    employee_to_be_congrats = []

    current_datetime = datetime.now()
    week_starts = current_datetime

    # date to datetime-format in birthday_list
    for employee in birthday_list:

        birthday = datetime.strptime(employee["birthday"], '%Y-%m-%d')
        birthday_this_year = datetime(year=current_datetime.year, month=birthday.month, day=birthday.day)
        employee['birthday'] = birthday_this_year


    # check if today is Mon, if not: find next Mon date.
    if week_starts.weekday() == 0:
        print(f'Monday date: {week_starts.strftime("%d.%m.%y")}\n')

    else:
        while week_starts.weekday() != 0:
            week_starts += timedelta(days=1)
        print(f'Monday date: {week_starts.strftime("%d.%m.%y")}\n')


    # making a list whom user should congrats this week
    for employee in birthday_list:

        difference = (employee["birthday"].date() - week_starts.date()).days

        # check if a person's birthday this week
        if -2 <= difference < 5:
            employee_to_be_congrats.append(employee)


    # distribute by days of the week
    for employee in employee_to_be_congrats:

        emp_birth_wd = employee["birthday"].weekday()

        if emp_birth_wd == 0 or emp_birth_wd == 5 or emp_birth_wd == 6:
            week_days['Monday'].append(employee['name'])
        else:
            week_days[employee["birthday"].strftime('%A')].append(employee['name'])

         
    # print day of week and names
    for weekday in week_days:
        names = week_days.get(weekday)

        if names:
            print(f"{weekday}: {', '.join(names)}")
        else:
            continue


birthday_list = [
                {"name": "Mark",
                 "birthday": "2000-04-15"},

                {"name": "John",
                 "birthday": "1989-04-16"},

                {"name": "Steve",
                 "birthday": "1992-04-17"},

                {"name": "Kent",
                 "birthday": "1976-04-18"},

                {"name": "Joey",
                 "birthday": "2004-04-21"},

                {"name": "Brain",
                 "birthday": "1995-04-22"},

                {"name": "Emma",
                 "birthday": "1999-04-23"},

                {"name": "Raychel",
                 "birthday": "1990-04-25"},

                {"name": "Phebe",
                 "birthday": "1980-04-28"},

                {"name": "Monika",
                 "birthday": "1975-05-01"},

                {"name": "Tom",
                 "birthday": "2000-12-26"}
                ]


if __name__ == "__main__":
    get_birthdays_per_week(birthday_list)
