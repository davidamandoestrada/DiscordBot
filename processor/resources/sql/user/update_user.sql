-- :name update_user :affected
update discord_user
set user_name = :user_name,
avatar_url = :avatar_url
where id = :id