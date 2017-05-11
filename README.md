# Supersearch

This app allows to search content in Youtube and Twitter services using keywords entered by user. The search commits through Twitter API and YouTube API.

Firstly, user should sign in or sign up if he hasn't account. On the main page, user can type search query and obtain list of videos and tweets. Users with admins rules can navigate to statistics page. On this page the admin can watch statistics for each users with their search queries and statistics for queries. Also admin can select date range and watch all the queries during this period.

Each user has account page that contains user's queries, bookmarks and form for password changing.

All the secret data like API keys and credentials to database stores in the config.py file. And all required packages contains requirements.txt file.

#### API calls
```sh
/supersearch_rest/api/users
```
Method GET, returns json with users list. Each user has his queries and total count of queries. User info contains user id and login.

#### Link for demo app - https://supersearch.herokuapp.com/
