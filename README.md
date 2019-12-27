From memory, the steps to get this to work are:

1. You need a Twitter account with verified email and phone number.

1. Register for a developer account at https://developer.twitter.com/en/dashboard - approval was instant for me for this use case (I choose the "want to play with the API"-style option in the first step and explained what I was planning to do)

1. Create an app at https://developer.twitter.com/en/apps. Obtain the "API key" and "API secret key" from the "Keys and token" page ("Consumer API keys" section).

1. `curl --user <API_KEY> -d 'grant_type=client_credentials' https://api.twitter.com/oauth2/token`
(Enter the 'API secret key' when curl asks you for the password.)

1. Extract the `access_token` and save it to a file named `bearer.secret`.

1. Optional: Fetch example data:
`curl --header 'Authorization: Bearer <access_token>' 'https://api.twitter.com/1.1/statuses/user_timeline.json?exclude_replies=true&include_rts=false&screen_name=realdonaldtrump&count=200&tweet_mode=extended'`