-- :name find_user_by_user_name :one
select * from users where user_name = :user_name