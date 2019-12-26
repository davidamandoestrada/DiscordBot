-- :name find_messages_by_user_id :many
select * from message where user_id = :user_id