+++
title = "Sending Python strings to Slack via Snowflake's notification stored procedure"
date = "2025-11-22"
description="A guide to properly formatting escape sequences so Python strings/messages are sent to Slack via Snowflake's notification service"
tags = ["SQL", "Snowflake", "Python", "Slack"]
+++

If you want to send a message to Slack via Snowflake's [notification stored procedure](https://docs.snowflake.com/en/user-guide/notifications/snowflake-notifications) you need to make sure any newline characters (or other other escape sequences like `\t`) are properly formatted/escaped in order to be sent and rendered in Slack as intended.

### Sending a raw string

In Snowflake, this query executes with no issue:

```SQL
SELECT 'Hello\nWorld' ;
```

`\n`, as you are no doubt aware, is the escape sequence for a newline character in Snowflake (and programming languages like Python).


If we want to send the message `Hello World` with a newline character the following **won't** work (the message won't be sent):

```SQL
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  SNOWFLAKE.NOTIFICATION.TEXT_PLAIN(
    SNOWFLAKE.NOTIFICATION.SANITIZE_WEBHOOK_CONTENT('Hello\nWorld')
  ),
  SNOWFLAKE.NOTIFICATION.INTEGRATION('example_slack_integration')
);
```

Like in our earlier query, Snowflake is seeing the escape sequence and returning a literal newline character. The problem is that behind the scenes the notification stored procedure is taking the input string and converting it to a JSON object (see the [documentation here](https://docs.snowflake.com/sql-reference/functions/text_plain)) and to represent a newline character in a JSON object you need to use the string literal `\n`. But Snowflake isn't passing a string literal `\n`, it's passing an actual newline character, breaking the function.


You can see this problem demonstrated when you run the following in Snowflake:

```SQL
SELECT PARSE_JSON('{"hello": "\nworld"}') ;
```

```
SQL Error [100069] [22P02]: Error parsing JSON: unterminated string, line 2, pos 0
```
If we escape the newline character the query works:

```SQL
SELECT PARSE_JSON('{"hello": "\\nworld"}') ;
```

As does the notification:

```SQL
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  SNOWFLAKE.NOTIFICATION.TEXT_PLAIN(
    SNOWFLAKE.NOTIFICATION.SANITIZE_WEBHOOK_CONTENT('Hello\\nWorld')
  ),
  SNOWFLAKE.NOTIFICATION.INTEGRATION('example_slack_integration')
```

### Sending a Python string

The same concept applies with Python however simply escaping the newline escape sequence in a raw string won't work:

```py
spam = "Hello\\nWorld"
print(spam)
```

What's returned: 

`Hello \n World`

By including an escape character in our string we're ensuring that Python isn't intrepeting the `\n` as a literal newline character. 

However we still need to pass this string to Snowflake, which *will* intrepet the `\n` as a newline character and we encounter the problem mentioned above. 

In other words, we've made sure Python knows not to print a newline character... but the resulting string (`Hello\nWorld`) will still be intrepeted by Snowflake as containing a newline character.

Thankfully the solution is simple. You can use additional backslashes or you create a raw string (which tells Python not to treat backslashes as escape characters):

```py
# Solution 1
spam = "Hello\\\\nWorld"

# Solution 2
spam r"Hello\\nWorld"
```

I prefer Solution 2 as it's quite explicit as to what's being passed to Snowflake. 

Snowflake will see the `Hello\\nWorld` and (thanks to the backslash) will understand that the `\n` needs to be sent as is to the JSON function.