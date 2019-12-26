-- :name find_messages_by_user_name :many
select * from message where user_name = :user_name