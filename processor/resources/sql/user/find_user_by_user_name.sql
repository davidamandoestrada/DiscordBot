-- :name find_user_by_user_name :one
select * from discord_user where user_name = :user_name